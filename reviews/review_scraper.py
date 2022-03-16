import pyarrow.parquet as pq
import pyarrow as pa
from scraper_base.scraper import IdScraper
from config.constants import ID_CONFIG_LOCATION, REVIEW_CONFIG_LOCATION
from reviews.parser import parse_reviews
import json
import copy
import os

class ReviewScraper(IdScraper):
    def __init__(self, scraper_index):
        super().__init__(scraper_index)

    def get_config(self):
        with open(REVIEW_CONFIG_LOCATION, "r") as f:
            config = json.load(f)
        return config

    def get_ids(self):
        with open(ID_CONFIG_LOCATION, "r") as f:
            id_config = json.load(f)
        return id_config['id_configs'][self.index]

    def insert_id_into_config(self, id, config):
        cfg = copy.deepcopy(config)
        # TODO do this id thing dynamically configure the path to id
        cfg['request_config']['variables']['request']['listingId'] = id
        cfg['request_config']['params'][4][1] = json.dumps(cfg['request_config']['variables'])
        del cfg['request_config']['variables']
        return cfg

    def parse_result(self, id_, result):
        return parse_reviews(id_, result)

    def write_result(self, id, result, out_location):
        table = pa.Table.from_pandas(result)
        pq.write_to_dataset(table, root_path=out_location)

