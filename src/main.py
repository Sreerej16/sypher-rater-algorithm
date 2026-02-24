import sys
import os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modules'))

import pandas as pd
import json
import warnings
warnings.filterwarnings("ignore")
from config_reader import load_config
from file_io import read_excel_from_config, read_excel_sheets_to_dfs, read_input_csv
from modules.calculation_dispatch import process_all_calculations  # Calculation logic module
from modules.file_io import save_to_csv
from modules.utils.json_handler import get_list_of_input_attributes

# Step 1: Load the config data
input = load_config('input.json')
files = load_config('files.json')
reference = load_config('reference.json')

# Step 2: Read the data dictionary json (resolve all paths relative to project root)
def abs_path(p): return os.path.join(PROJECT_ROOT, p) if p else p
reference_path = abs_path(files.get('files', {}).get('reference'))
reference_data_excel_path = abs_path(files.get('files', {}).get('reference_data_excel'))
input_file_path = abs_path(files.get('files', {}).get('input_file'))
output_file_all = abs_path(files.get('files', {}).get('output_file_all'))
output_file_path_premium = abs_path(files.get('files', {}).get('output_file_premium'))
output_file_factor_and_premium = abs_path(files.get('files', {}).get('output_file_factor_and_premium'))
input_json = input.get('input')


print(f"Reference Config Path: {reference_path}")
print(f"Excel Path: {reference_data_excel_path}")
print(f"Input Path: {input_file_path}")
print(f"Output Path: {output_file_all}")
#print(f"Input json: {input_json}")

#with open(reference_path, 'r') as json_file:
#    json.load(json_file)

# Step 3: Read the excel file with the reference data
ref_df = read_excel_from_config(reference_data_excel_path)

# Step 4: Read the specified sheets into DataFrames
dataframes = read_excel_sheets_to_dfs(reference_path, reference_data_excel_path)

# Step 5: Print the DataFrames to verify - comment out later
# for table_name, df in dataframes.items():
#     print(f"\nDataFrame for {table_name}:")

# Step 6: Load the input CSV containing the attributes
input_df = read_input_csv(input_file_path)
#print (input_df.head())

# Step 7: Process the calculations using the input attributes and reference data
input_attrs = get_list_of_input_attributes()
output_df = process_all_calculations(input_df, dataframes, input_json)

# Step 8: Rename the output columns to indicate inputs, factors and premium. Reorder output as needed

# Step 9: Save the DataFrame with all calculations into the output CSV
save_to_csv(output_df, output_file_all)

for col in input_attrs:
    if col not in output_df.columns:
        output_df[col] = pd.NA
extracted_df = output_df[input_attrs]
additional_columns_1 = output_df.columns[output_df.columns.str.endswith('_factor') | output_df.columns.str.endswith('_premium')]
extracted_df_1 = pd.concat([extracted_df, output_df[additional_columns_1]], axis=1)

save_to_csv(extracted_df_1, output_file_factor_and_premium)

additional_columns_2 = output_df.columns[output_df.columns.str.endswith('_premium')]
extracted_df_2 = pd.concat([extracted_df, output_df[additional_columns_2]], axis=1)

save_to_csv(extracted_df_2, output_file_path_premium)

print(f"Process complete. Outputs saved to '{output_file_all}', '{output_file_factor_and_premium}', and '{output_file_path_premium}'.")





