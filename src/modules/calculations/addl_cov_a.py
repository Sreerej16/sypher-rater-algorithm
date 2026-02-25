import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def addl_cov_a_factor_calc(input_df, dataframes, input_attributes):
    addl_cov_a_df  = dataframes.get('addl_cov_a_df')
    addl_coverage_a = find_input_attribute(input_attributes, 'addl_coverage_a')
    year_built      = find_input_attribute(input_attributes, 'year_built')
    nhw_deductible  = find_input_attribute(input_attributes, 'nhw_deductible')
    hur_deductible  = find_input_attribute(input_attributes, 'hur_deductible')

    addl_cov_a_df['addl_coverage_a'] = addl_cov_a_df['addl_coverage_a'].astype(str)

    # Merge to get the multiplier (aop, nhw, hur columns in reference table)
    input_df = pd.merge(input_df,
                        addl_cov_a_df,
                        how='left',
                        left_on=addl_coverage_a,
                        right_on='addl_coverage_a')

    input_df.rename(columns={
        'aop': 'addl_cov_a_multiplier_aop',
        'nhw': 'addl_cov_a_multiplier_nhw',
        'hur': 'addl_cov_a_multiplier_hur'
    }, inplace=True)

    input_df['addl_cov_a_multiplier_aop'].fillna(0, inplace=True)
    input_df['addl_cov_a_multiplier_nhw'].fillna(0, inplace=True)
    input_df['addl_cov_a_multiplier_hur'].fillna(0, inplace=True)

    # Premium = Multiplier × Base Rate × DTC × AOI × PCC × Age of Home × Year Built × Wind Excl
    # * Year Built Factor for HUR: if year_built >= 2002, use 0.500; otherwise use table factor
    # ** Year Built Factor for AOP and NHW: ALWAYS = 1.000
    year_built_hur_factor = np.where(
        pd.to_numeric(input_df[year_built], errors='coerce') >= 2002,
        0.500,
        input_df['year_built_hur_factor']
    )

    for peril in ['aop', 'nhw', 'hur']:
        yb_factor = year_built_hur_factor if peril == 'hur' else input_df[f'year_built_{peril}_factor']

        input_df[f'addl_cov_a_{peril}_premium'] = (
            input_df[f'addl_cov_a_multiplier_{peril}'] *
            input_df[f'base_rates_{peril}_factor'] *
            input_df[f'distance_to_coast_{peril}_factor'] *
            input_df[f'amount_of_insurance_{peril}_factor'] *
            input_df[f'protection_class_construction_{peril}_factor'] *
            input_df[f'home_age_{peril}_factor'] *
            yb_factor
        ).round(2)

    # *** Wind Exclusion Factor (Step 44.8): when both NHW and HUR deductibles are excluded,
    # apply 0.000 to NHW and HUR perils. AOP is ALWAYS = 1.000 (**), so AOP is unaffected.
    wind_excl_mask = (
        (input_df[nhw_deductible] == 'wind_hail_cov_excl') &
        (input_df[hur_deductible] == 'wind_hail_cov_excl')
    )
    input_df['addl_cov_a_nhw_premium'] = np.where(wind_excl_mask, 0, input_df['addl_cov_a_nhw_premium'])
    input_df['addl_cov_a_hur_premium'] = np.where(wind_excl_mask, 0, input_df['addl_cov_a_hur_premium'])

    input_df['addl_cov_a_premium'] = (
        input_df['addl_cov_a_aop_premium'] +
        input_df['addl_cov_a_nhw_premium'] +
        input_df['addl_cov_a_hur_premium']
    ).round(0)

    input_df['invalid_lookup'] = np.where(input_df['addl_coverage_a'].isna(), True, input_df['invalid_lookup'])
    input_df['error_msg'] = np.where(input_df['addl_coverage_a'].isna(),
                                     input_df['error_msg'] + ',' + 'Invalid Addl Cov A',
                                     input_df['error_msg'])

    return input_df
