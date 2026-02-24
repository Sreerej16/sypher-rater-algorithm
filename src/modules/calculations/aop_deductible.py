import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def aop_deductible_factor_calc(input_df,dataframes, input_attributes):
    
    aop_deductible_df = dataframes.get('aop_deductible_df')
    coverage_a_df     = dataframes.get('coverage_a_df')
    
    coverage_a_amt        = find_input_attribute(input_attributes, 'coverage_a_amt')
    aop_deductible    = find_input_attribute(input_attributes, 'aop_deductible')

    # Sort the coverage_a_df by min_cov_a_range to ensure bins are monotonically increasing
    coverage_a_df = coverage_a_df.sort_values('min_cov_a_range').reset_index(drop=True)
    bins = coverage_a_df['min_cov_a_range'].to_list() + [float('inf')]  # Adding infinity for the last bin
    labels = coverage_a_df['min_cov_a_range'].to_list()
   
    # Use pd.cut to assign the appropriate group
    input_df['coverage_a_aop'] = pd.cut(input_df[coverage_a_amt], bins=bins, labels=labels, right=False)
   
    input_df = pd.merge(input_df,
                        coverage_a_df,
                        how='left',
                        left_on = 'coverage_a_aop',
                        right_on ='min_cov_a_range')
    
    input_df[aop_deductible] = input_df[aop_deductible].astype(str)
    aop_deductible_df['aop_deductible'] = aop_deductible_df['aop_deductible'].astype(str)
    input_df = pd.merge(input_df,
                        aop_deductible_df,
                        how='left',
                        left_on=['cov_a_range',aop_deductible],
                        right_on=['coverage_a_range','aop_deductible'])
    
    # Rename columns after the merge
    input_df.rename(columns={'aop': 'aop_deductible_aop_factor', 'nhw': 'aop_deductible_nhw_factor', 'hur': 'aop_deductible_hur_factor'}, inplace=True)
    input_df['aop_deductible_aop_factor'].fillna(1, inplace=True)
    input_df['aop_deductible_nhw_factor'].fillna(1, inplace=True)
    input_df['aop_deductible_hur_factor'].fillna(1, inplace=True)

    input_df['aop_deductible_aop_factor'] = pd.to_numeric(input_df['aop_deductible_aop_factor'], errors='coerce').fillna(1)
    input_df['aop_deductible_nhw_factor'] = pd.to_numeric(input_df['aop_deductible_nhw_factor'], errors='coerce').fillna(1)
    input_df['aop_deductible_hur_factor'] = pd.to_numeric(input_df['aop_deductible_hur_factor'], errors='coerce').fillna(1)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['aop_deductible'].isna(),True,input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['aop_deductible'].isna(), 
                                     input_df['error_msg']+','+'Invalid aop deductible discount', 
                                     input_df['error_msg'])
    input_df.drop(columns = ['coverage_a_aop','cov_a_range','coverage_a_range','min_cov_a_range'],inplace = True)
    
    return input_df
    