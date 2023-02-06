# Google Maps interface. Gets the route needed to follow given the starting and ending 
# coordinates


import urllib.request, json
from pprint import pprint

dir = "maps/"

# Makes the call to google maps api and stores the response
def request_api(origin_coord, destination_coord):
    ori_coord = str(origin_coord[0]) + "," + str(origin_coord[1])
    dest_coord = str(destination_coord[0]) + "," + str(destination_coord[1])

    # Read the API key from the file - NOT IN THE REPO
    with open(dir + "key.txt", "r") as f:
        key = f.read()

    #Sends the request and reads the response.
    #response = urllib.request.urlopen("https://maps.googleapis.com/maps/api/directions/json?").read()
    #Loads response as JSON

    body = "https://maps.googleapis.com/maps/api/directions/json?"
    # Atributes for the api
    origin = "origin=" + ori_coord                                # Format: 53.306292,-6.218746
    destination = "&destination=" + dest_coord
    mode = "&mode=walking"
    language = "&language=en"
    alternatives = "&alternatives=false"
    units = "&units=metric"
    api_key = "&key=" + key

    # Construct url
    response = body + origin + destination + mode + language + alternatives + units + api_key
    print("Requesting data from Maps")
    response_final = urllib.request.urlopen(response).read()

    # Store response in 'response.json' for further processing
    with open(dir + "response.json", "w") as f:
        f.write(response_final.decode("utf-8"))

    process_data()

# Takes the data in 'response.json' and parse the needed information
def process_data():
    print("Processing data")
    
    # Read the file and load data in a variable
    with open(dir + "response.json", "r") as f:
        response = f.read()

    directions = json.loads(response)

    # Extract the field of interest from the data - The steps required for the first route in walking mode
    steps = directions["routes"][0]["legs"][0]["steps"]

    nodes = {}
    # Extract the nodes for the route. A node is each turning point in the route
    for node_number, step in enumerate(steps):
        nodes[node_number] = f"{step['end_location']['lat']}, {step['end_location']['lng']}"

    # Store the nodes in 'nodes.json'
    print("Nodes extracted")
    with open(dir + "nodes.json", "w") as f:
            f.write(json.dumps(nodes))

# Returns the coordinates for the next node given the current node index
def get_node(node):
    print(f"Getting information for node {node + 1}")
    with open(dir + "nodes.json", "r") as f:
        nodes = json.loads(f.read())

    num_nodes = len(nodes) - 1
    # If the current node index is greater than the number of nodes, the end point has been reached
    if node > num_nodes:
        print("NO MORE NODES")
        return "END"

    # Otherwise, split the coordinates and return them as a 2 element list of floats
    proc_node = []
    for el in nodes[str(node)].split(", "):
        proc_node.append(float(el))

    return proc_node

# Testing
if __name__ == "__main__":
    # Coordinates of two places in UCD
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