import requests
import traceback
import json
import urllib3.util.retry

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

    def _make_request(self, headers, params, api_url, proxies=None):
        response = None
        for i in range(NUM_REQUEST_TRIES):
            try:
                response = self.make_request(headers, params, api_url, proxies)
            except urllib3.util.retry.MaxRetryError as e:
                print(f"MaxRetryError triggered: {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.ProxyError as e:
                print(f"ProxyError triggered: {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.SSLError as e:
                print(f"SSL Error triggered (usually max retries): {e}")
                continue  # continues thru loop if fails
            break       # if different error or out of tries break

        if response is None:
            raise()

        return response


    def _parse_result(self, id, result):
        parsed = None

        for i in range(NUM_REQUEST_TRIES):
            try:
                parsed = self.parse_result(id, result)
            except KeyError as e:
                print(f"Key error in request/parse: {e}")
                continue    # continues thru loop if fails
            except TypeError as e:
                traceback.print_exc()
                print(f"TypeError triggered: {e}")
                res_json = json.loads(result.text)
                if "errors" in res_json.keys():
                    [print(err['message']) for err in res_json['errors']]
                    break
                # print(result)
                # print(json.dumps(json.loads(result.text), indent=4))
                continue
            break

        # if parsed is None:
        #     raise()

        return parsed

    # def request_and_parse(self, id_, request_config):
    #     parsed = None
    #     for i in range(NUM_REQUEST_TRIES):
    #
    #         if i > 0:
    #             print(f"try {i + 1} doing request and parse")
    #
    #         try:
    #             result = self.make_request(**request_config)
    #             parsed = self.parse_result(id_, result)
    #         except KeyError as e:
    #             print(f"Key error in request/parse: {e}")
    #             continue    # continues thru loop if fails
    #         except urllib3.util.retry.MaxRetryError as e:
    #             print(f"MaxRetryError triggered: {e}")
    #             continue  # continues thru loop if fails
    #         except requests.exceptions.ProxyError as e:
    #             print(f"ProxyError triggered: {e}")
    #             continue  # continues thru loop if fails
    #         except requests.exceptions.SSLError as e:
    #             print(f"SSL Error triggered (usually max retries): {e}")
    #             continue  # continues thru loop if fails
    #         except TypeError as e:
    #             traceback.print_exc()
    #             print(f"TypeError triggered: {e}")
    #             print(result)
    #             print(json.dumps(json.loads(result.text), indent=4))
    #             continue
    #         break       # if different error or out of tries break
    #
    #     if parsed is None:
    #         raise()
    #
    #     return parsed

    def run(self):
        for id_ in self.ids:
            print(f"Running ID: {id_}")
            for cfg in self.config['configs']:
                edited_config = self.insert_id_into_config(id_, cfg)

                result = self._make_request(**edited_config["request_config"])
                if result is None:
                    print("Unable to get result")
                else:
                    parsed = self._parse_result(id_, result)
                    if parsed is None:
                        print("Unable to parse")
                    else:
                        # parsed = self.request_and_parse(id_, edited_config['request_config'])
                        self.write_result(id_, parsed, cfg['out_location'])

