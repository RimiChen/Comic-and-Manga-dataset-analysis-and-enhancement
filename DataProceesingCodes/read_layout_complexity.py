
import csv
import json

final_count = {}


### read csv
CSV_FILE = "layout_complexity.csv"

with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row)
        #print(row['Transitions1'], row['Tansitions2'])
        key_1 = row['folder']
        key_2 = row['complex score']
        final_count[key_1] = key_2


json_file = open("ordered_layout_complexity.json", "w")
# magic happens here to make it pretty-printed
json_file.write(json.dumps(final_count, indent=4))
json_file.close()   

