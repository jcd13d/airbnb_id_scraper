import requests
import json
from bs4 import BeautifulSoup


def get_pricing_id(id):
    # TODO eventually want to do this better, create db mapping and hit that
    # internally before doing an extra external ping
    url = f"https://www.airbnb.com/rooms/{id}?federated_search_id=9466eeb6-d017-4d53-8a89-de02a89e6985&source_impression_id=p3_1645900145_ErN%2FLgsBQ8Zeikmz"
    r = requests.get(url)  # , headers=headers)#, params=params)
    soup = BeautifulSoup(r.content, 'html.parser')
    tag = soup.find("script", {"id": "data-state"})
    x = json.loads(tag.text)
    string = x['niobeMinimalClientData'][0][0]
    new_id = json.loads(string[string.find("{"):])['id']
    return new_id
