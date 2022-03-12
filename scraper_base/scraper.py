import requests


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

    def run(self):
        for id_ in self.ids:
            for cfg in self.config['configs']:
                edited_config = self.insert_id_into_config(id_, cfg)
                result = self.make_request(**edited_config["request_config"])
                parsed = self.parse_result(id_, result)
                self.write_result(id_, parsed, cfg['out_location'])
