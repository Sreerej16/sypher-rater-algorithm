import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def central_fire_alarm_factor_calc(input_df, dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    fire_alarm = find_input_attribute(input_attributes, 'fire_alarm')
    input_df[fire_alarm].fillna('none',inplace=True)

    central_fire_alarm_df = dataframes.get('central_fire_alarm_df')
    central_fire_alarm_df['fire_alarm'].fillna('none',inplace=True)
    input_df = pd.merge(input_df, 
                        central_fire_alarm_df,
                        how='left', 
                        left_on=fire_alarm, 
                        right_on='fire_alarm')
    
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'fire_alarm_aop_factor', 
        'nhw': 'fire_alarm_nhw_factor', 
        'hur': 'fire_alarm_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['fire_alarm_aop_factor'].fillna(1, inplace=True)
    input_df['fire_alarm_nhw_factor'].fillna(1, inplace=True)
    input_df['fire_alarm_hur_factor'].fillna(1, inplace=True)
    
    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['fire_alarm'].isna(), True, input_df['invalid_lookup'])
    
    #Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['fire_alarm'].isna(), 
                                     input_df['error_msg']+','+'Invalid Fire Alarm', 
                                     input_df['error_msg'])
    
    return input_df
