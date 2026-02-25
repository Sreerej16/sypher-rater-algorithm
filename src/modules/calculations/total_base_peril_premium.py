import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def total_base_peril_premium_calc(input_df, dataframes, input_attributes):


    required_cols = [
        # AOP
        'base_rates_aop_factor','distance_to_coast_aop_factor','amount_of_insurance_aop_factor',
        'protection_class_construction_aop_factor','home_age_aop_factor','year_built_aop_factor',
        'roof_age_aop_factor','windstorm_aop_factor','tier_aop_factor','cap_on_credit_aop_factor',
        'aop_deductible_aop_factor','nhw_deductible_aop_factor','hur_deductible_aop_factor',
        'coverage_b_aop_factor','coverage_c_aop_factor','coverage_d_aop_factor',
        'water_damage_limitation_aop_factor','usage_aop_factor','prior_coverage_aop_factor',
        'prior_claims_aop_factor','prior_coverage_aop_factor','prior_claims_aop_factor',

        # NHW
        'base_rates_nhw_factor','distance_to_coast_nhw_factor','amount_of_insurance_nhw_factor',
        'protection_class_construction_nhw_factor','home_age_nhw_factor','year_built_nhw_factor',
        'roof_age_nhw_factor','windstorm_nhw_factor','tier_nhw_factor','cap_on_credit_nhw_factor',
        'aop_deductible_nhw_factor','nhw_deductible_nhw_factor','hur_deductible_nhw_factor',
        'coverage_b_nhw_factor','coverage_c_nhw_factor','coverage_d_nhw_factor',
        'water_damage_limitation_nhw_factor','usage_nhw_factor','prior_coverage_nhw_factor',
        'prior_claims_nhw_factor','prior_coverage_nhw_factor','prior_claims_nhw_factor',

        # HUR
        'base_rates_hur_factor','distance_to_coast_hur_factor','amount_of_insurance_hur_factor',
        'protection_class_construction_hur_factor','home_age_hur_factor','year_built_hur_factor',
        'roof_age_hur_factor','windstorm_hur_factor','tier_hur_factor','cap_on_credit_hur_factor',
        'aop_deductible_hur_factor','nhw_deductible_hur_factor','hur_deductible_hur_factor',
        'coverage_b_hur_factor','coverage_c_hur_factor','coverage_d_hur_factor',
        'water_damage_limitation_hur_factor','usage_hur_factor','prior_coverage_hur_factor',
        'prior_claims_hur_factor','prior_coverage_hur_factor','prior_claims_hur_factor'
    ]

    for col in required_cols:
        if col not in input_df.columns:
            input_df[col] = 1  # default factor

    # --- Calculate total premiums ---
    input_df["total_base_aop_premium"] = (
        input_df[[col for col in required_cols if col.endswith("_aop_factor")]].prod(axis=1)
    ).astype(float).round(2)

    input_df["total_base_nhw_premium"] = (
        input_df[[col for col in required_cols if col.endswith("_nhw_factor")]].prod(axis=1)
    ).astype(float).round(2)

    input_df["total_base_hur_premium"] = (
        input_df[[col for col in required_cols if col.endswith("_hur_factor")]].prod(axis=1)
    ).astype(float).round(2)

    input_df['total_base_premium'] = (
        input_df[['total_base_aop_premium','total_base_nhw_premium','total_base_hur_premium']]
        .sum(axis=1)
        .astype(float)
        .round(2)
    )

    # # --- Minimum premium calculation (unchanged) ---
    # min_premium_df = dataframes.get("min_premium_df")
    # nhw_deductible = find_input_attribute(input_attributes, 'nhw_deductible')
    # hur_deductible = find_input_attribute(input_attributes, 'hur_deductible')


    # input_df['distance_to_coast'] = input_df['distance_to_coast'].astype(str)

    # input_df['windstorm_and_hail_coverage'] = np.where(
    #     (input_df[nhw_deductible] == 'wind_hail_cov_excl') &
    #     (input_df[hur_deductible] == 'wind_hail_cov_excl'),
    #     'excl',
    #     'incl'
    # )

    # one_mile_or_less = ["0_ft_1000_ft","1001_ft_2500_ft","2501_ft_1_mi"]
    # input_df['distance_to_coast_value'] = np.where(
    #     input_df['distance_to_coast'].isin(one_mile_or_less),
    #     "1_mile_or_less",
    #     "greater_than_1_mile"
    # )

    # input_df = pd.merge(
    #     input_df, min_premium_df,
    #     how='left',
    #     left_on=['windstorm_and_hail_coverage','distance_to_coast_value'],
    #     right_on=['windstorm_and_hail_coverage','distance_to_coast_ref']
    # )

    # input_df['coverage_a_min_premium_perc']  = (
    #     input_df[['coverage_a_amt','percent_of_coverage_a_minimum_premium']].prod(axis=1)
    # )
    # input_df['minimum_premium'] = (
    #     input_df[['coverage_a_min_premium_perc','fixed_amount_minimum_premium']].max(axis=1)
    # )

    # adjusted_base = input_df[['total_base_premium','minimum_premium']].max(axis=1)
    # input_df['adjusted_total_base_premium'] = np.where(
    #     (adjusted_base % 1) < 0.5,
    #     np.floor(adjusted_base),
    #     np.ceil(adjusted_base)
    # ).astype(int)

    # input_df.drop(columns=['distance_to_coast_ref'], inplace=True, errors="ignore")

    return input_df