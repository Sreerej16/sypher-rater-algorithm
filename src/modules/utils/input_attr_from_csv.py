import pandas as pd
import json

# Load the CSV file into a DataFrame
df = pd.read_csv('data.csv')

# Create the JSON structure
output_json = {"input": []}

# Populate the JSON structure with data from the DataFrame
for index, row in df.iterrows():
    field_dict = {row['src_field']: {"field": row['field'], "type": row['type']}}
    output_json["input"].append(field_dict)

# Convert to JSON string (optional)
json_output = json.dumps(output_json, indent=4)

# Print or save the JSON output
print(json_output)

# Optionally save to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_output)
