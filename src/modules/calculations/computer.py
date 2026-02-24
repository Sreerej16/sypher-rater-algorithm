import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def computer_factor_calc(input_df,dataframes, input_attributes):
    home_comp_limit=find_input_attribute(input_attributes, 'home_computer_coverage')
    computer_df = dataframes.get('computer_df')

    if input_df['home_computer_coverage'].isna().any():
        input_df['computer_premium'] = pd.NA
        return input_df
    
    input_df['home_computer_coverage_value'] = computer_df['rate_per_$1,000'].values[0]

    # Create a mask for rows where home_comp_limit is 'Excluded'
    excluded_mask = input_df[home_comp_limit] == 'excl'

    # Calculate the premium for non-excluded rows
    input_df['computer_premium'] = pd.to_numeric(input_df[home_comp_limit], errors='coerce') / 1000 * input_df['home_computer_coverage_value']
    input_df['computer_premium'] = input_df['computer_premium'].astype(float).round(0)

    # Set the premium to 0 for excluded rows
    input_df.loc[excluded_mask, 'computer_premium'] = 0

    return input_df