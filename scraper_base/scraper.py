import requests
from config.constants import NUM_REQUEST_TRIES


class IdScraper:
    def __init__(self, scraper_index):
        self.index = scraper_index
        self.config = self.get_config()
        self.ids = self.get_ids()

    def make_request(self, headers, params, api_url, proxies=None):
        return requests.get(api_url, headers=headers, params=params, proxies=proxies)

    def get_ids(self, **kwargs):
        """
        Get IDs from a configuration
        :param kwargs:
        :return: List of IDs
        """
        raise NotImplementedError("Not Implemented")

    def get_config(self, **kwargs):
        """
        Get general config
        :param kwargs:
        :return: Dict
        """
        raise NotImplementedError("Not Implemented")

    def parse_result(self, id, result):
        """
        Parse result into form needed for writing data to disk
        :param id: Listing ID
        :param result: Result in final form before writing
        :return:
        """
        raise NotImplementedError("Not Implemented")

    def write_result(self, id_, result, out_location):
        """
        Write result to disk
        :param id_:
        :param result:
        :param out_location:
        :return:
        """
        raise NotImplementedError("Not Implemented")

    def insert_id_into_config(self, id, config):
        """
        Since we use one "static" config but many IDs we will probably need to insert the ID into
        the static config. You can do that here.
        :param id:
        :param config:
        :return:
        """
        raise NotImplementedError("Not Implemented")

    def request_and_parse(self, id_, request_config):
        parsed = None
        for i in range(NUM_REQUEST_TRIES):

            if i > 0:
                print(f"try {i + 1} doing request and parse")

            try:
                result = self.make_request(**request_config)
                parsed = self.parse_result(id_, result)
            except KeyError as e:
                print(f"Key error in request/parse: {e}")
                continue    # continues thru loop if fails
            break       # if different error or out of tries break

        if parsed is None:
            raise()

        return parsed

    def run(self):
        for id_ in self.ids:
            for cfg in self.config['configs']:
                edited_config = self.insert_id_into_config(id_, cfg)
                # result = self.make_request(**edited_config["request_config"])
                # parsed = self.parse_result(id_, result)
                parsed = self.request_and_parse(id_, edited_config['request_config'])
                self.write_result(id_, parsed, cfg['out_location'])
