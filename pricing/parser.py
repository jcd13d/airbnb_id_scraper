import datetime
import json

import pandas as pd


def price_string_to_int(string):
    return int(string[1:]), string[0]


def parse_pricing(id, response):
    # TODO parse this more reliably, configure path?
    # theres another price location in the return we can parse... looks like the same info though.
    pricing_items = json.loads(response.text)['data']['presentation']['stayProductDetailPage']['sections']['sections'][0]['section']['barPrice']['explanationData']['priceGroups'][0]['items']
    data_dict = {}
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data_dict['cleaning_fee'] = []
    data_dict['service_fee'] = []
    data_dict['total_price'] = []
    data_dict['total_price_description'] = []
    data_dict['currency'] = []
    data_dict['pull_time'] = []
    data_dict['id'] = []
    for item in pricing_items:
        description = item['description']
        price, currency = price_string_to_int(item['priceString'])

        if description == "Cleaning fee":
            data_dict["cleaning_fee"].append(price)
        elif description == "Service fee":
            data_dict["service_fee"].append(price)
        elif "night" in description:
            data_dict["total_price"].append(price)
            data_dict["total_price_description"].append(description)
            data_dict['currency'].append(currency)
            data_dict['pull_time'].append(time)
            data_dict['id'].append(id)

    return pd.DataFrame(data_dict)

