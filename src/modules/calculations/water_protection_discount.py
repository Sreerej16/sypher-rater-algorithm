import pandas as pd
def water_protection_discount_calc(input_df):
    input_df['water_protection_aop_factor'] = input_df[['water_detection_aop_factor','tankless_water_heater_aop_factor']].min(axis=1).astype(float)
    input_df['water_protection_nhw_factor'] = input_df[['water_detection_nhw_factor','tankless_water_heater_nhw_factor']].min(axis=1).astype(float)
    input_df['water_protection_hur_factor'] = input_df[['water_detection_hur_factor','tankless_water_heater_hur_factor']].min(axis=1).astype(float)
    return input_df