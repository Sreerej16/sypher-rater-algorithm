import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def home_sharing_factors_calc(input_df,dataframes, input_attributes):
    
    homesharing_coverage =find_input_attribute(input_attributes, 'homesharing_coverage')
    coverage_e_amt=find_input_attribute(input_attributes, 'coverage_e_amt')
    coverage_f_amt=find_input_attribute(input_attributes, 'coverage_f_amt')
    
    home_sharing_prop_prem_df = dataframes.get('home_sharing_prop_prem_df')
    home_sharing_liab_prem_df = dataframes.get('home_sharing_liab_prem_df')

    if input_df['homesharing_coverage'].isna().any():
        input_df['home_sharing_liab_premium'] = pd.NA
        input_df['home_sharing_prop_premium'] = pd.NA
        return input_df
    
    input_df['home_sharing_prop_surcharge'] = home_sharing_prop_prem_df['premium_surcharge'].values[0]
    
    input_df['home_sharing_liab_premium'] = np.where(
    ((input_df[coverage_e_amt] == 'excl') & (input_df[coverage_f_amt] == 'excl')) | (input_df[homesharing_coverage] == 'excl'),
    0, home_sharing_liab_prem_df['premium'].values[0]
    ).astype(int)

    input_df['home_sharing_prop_premium'] = np.where(
        (input_df[homesharing_coverage] == 'excl'),
        0,
        np.round(input_df['total_base_premium'] * input_df['home_sharing_prop_surcharge']).astype(int)
    )

    input_df['home_sharing_premium'] = input_df[['home_sharing_prop_premium', 'home_sharing_liab_premium']].sum(axis=1)


    return input_df
