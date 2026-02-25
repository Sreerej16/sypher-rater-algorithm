import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def hur_deductible_factor_calc(input_df,dataframes, input_attributes):

    coverage_a_df     = dataframes.get('coverage_a_df')
    
    coverage_a_amt        = find_input_attribute(input_attributes, 'coverage_a_amt')

    hur_deductible_df = dataframes.get('hur_deductible_df')
    
    hur_deductible    = find_input_attribute(input_attributes, 'hur_deductible')

    # Sort the coverage_a_df by min_cov_a_range to ensure bins are monotonically increasing
    coverage_a_df = coverage_a_df.sort_values('min_cov_a_range').reset_index(drop=True)
    bins = coverage_a_df['min_cov_a_range'].to_list() + [float('inf')]  # Adding infinity for the last bin
    labels = coverage_a_df['min_cov_a_range'].to_list()

    # Use pd.cut to assign the appropriate group
    input_df['coverage_a_hur'] = pd.cut(input_df[coverage_a_amt], bins=bins, labels=labels, right=False)
    input_df = pd.merge(input_df,
                        coverage_a_df,
                        how='left',
                        left_on = 'coverage_a_hur',
                        right_on ='min_cov_a_range')
    
    input_df[hur_deductible] = input_df[hur_deductible].replace('excl', 'wind_hail_cov_excl')
    
    hur_deductible_df['nhw_deductible_ref'] = hur_deductible_df['nhw_deductible_ref'].astype(str)
    input_df[hur_deductible] = input_df[hur_deductible].astype(str)
    input_df['cov_a_range'] = np.where(input_df[hur_deductible]=='wind_hail_cov_excl',
                                       'any',
                                       input_df['cov_a_range'])
    

    input_df = pd.merge(input_df,
                        hur_deductible_df,
                        how='left',
                        left_on=['cov_a_range', hur_deductible],
                        right_on=['coverage_a_range','nhw_deductible_ref'])
    
    input_df.rename(columns={'aop': 'hur_deductible_aop_factor', 
                             'nhw': 'hur_deductible_nhw_factor',
                             'hur':  'hur_deductible_hur_factor'}, inplace=True)
    
    print(input_df.iloc[[9]])
    # Fill missing columns after the merge with default values
    input_df['hur_deductible_aop_factor'].fillna(1, inplace=True)
    input_df['hur_deductible_nhw_factor'].fillna(1, inplace=True)
    input_df['hur_deductible_hur_factor'].fillna(1, inplace=True)

    
    input_df['invalid_lookup'] = np.where(input_df['nhw_deductible_ref'].isna(), True, input_df['invalid_lookup'])
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['nhw_deductible_ref'].isna(), 
                                     input_df['error_msg']+','+'Invalid Hurricane  deductible  discount', 
                                     input_df['error_msg'])
    input_df.drop(columns =['coverage_a_hur','cov_a_range','nhw_deductible_ref','coverage_a_range','min_cov_a_range'],inplace=True)
    return input_df