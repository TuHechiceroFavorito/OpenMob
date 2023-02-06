# File used during api tutorial for ElecSoc members

import requests

url = "https://httpbin.org/get"

args = {"something":"in here"}

req = requests.get(url, params=args)
print(req.content.decode("utf-8"))