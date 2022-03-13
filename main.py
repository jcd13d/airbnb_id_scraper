from occupancy.occupancy_scraper import OccupancyScraper
from pricing.pricing_scraper import PricingScraper
import datetime
import os


def get_scrapers(id_):
    scrapers = [
        OccupancyScraper(id_),
        PricingScraper(id_)
    ]
    return scrapers


if __name__ == "__main__":
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Start: {time}")
    scrapers = get_scrapers(int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX']))
    [scraper.run() for scraper in scrapers]
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"End: {time}")


    # Start: 12/03/2022 21:26:03 for miami run
    # killed 1103PM ran 1843 occupancy 23:03
    # 2.3 hours


