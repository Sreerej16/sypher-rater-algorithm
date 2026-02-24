import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def animal_liability_factor_calc(input_df, dataframes, input_attributes):
    
    animal_liability_coverage=find_input_attribute(input_attributes, 'animal_liability_coverage')
    animal_liability_df= dataframes.get ('animal_liability_df')

    if input_df['animal_liability_coverage'].isna().any():
        input_df['animal_liability_premium'] = pd.NA
        return input_df
    
    animal_liability_df['animal_liability_coverage'] = animal_liability_df['animal_liability_coverage'].astype(str)
    input_df[animal_liability_coverage] = input_df[animal_liability_coverage].astype(str)
    # Perform a left join (merge) on the 'Animal Liability Coverage Limit'
    input_df = pd.merge(input_df,
                         animal_liability_df, 
                         left_on=animal_liability_coverage, 
                         right_on='animal_liability_coverage', 
                         how='left')
    
    # Fill missing columns after the merge with default values
    input_df['animal_liability_premium'].fillna(0, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df[animal_liability_coverage].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df[animal_liability_coverage].isna(), 
                                     input_df['error_msg']+','+'Invalid animal liability limit ', 
                                     input_df['error_msg'])

    return input_df
    
