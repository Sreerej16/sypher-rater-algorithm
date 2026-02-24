import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def water_backup_factor_calc(input_df,dataframes, input_attributes):
    water_backup_coverage=find_input_attribute(input_attributes, 'water_backup_coverage')
    water_backup_df = dataframes.get('water_backup_df')

    if input_df['water_backup_coverage'].isna().any():
        input_df['water_backup_premium'] = pd.NA
        return input_df
    
    water_backup_df['water_backup_coverage'] = water_backup_df['water_backup_coverage'].astype(str)
    input_df[water_backup_coverage] = input_df[water_backup_coverage].astype(str)
    input_df[water_backup_coverage].replace('0','excl',inplace=True)
    input_df = pd.merge(input_df,
                        water_backup_df,
                        how='left',
                        left_on = water_backup_coverage,
                        right_on = 'water_backup_coverage')
    
    input_df['water_backup_premium'].fillna(0, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['water_backup_coverage'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['water_backup_coverage'].isna(), 
                                     input_df['error_msg']+','+'Invalid water backup limit', 
                                     input_df['error_msg'])
    
  

    return input_df