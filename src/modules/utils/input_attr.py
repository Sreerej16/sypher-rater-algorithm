import pandas as pd
import json

# Step 1: Load the CSV file and extract the header
csv_file_path = '..\..\..\data\input_files\Risk Characteristics_v1.1.csv'
df = pd.read_csv(csv_file_path)

# Extract column names from the header
columns = df.columns.tolist()

config = {
    "input": [{ col: {"field" :col, "type": "str" }} for col in columns]  # Change structure to include field and type
}

# Step 3: Write the configuration to a JSON file
config_file_path = 'input.json'
with open(config_file_path, 'w') as config_file:
    json.dump(config, config_file, indent=4)

with open(config_file_path, 'r') as json_file:
    config = json.load(json_file)

policy_number_field = config['input'][0]['policy_number']['field']  # Accessing policy_number field

print(policy_number_field)

print(f"Configuration file saved to {config_file_path}")

