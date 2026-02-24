import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def equipment_breakdown_factor_calc(input_df,dataframes, input_attributes):
    equipment_breakdown_coverage=find_input_attribute(input_attributes, 'equipment_breakdown_coverage')
    equipment_breakdown_df = dataframes.get('equipment_breakdown_df')
    equipment_breakdown_df['equipment_breakdown_coverage'] = equipment_breakdown_df['equipment_breakdown_coverage'].astype(str)

    if input_df['equipment_breakdown_coverage'].isna().any():
        input_df['equipment_breakdown_premium'] = pd.NA
        return input_df
    
    input_df[equipment_breakdown_coverage] = input_df[equipment_breakdown_coverage].astype(str)
    input_df[equipment_breakdown_coverage].replace('0','excl',inplace=True)
    input_df = pd.merge(input_df,
                        equipment_breakdown_df ,
                        how='left',
                        left_on=equipment_breakdown_coverage,
                        right_on = 'equipment_breakdown_coverage'
                        )
    


    # Fill missing columns after the merge with default values
    input_df['equipment_breakdown_premium'].fillna(0, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['equipment_breakdown_coverage'].isna(), True, input_df['invalid_lookup'])

    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['equipment_breakdown_coverage'].isna(), 
                                     input_df['error_msg']+','+'Invalid eb_limit', 
                                     input_df['error_msg'])
    
    return input_df