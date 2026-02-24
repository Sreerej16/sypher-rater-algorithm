import pandas as pd
def total_premium_excluding_fees_calc(input_df):
    # List of premium columns to sum
    premium_columns = ['adjusted_total_base_premium','calculated_coverage_e_premium','calculated_coverage_f_premium',
                       'solar_panel_premium','sinkhole_premium','structures_rented_liab_premium',
                       'structures_rented_prop_premium','increased_spec_limits_premium','scheduled_pp_premium',
                       'loss_assessment_premium','limited_fungi_premium','golf_cart_premium','water_backup_premium','animal_liability_premium',
                       'ltd_hur_screened_encl_premium','equipment_breakdown_premium','personal_injury_premium','computer_premium']
    
    # Calculate total premium excluding fees 
    input_df['total_excl_fees_premium'] = input_df[premium_columns].sum(axis=1).astype(float).round(0)
    
    return input_df
