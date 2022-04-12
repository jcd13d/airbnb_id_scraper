import datetime
import json

import pandas as pd


def price_string_to_int(string):
    string = string.replace(",", "")
    leading_char = string[0]
    pos_neg = 1

    if leading_char == "-":
        # number is negative
        pos_neg = -1
        string = string[1:]

    return pos_neg*int(string[1:]), string[0]


def parse_pricing(id, response, check_in, check_out):
    df = None
    try:
        df = parse_pricing_helper(id, response, check_in, check_out)
    except ValueError as e:
        print(json.dumps(json.loads(response.text), indent=4))
        print(f"Value Error in price parsing: {e}")

    return df


def parse_pricing_helper(id, response, check_in, check_out):
    # TODO parse this more reliably, configure path?
    # theres another price location in the return we can parse... looks like the same info though.
    # TODO need to handle when no cleaning fee
    # TDOO need to handle negative price and commas
    # make area for negative price - early bird discount.. be sure to log every time we find a
    # key we dont recognize
    pricing_items = json.loads(response.text)['data']['presentation']['stayProductDetailPage']['sections']['sections'][0]['section']['barPrice']['explanationData']['priceGroups'][0]['items']
    data_dict = {}
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    features = [
        'cleaning_fee',
        'service_fee',
        'total_price',
        'check_in',
        'check_out',
        'total_price_description',
        'currency',
        'pull_time',
        'id'
    ]
    for feature in features:
        data_dict[feature] = []

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
            data_dict['check_in'] = check_in
            data_dict['check_out'] = check_out

    for feature in features:
        if len(data_dict[feature]) == 0:
            data_dict[feature].append(None)

    return pd.DataFrame(data_dict)

