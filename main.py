from pricing.pricing_scraper import PricingScraper
from reviews.review_scraper import ReviewScraper
from occupancy.occupancy_scraper import OccupancyScraper
import datetime
import os
import faulthandler; faulthandler.enable()


def get_scrapers(index):
    scrapers = [
        OccupancyScraper(index),
        # ReviewScraper(index),
        PricingScraper(index),
    ]
    return scrapers


if __name__ == "__main__":
    start = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    try:
        index = int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])
    except KeyError as e:
        print("Not running on batch! default to index 0.")
        index = 0

    scrapers = get_scrapers(index)
    [scraper.run() for scraper in scrapers]
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"Start: {start}")
    print(f"End: {time}")

    [scraper.print_error_stats() for scraper in scrapers]


