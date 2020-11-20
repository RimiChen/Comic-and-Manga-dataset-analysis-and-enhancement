
import csv
import json

transitions = {}
second_transitions = {}
final_count = {}


### read csv
CSV_FILE = "COMICS_anotated_pairs.csv"

with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row['Transitions1'], row['Tansitions2'])
        key_1 = row['Transitions1']
        if key_1 not in transitions:
            transitions[key_1] = 1
        else:
            transitions[key_1] = transitions[key_1] +1
        key_2 = row['Transitions2']
        if key_2 not in second_transitions:
            second_transitions[key_2] = 1
        else:
            second_transitions[key_2] = second_transitions[key_2] +1


final_count["1"]= transitions
final_count["2"] = second_transitions

json_file = open("COMICS_transitions.json", "w")
# magic happens here to make it pretty-printed
json_file.write(json.dumps(final_count, indent=4))
json_file.close()   

