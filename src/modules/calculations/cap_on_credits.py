import pandas as pd
import numpy as np
import math
from utils.rounding_utils import custom_round

def cap_on_credits_factor_calc(input_df,dataframes, input_attributes):

    cap_on_credit_df = dataframes.get('cap_on_credits_df')

    mul_fact_aop = input_df[['protection_device_aop_factor','employee_discount_aop_factor','wind_loss_mitigation_aop_factor','bceg_aop_factor']].prod(axis=1).round(5)
    mul_fact_nhw = input_df[['protection_device_nhw_factor','employee_discount_nhw_factor','wind_loss_mitigation_nhw_factor','bceg_nhw_factor']].prod(axis=1).round(5)
    mul_fact_hur = input_df[['protection_device_hur_factor','employee_discount_hur_factor','wind_loss_mitigation_hur_factor','bceg_hur_factor']].prod(axis=1).round(5)
    
    # Apply the max function element-wise with cap on credit values
    cap_on_credit_aop = mul_fact_aop.combine(cap_on_credit_df['aop'].iloc[0], max)
    cap_on_credit_nhw = mul_fact_nhw.combine(cap_on_credit_df['nhw'].iloc[0], max)
    cap_on_credit_hur = mul_fact_hur.combine(cap_on_credit_df['hur'].iloc[0], max)
    
    # Assign the results back to the DataFrame
    input_df['cap_on_credit_aop_factor'] = cap_on_credit_aop
    input_df['cap_on_credit_nhw_factor'] = cap_on_credit_nhw
    input_df['cap_on_credit_hur_factor'] = cap_on_credit_hur

    input_df['cap_on_credit_aop_factor'] = custom_round(input_df['cap_on_credit_aop_factor'])
    input_df['cap_on_credit_nhw_factor'] = custom_round(input_df['cap_on_credit_nhw_factor'])
    input_df['cap_on_credit_hur_factor'] = custom_round(input_df['cap_on_credit_hur_factor'])

    
    return input_df