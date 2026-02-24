import pandas as pd
import numpy as np

from utils.json_handler import find_input_attribute

def water_detection_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    smart_home_water_protection_devices = find_input_attribute(input_attributes, 'smart_home_water_protection_devices')

    # Get the relevant DataFrame for water detection devices from the provided dictionary
    water_detection_df = dataframes.get('water_detection_df')

    # Fill NA values in the input DataFrame
    input_df[smart_home_water_protection_devices].fillna('None', inplace=True)
    water_detection_df['smart_home_water_protection_devices'].fillna('None', inplace=True)
    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df,
                        water_detection_df,
                        how='left',
                        left_on=smart_home_water_protection_devices,
                        right_on='smart_home_water_protection_devices')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'water_detection_aop_factor',
        'nhw': 'water_detection_nhw_factor',
        'hur': 'water_detection_hur_factor'
    }, inplace=True)

    # Fill missing values for water_detect_aop, water_detect_nhw, water_detect_hur with 1
    input_df['water_detection_aop_factor'].fillna(1, inplace=True)
    input_df['water_detection_nhw_factor'].fillna(1, inplace=True)
    input_df['water_detection_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['smart_home_water_protection_devices'].isna(), True, input_df['invalid_lookup'])

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['smart_home_water_protection_devices'].isna(),
                                      input_df['error_msg']+','+"Invalid Water Detection...",
                                      input_df.get('error_msg', ''))

    # Return the updated DataFrame
    return input_df
