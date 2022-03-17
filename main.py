from pricing.pricing_scraper import PricingScraper
from reviews.review_scraper import ReviewScraper
from occupancy.occupancy_scraper import OccupancyScraper
import datetime
import os


def get_scrapers(index):
    scrapers = [
        OccupancyScraper(index),
        ReviewScraper(index),
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


    # PRICING RUNS

    # Start: 12/03/2022 21:26:03 for miami run
    # killed 1103PM ran 1843 occupancy 23:03
    # 2.3 hours

    # End: 13/03/2022 19:19:29

    # 11 min

    # Start: 13 / 03 / 2022
    # 19: 48:00
    # End: 13 / 03 / 2022
    # 20: 03:39
    # 15 min

    # Start: 13 / 03 / 2022
    # 21: 25:03
    # End: 13 / 03 / 2022
    # 21: 42:29

    """
            SSL Error: 1
        Type Error: 8
        Timeouts: 0
        Max Retry: 0
        Proxy Error: 21
        Key Error: 72
        Connection Error: 0
        Num Requests: 287
        Num IDs Run: 100
        
    Start: 14/03/2022 19:46:03
    End: 14/03/2022 19:53:47
    """

    # OCC RUNS


