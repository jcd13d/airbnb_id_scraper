from scraper_base.scraper import IdScraper
from config.constants import ID_CONFIG_LOCATION, REVIEW_CONFIG_LOCATION
from reviews.parser import parse_reviews
import json
import copy


class ReviewScraper(IdScraper):
    def __init__(self, scraper_index, trigger_time):
        super().__init__(scraper_index, trigger_time)

    def get_config(self):
        with self.s3.open(REVIEW_CONFIG_LOCATION, "r") as f:
            config = json.load(f)
        return config

    def get_ids(self):
        with self.s3.open(ID_CONFIG_LOCATION, "r") as f:
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
        return parse_reviews(id_, result, self.get_current_time())

    def write_result(self, data, out_config):
        self.dataframe_to_s3(data, **out_config)

