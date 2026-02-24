import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def coverage_d_factor_calc(input_df,dataframes, input_attributes):
    
    coverage_d_df = dataframes.get('coverage_d_df')
    
    coverage_d_pct    = find_input_attribute(input_attributes, 'coverage_d_pct')

    coverage_d_pct = pd.to_numeric(input_df[coverage_d_pct], errors='coerce')

    input_df = pd.merge(input_df,
                        coverage_d_df,
                        left_on = coverage_d_pct,
                        right_on = 'coverage_d_pct'
                        )
    
    input_df.rename(columns={'aop': 'coverage_d_aop_factor', 
                             'nhw': 'coverage_d_nhw_factor',
                             'hur':'coverage_d_hur_factor'}, inplace=True)
    input_df['coverage_d_aop_factor']  =   input_df['coverage_d_aop_factor'].round(3)
    input_df['coverage_d_nhw_factor']  =   input_df['coverage_d_nhw_factor'].round(3)
    input_df['coverage_d_hur_factor']  =   input_df['coverage_d_hur_factor'].round(3)
    # Fill missing columns after the merge with default values
    input_df['coverage_d_aop_factor'].fillna(1, inplace=True)
    input_df['coverage_d_nhw_factor'].fillna(1, inplace=True)
    input_df['coverage_d_hur_factor'].fillna(1, inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['coverage_d_pct'].isna(), True, input_df['invalid_lookup'])
    
    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['coverage_d_pct'].isna(),
                                    input_df['error_msg']+','+'Invalid Coverage D', 
                                    input_df['error_msg'])


    return input_df
