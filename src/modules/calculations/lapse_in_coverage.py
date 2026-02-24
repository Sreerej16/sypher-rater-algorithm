import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def lapse_in_coverage_factor_calc(input_df, dataframes, input_attributes):
    prior_coverage    = find_input_attribute(input_attributes, 'prior_coverage')

    # From the array of dataframes, get the relevant df 
    lapse_in_coverage_df = dataframes.get('lapse_in_coverage_df')
    # lapse_in_coverage_df['prior_coverage'] = lapse_in_coverage_df['prior_coverage'].astype(str)

    # # Convert 'lapse_in_coverage' column to lowercase in input_df
    # input_df['lapse_category'] = input_df[prior_coverage].str.lower()

# Convert 'Lapse' column to lowercase in lapse_in_coverage_df
    # lapse_in_coverage_df['prior_coverage'] = lapse_in_coverage_df['prior_coverage'].str.lower()
    input_df = pd.merge(input_df, 
                        lapse_in_coverage_df,
                        how='left', 
                        left_on='prior_coverage', 
                        right_on='prior_coverage')
    
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'prior_coverage_aop_factor', 
        'nhw': 'prior_coverage_nhw_factor', 
        'hur': 'prior_coverage_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['prior_coverage_aop_factor'].fillna(1, inplace=True)
    input_df['prior_coverage_nhw_factor'].fillna(1, inplace=True)
    input_df['prior_coverage_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['prior_coverage'].isna(),
                                          True, 
                                          input_df['invalid_lookup'])
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['prior_coverage'].isna(), 
                                    input_df['error_msg']+','+ 'Invalid Lapse', 
                                     input_df['error_msg'])
    


    return input_df