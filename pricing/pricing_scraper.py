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
    def __init__(self, scraper_index, trigger_time):
        super().__init__(scraper_index, trigger_time)
        self.curr_check_in = None
        self.curr_check_out = None
        self.id_map = {}

    def get_config(self):
        with self.s3.open(PRICING_CONFIG_LOCATION, "r") as f:
            config = json.load(f)
        return config

    def get_ids(self):
        with self.s3.open(ID_CONFIG_LOCATION, "r") as f:
            id_config = json.load(f)
        return id_config['id_configs'][self.index]

    def get_pricing_id(self, id, config):

        try:
            return self.id_map[id]
        except KeyError as e:
            pass

        new_id = None
        self.requests_count += 1
        for i in range(NUM_REQUEST_TRIES):
            if i > 0:
                print(f"try {i + 1} getting pricing ID")
            try:
                new_id = get_pricing_id(id, self.config, self)
            except requests.exceptions.ReadTimeout as e:
                print(f"Read timeout in pricing ID... issue w short timeout wait: {e}")
                continue
            except KeyError as e:
                self.key_error += 1
                print(f"Key error in pricing id: {e}")
                print(self.last_request)
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

        self.id_map[id] = new_id

        return new_id

    def insert_id_into_config(self, id, config):
        cfg = copy.deepcopy(config)
        # TODO do this id thing dynamically configure the path to id
        cfg['request_config']['variables']['id'] = self.get_pricing_id(id, self.config)
        self.curr_check_in = config['request_config']['variables']['pdpSectionsRequest']['checkIn']
        self.curr_check_out = config['request_config']['variables']['pdpSectionsRequest']['checkOut']
        cfg['request_config']['params'][4][1] = json.dumps(cfg['request_config']['variables'])
        del cfg['request_config']['variables']
        return cfg

    def parse_result(self, id_, result):
        return parse_pricing(id_, result, self.curr_check_in, self.curr_check_out, self.get_current_time())

    def write_result(self, data, out_config):
        self.dataframe_to_s3(data, **out_config)
