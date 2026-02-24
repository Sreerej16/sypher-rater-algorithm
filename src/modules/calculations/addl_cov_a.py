import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def addl_cov_a_factor_calc(input_df, dataframes, input_attributes):
    # From the array of dataframes, get the relevant df 
    addl_cov_a_df = dataframes.get('addl_cov_a_df')
    
    addl_coverage_a    = find_input_attribute(input_attributes, 'addl_coverage_a')
 
    if input_df['addl_coverage_a'].isna().any():
        return input_df
    # Ensure data types match for merge
    addl_cov_a_df['addl_coverage_a'] = addl_cov_a_df['addl_coverage_a'].astype(str)
    input_df[addl_coverage_a] = input_df[addl_coverage_a].astype(str)
    
    input_df = pd.merge(input_df, 
                        addl_cov_a_df,
                        how='left', 
                        left_on= addl_coverage_a, 
                        right_on='addl_coverage_a')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'addl_cov_a_aop_factor', 
        'nhw': 'addl_cov_a_nhw_factor', 
        'hur': 'addl_cov_a_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['addl_cov_a_aop_factor'].fillna(1, inplace=True)
    input_df['addl_cov_a_nhw_factor'].fillna(1, inplace=True)
    input_df['addl_cov_a_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['addl_coverage_a'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['addl_coverage_a'].isna(), 
                                     input_df['error_msg']+','+'Invalid Increased Cov A', 
                                     input_df['error_msg'])
    


    return input_df