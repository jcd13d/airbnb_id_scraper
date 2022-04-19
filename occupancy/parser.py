import pandas as pd
import datetime
import json


def parse_occupancy(id, response):
    occ_dict = json.loads(response.text)
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data_dict = {}
    data_dict["date"] = []
    data_dict["available"] = []
    data_dict["max_nights"] = []
    data_dict["min_nights"] = []
    data_dict["available_for_checkin"] = []
    data_dict["available_for_checkout"] = []
    data_dict["bookable"] = []
    data_dict["pulled"] = []
    for month_dict in occ_dict["data"]["merlin"]["pdpAvailabilityCalendar"]["calendarMonths"]:
        for day_dict in month_dict["days"]:
            data_dict["date"].append(str(day_dict["calendarDate"]))
            data_dict["available"].append(bool(day_dict["available"]))
            data_dict["max_nights"].append(int(day_dict["maxNights"]))
            data_dict["min_nights"].append(int(day_dict["minNights"]))
            data_dict["available_for_checkin"].append(bool(day_dict["availableForCheckin"]))
            data_dict["available_for_checkout"].append(bool(day_dict["availableForCheckout"]))
            data_dict["bookable"].append(bool(day_dict["bookable"]))

    data_dict["id"] = id
    data_dict["pulled"] = str(time)
    df = pd.DataFrame(data_dict)
    df["pulled"] = df["pulled"].astype(str)
    df["date"] = df["date"].astype(str)
    df["available"] = df["available"].astype(bool)
    df["max_nights"] = df["max_nights"].astype(int)
    df["min_nights"] = df["min_nights"].astype(int)
    df["available_for_checkin"] = df["available_for_checkin"].astype(bool)
    df["available_for_checkout"] = df["available_for_checkout"].astype(bool)
    df["bookable"] = df["bookable"].astype(bool)
    print(df)
    return df

