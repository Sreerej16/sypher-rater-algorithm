import pandas as pd
import numpy as np

from utils.json_handler import find_input_attribute

def building_code_effective_grading_factor_calc(input_df,dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    bceg = find_input_attribute(input_attributes, 'bceg')
    bceg_df = dataframes.get('building_code_effective_grading_df')
    bceg_df['bceg'] = bceg_df['bceg'].astype(str)
    input_df[bceg]   = input_df[bceg].astype(str)
    input_df = pd.merge(input_df,
                        bceg_df ,
                        how='left',
                        left_on=bceg,
                        right_on = 'bceg'
                        )
    input_df.rename(columns={
        'aop': 'bceg_aop_factor', 
        'nhw': 'bceg_nhw_factor', 
        'hur': 'bceg_hur_factor'
    }, inplace=True)
    input_df['bceg_aop_factor'] = input_df['bceg_aop_factor'].round(3)
    input_df['bceg_nhw_factor'] = input_df['bceg_nhw_factor'].round(3)
    input_df['bceg_hur_factor'] = input_df['bceg_hur_factor'].round(3)
    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['bceg_aop_factor'].fillna(1, inplace=True)
    input_df['bceg_nhw_factor'].fillna(1, inplace=True)
    input_df['bceg_hur_factor'].fillna(1, inplace=True)
    
    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['bceg'].isna(), True, input_df['invalid_lookup'] )
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['bceg'].isna(), 
                                     input_df['error_msg']+','+'Invalid building Code effectivenss grading', 
                                     input_df['error_msg'])
    
    return input_df