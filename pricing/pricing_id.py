import requests
import json
from bs4 import BeautifulSoup


def request_pricing_id(id, proxies, obj=None):
    # TODO eventually want to do this better, create db mapping and hit that
    # internally before doing an extra external ping
    url = f"https://www.airbnb.com/rooms/{int(id)}?federated_search_id=fea61919-9f66-4005-a6cd-4a979c5b045e&source_impression_id=p3_1647145020_gJKhEqRJmmrMnYcL"
    headers = {
        "authority": "www.airbnb.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "device-memory": "8",
        "dpr": "0.9",
        "ect": "4g",
        "referer": "https://www.airbnb.com/rooms/134238?adults=1&category_tag=Tag%3A8536&children=0&infants=0&search_mode=flex_destinations_search&check_in=2023-01-11&check_out=2023-01-17&federated_search_id=3b667d77-ae15-4f21-930a-ddcdf0a046ee&source_impression_id=p3_1667948539_QD7zmlrahlewwCFE",
        "sec-ch-ua": "\"Google Chrome\";v=\"107\", \"Chromium\";v=\"107\", \"Not=A?Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "viewport-width": "2598",
        "x-airbnb-api-key": "d306zoyjsyarp7ifhu67rjxn52tv0t20",
        "x-airbnb-graphql-platform": "web",
        "x-airbnb-graphql-platform-client": "minimalist-niobe",
        "x-airbnb-supports-airlock-v2": "true",
        "x-client-request-id": "02g3t4q1s9ajma1lgth2x0uyolnf",
        "x-csrf-without-token": "1",
        "x-niobe-short-circuited": "true"
    }
    # proxies = {
    #     "http": "http://jdiemmanuele:pXvpvIJKHLLnr0Mk_country-UnitedStates@52.55.139.214:31112",
    #     "https": "http://jdiemmanuele:pXvpvIJKHLLnr0Mk_country-UnitedStates@52.55.139.214:31112"
    # }
    # proxies = None
    print(url)
    r = requests.get(url, proxies=proxies, headers=headers, timeout=4)  # , params=params)
    if obj:
        obj.last_request = r.text
    soup = BeautifulSoup(r.content, 'html.parser')
    permission = soup.find("script", {"id": "data-deferred-state"})

    # checking manually if 403 error useful if want to be pulling from mapping somewhere
    # # print(json.dumps(json.loads(permission.text), indent=4))
    # print(json.dumps(json.loads(permission.text)["niobeMinimalClientData"][0][1]['error']["message"], indent=4))
    # print("403" in json.dumps(json.loads(permission.text)["niobeMinimalClientData"][0][1]['error']["message"], indent=4))

    tag = soup.find("script", {"id": "data-state"})
    x = json.loads(tag.text)
    string = x['niobeMinimalClientData'][0][0]
    new_id = json.loads(string[string.find("{"):])['id']
    return new_id


def get_pricing_id(id, config, obj=None):
    # print(config['configs'].keys())
    if "proxies" in config["configs"][0]['request_config']:
        proxies = config["configs"][0]['request_config'].get("proxies")
    else:
        proxies = None
    new_id = request_pricing_id(id, proxies, obj=obj)
    return new_id


if __name__ == "__main__":
    # testing
    get_pricing_id(1)
    get_pricing_id(21026933.0)
