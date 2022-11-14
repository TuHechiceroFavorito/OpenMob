import requests

url = "https://httpbin.org/get?key=value"

args = {"key":"value"}

req = requests.get(url, params=args)
print(req.content.decode("utf-8"))