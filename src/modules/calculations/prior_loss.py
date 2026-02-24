import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def prior_loss_factor_calc(input_df, dataframes, input_attributes):
    prior_claims   = find_input_attribute(input_attributes, 'prior_claims')
    # From the array of dataframes, get the relevant df 
    prior_loss_df = dataframes.get('prior_loss_df')
    prior_loss_df['Number or Prior Claims'] = prior_loss_df['Number or Prior Claims'].astype(str)
    input_df['prior_claims']


    # Categorize the input into the prior claims bucket
    input_df['prior_claims_category'] = np.where(input_df[prior_claims] >= 2, '2+', input_df[prior_claims].astype(str))

    input_df = pd.merge(input_df,
                        prior_loss_df,
                        how='left',
                        left_on='prior_claims_category',
                        right_on='Number or Prior Claims')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'prior_claims_aop_factor', 
        'nhw': 'prior_claims_nhw_factor', 
        'hur': 'prior_claims_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['prior_claims_aop_factor'].fillna(1, inplace=True)
    input_df['prior_claims_nhw_factor'].fillna(1, inplace=True)
    input_df['prior_claims_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['Number or Prior Claims'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['Number or Prior Claims'].isna(), 
                                     input_df['error_msg']+','+'Invalid Prior Claims', 
                                     input_df['error_msg'])
    
    # Drop extra columns from the merge
    input_df.drop(columns=['prior_claims_category','Number or Prior Claims'], inplace=True)

    return input_df