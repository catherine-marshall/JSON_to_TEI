# This is the updated version
import json

filename = "Korean_test_report.json"

with open(filename, 'r', encoding='utf-8') as json_file:
    json_load = json.load(json_file)
    print(json_load)