import pandas as pd
import numpy as np
from datetime import datetime
from utils.json_handler import find_input_attribute

def age_of_roof_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    effective_date        = find_input_attribute(input_attributes, 'effective_date')
    roof_year       = find_input_attribute(input_attributes, 'roof_year')
    roof_material   = find_input_attribute(input_attributes, 'roof_material')
    # From the array of dataframes, get the relevant df 
    age_of_roof_df = dataframes.get('age_of_roof_df')
    age_of_roof_df['roof_age_ref'] = age_of_roof_df['roof_age_ref'].astype(str)
    
    input_df[roof_year] = pd.to_numeric(input_df[roof_year], errors="coerce")
    # Calculate roof age
    input_df['roof_age_value'] = input_df[effective_date].dt.year - input_df[roof_year]

    input_df['roof_age'] = pd.to_numeric(input_df['roof_age'], errors='coerce')

    # Categorize roof age: '60+' if >= 60, otherwise the actual value as string
    input_df['roof_age_category'] = np.where(input_df['roof_age_value'] >= 30, '30+', input_df['roof_age_value'].astype(str))
    
    # Transform roof material based on rules
    input_df['calculated_roof_material'] = np.where(input_df[roof_material].isin(['reinf_concrete', 'slate_tile']), 'all_other',input_df[roof_material])

    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df, 
                        age_of_roof_df,
                        how='left', 
                        left_on=('roof_age_category','calculated_roof_material'), 
                        right_on=('roof_age_ref','roof_material_ref'))

    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'roof_age_aop_factor', 
        'nhw': 'roof_age_nhw_factor', 
        'hur': 'roof_age_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['roof_age_aop_factor'].fillna(1, inplace=True)
    input_df['roof_age_nhw_factor'].fillna(1, inplace=True)
    input_df['roof_age_hur_factor'].fillna(1, inplace=True)


    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['roof_age_ref'].isna(), True, input_df['invalid_lookup'])
    input_df['invalid_lookup'] = np.where(input_df['roof_material_ref'].isna(), True, input_df['invalid_lookup'])

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where((input_df['roof_age_ref'].isna() |input_df['roof_material_ref'].isna()), 
                                     input_df['error_msg']+','+'Invalid Age of Roof/ Roof Material', 
                                     input_df['error_msg'])
    
    # Drop extra columns from the merge
    input_df.drop(columns=[ 'roof_age_ref','roof_material_ref'], inplace=True)
   
    return input_df
