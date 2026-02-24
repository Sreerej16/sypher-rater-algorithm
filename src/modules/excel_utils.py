# modules/excel_utils.py

import pandas as pd
import json

def load_excel_metadata(excel_file):
    """
    Loads metadata from an Excel file. Each sheet in the Excel file is expected to have:
    - First row: Indicates whether a column is a 'lookup' or a 'factor'.
    - Second row: Contains column headers.
    - Third row onward: Data values.

    Parameters:
        excel_file (str): Path to the Excel file.

    Returns:
        dict: A data dictionary with metadata extracted from the Excel file.
        dict: A dictionary of DataFrames representing the factor tables.
    """
    # Read all sheets into a dictionary of DataFrames
    factor_tables = pd.read_excel(excel_file, sheet_name=None, header=None)
    data_dict = {}

    for sheet_name, df in factor_tables.items():
        if df.empty:
            continue  # Skip empty sheets

        # Read the first row (lookup/factor indicator) and second row (headers)
        indicator_row = df.iloc[0].fillna('')  # First row: lookup or factor indicator
        headers_row = df.iloc[1].fillna('')  # Second row: actual headers

        # Ensure all headers are strings and strip any extra whitespace
        headers_row = headers_row.apply(lambda x: str(x).strip() if isinstance(x, str) else str(x))

        # Identify lookup keys and factor columns based on the indicator row
        lookup_keys = [
            col for col in headers_row[indicator_row.str.lower() == 'lookup']
            if isinstance(col, str) and col.strip() != ""
        ]
        
        factor_columns = {
            f"{col.lower()}_factor": col
            for col in headers_row[indicator_row.str.lower() == 'factor']
            if isinstance(col, str) and col.strip() != ""
        }

        # Use the sheet name as the attribute name
        attribute_name = sheet_name.lower().replace(' ', '_')

        # Build the configuration for this attribute
        data_dict[attribute_name] = {
            'sheet_name': sheet_name,
            'lookup_keys': lookup_keys if lookup_keys else [],  # Handle empty list if no lookup keys
            'factor_columns': factor_columns
        }

        # Skip only the first two rows (indicator and header) to load actual data
        factor_tables[sheet_name] = df.iloc[2:].reset_index(drop=True)

        # Set the headers from the second row
        factor_tables[sheet_name].columns = headers_row

    return data_dict, factor_tables


def save_data_dict_to_json(data_dict, json_file_path):
    """
    Saves the data dictionary to a JSON file for manual editing or future use.

    Parameters:
        data_dict (dict): The data dictionary to save.
        json_file_path (str): The path to the JSON file.
    """
    with open(json_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)
    print(f"Data dictionary has been generated and saved to '{json_file_path}'.")


def load_reference(json_file, excel_file):
    """
    Loads the data dictionary from a JSON file and loads corresponding data from the Excel file.

    Parameters:
        json_file (str): Path to the JSON file containing the data dictionary.
        excel_file (str): Path to the Excel file containing the reference tables.

    Returns:
        dict: Loaded data dictionary.
        dict: Loaded factor tables from the Excel file.
    """
    with open(json_file, 'r') as f:
        data_dict = json.load(f)

    # Load the factor tables from the Excel file with headers from the second row (index 1)
    factor_tables = pd.read_excel(excel_file, sheet_name=None, header=1)

    return data_dict, factor_tables


def dump_reference_to_excel(data_dict, factor_tables, output_excel):
    """
    Dumps the contents of the data dictionary and factor tables into an Excel file.

    Parameters:
        data_dict (dict): The data dictionary to dump.
        factor_tables (dict): The factor tables to include.
        output_excel (str): The path to the output Excel file.
    """
    with pd.ExcelWriter(output_excel) as writer:
        for attribute, config in data_dict.items():
            sheet_name = config['sheet_name']
            if sheet_name in factor_tables:
                factor_tables[sheet_name].to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Data dictionary contents have been written to '{output_excel}'.")


def create_input_layout_excel(data_dict, output_excel):
    """
    Creates an Excel file layout based on the lookup keys found in the data dictionary.

    Parameters:
        data_dict (dict): The data dictionary with metadata.
        output_excel (str): The path to the output Excel file.
    """
    lookup_columns = []

    # Collect all lookup keys from all attributes
    for attribute, config in data_dict.items():
        lookup_columns.extend(config.get('lookup_keys', []))

    # Remove duplicates while keeping order
    lookup_columns = list(dict.fromkeys(lookup_columns))

    # Create a DataFrame with lookup columns
    input_layout_df = pd.DataFrame(columns=lookup_columns)

    # Save the layout to an Excel file
    with pd.ExcelWriter(output_excel) as writer:
        input_layout_df.to_excel(writer, sheet_name='Input Layout', index=False)
    print(f"Input layout Excel file has been generated at '{output_excel}'.")
