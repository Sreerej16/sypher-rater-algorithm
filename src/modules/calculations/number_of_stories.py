import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def number_of_stories_factor_calc(input_df, dataframes, input_attributes):
    
    # From the array of dataframes, get the relevant df 
    number_of_stories_df = dataframes.get('number_of_stories_df')
    
    no_of_stories    = find_input_attribute(input_attributes, 'no_of_stories')
    input_df[no_of_stories] = input_df[no_of_stories].astype(str)
    number_of_stories_df['no_of_stories'] = number_of_stories_df['no_of_stories'].astype(str)
    input_df[no_of_stories] = input_df[no_of_stories].astype(str)
    input_df = pd.merge(input_df, 
                        number_of_stories_df,
                        how='left', 
                        left_on= no_of_stories, 
                        right_on='no_of_stories')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'no_of_stories_aop_factor', 
        'nhw': 'no_of_stories_nhw_factor', 
        'hur': 'no_of_stories_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['no_of_stories_aop_factor'].fillna(1, inplace=True)
    input_df['no_of_stories_nhw_factor'].fillna(1, inplace=True)
    input_df['no_of_stories_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['no_of_stories'].isna(), True, input_df['invalid_lookup'] )
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['no_of_stories'].isna(), 
                                     input_df['error_msg']+','+'Invalid number_of_stories', 
                                     input_df['error_msg'])
    
    return input_df