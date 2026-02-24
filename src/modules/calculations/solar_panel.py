import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def solar_panel_factor_calc(input_df,dataframes, input_attributes):
    
    solar_panel_coverage   = find_input_attribute(input_attributes, 'solar_panel_coverage')
    
    solar_panel_cov_df = dataframes.get('solar_panel_coverage_df')
    solar_panel_aoi_df = dataframes.get('solar_panel_aoi_df')

    if input_df['solar_panel_coverage'].isna().any():
        input_df['solar_panel_premium'] = pd.NA
        return input_df
    
    input_df['solar_panel_coverage_aop'] = solar_panel_cov_df.loc[solar_panel_cov_df['solar_panel_coverage']=='incl','aop'].values[0]
    input_df['solar_panel_coverage_nhw'] = solar_panel_cov_df.loc[solar_panel_cov_df['solar_panel_coverage']=='incl','nhw'].values[0]
    input_df['solar_panel_coverage_hur'] = solar_panel_cov_df.loc[solar_panel_cov_df['solar_panel_coverage']=='incl','hur'].values[0]


    input_df['solar_panel_aoi_aop'] = solar_panel_aoi_df.loc[solar_panel_aoi_df['amount_of_insurance']=='per_$1,000','aop'].values[0]
    input_df['solar_panel_aoi_nhw'] = solar_panel_aoi_df.loc[solar_panel_aoi_df['amount_of_insurance']=='per_$1,000','nhw'].values[0]
    input_df['solar_panel_aoi_hur'] = solar_panel_aoi_df.loc[solar_panel_aoi_df['amount_of_insurance']=='per_$1,000','hur'].values[0]
    
    input_df[solar_panel_coverage] = pd.to_numeric(input_df[solar_panel_coverage], errors='coerce')
    input_df['solar_panel_aop']= (input_df['base_rates_aop_factor']*
                                  input_df['solar_panel_coverage_aop']*
                                  input_df['solar_panel_aoi_aop']*
                                  (input_df[solar_panel_coverage]/1000)*
                                  input_df['aop_deductible_aop_factor']).astype(float).round(2)
    
    input_df['solar_panel_nhw']= (input_df['base_rates_nhw_factor']*
                                  input_df['solar_panel_coverage_nhw']*
                                  input_df['solar_panel_aoi_nhw']*
                                  (input_df[solar_panel_coverage]/1000)*
                                  input_df['nhw_deductible_nhw_factor']).astype(float).round(2)
    
    input_df['solar_panel_hur']= (input_df['base_rates_hur_factor']*
                                  input_df['solar_panel_coverage_hur']*
                                  input_df['solar_panel_aoi_hur']*
                                  (input_df[solar_panel_coverage]/1000)*
                                  input_df['hur_deductible_hur_factor']).astype(float).round(2)
    
    solar_panel = input_df[['solar_panel_aop', 'solar_panel_nhw', 'solar_panel_hur']].sum(axis=1)

    input_df['solar_panel_premium'] = np.where(
        (solar_panel % 1) < 0.5,
        np.floor(solar_panel),
        np.ceil(solar_panel)
    ).astype(int)

    return input_df
    
    
    

    
    
