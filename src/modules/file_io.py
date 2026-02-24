# modules/file_io.py

import pandas as pd

def load_input_csv(input_file_path):
    """
    Loads an input CSV file into a DataFrame.

    Parameters:
        input_file_path (str): The path to the input CSV file.

    Returns:
        pd.DataFrame: The loaded input DataFrame.
    """
    return pd.read_csv(input_file_path)

def save_to_csv(df, output_file_path):
    """
    Saves a DataFrame to a CSV file.

    Parameters:
        df (pd.DataFrame): The DataFrame to save.
        output_file_path (str): The path to the output CSV file.
    """
    df.to_csv(output_file_path, index=False)
    print(f"DataFrame saved to '{output_file_path}'.")
