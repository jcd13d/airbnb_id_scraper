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
        self.ssl = 0
        self.type_error = 0
        self.timeout = 0
        self.max_retry = 0
        self.proxy = 0
        self.key_error = 0
        self.requests_count = 0
        self.id_count = len(self.ids)
        self.connection = 0
        self.airbnb_error = 0

    def print_error_stats(self):
        print(f"""
        SSL Error: {self.ssl}
        Type Error: {self.type_error}
        Timeouts: {self.timeout}
        Max Retry: {self.max_retry}
        Proxy Error: {self.proxy}
        Key Error: {self.key_error}
        Connection Error: {self.connection}
        Airbnb Error: {self.airbnb_error}
        Num Requests: {self.requests_count}
        Num IDs Run: {self.id_count}
        """)

    def make_request(self, headers, params, api_url, proxies=None, timeout=3):
        self.requests_count += 1
        return requests.get(api_url, headers=headers, params=params, proxies=proxies, timeout=timeout)

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
            if i > 0:
                print(f"try {i + 1} making request")
            try:
                response = self.make_request(headers, params, api_url, proxies)
            except urllib3.util.retry.MaxRetryError as e:
                self.max_retry += 1
                traceback.print_exc()
                print(f"MaxRetryError triggered: {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.ProxyError as e:
                self.proxy += 1
                traceback.print_exc()
                print(f"ProxyError triggered: {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.SSLError as e:
                self.ssl += 1
                traceback.print_exc()
                print(f"SSL Error triggered (usually max retries): {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.ReadTimeout as e:
                self.timeout += 1
                traceback.print_exc()
                print(f"Timed out based on wait limit set: {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.ConnectionError as e:
                self.connection += 1
                traceback.print_exc()
                print(f"Connection Error triggered: {e}")
                continue  # continues thru loop if fails
            break       # if different error or out of tries break

        if response is None:
            raise()

        return response


    def _parse_result(self, id, result):
        parsed = None

        for i in range(NUM_REQUEST_TRIES):
            if i > 0:
                print(f"try {i + 1} parsing result")
            try:
                parsed = self.parse_result(id, result)

            except TypeError as e:
                self.type_error += 1
                traceback.print_exc()
                print(f"TypeError triggered: {e}")
                res_json = json.loads(result.text)
                if "errors" in res_json.keys():
                    self.airbnb_error += 1
                    [print(err['message']) for err in res_json['errors']]
                    break   # break loop, this isn't solved with multiple retries
                continue # usually type errors are random weird responses and can be resolved by trying again
            # except KeyError as e:
            #     if "'barPrice'" == str(e):
            #         break # break - this is handled in try except with both request and parsed
            #     raise(e)
            break   # breaking since we didnt have an error we know we should retry on

        # if parsed is None:
        #     raise()

        return parsed


    def _request_and_parse(self, request_config, id_):
        # TODO extract this out and have larger try except for errors that
        # make us need to re request but found in parsing
        # result = self._make_request(**request_config)
        # if result is None:
        #     print("Unable to get result")
        # else:
        #     parsed = self._parse_result(id_, result)
        #     if parsed is None:
        #         print("Unable to parse")
        #     else:
        #         # parsed = self.request_and_parse(id_, edited_config['request_config'])
        #         # self.write_result(id_, parsed, cfg['out_location'])
        parsed = None
        result = None
        for i in range(NUM_REQUEST_TRIES):
            if i > 0:
                print(f"try {i + 1} request and parse")
            try:
                result = self._make_request(**request_config)
                if result is None:
                    break   # result failed break loop
                parsed = self._parse_result(id_, result)
            except KeyError as e:
                self.key_error += 1
                traceback.print_exc()
                print(f"Key error in request/parse: {e}")
                if "'barPrice'" == str(e):
                    print(f"Retrying because {e} error")
                    continue  # continues thru loop if fails
            except TypeError as e:
                self.type_error += 1
                traceback.print_exc()
                print(f"TypeError triggered: {e}")
                res_json = json.loads(result.text)
                if "errors" in res_json.keys():
                    [print(err['message']) for err in res_json['errors']]
                    break  # break loop, this isn't solved with multiple retries
                continue  # usually type errors are random weird responses and can be resolved by trying again
            break # break if different error

        # if result is None:
        #     raise()
        #
        # if parsed is None:
        #     raise()

        return parsed

    def run(self):
        for id_ in self.ids:
            print(f"Running ID: {id_}")
            for cfg in self.config['configs']:
                edited_config = self.insert_id_into_config(id_, cfg)
                parsed = self._request_and_parse(edited_config["request_config"], id_)
                if parsed is not None:
                    self.write_result(id_, parsed, cfg['out_location'])
                else:
                    print("Received None from request and parse")
                    traceback.print_exc()
        self.print_error_stats()

