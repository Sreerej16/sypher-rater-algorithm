import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def employee_discount_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    employee_discount = find_input_attribute(input_attributes, 'employee_discount')
    # From the array of dataframes, get the relevant df 
    employee_discount_df = dataframes.get('employee_discount_df')
    
    # Perform the merge with the lookup DataFrame
    input_df = pd.merge(input_df, 
                        employee_discount_df ,
                        how='left', 
                        left_on=employee_discount, 
                        right_on='employee_discount')
    
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'employee_discount_aop_factor', 
        'nhw': 'employee_discount_nhw_factor', 
        'hur': 'employee_discount_hur_factor'
    }, inplace=True)
    input_df['employee_discount_aop_factor']  =  input_df['employee_discount_aop_factor'].round(3)
    input_df['employee_discount_nhw_factor']  =  input_df['employee_discount_nhw_factor'].round(3)
    input_df['employee_discount_hur_factor']  =  input_df['employee_discount_hur_factor'].round(3)
    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['employee_discount_aop_factor'].fillna(1, inplace=True)
    input_df['employee_discount_nhw_factor'].fillna(1, inplace=True)
    input_df['employee_discount_hur_factor'].fillna(1, inplace=True)
    
    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['employee_discount'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['employee_discount'].isna(), 
                                     input_df['error_msg']+','+'Invalid employee discount', 
                                     input_df['error_msg'])
    
    return input_df
