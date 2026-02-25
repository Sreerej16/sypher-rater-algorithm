import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def ordinance_or_law_factor_calc(input_df, dataframes, input_attributes):
    ordinance_or_law_df = dataframes.get('ordinance_or_law_df')
    ordinance_or_law    = find_input_attribute(input_attributes, 'ordinance_or_law')
    year_built          = find_input_attribute(input_attributes, 'year_built')
    nhw_deductible      = find_input_attribute(input_attributes, 'nhw_deductible')
    hur_deductible      = find_input_attribute(input_attributes, 'hur_deductible')

    input_df[ordinance_or_law] = input_df[ordinance_or_law].astype(str).replace('0', 'no_cov')
    ordinance_or_law_df['ordinance_or_law'] = ordinance_or_law_df['ordinance_or_law'].astype(str)

    # Merge to get the multiplier (aop, nhw, hur columns in reference table)
    input_df = pd.merge(input_df,
                        ordinance_or_law_df,
                        how='left',
                        left_on=ordinance_or_law,
                        right_on='ordinance_or_law')

    input_df.rename(columns={
        'aop': 'ordinance_or_law_multiplier_aop',
        'nhw': 'ordinance_or_law_multiplier_nhw',
        'hur': 'ordinance_or_law_multiplier_hur'
    }, inplace=True)

    input_df['ordinance_or_law_multiplier_aop'].fillna(0, inplace=True)
    input_df['ordinance_or_law_multiplier_nhw'].fillna(0, inplace=True)
    input_df['ordinance_or_law_multiplier_hur'].fillna(0, inplace=True)

    # Premium = Multiplier × Base Rate × DTC × AOI × PCC × Age of Home × Year Built × Roof Age × Wind Excl
    # * Year Built Factor for HUR: if year_built >= 2002, use 0.500; otherwise use table factor
    # ** Year Built Factor for AOP and NHW: ALWAYS = 1.000
    year_built_hur_factor = np.where(
        pd.to_numeric(input_df[year_built], errors='coerce') >= 2002,
        0.500,
        input_df['year_built_hur_factor']
    )

    for peril in ['aop', 'nhw', 'hur']:
        yb_factor   = year_built_hur_factor if peril == 'hur' else input_df[f'year_built_{peril}_factor']
        roof_factor = 1.000 if peril == 'hur' else input_df[f'roof_age_{peril}_factor']  # HUR always 1.000

        input_df[f'ordinance_or_law_{peril}_premium'] = (
            input_df[f'ordinance_or_law_multiplier_{peril}'] *
            input_df[f'base_rates_{peril}_factor'] *
            input_df[f'distance_to_coast_{peril}_factor'] *
            input_df[f'amount_of_insurance_{peril}_factor'] *
            input_df[f'protection_class_construction_{peril}_factor'] *
            input_df[f'home_age_{peril}_factor'] *
            yb_factor *
            roof_factor
        ).round(0)

    # *** Wind Exclusion Factor (Step 43.9): when both NHW and HUR deductibles are excluded, apply 0.000 to NHW and HUR
    wind_excl_mask = (
        (input_df[nhw_deductible] == 'wind_hail_cov_excl') &
        (input_df[hur_deductible] == 'wind_hail_cov_excl')
    )
    input_df['ordinance_or_law_nhw_premium'] = np.where(wind_excl_mask, 0, input_df['ordinance_or_law_nhw_premium'])
    input_df['ordinance_or_law_hur_premium'] = np.where(wind_excl_mask, 0, input_df['ordinance_or_law_hur_premium'])

    input_df['ordinance_or_law_premium'] = (
        input_df['ordinance_or_law_aop_premium'] +
        input_df['ordinance_or_law_nhw_premium'] +
        input_df['ordinance_or_law_hur_premium']
    )

    input_df['invalid_lookup'] = np.where(input_df['ordinance_or_law'].isna(), True, input_df['invalid_lookup'])
    input_df['error_msg'] = np.where(input_df['ordinance_or_law'].isna(),
                                     input_df['error_msg'] + ',' + 'Invalid Ordinance or Law',
                                     input_df['error_msg'])

    return input_df