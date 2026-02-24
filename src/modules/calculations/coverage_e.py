import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def coverage_e_factor_calc(input_df,dataframes, input_attributes):
    zone_df       = dataframes.get('county_zone_df')
    zone_df['zone'] = zone_df['zone'].astype(str)
    coverage_e_df = dataframes.get('coverage_e_df')
    coverage_e_df['coverage_e_amt'] = coverage_e_df['coverage_e_amt'] .astype(str)

    location_county     = find_input_attribute(input_attributes, 'location_county')
    coverage_e_amt = find_input_attribute(input_attributes, 'coverage_e_amt')

    input_df      = pd.merge(input_df,
                             zone_df,
                             how = 'left',
                             left_on = location_county,
                             right_on = 'county')

    # Fill missing columns after the merge with default values
    input_df['zone'].fillna('0', inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['zone'].isna(), True, input_df['invalid_lookup'])

    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['zone'].isna(), 'Invalid Zone', input_df['error_msg'])
    input_df[coverage_e_amt]  = input_df[coverage_e_amt].astype(str)
    input_df        = pd.merge(input_df,
                               coverage_e_df,
                               how = 'left',
                               left_on  = coverage_e_amt,
                               right_on = 'coverage_e_amt'
                               )
    input_df['calculated_coverage_e_premium'] = np.where(input_df['zone'] == '1', 
                                       input_df['zone_1_premium'], 
                                       np.where(input_df['zone'] == '2', 
                                                input_df['zone_2_premium'], 0))
    input_df['calculated_coverage_e_premium'].fillna(1, inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['coverage_e_amt'].isna(), True, input_df['invalid_lookup']) 
    input_df['error_msg'] = np.where(input_df['coverage_e_amt'].isna(), 
                                     input_df['error_msg']+','+'Invalid Coverage E premium', 
                                     input_df['error_msg'])
    input_df.drop(columns=['zone_1_premium','zone_2_premium'],inplace=True)
    return input_df
