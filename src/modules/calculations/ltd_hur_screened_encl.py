import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def ltd_hur_screened_encl_factor_calc(input_df,dataframes, input_attributes):
    
    limited_hurricane_coverage=find_input_attribute(input_attributes, 'limited_hurricane_coverage')
    
    ltd_hur_df = dataframes.get('ltd_hur_screened_encl_df')

    if input_df[limited_hurricane_coverage].isna().any():
        input_df['ltd_hur_screened_encl_premium'] = pd.NA
        return input_df
    
    input_df['scrn_encl_carports_fact'] = ltd_hur_df['screened_enclosures_and_carports_factor'].values[0]

    # Mask for 'Excluded' rows
    scrn_encl_excluded_mask = input_df[limited_hurricane_coverage] == 'excl'

    # Mask for non-'Excluded' rows
    scrn_encl_non_excluded_mask = input_df[limited_hurricane_coverage] != 'excl'


    # Initialize columns with defaults
    input_df['ltd_hur_screened_encl_limit'] = 0.0
    input_df['ltd_hur_screened_encl_premium'] = 0

    # Calculate limit ONLY for non-excluded rows
    input_df.loc[scrn_encl_non_excluded_mask, 'ltd_hur_screened_encl_limit'] = (
        pd.to_numeric(input_df.loc[scrn_encl_non_excluded_mask, limited_hurricane_coverage], errors='coerce') / 50000
    )
    # Calculate 'ltd_hur_screened_encl_premium' for non-'Excluded' rows using input_df.loc
    try:
        input_df.loc[scrn_encl_non_excluded_mask, 'ltd_hur_screened_encl_premium'] = (
            input_df.loc[scrn_encl_non_excluded_mask, 'base_rates_hur_factor'] *
            input_df.loc[scrn_encl_non_excluded_mask, 'distance_to_coast_hur_factor'] *
            input_df.loc[scrn_encl_non_excluded_mask, 'ltd_hur_screened_encl_limit'] *
            input_df.loc[scrn_encl_non_excluded_mask, 'hur_deductible_hur_factor'] *
            input_df.loc[scrn_encl_non_excluded_mask, 'scrn_encl_carports_fact'].astype(float)
        )
    except (KeyError, ValueError, TypeError) as e:
        input_df.loc[:, 'error_msg'] = input_df['error_msg'] + f',Error calculating ltd_hur_screened_encl_premium: {str(e)} - filled with 0'
        input_df.loc[:, 'invalid_lookup'] = True
        input_df['ltd_hur_screened_encl_premium'] = 0
        return input_df

    input_df['ltd_hur_screened_encl_premium'] = input_df['ltd_hur_screened_encl_premium'].fillna(0).round(0).astype(int)

    return input_df