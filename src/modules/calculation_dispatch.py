# modules/calculation_dispatch.py

import json
from calculations.base_rates import baserates_calc
from calculations.step_premium import calculate_step_premiums
from calculations.distance_to_coast import distance_to_coast_calc
from calculations.amount_of_insurance import covafactors_calc
from calculations.protection_class_construction_type import protection_class_construction_calc
from calculations.age_of_home import age_of_home_calc
from calculations.year_built import year_built_calc
from calculations.age_of_roof import age_of_roof_factor_calc
from calculations.roof_payment_schedule import roof_payment_schedule_factor_calc
from calculations.insurance_tier import insurance_tier_factor_calc
from calculations.secured_community import secured_community_factor_calc
from calculations.central_burglar_alarm import central_burglar_alarm_factor_calc
from calculations.central_fire_alarm import central_fire_alarm_factor_calc
from calculations.full_sprinkler_system import full_sprinkler_system_factor_calc
from calculations.tankless_water_heater import tankless_waterheater_factor_calc
from calculations.water_detection import water_detection_factor_calc
from calculations.fire_protection_discount import fire_protection_factor_calc
from calculations.water_protection_discount import water_protection_discount_calc
from calculations.protection_device_credit import protection_device_factor_calc
from calculations.senior_discount import senior_citizen_discount_factor_calc
from calculations.employee_discount import employee_discount_factor_calc
from calculations.wind_loss_mitigation import wind_loss_mitigation_factor_calc
from calculations.building_code_effectiveness_grading import building_code_effective_grading_factor_calc
from calculations.cap_on_credits import cap_on_credits_factor_calc
from calculations.aop_deductible import aop_deductible_factor_calc
from calculations.total_base_peril_premium import total_base_peril_premium_calc
from calculations.hur_deductible import hur_deductible_factor_calc
from calculations.nhw_deductible import nhw_deductible_factor_calc
from calculations.coverage_b import coverage_b_factor_calc
from calculations.coverage_c import coverage_c_factor_calc
from calculations.coverage_d import coverage_d_factor_calc
from calculations.prior_loss import prior_loss_factor_calc
from calculations.lapse_in_coverage import lapse_in_coverage_factor_calc
from calculations.personal_property_rep_cost import personal_property_rep_cost_factor_calc
from calculations.ordinance_or_law import ordinance_or_law_factor_calc
from calculations.addl_cov_a import addl_cov_a_factor_calc
from calculations.occupancy_usage import occupancy_usage_factor_calc
from calculations.water_damage import water_damage_factor_calc
from calculations.coverage_e import coverage_e_factor_calc
from calculations.coverage_f import coverage_f_factor_calc
from calculations.solar_panel import solar_panel_factor_calc
from calculations.sink_hole import sink_hole_factor_calc
from calculations.structures_rented import structures_rented_factors_calc
from calculations.increased_spec_limits import increased_spec_limits_factor_calc
from calculations.electronic_documents import electronic_documents_factor_calc
from calculations.personal_injury import personal_injury_factor_calc
from calculations.scheduled_pp import scheduled_pp_factor_calc
from calculations.loss_assessment import loss_assessment_factor_calc
from calculations.limited_fungi import limited_fungi_factor_calc
from calculations.golf_cart import golf_cart_factor_calc
from calculations.water_backup import water_backup_factor_calc
from calculations.animal_liability import animal_liability_factor_calc
from calculations.ltd_hur_screened_encl import ltd_hur_screened_encl_factor_calc
from calculations.cyber_guard import cyber_guard_factor_calc
from calculations.computer import computer_factor_calc
from calculations.fees_assessments import fees_assessments_calc
from calculations.total_premium_excluding_fees import total_premium_excluding_fees_calc
from calculations.total_premium_including_fees import total_premium_including_fees_calc

def process_all_calculations(input_df, dataframes, input_attributes):
    """
    This function processes all branch-specific calculations in sequence
    and returns the expanded DataFrame.
    Parameters:
        input_df (pd.DataFrame): The input DataFrame with attributes.
        factor_tables (dict): Dictionary containing factor tables as DataFrames.
    Returns:
        pd.DataFrame: The expanded DataFrame with all calculations applied.
    """
    # Process the BaseRates calculations
    input_df['error_msg']  = ""
    input_df['invalid_lookup'] = False

    # Lookup base premium factors
    input_df = baserates_calc(input_df,dataframes, input_attributes)
    input_df = distance_to_coast_calc(input_df,dataframes , input_attributes)
    input_df = covafactors_calc(input_df,dataframes, input_attributes)
    input_df = protection_class_construction_calc(input_df,dataframes, input_attributes)
    input_df = age_of_home_calc(input_df,dataframes, input_attributes)
    input_df = year_built_calc(input_df,dataframes, input_attributes)
    input_df = age_of_roof_factor_calc(input_df,dataframes, input_attributes)
    input_df = roof_payment_schedule_factor_calc(input_df,dataframes, input_attributes)
    input_df = insurance_tier_factor_calc(input_df,dataframes, input_attributes)
    input_df = secured_community_factor_calc(input_df,dataframes, input_attributes)
    input_df = central_burglar_alarm_factor_calc(input_df,dataframes, input_attributes)
    input_df = central_fire_alarm_factor_calc(input_df,dataframes, input_attributes)
    input_df = full_sprinkler_system_factor_calc(input_df,dataframes, input_attributes)
    input_df = tankless_waterheater_factor_calc(input_df,dataframes, input_attributes)
    input_df = water_detection_factor_calc(input_df,dataframes, input_attributes)
    input_df = fire_protection_factor_calc(input_df)
    input_df = water_protection_discount_calc(input_df)
    input_df = protection_device_factor_calc(input_df)
    input_df = senior_citizen_discount_factor_calc(input_df, dataframes, input_attributes)
    input_df = employee_discount_factor_calc(input_df,dataframes, input_attributes)
    input_df = wind_loss_mitigation_factor_calc(input_df,dataframes, input_attributes)
    input_df = building_code_effective_grading_factor_calc(input_df,dataframes, input_attributes)
    input_df = cap_on_credits_factor_calc(input_df,dataframes, input_attributes)
    input_df = aop_deductible_factor_calc(input_df,dataframes, input_attributes)
    input_df = nhw_deductible_factor_calc(input_df,dataframes, input_attributes)
    input_df = hur_deductible_factor_calc(input_df,dataframes, input_attributes)
    
    
    
    input_df = coverage_b_factor_calc(input_df,dataframes, input_attributes)
    input_df = coverage_c_factor_calc(input_df,dataframes, input_attributes)
    input_df = coverage_d_factor_calc(input_df,dataframes, input_attributes)
    input_df = water_damage_factor_calc(input_df,dataframes, input_attributes)
    input_df = occupancy_usage_factor_calc(input_df,dataframes, input_attributes)
    input_df = lapse_in_coverage_factor_calc(input_df,dataframes, input_attributes)
    input_df = prior_loss_factor_calc(input_df,dataframes, input_attributes)  
    
    # # # Calculate step premiums for each factor
    # input_df = calculate_step_premiums(input_df)
    
    # # # Calculate base premium amounts
    input_df = total_base_peril_premium_calc(input_df,dataframes, input_attributes)
    
    # # # # Lookup additional factors
    input_df = coverage_e_factor_calc(input_df,dataframes, input_attributes)
    input_df = coverage_f_factor_calc(input_df,dataframes, input_attributes)
    input_df = solar_panel_factor_calc(input_df,dataframes, input_attributes)
    input_df = sink_hole_factor_calc(input_df,dataframes, input_attributes)
    input_df = structures_rented_factors_calc(input_df,dataframes, input_attributes)
    input_df = increased_spec_limits_factor_calc(input_df,dataframes, input_attributes)   
    input_df = scheduled_pp_factor_calc(input_df,dataframes, input_attributes)
    input_df = loss_assessment_factor_calc(input_df,dataframes, input_attributes)
    input_df = limited_fungi_factor_calc(input_df,dataframes, input_attributes)
    input_df = golf_cart_factor_calc(input_df,dataframes, input_attributes)
    input_df = water_backup_factor_calc(input_df,dataframes, input_attributes)
    input_df = animal_liability_factor_calc(input_df,dataframes, input_attributes)
    input_df = ltd_hur_screened_encl_factor_calc(input_df,dataframes, input_attributes)
    input_df = cyber_guard_factor_calc(input_df,dataframes, input_attributes)
    input_df = personal_injury_factor_calc(input_df,dataframes, input_attributes)
    input_df = computer_factor_calc(input_df,dataframes, input_attributes)

    input_df = ordinance_or_law_factor_calc(input_df,dataframes, input_attributes)
    input_df = addl_cov_a_factor_calc(input_df,dataframes, input_attributes)
    input_df = personal_property_rep_cost_factor_calc(input_df,dataframes, input_attributes)


    input_df = electronic_documents_factor_calc(input_df,dataframes, input_attributes)

    # # Calculate total premium amounts with additional factors
    input_df = total_premium_excluding_fees_calc(input_df, dataframes, input_attributes)
    input_df = fees_assessments_calc(input_df, dataframes)
    input_df = total_premium_including_fees_calc(input_df, input_attributes)
    
    return input_df

