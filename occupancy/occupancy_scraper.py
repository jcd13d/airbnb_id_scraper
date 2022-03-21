from scraper_base.scraper import IdScraper
from config.constants import OCC_CONFIG_LOCATION, ID_CONFIG_LOCATION
from occupancy.parser import parse_occupancy
import json
import copy


class OccupancyScraper(IdScraper):
    def __init__(self, scraper_index):
        super().__init__(scraper_index)

    def get_config(self):
        with self.s3.open(OCC_CONFIG_LOCATION, "r") as f:
            config = json.load(f)
        return config

    def get_ids(self):
        with self.s3.open(ID_CONFIG_LOCATION, "r") as f:
            id_config = json.load(f)
        return id_config['id_configs'][self.index]

    def insert_id_into_config(self, id, config):
        cfg = copy.deepcopy(config)
        cfg['request_config']['variables']['request']['listingId'] = id
        cfg['request_config']['params'][4][1] = json.dumps(cfg['request_config']['variables'])
        del cfg['request_config']['variables']
        return cfg

    def parse_result(self, id_, result):
        parsed = parse_occupancy(id_, result)

        return parsed

    def write_result(self, out_config):
        self.dataframe_to_s3(**out_config)
