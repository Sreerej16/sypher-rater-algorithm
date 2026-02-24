import pandas as pd
import numpy as np

def calculate_step_premiums(input_df):
    """
    Calculate step premiums for each rating factor showing the incremental premium change.
    This mimics the Excel formula: 
    (PRODUCT(F$8:F_current)+PRODUCT(G$8:G_current)+PRODUCT(H$8:H_current)) - 
    (PRODUCT(F$8:F_previous)+PRODUCT(G$8:G_previous)+PRODUCT(H$8:H_previous))
    """
    
    # List of factor columns in order (matching Excel steps)
    # Format: (factor_name, is_base_rate)
    factor_columns = [
        ('base_rates', True),  # Base rate (not multiplicative)
        ('distance_to_coast', False),
        ('amount_of_insurance', False),
        ('protection_class_construction', False),
        ('home_age', False),
        ('year_built', False),
        ('roof_age', False),
        ('windstorm', False),  # Wind/Hail Roof Surfacing Payment Schedule Factor
        ('tier', False),  # Insurance Tier Factor
        ('protection_device', False),
        ('employee_discount', False),
        ('wind_loss_mitigation', False),
        ('bceg', False),
        ('cap_on_credit', False),
        ('aop_deductible', False),
        ('nhw_deductible', False),
        ('hur_deductible', False),
        ('coverage_b', False),
        ('coverage_c', False),
        ('coverage_d', False),
        ('no_of_stories', False),
        ('water_damage_limitation', False),
        ('usage', False),
        ('townhouse_rowhouse', False),
        ('ordinance_or_law', False),
        ('addl_cov_a', False),
        ('personal_property_rep_cost', False),
        ('prior_coverage', False),
        ('prior_claims', False)
    ]
    
    # Initialize cumulative products
    cumulative_aop = 1.0
    cumulative_nhw = 1.0
    cumulative_hur = 1.0
    
    # Store step premiums for each factor
    step_premiums = {}
    
    for factor_name, is_base in factor_columns:
        aop_col = f'{factor_name}_aop_factor'
        nhw_col = f'{factor_name}_nhw_factor'
        hur_col = f'{factor_name}_hur_factor'
        
        # Check if columns exist in the dataframe
        if aop_col not in input_df.columns or nhw_col not in input_df.columns or hur_col not in input_df.columns:
            print(f"Warning: Columns for {factor_name} not found, skipping...")
            continue
        
        # Get the factor values (assuming single row dataframe)
        aop_factor = input_df[aop_col].iloc[0] if not pd.isna(input_df[aop_col].iloc[0]) else 1.0
        nhw_factor = input_df[nhw_col].iloc[0] if not pd.isna(input_df[nhw_col].iloc[0]) else 1.0
        hur_factor = input_df[hur_col].iloc[0] if not pd.isna(input_df[hur_col].iloc[0]) else 1.0
        
        if is_base:
            # For base rates, these are the actual premium amounts, not factors
            cumulative_aop = aop_factor
            cumulative_nhw = nhw_factor
            cumulative_hur = hur_factor
            step_premium = cumulative_aop + cumulative_nhw + cumulative_hur
        else:
            # Store previous total
            prev_total = cumulative_aop + cumulative_nhw + cumulative_hur
            
            # Multiply by current factors
            cumulative_aop *= aop_factor
            cumulative_nhw *= nhw_factor
            cumulative_hur *= hur_factor
            
            # Calculate step premium (the incremental change)
            curr_total = cumulative_aop + cumulative_nhw + cumulative_hur
            step_premium = curr_total - prev_total
        
        # Store step premium with rounded value
        step_premiums[f'{factor_name}_step_premium'] = round(step_premium, 2)
        
        # Also store the cumulative values for debugging/verification
        step_premiums[f'{factor_name}_cumulative_aop'] = round(cumulative_aop, 2)
        step_premiums[f'{factor_name}_cumulative_nhw'] = round(cumulative_nhw, 2)
        step_premiums[f'{factor_name}_cumulative_hur'] = round(cumulative_hur, 2)
        step_premiums[f'{factor_name}_cumulative_total'] = round(cumulative_aop + cumulative_nhw + cumulative_hur, 2)
    
    # Add all step premiums to the dataframe
    for col_name, value in step_premiums.items():
        input_df[col_name] = value
    
    # Add a final total step premium sum (should equal the total base premium)
    total_step_premium = sum([v for k, v in step_premiums.items() if k.endswith('_step_premium')])
    input_df['total_step_premium_sum'] = round(total_step_premium, 2)
    
    return input_df