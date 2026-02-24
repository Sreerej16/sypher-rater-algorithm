import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def coverage_b_factor_calc(input_df,dataframes, input_attributes):
    
    coverage_b_df = dataframes.get('coverage_b_df')
    
    coverage_b_pct    = find_input_attribute(input_attributes, 'coverage_b_pct')
    input_df[coverage_b_pct]  = input_df[coverage_b_pct].astype(str)
    coverage_b_df['coverage_b_pct'] = coverage_b_df['coverage_b_pct'].astype(str)
    input_df = pd.merge(input_df,
                        coverage_b_df,
                        how='left',
                        left_on= coverage_b_pct,
                        right_on = 'coverage_b_pct'
                        )
    input_df.rename(columns={'aop': 'coverage_b_aop_factor', 
                             'nhw': 'coverage_b_nhw_factor',
                             'hur':'coverage_b_hur_factor'}, inplace=True)
    # Fill missing columns after the merge with default values
    input_df['coverage_b_aop_factor'].fillna(1, inplace=True)
    input_df['coverage_b_nhw_factor'].fillna(1, inplace=True)
    input_df['coverage_b_hur_factor'].fillna(1, inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['coverage_b_pct'].isna(), True, input_df['invalid_lookup'])

    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['coverage_b_pct'].isna(), 
                                     input_df['error_msg']+','+'Invalid Coverage B',
                                       input_df['error_msg'])

    # Drop extra columns from the merge
    # input_df.drop(columns=['Cov A percent'], inplace=True)
    return input_df