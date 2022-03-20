import pandas as pd
import datetime
import json


def parse_reviews(id, response):
    rev_dict = json.loads(response.text)
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data_dict = {}
    data_dict["date_of_review"] = []
    data_dict["review"] = []
    data_dict["rating"] = []
    data_dict["pulled"] = []    # Do we need this or only the one below???
    for review in rev_dict["data"]["merlin"]["pdpReviews"]["reviews"]:
        data_dict["date_of_review"].append(str(review["createdAt"]))
        data_dict["review"].append(str(review["comments"]).encode('utf-8','ignore').decode("utf-8"))
        data_dict["rating"].append(int(review["rating"]))

    data_dict["id"] = id
    data_dict["pulled"] = time
    return pd.DataFrame(data_dict)

