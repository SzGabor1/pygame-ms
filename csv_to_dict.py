import csv
import json

csv_file = "new_map\MSmap._dungeonentrance.csv"
map_data = []

with open(csv_file, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)

    for i, row in enumerate(csv_reader):
        for j, value in enumerate(row):

            value = int(value)

            if value != -1:
                if value == 142:
                    print('142')

                map_data.append({"i": i, "j": j, "value": value})

python_file = "world_dungeonentrance"

with open(python_file, 'w') as pyfile:
    pyfile.write("map_data = ")
    json.dump(map_data, pyfile, indent=4)

print(f"Dictionary saved to {python_file}")
