import requests.exceptions
import urllib3
import traceback
import s3fs
from scraper_base.scraper import IdScraper
from config.constants import PRICING_CONFIG_LOCATION, ID_CONFIG_LOCATION, NUM_REQUEST_TRIES
from pricing.parser import parse_pricing
from pricing.pricing_id import get_pricing_id
import datetime
import json
import copy


class PricingScraper(IdScraper):
    def __init__(self, scraper_index):
        super().__init__(scraper_index)

    def get_config(self):
        with self.s3.open(PRICING_CONFIG_LOCATION, "r") as f:
            config = json.load(f)
        return config

    def get_ids(self):
        with self.s3.open(ID_CONFIG_LOCATION, "r") as f:
            id_config = json.load(f)
        return id_config['id_configs'][self.index]

    def get_pricing_id(self, id):
        new_id = None
        self.requests_count += 1
        for i in range(NUM_REQUEST_TRIES):
            if i > 0:
                print(f"try {i + 1} getting pricing ID")
            try:
                new_id = get_pricing_id(id)
            except requests.exceptions.ReadTimeout as e:
                print(f"Read timeout in pricing ID... issue w short timeout wait: {e}")
                continue
            except KeyError as e:
                self.key_error += 1
                print(f"Key error in pricing id: {e}")
                continue
            except AttributeError as e:
                self.attribute_error += 1
                print(f"Attribute Error in pricing id, has been None return: {e}")
                continue
            except urllib3.util.retry.MaxRetryError as e:
                self.max_retry += 1
                traceback.print_exc()
                print(f"MaxRetryError triggered during pricing ID request: {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.ProxyError as e:
                self.proxy += 1
                traceback.print_exc()
                print(f"ProxyError triggered during pricing ID request: {e}")
                continue  # continues thru loop if fails
            except requests.exceptions.ConnectionError as e:
                self.connection += 1
                traceback.print_exc()
                print(f"Connection Error triggered during pricing ID request: {e}")
                continue  # continues thru loop if fails
            break

        if new_id is None:
            raise()

        return new_id

    def insert_id_into_config(self, id, config):
        cfg = copy.deepcopy(config)
        # TODO do this id thing dynamically configure the path to id
        cfg['request_config']['variables']['id'] = self.get_pricing_id(id)
        # today = datetime.datetime.now().strftime("%Y-%d-%m")
        # tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%d-%m")
        # cfg['request_config']['variables']['checkIn'] = today
        # cfg['request_config']['variables']['checkOut'] = tomorrow
        cfg['request_config']['params'][4][1] = json.dumps(cfg['request_config']['variables'])
        # print(cfg['request_config']['variables']['checkIn'])
        del cfg['request_config']['variables']
        return cfg

    def parse_result(self, id_, result):
        return parse_pricing(id_, result)

    def write_result(self, out_config):
        self.dataframe_to_s3(**out_config)
