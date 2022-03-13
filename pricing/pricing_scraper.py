import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from scraper_base.scraper import IdScraper
from config.constants import PRICING_CONFIG_LOCATION, ID_CONFIG_LOCATION, NUM_REQUEST_TRIES
from pricing.parser import parse_pricing
from pricing.pricing_id import get_pricing_id
import datetime
import json
import copy
import os


class PricingScraper(IdScraper):
    def __init__(self, scraper_index):
        super().__init__(scraper_index)

    def get_config(self):
        with open(PRICING_CONFIG_LOCATION, "r") as f:
            config = json.load(f)
        return config

    def get_ids(self):
        with open(ID_CONFIG_LOCATION, "r") as f:
            id_config = json.load(f)
        return id_config['id_configs'][self.index]

    def get_pricing_id(self, id):
        new_id = None
        for i in range(NUM_REQUEST_TRIES):
            if i > 0:
                print(f"try {i + 1} getting pricing ID")
            try:
                new_id = get_pricing_id(id)
            except KeyError as e:
                print(f"Key error in pricing id: {e}")
                continue
            break

        if new_id is None:
            raise()

        return new_id

    def insert_id_into_config(self, id, config):
        cfg = copy.deepcopy(config)
        # TODO do this id thing dynamically configure the path to id
        cfg['request_config']['variables']['id'] = self.get_pricing_id(id)
        today = datetime.datetime.now().strftime("%Y-%d-%m")
        tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%d-%m")
        cfg['request_config']['variables']['checkIn'] = today
        cfg['request_config']['variables']['checkOut'] = tomorrow
        cfg['request_config']['params'][4][1] = json.dumps(cfg['request_config']['variables'])
        del cfg['request_config']['variables']
        return cfg

    def parse_result(self, id_, result):
        return parse_pricing(id_, result)

    def write_result(self, id, result, out_location):
        table = pa.Table.from_pandas(result)
        pq.write_to_dataset(table, root_path=out_location)
        # print(pd.read_parquet(out_location))


