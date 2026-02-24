import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def limited_fungi_factor_calc(input_df,dataframes, input_attributes):
    limited_fungi_df = dataframes.get('limited_fungi_df')
    limited_fungi_df['calculated_fungi_limit'] =  (limited_fungi_df[['property_covered_loss_limit', 'property_policy_aggregate_limit', 'liability_policy_aggregate_limit']].astype(str)).agg('_'.join, axis=1)

    limited_fungi_coverage=find_input_attribute(input_attributes, 'limited_fungi_coverage')

    if input_df[limited_fungi_coverage].isna().any():
        input_df['limited_fungi_premium'] = pd.NA
        return input_df

    input_df = pd.merge(input_df,
                        limited_fungi_df[['calculated_fungi_limit','limited_fungi_premium']],
                        how = 'left',
                        left_on = limited_fungi_coverage,
                        right_on = 'calculated_fungi_limit'
                        )
    input_df['limited_fungi_premium'].fillna(0, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['calculated_fungi_limit'].isna(), True, input_df['invalid_lookup'] )
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['calculated_fungi_limit'].isna(), 
                                     input_df['error_msg']+','+'Invalid fungi limit ', 
                                     input_df['error_msg'])
    


    return input_df
    