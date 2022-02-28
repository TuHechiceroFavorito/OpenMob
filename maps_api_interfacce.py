"""
Simple Program to help you get started with Google's APIs
"""
import urllib.request, json, os, sys

def request_api():
    # Read the API key from the file
    with open("key.txt", "r") as f:
        key = f.read()

    #Sends the request and reads the response.
    #response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/directions/json?").read()
    #Loads response as JSON

    body = "https://maps.googleapis.com/maps/api/directions/json?"
    origin = "origin=53.306292,-6.218746"
    destination = "&destination=53.303965,-6.217158"
    mode = "&mode=walking"
    language = "&language=en"
    alternatives = "&alternatives=false"
    units = "&units=metric"
    api_key = "&key=" + key


    response = body + origin + destination + mode + language + alternatives + units + api_key
    response_final = urllib.request.urlopen(response).read()

    with open("response.json", "w") as f:
        f.write(response_final.decode("utf-8"))


def test_reading():
    with open("response.json", "r") as f:
        response = f.read()

    directions = json.loads(response)


    i=1

    for x in directions["routes"][0]["legs"][0]["steps"]:
        # if x == "distance":
        print(f"distance {x['distance']}") 
        print(f"duration {x['duration']}")    
        print(f"end_location {x['end_location']}")
        print(f"start_location {x['start_location']}\n")
        print(f"***Node {i} has been reached***\n")

        i+=1

test_reading()

# sys.stdout.close()
