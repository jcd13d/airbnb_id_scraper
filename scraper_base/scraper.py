import os.path
import datetime

import pandas as pd
import requests
import traceback
import json
import urllib3.util.retry
import s3fs
from fastparquet import write
from config.constants import NUM_REQUEST_TRIES


class IdScraper:
    def __init__(self, scraper_index):
        self.index = scraper_index
        self.s3 = s3fs.S3FileSystem()
        self.s3_myopen = self.s3.open
        self.config = self.get_config()
        self.ids = self.get_ids()
        self.run_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.data = None
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
        self.attribute_error = 0

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
        AttributeError Error: {self.attribute_error}
        Num Requests: {self.requests_count}
        Num IDs Run: {self.id_count}
        """)

    def make_request(self, headers, params, api_url, proxies=None, timeout=3):
        print("running req func")
        self.requests_count += 1
        return requests.get(api_url, headers=headers, params=params, proxies=proxies, timeout=timeout)

    def append_to_data(self, df):
        if self.data is None:
            self.data = df
        else:
           self.data = pd.concat([self.data, df])

    def dataframe_to_s3(self, s3_path, partitionBy: list=[]):
        print("writing df")

        path = os.path.join(s3_path, f"array_{self.index}", self.run_time)

        if self.s3.exists(path):
            write(path, self.data, file_scheme='hive', partition_on=partitionBy, append=True, open_with=self.s3_myopen)
        else:
            print("new df")
            write(path, self.data, file_scheme='hive', partition_on=partitionBy, append=False, open_with=self.s3_myopen)

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

    def write_result(self, out_config):
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
        print("make request _")
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
        print("parse")
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

        return parsed


    def _request_and_parse(self, request_config, id_):
        print("request and parse")
        # TODO extract this out and have larger try except for errors that

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

        return parsed

    def tear_down(self):
        self.s3.end_transaction()
        self.s3 = None
        self.s3_myopen = None

    def run(self):
        for cfg in self.config['configs']:
            for id_ in self.ids:
                print(f"Running ID: {id_}")
                edited_config = self.insert_id_into_config(id_, cfg)
                parsed = self._request_and_parse(edited_config["request_config"], id_)
                if parsed is not None:
                    self.append_to_data(parsed)
                else:
                    print("Received None from request and parse")
                    traceback.print_exc()

            self.write_result(cfg['out_config'])
        self.print_error_stats()

        self.tear_down()



