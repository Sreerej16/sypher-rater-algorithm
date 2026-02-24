import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def coverage_f_factor_calc(input_df,dataframes, input_attributes):
    
    coverage_f_amt   = find_input_attribute(input_attributes, 'coverage_f_amt')
    
    coverage_f_df = dataframes.get('coverage_f_df')
    # coverage_f_df.rename(columns={'Coverage F Limit ':'Coverage F Limit'},inplace=True)
    coverage_f_df['coverage_f_amt'] = coverage_f_df['coverage_f_amt'] .astype(str)
    # Fill missing columns after the merge with default values
    input_df['zone'].fillna('0', inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['zone'].isna(), True, input_df['invalid_lookup'])

    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['zone'].isna(), 'Invalid Zone', input_df['error_msg'])
    input_df[coverage_f_amt]  = input_df[coverage_f_amt].astype(str)
    input_df        = pd.merge(input_df,
                               coverage_f_df,
                               how = 'left',
                               left_on  = coverage_f_amt,
                               right_on = 'coverage_f_amt'
                               )
    input_df['calculated_coverage_f_premium'] = np.where(input_df['zone'] == '1', 
                                       input_df['zone_1_premium'], 
                                       np.where(input_df['zone'] == '2', 
                                                input_df['zone_2_premium'], 0))
    input_df['calculated_coverage_f_premium'].fillna(0, inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['coverage_f_amt'].isna(), True, input_df['invalid_lookup'] ) 
    input_df['error_msg'] = np.where(input_df['coverage_f_amt'].isna(), 
                                     input_df['error_msg']+','+'Invalid Coverage F premium',
                                     input_df['error_msg'])
    input_df.drop(columns=['zone_1_premium','zone_2_premium'],inplace=True)
    return input_df
