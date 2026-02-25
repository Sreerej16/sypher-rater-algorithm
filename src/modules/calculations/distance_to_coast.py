import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def transform_distance_to_coast(value):
    if value is None or pd.isna(value):
        return ''
    try:
        value = float(value)
    except (ValueError, TypeError):
        return value
    if 0 <= value < 0.189583:
        return "0_ft_1000_ft"
    elif 0.189583 <= value < 0.473674:
        return "1001_ft_2500_ft"
    elif 0.473674 <= value < 1:
        return "2501_ft_1_mi"
    elif 1 <= value < 2:
        return "gt_1_mi_2_mi"
    elif 2 <= value < 3:
        return "gt_2_mi_3mi"
    elif 3 <= value < 5:
        return "gt_3_mi_5_mi"
    elif 5 <= value < 10:
        return "gt_5_mi_10_mi"
    else:
        return "gt_10_mi"

def distance_to_coast_calc(input_df,dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    distance_to_coast = find_input_attribute(input_attributes, 'distance_to_coast')

    # Load the data from CSV files
    # dtc_group_df = dataframes.get('miles_to_group_df')
    dtc_df       = dataframes.get('distance_to_coast_df')

    
    input_df['distance_to_coast'] = input_df[distance_to_coast].apply(transform_distance_to_coast)

    input_df = pd.merge(input_df,dtc_df, how='left', left_on='distance_to_coast', right_on='distance_to_coast')
    input_df.rename(columns={'aop': 'distance_to_coast_aop_factor', 
                             'nhw': 'distance_to_coast_nhw_factor',
                             'hur':'distance_to_coast_hur_factor'}, inplace=True)

    # Check for missing values before filling with 1 and add detailed warning with input values
    missing_dtc_mask = (input_df['distance_to_coast_aop_factor'].isna() |
                         input_df['distance_to_coast_nhw_factor'].isna() |
                         input_df['distance_to_coast_hur_factor'].isna())

    if missing_dtc_mask.any():
        # For each row with missing values, append detailed error message with input combinations
        input_df.loc[missing_dtc_mask, 'error_msg'] = input_df.loc[missing_dtc_mask].apply(
            lambda row: row['error_msg'] + f',Missing distance_to_coast factor(s) with distance_to_coast="{row[distance_to_coast]}" - filled with 1',
            axis=1
        )
        input_df.loc[missing_dtc_mask, 'invalid_lookup'] = True

    # Fill missing columns after the merge with default values
    input_df['distance_to_coast_aop_factor'].fillna(1, inplace=True)
    input_df['distance_to_coast_nhw_factor'].fillna(1, inplace=True)
    input_df['distance_to_coast_hur_factor'].fillna(1, inplace=True)
    # input_df.drop(columns=['distance_to_coast_group','Distance to Coast'],inplace=True)

    return input_df


