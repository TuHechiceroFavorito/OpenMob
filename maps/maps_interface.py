"""
Simple Program to help you get started with Google's APIs
"""
import urllib.request, json
from pprint import pprint

dir = "maps/"


def request_api(origin_coord, destination_coord):
    ori_coord = str(origin_coord[0]) + "," + str(origin_coord[1])
    dest_coord = str(destination_coord[0]) + "," + str(destination_coord[1])

    # Read the API key from the file
    with open(dir + "key.txt", "r") as f:
        key = f.read()

    #Sends the request and reads the response.
    #response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/directions/json?").read()
    #Loads response as JSON

    body = "https://maps.googleapis.com/maps/api/directions/json?"
    origin = "origin=" + ori_coord                                # Fornmat: 53.306292,-6.218746
    destination = "&destination=" + dest_coord
    mode = "&mode=walking"
    language = "&language=en"
    alternatives = "&alternatives=false"
    units = "&units=metric"
    api_key = "&key=" + key


    response = body + origin + destination + mode + language + alternatives + units + api_key
    print("Requesting data from Maps")
    response_final = urllib.request.urlopen(response).read()

    with open(dir + "response.json", "w") as f:
        f.write(response_final.decode("utf-8"))

    process_data()


def process_data():
    print("Processing data")
    with open(dir + "response.json", "r") as f:
        response = f.read()

    directions = json.loads(response)

    steps = directions["routes"][0]["legs"][0]["steps"]

    nodes = {}

    for node_number, step in enumerate(steps):
        nodes[node_number] = f"{step['end_location']['lat']}, {step['end_location']['lng']}"

    print("Nodes extracted")
    with open(dir + "nodes.json", "w") as f:
            f.write(json.dumps(nodes))

def get_node(node):
    print(f"Getting information for node {node + 1}")
    with open(dir + "nodes.json", "r") as f:
        nodes = json.loads(f.read())

    num_nodes = len(nodes) - 1

    if node > num_nodes:
        print("NO MORE NODES")
        return "END"

    proc_node = []
    for el in nodes[str(node)].split(", "):
        proc_node.append(float(el))

    return proc_node

if __name__ == "__main__":
    origin = [53.306292,-6.218746]
    destination = [53.303965,-6.217158]
    request_api(origin, destination)

    node = 0
    coord = get_node(node)
    while coord != "END":
        print(coord)
        node += 1
        coord = get_node(node)

    print("End of trip")