import pandas as pd
def fire_protection_factor_calc(input_df):
    input_df['fire_protection_aop_factor'] = input_df[['fire_alarm_aop_factor','fire_sprinkler_protection_aop_factor']].min(axis = 1)
    input_df['fire_protection_nhw_factor'] = input_df[['fire_alarm_nhw_factor','fire_sprinkler_protection_nhw_factor']].min(axis = 1)
    input_df['fire_protection_hur_factor'] = input_df[['fire_alarm_hur_factor','fire_sprinkler_protection_hur_factor']].min(axis = 1)
    return input_df