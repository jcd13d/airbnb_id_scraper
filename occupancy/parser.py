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
            data_dict["date"].append(day_dict["calendarDate"])
            data_dict["available"].append(day_dict["available"])
            data_dict["max_nights"].append(day_dict["maxNights"])
            data_dict["min_nights"].append(day_dict["minNights"])
            data_dict["available_for_checkin"].append(day_dict["availableForCheckin"])
            data_dict["available_for_checkout"].append(day_dict["availableForCheckout"])
            data_dict["bookable"].append(day_dict["bookable"])

    data_dict["id"] = id
    data_dict["pulled"] = time
    return pd.DataFrame(data_dict)

