import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def senior_citizen_discount_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    senior_discount = find_input_attribute(input_attributes, 'senior_discount')

    # From the array of dataframes, get the relevant df
    senior_discount_df = dataframes.get('senior_discount_df')
    senior_discount_df['senior_discount'] = senior_discount_df['senior_discount'].astype(str).str.lower()

    input_df[senior_discount] = input_df[senior_discount].astype(str).str.lower()

    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df,
                        senior_discount_df,
                        how='left',
                        left_on=senior_discount,
                        right_on='senior_discount')

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'senior_discount_aop_factor',
        'nhw': 'senior_discount_nhw_factor',
        'hur': 'senior_discount_hur_factor'
    }, inplace=True)


    # Fill missing values with 1
    input_df['senior_discount_aop_factor'].fillna(1, inplace=True)
    input_df['senior_discount_nhw_factor'].fillna(1, inplace=True)
    input_df['senior_discount_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups
    input_df['invalid_lookup'] = np.where(input_df['senior_discount'].isna(), True, input_df['invalid_lookup'])
    input_df['error_msg'] = np.where(input_df['senior_discount'].isna(),
                                     input_df['error_msg'] + ',' + 'Invalid Senior Discount',
                                     input_df['error_msg'])

    return input_df
