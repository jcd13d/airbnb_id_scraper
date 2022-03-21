import pandas as pd
import json
import numpy as np

def id_list_to_config(ids):
    ids = np.array(ids)

    total_listings = len(ids)
    listings_per_container = 300

    num_containers = (np.ceil(total_listings/listings_per_container))

    ids2 = np.pad(ids, (0, int(num_containers*listings_per_container) - total_listings))
    ids2 = ids2.reshape(-1, listings_per_container)

    ids2 = ids2.tolist()
    ids2 = [list(filter((0.0).__ne__, x)) for x in ids2] # filter out pad zeros
    return ids2

if __name__ == "__main__":

    with open("config/miami_ids.json", "r") as f:
        ids = json.load(f)

    ids = ids['id_configs'][0]

    ids2 = id_list_to_config(ids)

    new_config = {}
    new_config['id_configs'] = ids2
    with open("config/big_batch_ids.json", "w") as f:
        json.dump(new_config, f, indent=4)


