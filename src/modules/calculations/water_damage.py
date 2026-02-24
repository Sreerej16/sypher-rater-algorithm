import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def water_damage_factor_calc(input_df, dataframes, input_attributes):
    
    # From the array of dataframes, get the relevant df 
    water_damage_df    = dataframes.get('water_damage_df')
    
    water_damage_limitation = find_input_attribute(input_attributes, 'water_damage_limitation')
    # age_of_home        = find_input_attribute(input_attributes, 'age_of_home')

    if input_df['water_damage_limitation'].isna().any():
        return input_df
    
    input_df[water_damage_limitation] = input_df[water_damage_limitation].astype(str)
    water_damage_df['home_age_ref'] = water_damage_df['home_age_ref'].astype(str)
    water_damage_df['water_damage_limitation'] = water_damage_df['water_damage_limitation'].astype(str)
    #input_df['home_age_category'] = np.where(input_df[age_of_home] >=60,'60+',input_df[age_of_home].astype(str))
    input_df['home_age_category'] = input_df['home_age_category'].astype(str)
    input_df['home_age_category'] = np.where(input_df[water_damage_limitation]=='full_limit',
                                             'any',
                                             input_df['home_age_category'])
    input_df = pd.merge(input_df, 
                        water_damage_df,
                        how='left', 
                        left_on=[water_damage_limitation,'home_age_category'],
                        right_on=['water_damage_limitation','home_age_ref'])
    input_df.rename(columns={'aop':'water_damage_limitation_aop_factor',
                             'nhw':'water_damage_limitation_nhw_factor',
                             'hur':'water_damage_limitation_hur_factor'},inplace=True)
    #input_df.loc[input_df[water_damage_limit]=='Full Limit',['water_damage_aop_factor','water_damage_nhw_factor','water_damage_hur_factor']] = 1

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['water_damage_limitation_aop_factor'].fillna(1, inplace=True)
    input_df['water_damage_limitation_nhw_factor'].fillna(1, inplace=True)
    input_df['water_damage_limitation_hur_factor'].fillna(1, inplace=True)


    # DEBUG: Check if home_age column exists
    # print("DEBUG: Columns in input_df before home_age access:", input_df.columns.tolist())
    if 'home_age' not in input_df.columns:
        print("ERROR: 'home_age' column missing in water_damage calculation!")
        return input_df
    
    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['home_age_ref'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['home_age_ref'].isna(), 
                                     input_df['error_msg']+','+'Invalid water damage limitation or age of home.', 
                                     input_df['error_msg'])

    # input_df.drop(columns=['home_age_category'],inplace=True)
    return input_df
