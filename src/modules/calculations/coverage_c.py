import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def coverage_c_factor_calc(input_df,dataframes, input_attributes):
    
    coverage_c_df = dataframes.get('coverage_c_df')
    
    coverage_c_pct    = find_input_attribute(input_attributes, 'coverage_c_pct')
    #input_df[coverage_c]   = input_df[coverage_c].astype(str)
    #coverage_c_df['Cov A percent']  = coverage_c_df['Cov A percent'].astype(str)
    coverage_c_pct = pd.to_numeric(input_df[coverage_c_pct], errors='coerce')

    input_df = pd.merge(input_df,
                        coverage_c_df,
                        how='left',
                        left_on= coverage_c_pct,
                        right_on = 'coverage_c_pct'
                        )
    input_df.rename(columns={'aop': 'coverage_c_aop_factor', 
                             'nhw': 'coverage_c_nhw_factor',
                             'hur':'coverage_c_hur_factor'}, inplace=True)
    
    input_df['coverage_c_aop_factor']  =  input_df['coverage_c_aop_factor'].round(3)
    input_df['coverage_c_nhw_factor']  =  input_df['coverage_c_nhw_factor'].round(3)
    input_df['coverage_c_hur_factor']  =  input_df['coverage_c_hur_factor'].round(3)
    # Fill missing columns after the merge with default values
    input_df['coverage_c_aop_factor'].fillna(1, inplace=True)
    input_df['coverage_c_nhw_factor'].fillna(1, inplace=True)
    input_df['coverage_c_hur_factor'].fillna(1, inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['coverage_c_pct'].isna(), True, input_df['invalid_lookup'])
    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['coverage_c_pct'].isna(),
                                      input_df['error_msg']+','+'Invalid Coverage C', 
                                      input_df['error_msg'])

    # Drop extra columns from the merge
    # input_df.drop(columns=['Cov A percent'], inplace=True)
    
    return input_df