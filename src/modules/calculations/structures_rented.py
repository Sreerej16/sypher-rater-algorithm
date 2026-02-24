import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def structures_rented_factors_calc(input_df,dataframes, input_attributes):
    
    coverage_e_amt=find_input_attribute(input_attributes, 'coverage_e_amt')
    coverage_f_amt=find_input_attribute(input_attributes, 'coverage_f_amt')
    structures_rented=find_input_attribute(input_attributes, 'structures_rented')
    
    struc_rented_prop_prem_df = dataframes.get('struc_rented_prop_prem_df')
    struc_rented_liab_prem_df = dataframes.get('struc_rented_liab_prem_df')

    if structures_rented is None or structures_rented not in input_df.columns or input_df[structures_rented].isna().any():
        input_df['structures_rented_liab_premium'] = pd.NA
        input_df['structures_rented_prop_premium'] = pd.NA
        return input_df
    
    input_df['structures_rented_prop_rate'] = struc_rented_prop_prem_df['rate_per_$1,000'].values[0]
    #input_df['structures_rented_prop_surcharge']     = struc_rented_liab_prem_df['Premium'].values[0]

     # Liability premium calculation
    input_df['structures_rented_liab_premium'] = np.where(
        ((input_df[coverage_e_amt] == 'excl') & (input_df[coverage_f_amt] == 'excl')) | (input_df[structures_rented] == 0),
        0,struc_rented_liab_prem_df['premium'].values[0]).astype(int)

     # Property premium calculation
    input_df['structures_rented_numeric'] = pd.to_numeric(input_df[structures_rented], errors='coerce').fillna(0)
    input_df['structures_rented_prop_premium'] = (input_df['structures_rented_numeric'] / 1000 * input_df['structures_rented_prop_rate']).round(0)
    
    # Adding both premiums to create structures_rented_premium
    input_df['structures_rented_premium'] = input_df['structures_rented_liab_premium'] + input_df['structures_rented_prop_premium']
    
    return input_df