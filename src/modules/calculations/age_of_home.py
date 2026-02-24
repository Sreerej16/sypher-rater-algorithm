import pandas as pd
import numpy as np
from datetime import datetime
from utils.json_handler import find_input_attribute

def age_of_home_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    effective_date = find_input_attribute(input_attributes, 'effective_date')
    year_built = find_input_attribute(input_attributes, 'year_built')

    # Load the age of home lookup DataFrame
    age_of_home_df = dataframes.get('age_of_home_df')
    #age_of_home_df['age_of_home'] = age_of_home_df['age_of_home'].astype(str)
    
    #Getting date in different format,so using below formating. 
    # Replace '/' with '-' and convert 'eff_date' to datetime
    #input_df[eff_date] = input_df[eff_date].replace('/', '-', regex=True)
    
    input_df[effective_date] = pd.to_datetime(input_df[effective_date])
    # Calculate 'Policy Year' and 'home_age'
    input_df[year_built] = pd.to_numeric(input_df[year_built], errors="coerce")
    input_df['age_of_home'] = input_df[effective_date].dt.year- input_df[year_built]
    age_of_home_df['home_age']  = age_of_home_df['home_age'].astype(str)
    # Categorize home age: '60+' if >= 60, otherwise the actual value as string
    
    input_df['home_age_category'] = np.where(input_df['age_of_home'] >= 60, '60+', input_df['age_of_home'].astype(str))
    input_df['home_age_category'] = input_df['home_age_category'].astype(str)
    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df, 
                        age_of_home_df,
                        how='left', 
                        suffixes=('', '_r'),
                        left_on='home_age_category', 
                        right_on='home_age')
    
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'home_age_aop_factor', 
        'nhw': 'home_age_nhw_factor', 
        'hur': 'home_age_hur_factor'
    }, inplace=True)
    #
    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    # input_df['home_age_aop_factor'].fillna(1, inplace=True)
    # input_df['home_age_nhw_factor'].fillna(1, inplace=True)
    # input_df['home_age_hur_factor'].fillna(1, inplace=True)

    
    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['home_age'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['home_age_category'].isna(), 
                                     input_df['error_msg']+','+'Invalid Effective Date/Year Built', 
                                     input_df['error_msg'])
    
    # Drop extra columns from the merge
    input_df.drop(columns=['home_age_r'], inplace=True, errors='ignore')

    return input_df