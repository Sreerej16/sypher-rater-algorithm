import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def ordinance_or_law_factor_calc(input_df, dataframes, input_attributes):
    # From the array of dataframes, get the relevant df 
    ordinance_or_law_df = dataframes.get('ordinance_or_law_df')
    
    ordinance_or_law             = find_input_attribute(input_attributes, 'ordinance_or_law')

    # print(input_df['ordinance_or_law'])
    if input_df['ordinance_or_law'].isna().any():
        # print('ordinance or law is exiting')
        return input_df


    
    input_df[ordinance_or_law]   = input_df[ordinance_or_law].astype(str)
    input_df[ordinance_or_law] = input_df[ordinance_or_law].replace('0.0', 'no_cov')
    ordinance_or_law_df['ordinance_or_law']  = ordinance_or_law_df['ordinance_or_law'].astype(str)

    input_df            = pd.merge(input_df, 
                        ordinance_or_law_df,
                        how='left', 
                        left_on= ordinance_or_law, 
                        right_on='ordinance_or_law')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'ordinance_or_law_aop_factor', 
        'nhw': 'ordinance_or_law_nhw_factor', 
        'hur': 'ordinance_or_law_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['ordinance_or_law_aop_factor'].fillna(1, inplace=True)
    input_df['ordinance_or_law_nhw_factor'].fillna(1, inplace=True)
    input_df['ordinance_or_law_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['ordinance_or_law'].isna(), True, input_df['invalid_lookup']==True)
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['ordinance_or_law'].isna(), 
                                     input_df['error_msg']+','+'Invalid Increased Cov A', 
                                     input_df['error_msg'])
    # input_df.drop(columns=['Cov A percent'],inplace = True)

    return input_df