from occupancy.occupancy_scraper import OccupancyScraper
import os


def get_scrapers(id_):
    scrapers = [
        OccupancyScraper(id_)
    ]
    return scrapers


if __name__ == "__main__":
    scrapers = get_scrapers(int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX']))
    [scraper.run() for scraper in scrapers]


