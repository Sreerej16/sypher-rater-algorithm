import pandas as pd
import numpy as np

from utils.json_handler import find_input_attribute

def full_sprinkler_system_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    fire_sprinkler_protection = find_input_attribute(input_attributes, 'fire_sprinkler_protection')

    # Get the relevant DataFrame for sprinklers from the provided dictionary
    full_sprinkler_system_df = dataframes.get('full_sprinkler_system_df')
    # Fill NaN values in 'sprinkler_system' and 'Sprinklers' columns
    input_df[fire_sprinkler_protection].fillna('none', inplace=True)
    full_sprinkler_system_df['fire_sprinkler_protection'].fillna('none', inplace=True)

    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df, 
                        full_sprinkler_system_df,
                        how='left', 
                        left_on=fire_sprinkler_protection, 
                        right_on='fire_sprinkler_protection')
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'fire_sprinkler_protection_aop_factor', 
        'nhw': 'fire_sprinkler_protection_nhw_factor', 
        'hur': 'fire_sprinkler_protection_hur_factor'
    }, inplace=True)

    # Fill missing values for spr_aop, spr_nhw, spr_hur with 1
    input_df['fire_sprinkler_protection_aop_factor'].fillna(1, inplace=True)
    input_df['fire_sprinkler_protection_nhw_factor'].fillna(1, inplace=True)
    input_df['fire_sprinkler_protection_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['fire_sprinkler_protection'].isna(), True, input_df['invalid_lookup'])

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['fire_sprinkler_protection'].isna(), 
                                      input_df['error_msg']+','+"Invalid Sprinkler System", 
                                      input_df.get('error_msg', ''))

    # Return the updated DataFrame
    return input_df
