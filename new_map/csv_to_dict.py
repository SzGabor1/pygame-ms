import csv
import json

# Define the input CSV file path
csv_file = "new_map\MSmap._grass.csv"

# Create an empty list to store the data
map_data = []

# Open the CSV file and read its contents, skipping the header row
with open(csv_file, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    # Skip the header row
    next(csv_reader)
    for i, row in enumerate(csv_reader):
        for j, value in enumerate(row):
            # Convert the value to an integer
            value = int(value)
            # Check if the value is not -1
            if value != -1:
                # Create a dictionary entry for this cell
                map_data.append({"i": i, "j": j, "value": value})

# Define the output Python file path
python_file = "map_data.py"

# Save the list of dictionaries to a Python file
with open(python_file, 'w') as pyfile:
    pyfile.write("map_data = ")
    json.dump(map_data, pyfile, indent=4)

print(f"Dictionary saved to {python_file}")
