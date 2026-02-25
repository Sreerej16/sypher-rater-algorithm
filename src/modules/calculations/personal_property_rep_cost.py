import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def personal_property_rep_cost_factor_calc(input_df, dataframes, input_attributes):
    personal_property_rep_cost_df = dataframes.get('personal_property_rep_cost_df')
    coverage_b_df                 = dataframes.get('coverage_b_df')
    personal_property_rep_cost    = find_input_attribute(input_attributes, 'personal_property_rep_cost')
    nhw_deductible                = find_input_attribute(input_attributes, 'nhw_deductible')
    hur_deductible                = find_input_attribute(input_attributes, 'hur_deductible')

    input_df[personal_property_rep_cost] = input_df[personal_property_rep_cost].astype(str).replace('0.0', 'no_cov')
    personal_property_rep_cost_df['personal_property_rep_cost'] = personal_property_rep_cost_df['personal_property_rep_cost'].astype(str)

    # Merge to get the multiplier (aop, nhw, hur columns in reference table)
    input_df = pd.merge(input_df,
                        personal_property_rep_cost_df,
                        how='left',
                        left_on=personal_property_rep_cost,
                        right_on='personal_property_rep_cost')

    input_df.rename(columns={
        'aop': 'personal_property_rep_cost_multiplier_aop',
        'nhw': 'personal_property_rep_cost_multiplier_nhw',
        'hur': 'personal_property_rep_cost_multiplier_hur'
    }, inplace=True)

    input_df['personal_property_rep_cost_multiplier_aop'].fillna(0, inplace=True)
    input_df['personal_property_rep_cost_multiplier_nhw'].fillna(0, inplace=True)
    input_df['personal_property_rep_cost_multiplier_hur'].fillna(0, inplace=True)

    # Coverage B Exclusion Factor — T-321 with parameter (Percent of Coverage A = 0%)
    # AOP is always 1.000; NHW and HUR are looked up from the table at coverage_b_pct = '0'
    coverage_b_df = coverage_b_df.copy()
    coverage_b_df['coverage_b_pct'] = coverage_b_df['coverage_b_pct'].astype(str)
    cov_b_excl_row = coverage_b_df[coverage_b_df['coverage_b_pct'] == '0']
    cov_b_excl_factors = {
        'aop': 1.0,
        'nhw': cov_b_excl_row['nhw'].iloc[0] if not cov_b_excl_row.empty else 1.0,
        'hur': cov_b_excl_row['hur'].iloc[0] if not cov_b_excl_row.empty else 1.0,
    }

    # Premium = Multiplier × Base Rate × DTC × AOI × PCC × Age of Home × Year Built
    #          × (1 - (1 - WLM) × CovBExcl) × Water Damage Limitation
    for peril in ['aop', 'nhw', 'hur']:
        wlm_factor = input_df[f'wind_loss_mitigation_{peril}_factor']
        factor_calc  = 1 - (1 - wlm_factor) * cov_b_excl_factors[peril]  # Step 45.8

        input_df[f'personal_property_rep_cost_{peril}_premium'] = (
            input_df[f'personal_property_rep_cost_multiplier_{peril}'] *
            input_df[f'base_rates_{peril}_factor'] *
            input_df[f'distance_to_coast_{peril}_factor'] *
            input_df[f'amount_of_insurance_{peril}_factor'] *
            input_df[f'protection_class_construction_{peril}_factor'] *
            input_df[f'home_age_{peril}_factor'] *
            input_df[f'year_built_{peril}_factor'] *
            factor_calc *
            input_df[f'water_damage_limitation_{peril}_factor']
        ).round(2)

    # *** Wind Exclusion Factor (Step 45.10): when both NHW and HUR deductibles are excluded,
    # apply 0.000 to NHW and HUR perils. AOP is ALWAYS = 1.000 (**), so AOP is unaffected.
    wind_excl_mask = (
        (input_df[nhw_deductible] == 'wind_hail_cov_excl') &
        (input_df[hur_deductible] == 'wind_hail_cov_excl')
    )
    input_df['personal_property_rep_cost_nhw_premium'] = np.where(wind_excl_mask, 0, input_df['personal_property_rep_cost_nhw_premium'])
    input_df['personal_property_rep_cost_hur_premium'] = np.where(wind_excl_mask, 0, input_df['personal_property_rep_cost_hur_premium'])

    input_df['personal_property_rep_cost_premium'] = (
        input_df['personal_property_rep_cost_aop_premium'] +
        input_df['personal_property_rep_cost_nhw_premium'] +
        input_df['personal_property_rep_cost_hur_premium']
    ).round(0)

    input_df['invalid_lookup'] = np.where(input_df['personal_property_rep_cost'].isna(), True, input_df['invalid_lookup'])
    input_df['error_msg'] = np.where(input_df['personal_property_rep_cost'].isna(),
                                     input_df['error_msg'] + ',' + 'Invalid Personal Property Rep Cost',
                                     input_df['error_msg'])

    return input_df
