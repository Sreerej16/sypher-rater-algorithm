import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def total_premium_excluding_fees_calc(input_df, dataframes, input_attributes):
    # List of premium columns to sum
    premium_columns = ['total_base_premium','calculated_coverage_e_premium','calculated_coverage_f_premium',
                       'solar_panel_premium','sinkhole_premium','structures_rented_liab_premium',
                       'structures_rented_prop_premium','increased_spec_limits_premium','scheduled_pp_premium',
                       'loss_assessment_premium','limited_fungi_premium','golf_cart_premium','water_backup_premium',
                       'animal_liability_premium','ltd_hur_screened_encl_premium','cyber_guard_premium',
                       'personal_injury_premium','computer_premium','ordinance_or_law_premium','addl_cov_a_premium',
                       'personal_property_rep_cost_premium']

    # Calculate total premium excluding fees
    input_df['total_premium_before_min_premium'] = input_df[premium_columns].sum(axis=1).astype(float).round(0)

    # Determine minimum premium:
    # If both NHW and HUR deductibles are excluded, minimum premium is $0
    # Otherwise, use the dollar minimum premium from the reference table
    nhw_deductible = find_input_attribute(input_attributes, 'nhw_deductible')
    hur_deductible = find_input_attribute(input_attributes, 'hur_deductible')

    min_premium_df = dataframes.get('min_premium_df')
    min_premium_value = float(min_premium_df['minimum_premium'].iloc[0])

    both_wind_excl = (
        (input_df[nhw_deductible] == 'wind_hail_cov_excl') &
        (input_df[hur_deductible] == 'wind_hail_cov_excl')
    )
    input_df['minimum_premium'] = np.where(both_wind_excl, 0, min_premium_value)

    # Apply minimum premium: take the greater of total_premium_before_min_premium and minimum_premium
    input_df['total_excl_fees_premium'] = np.maximum(
        input_df['total_premium_before_min_premium'],
        input_df['minimum_premium']
    )
    print(input_df['total_excl_fees_premium'])
    return input_df
