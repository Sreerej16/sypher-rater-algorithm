import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def roof_payment_schedule_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    windstorm    = find_input_attribute(input_attributes, 'windstorm')
    
    # From the array of dataframes, get the relevant df 
    roof_payment_schedule_df = dataframes.get('roof_payment_schedule_df')
    roof_payment_schedule_df['roof_age_ref'] = roof_payment_schedule_df['roof_age_ref'].astype(str)

    if input_df['windstorm'].isna().any():
        return input_df
    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(
                    input_df,
                    roof_payment_schedule_df,
                    how='left',
                    left_on=['roof_age_category', 'calculated_roof_material'], 
                    right_on=['roof_age_ref', 'roof_material_ref'])
    
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'windstorm_aop_factor', 
        'nhw': 'windstorm_nhw_factor', 
        'hur': 'windstorm_hur_factor'
    }, inplace=True)

    input_df.loc[input_df[windstorm] == 'excl', 
             ['windstorm_aop_factor', 'windstorm_nhw_factor', 'windstorm_hur_factor']] = 1

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['windstorm_aop_factor'].fillna(1, inplace=True)
    input_df['windstorm_nhw_factor'].fillna(1, inplace=True)
    input_df['windstorm_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['roof_age_ref'].isna(), True,input_df['invalid_lookup'])

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['roof_age_ref'].isna(), 
                                     input_df['error_msg']+','+'Invalid Age of Roof/Roof Material', 
                                     input_df['error_msg'])
    
    # Drop extra columns from the merge
    input_df.drop(columns=['roof_age_category','roof_age_ref', 'roof_material_ref'])
   
    return input_df
