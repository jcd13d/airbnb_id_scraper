import s3fs
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
        # config = self.read_json_s3(S3_BUCKET_NAME, OCC_CONFIG_LOCATION)
        return config

    def get_ids(self):
        with self.s3.open(ID_CONFIG_LOCATION, "r") as f:
            id_config = json.load(f)
        # id_config = self.read_json_s3(S3_BUCKET_NAME, ID_CONFIG_LOCATION)
        return id_config['id_configs'][self.index]

    def insert_id_into_config(self, id, config):
        cfg = copy.deepcopy(config)
        # TODO do this id thing dynamically configure the path to id
        cfg['request_config']['variables']['request']['listingId'] = id
        cfg['request_config']['params'][4][1] = json.dumps(cfg['request_config']['variables'])
        del cfg['request_config']['variables']
        return cfg

    def parse_result(self, id_, result):
        parsed = parse_occupancy(id_, result)
        # for i in range(NUM_REQUEST_TRIES):
        #     try:
        #         parsed = parse_occupancy(id_, result)
        #     except TypeError as e:
        #         traceback.print_exc()
        #         print(f"TypeError triggered: {e}")
        #         print(result)
        #         print(json.dumps(json.loads(result.text), indent=4))
        #         continue
        #     break
        #
        # if parsed is None:
        #     raise()

        return parsed

    # def write_result(self, id, result, out_location):
    #     # result.to_parquet(os.path.join(out_location, f"{id}.parquet"))
    #     table = pa.Table.from_pandas(result)
    #     pq.write_to_dataset(table, root_path=out_location)
    #     # print(pd.read_parquet(out_location))

    def write_result(self, id, result, out_config):
        self.dataframe_to_s3(result, **out_config)
