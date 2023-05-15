
import json

#Takes a json file, opens it, then parses it into a dictionary######################
def parseJSON(filename):
    with open(filename, 'r', encoding='utf-8') as json_file:
        json_load = json.load(json_file)
    return json_load
