import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def personal_property_rep_cost_factor_calc(input_df, dataframes, input_attributes):
    personal_property_rep_cost     = find_input_attribute(input_attributes, 'personal_property_rep_cost')
    # From the array of dataframes, get the relevant df 
    personal_property_rep_cost_df = dataframes.get('personal_property_rep_cost_df')
    personal_property_rep_cost_df['personal_property_rep_cost'] = personal_property_rep_cost_df['personal_property_rep_cost'].astype(str)

    if input_df['personal_property_rep_cost'].isna().any():
        return input_df

    input_df = pd.merge(input_df, 
                        personal_property_rep_cost_df,
                        how='left', 
                        left_on=personal_property_rep_cost, 
                        right_on='personal_property_rep_cost')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'personal_property_rep_cost_aop_factor', 
        'nhw': 'personal_property_rep_cost_nhw_factor', 
        'hur': 'personal_property_rep_cost_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['personal_property_rep_cost_aop_factor'].fillna(1, inplace=True)
    input_df['personal_property_rep_cost_nhw_factor'].fillna(1, inplace=True)
    input_df['personal_property_rep_cost_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['personal_property_rep_cost'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['personal_property_rep_cost'].isna(), 
                                     input_df['error_msg']+','+'Invalid pprc', 
                                     input_df['error_msg'])
    


    return input_df