"""
Simple Program to help you get started with Google's APIs
"""
import urllib.request, json
#Sends the request and reads the response.
response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/directions/json?origin=53.306292,-6.218746&destination=53.303945,-6.217236&mode=walking&language=en&alternatives=false&units=metric&key=AIzaSyDX2viar6xzqIYr_vRabSQJROdDoHC2QjU").read()
#Loads response as JSON
directions = json.loads(response)
print(directions)