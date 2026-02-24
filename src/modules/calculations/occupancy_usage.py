import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def occupancy_usage_factor_calc(input_df, dataframes, input_attributes):
    # From the array of dataframes, get the relevant df 
    occupancy_usage_df = dataframes.get('occupancy_usage_df')
    
    usage              = find_input_attribute(input_attributes, 'usage')
    
    input_df[usage] = np.where(input_df[usage] == 'dwell_under_constr', 
                               'primary',
                               input_df[usage])
    conditions = [
    input_df['usage'] == 'primary',
    input_df['usage'] == 'secondary',
    input_df['usage'] == 'seasonal']

    # Define choices corresponding to conditions
    choices = ['primary',
               'secondary_seasonal',
               'secondary_seasonal']

    # Create a new column 'usage_category' based on conditions
    input_df['usage_category'] = np.select(conditions, choices, default='Unknown')

    input_df = pd.merge(input_df, 
                        occupancy_usage_df,
                        how='left', 
                        left_on='usage_category', 
                        right_on='usage_ref')


    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'usage_aop_factor', 
        'nhw': 'usage_nhw_factor', 
        'hur': 'usage_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['usage_aop_factor'].fillna(1, inplace=True)
    input_df['usage_nhw_factor'].fillna(1, inplace=True)
    input_df['usage_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['usage_ref'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['usage_ref'].isna(), 
                                     input_df['error_msg']+','+'Invalid Usage', 
                                     input_df['error_msg'])
    input_df.drop(columns = ['usage_category','usage_ref'],inplace=True)

    return input_df