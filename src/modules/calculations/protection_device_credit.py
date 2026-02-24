import pandas as pd
import numpy as np
import math
from utils.rounding_utils import custom_round

def protection_device_factor_calc(input_df):
    
    
    # AOP
    input_df['protection_device_aop_factor'] = (
        input_df[['secured_community_aop_factor', 'fire_protection_aop_factor',
                  'burglar_alarm_aop_factor', 'water_protection_aop_factor']].prod(axis=1)
    )

    input_df['protection_device_aop_factor'] = custom_round(input_df['protection_device_aop_factor'])

    # NHW
    input_df['protection_device_nhw_factor'] = (
        input_df[['secured_community_nhw_factor', 'fire_protection_nhw_factor',
                  'burglar_alarm_nhw_factor', 'water_protection_nhw_factor']].prod(axis=1)
    )

    input_df['protection_device_nhw_factor'] = custom_round(input_df['protection_device_nhw_factor'])

    # HUR
    input_df['protection_device_hur_factor'] = (
        input_df[['secured_community_hur_factor', 'fire_protection_hur_factor',
                  'burglar_alarm_hur_factor', 'water_protection_hur_factor']].prod(axis=1)
    )

    input_df['protection_device_hur_factor'] = custom_round(input_df['protection_device_hur_factor'])

    return input_df
