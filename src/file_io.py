import pandas as pd
import json

def read_excel_from_config(excel_file_path):
    """
    Read the reference data Excel file specified in the config.

    Parameters:
        config (dict): The configuration data containing the Excel file path.

    Returns:
        pd.DataFrame: The DataFrame containing the Excel data.
    """
    if excel_file_path:
        # Read the Excel file into a DataFrame
        try:
            df = pd.read_excel(excel_file_path)
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None
    else:
        print("Excel file path not found in the config.")
        return None
    
def load_json(file_path):
    """Load a JSON file."""
    with open(file_path, 'r') as json_file:
        return json.load(json_file)
    
def read_excel_sheets_to_dfs(json_file_path, excel_file_path):
    """
    Read specified sheets from an Excel file into DataFrames based on a JSON configuration.

    Parameters:
        json_file_path (str): Path to the JSON file.
        excel_file_path (str): Path to the Excel file.

    Returns:
        dict: A dictionary with table names as keys and DataFrames as values.
    """
    # Load the configuration from the JSON file
    config = load_json(json_file_path)
    print(config)

    # Dictionary to hold DataFrames
    dataframes = {}

    # Load the Excel file
    excel_file = pd.ExcelFile(excel_file_path)

    """Extract table_name and related sheet_name as pairs from the JSON data."""
    # Iterate through the JSON configuration
    for key, value in config.items():
        if 'table_name' in value and 'sheet_name' in value:
            table_name = value['table_name']
            sheet_name = value['sheet_name']

            if sheet_name in excel_file.sheet_names:
                # Read the specified sheet into a DataFrame
                df = excel_file.parse(sheet_name)
                dataframes[f"{table_name}_df"] = df
                print(f"Loaded sheet '{sheet_name}' into DataFrame named '{table_name}'.")
            else:
                print(f"Sheet '{sheet_name}' not found in the Excel file.")

    return dataframes

def read_input_csv(csv_file_path):
    """
    Read the reference data CSV file specified in the config.

    Parameters:
        config (dict): The configuration data containing the Excel file path.

    Returns:
        pd.DataFrame: The DataFrame containing the Excel data.
    """
    
    if csv_file_path:
        # Read the Excel file into a DataFrame
        try:
            df = pd.read_csv(csv_file_path)
            return df
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return None
    else:
        print("Excel file path not found in the config.")
        return None
    
    