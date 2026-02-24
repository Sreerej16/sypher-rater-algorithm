import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def secured_community_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    secured_community = find_input_attribute(input_attributes, 'secured_community')

    # From the array of dataframes, get the relevant df 
    secured_community_df = dataframes.get('secured_community_df')
    secured_community_df['secured_community'].fillna('none',inplace=True)
    secured_community_df['secured_community'] = secured_community_df['secured_community'].astype(str)

    # Set null values in input to None.
    input_df[secured_community].fillna('none',inplace=True)
    
    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df, 
                        secured_community_df,
                        how='left', 
                        left_on=secured_community, 
                        right_on='secured_community')
    
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'secured_community_aop_factor', 
        'nhw': 'secured_community_nhw_factor', 
        'hur': 'secured_community_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['secured_community_aop_factor'].fillna(1, inplace=True)
    input_df['secured_community_nhw_factor'].fillna(1, inplace=True)
    input_df['secured_community_hur_factor'].fillna(1, inplace=True)
    
    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['secured_community'].isna(), True, input_df['invalid_lookup'])
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['secured_community'].isna(), 
                                     input_df['error_msg']+','+'Invalid Secured Community', 
                                     input_df['error_msg'])
    
    return input_df
