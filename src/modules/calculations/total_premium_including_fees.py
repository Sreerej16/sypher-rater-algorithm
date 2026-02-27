import pandas as pd
from utils.json_handler import find_input_attribute
def total_premium_including_fees_calc(input_df, input_attributes):

    payment_plan = find_input_attribute(input_attributes, 'payment_plan')

    # Fee columns
    fee_columns = ['policy_fee', 'empa_fee','surplus_contribution', 'figa_assessment']

    # Premium columns (non-fee)
    premium_columns = ['total_base_premium','calculated_coverage_e_premium','calculated_coverage_f_premium',
                       'solar_panel_premium','sinkhole_premium','structures_rented_liab_premium',
                       'structures_rented_prop_premium','increased_spec_limits_premium','scheduled_pp_premium',
                       'loss_assessment_premium','limited_fungi_premium','golf_cart_premium','water_backup_premium',
                       'animal_liability_premium','ltd_hur_screened_encl_premium','cyber_guard_premium',
                       'personal_injury_premium','computer_premium','ordinance_or_law_premium','addl_cov_a_premium',
                       'personal_property_rep_cost_premium']
    
    # Check if any rows need setup fee
    has_setup_fee = input_df[payment_plan].isin(['SA60', 'Q40']).any()
    
    if has_setup_fee:
        input_df['setup_fee'] = 0
        input_df.loc[input_df[payment_plan].isin(['SA60', 'Q40']), 'setup_fee'] = 10
        fee_columns.append('setup_fee')
    
    # Calculate total fee
    input_df['total_fee'] = input_df[fee_columns].sum(axis=1).astype(float).round(0)
    
    # Calculate total premium including fees 
    all_columns = premium_columns + fee_columns
    input_df['total_incl_fees_premium'] = input_df[all_columns].sum(axis=1).astype(float).round(0)
    return input_df
