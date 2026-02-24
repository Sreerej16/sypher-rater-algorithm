import pandas as pd
import numpy as np

from utils.json_handler import find_input_attribute

def tankless_waterheater_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    tankless_water_heater = find_input_attribute(input_attributes, 'tankless_water_heater')

    # Get the relevant DataFrame for tankless water heaters from the provided dictionary
    tankless_water_heater_df = dataframes.get('tankless_water_heater_df')

    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df,
                        tankless_water_heater_df,
                        how='left',
                        left_on=tankless_water_heater,
                        right_on='tankless_water_heater')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'tankless_water_heater_aop_factor',
        'nhw': 'tankless_water_heater_nhw_factor',
        'hur': 'tankless_water_heater_hur_factor'
    }, inplace=True)

    # Fill missing values for tankless_aop, tankless_nhw, tankless_hur with 1
    input_df['tankless_water_heater_aop_factor'].fillna(1, inplace=True)
    input_df['tankless_water_heater_nhw_factor'].fillna(1, inplace=True)
    input_df['tankless_water_heater_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['tankless_water_heater'].isna(), True, input_df['invalid_lookup'])

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['tankless_water_heater'].isna(),
                                      input_df['error_msg']+','+"Invalid Tankless water heater discount",
                                      input_df.get('error_msg', ''))

    # Return the updated DataFrame
    return input_df
