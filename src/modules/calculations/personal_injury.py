import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def personal_injury_factor_calc(input_df, dataframes, input_attributes):
    
    pi_limit   = find_input_attribute(input_attributes, 'personal_injury_coverage')
    coverage_e_amt = find_input_attribute(input_attributes, 'coverage_e_amt')
    # From the array of dataframes, get the relevant df 
    personal_injury_df = dataframes.get('personal_injury_df')
    personal_injury_df['personal_injury_coverage_ref'] = personal_injury_df['personal_injury_coverage_ref'].astype(str)

    if input_df['personal_injury_coverage'].isna().any():
        input_df['personal_injury_premium'] = pd.NA
        return input_df
    # Merging with Excluded DataFrame where pi_limit is Excluded

    excluded_mask = input_df[pi_limit] == 'excl'
    included_mask = input_df[pi_limit] == 'incl'
    included_df   = input_df[included_mask].copy()
    
    incl_df = pd.merge(included_df,
                       personal_injury_df,
                       how= 'left',
                       left_on  = coverage_e_amt, 
                       right_on ='personal_injury_coverage_ref')
    
    # Concatenate the two merged DataFrames
    incl_df = incl_df.set_index(included_df.index)
    
    input_df.loc[included_mask, 'personal_injury_coverage_ref'] = incl_df['personal_injury_coverage_ref']
    input_df.loc[included_mask,'personal_injury_premium'] = incl_df['personal_injury_premium']
    input_df.loc[excluded_mask, 'personal_injury_coverage_ref'] = 'excl'
    input_df.loc[excluded_mask,'personal_injury_premium'] = 0
    

    # Incase any missing lookups,Fill missing values 
    input_df['personal_injury_premium'].fillna(0, inplace=True)
    
    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    #input_df['invalid_lookup'] = np.where(input_df['Personal Injury Coverage Limit'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['personal_injury_coverage_ref'].isna(), 
                                     input_df['error_msg']+','+'Invalid pi_limit', 
                                     input_df['error_msg'])
    
    input_df.drop(columns=['personal_injury_coverage_ref'],inplace = True)

    
    return input_df