import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def insurance_tier_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    tier = find_input_attribute(input_attributes, 'tier')

    # From the array of dataframes, get the relevant df 
    tier_df = dataframes.get('tier_df')

    tier = pd.to_numeric(input_df[tier], errors='coerce')

    input_df = pd.merge(input_df,
                                    tier_df,
                                    how='left',
                                    left_on=tier,
                                    right_on='tier_ref')
    input_df.rename(columns={'aop': 'tier_aop_factor', 'nhw': 'tier_nhw_factor','hur':'tier_hur_factor'}, inplace=True)

        # Fill missing columns after the merge with default values
    input_df['tier_aop_factor'].fillna(1, inplace=True)
    input_df['tier_nhw_factor'].fillna(1, inplace=True)
    input_df['tier_hur_factor'].fillna(1, inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['tier_ref'].isna(),True,input_df['invalid_lookup'] )
    
    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['tier_ref'].isna(), 
                                     input_df['error_msg']+','+'Invalid Zip Code',
                                     input_df['error_msg'])


    # Return the updated DataFrame
    input_df.drop(columns=['tier_ref'],inplace=True)
    return input_df









    



