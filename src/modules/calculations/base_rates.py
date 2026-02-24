import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def baserates_calc(input_df, dataframes, input_attributes):
    base_rate_df = dataframes.get ("base_rates_df")
    # Find the input attributes that are needed for lookup
    location_zipcode = find_input_attribute(input_attributes, 'location_zipcode')
    base_rate_df['location_zipcode'] = pd.to_numeric(base_rate_df['location_zipcode'], errors='coerce')
    input_df[location_zipcode] = pd.to_numeric(input_df[location_zipcode], errors='coerce')
    # Merge input_df with base_rate_df on 'location_zipcode_input' and 'location_zipcode'
    input_df = pd.merge(input_df, base_rate_df, how='left', left_on=location_zipcode, right_on='location_zipcode')
    input_df.rename(columns={'aop': 'base_rates_aop_factor', 'nhw': 'base_rates_nhw_factor','hur':'base_rates_hur_factor'}, inplace=True)
    
    # Fill missing columns after the merge with default values
    input_df['base_rates_aop_factor'].fillna(1, inplace=True)
    input_df['base_rates_nhw_factor'].fillna(1, inplace=True)
    input_df['base_rates_hur_factor'].fillna(1, inplace=True)

    input_df['invalid_lookup'] = np.where(input_df['location_zipcode'].isna(),True,input_df['invalid_lookup'] )
    
    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['location_zipcode'].isna(), 
                                     input_df['error_msg']+','+'Invalid Zip Code',
                                     input_df['error_msg'])
    input_df.drop(columns=['sinkhole_territory'],inplace=True)
    
    return input_df
  
