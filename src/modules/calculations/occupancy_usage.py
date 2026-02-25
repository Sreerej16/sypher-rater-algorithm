import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def occupancy_usage_factor_calc(input_df, dataframes, input_attributes):
    # From the array of dataframes, get the relevant df 
    occupancy_usage_df = dataframes.get('occupancy_usage_df')
    
    usage              = find_input_attribute(input_attributes, 'usage')
    
    input_df[usage] = np.where(input_df[usage] == 'dwell_under_constr', 
                               'primary',
                               input_df[usage])

    input_df = pd.merge(input_df, 
                        occupancy_usage_df,
                        how='left', 
                        left_on= usage, 
                        right_on='usage_ref')


    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'usage_aop_factor', 
        'nhw': 'usage_nhw_factor', 
        'hur': 'usage_hur_factor'
    }, inplace=True)

    # Check for missing values before filling with 1 and add detailed warning with input values
    missing_usage_mask = (input_df['usage_aop_factor'].isna() |
                           input_df['usage_nhw_factor'].isna() |
                           input_df['usage_hur_factor'].isna())

    if missing_usage_mask.any():
        # For each row with missing values, append detailed error message with input combinations
        input_df.loc[missing_usage_mask, 'error_msg'] = input_df.loc[missing_usage_mask].apply(
            lambda row: row['error_msg'] + f',Missing usage factor(s) with usage="{row[usage]}" - filled with 1',
            axis=1
        )
        input_df.loc[missing_usage_mask, 'invalid_lookup'] = True

    # Fill missing values for AOP, NHW, HUR with 1
    input_df['usage_aop_factor'].fillna(1, inplace=True)
    input_df['usage_nhw_factor'].fillna(1, inplace=True)
    input_df['usage_hur_factor'].fillna(1, inplace=True)
    input_df.drop(columns = ['usage_ref'],inplace=True)

    return input_df