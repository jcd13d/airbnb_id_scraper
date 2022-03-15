import requests
import json


if __name__ == "__main__":
    proxies = {
        "http": "http://jdiemmanuele:pXvpvIJKHLLnr0Mk_country-UnitedStates@3.223.24.247:31112",
        "https": "http://jdiemmanuele:pXvpvIJKHLLnr0Mk_country-UnitedStates@3.223.24.247:31112"
    }

    url = "https://ipv4.icanhazip.com"
    runs = 1000

    ip_dict = {}
    ssl_errors = 0
    proxy_errors = 0

    for i in range(runs):
        response = None
        try:
            response = requests.get(url, proxies=proxies, timeout=3).text
        except requests.exceptions.ProxyError as e:
            print("Proxy Error")
            ssl_errors += 1
        except requests.exceptions.SSLError as e:
            print("SSL Error")
            proxy_errors += 1

        print(response)
        if response in ip_dict.keys():
            ip_dict[response] += 1
        else:
            ip_dict[response] = 1

    print(json.dumps(ip_dict, indent=4))
    num_ips = len(ip_dict.keys())
    print(f"number of unique IPs: {num_ips} out of {runs}, {100*num_ips/runs}%")
    print(f"SSL Errors: {ssl_errors}")
    print(f"Proxy Errors: {proxy_errors}")
# number of unique IPs: 413 out of 1000, 41.3%
# SSL Errors: 367
# Proxy Errors: 4