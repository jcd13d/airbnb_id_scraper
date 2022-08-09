import sys
import argparse

from pricing.pricing_scraper import PricingScraper
from reviews.review_scraper import ReviewScraper
from occupancy.occupancy_scraper import OccupancyScraper
import datetime
import os
import faulthandler; faulthandler.enable()


def get_scrapers(index, trigger_time, selector="all"):
    scrapers = []
    if selector == "all" or "o" in selector:
        scrapers.append(OccupancyScraper(index, trigger_time))
    if selector == "all" or "r" in selector:
        scrapers.append(ReviewScraper(index, trigger_time))
    if selector == "all" or "p" in selector:
        scrapers.append(PricingScraper(index, trigger_time))
    return scrapers


if __name__ == "__main__":
    # start = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    time_format = "%Y/%m/%d %H:%M:%S"
    start = datetime.datetime.now().strftime(time_format)

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", help="pull time")
    parser.add_argument("-s", "--scrapers", help="which scrapers to run", default="all")

    args = parser.parse_args()

    try:
        index = int(os.environ['AWS_BATCH_JOB_ARRAY_INDEX'])
    except KeyError as e:
        print("Not running on batch! default to index 0.")
        index = 0

    scrapers = get_scrapers(index, selector=args.scrapers, trigger_time=args.time)

    [scraper.run() for scraper in scrapers]
    time = datetime.datetime.now().strftime(time_format)
    print(f"Start: {start}")
    print(f"End: {time}")

    [scraper.print_error_stats() for scraper in scrapers]


