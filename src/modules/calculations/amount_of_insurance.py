import pandas as pd
import numpy as np
import math
from utils.json_handler import find_input_attribute
from utils.rounding_utils import custom_round

def covafactors_calc(input_df, dataframes, input_attributes):
    cov_a_factors = dataframes.get('amount_of_insurance_df')
    cov_a_addl_factors = dataframes.get("covA_addl_limit_df")

    # Find the input attributes that are needed for lookup
    coverage_a_amt = find_input_attribute(input_attributes, 'coverage_a_amt')
    input_df['coverage_a_amt'] = input_df['coverage_a_amt'].astype('Int64')
    
    
    """
    Vectorized version of CovA and CovAaddl factors application to the input DataFrame
    based on Coverage A limits.
    Parameters:
        input_df (pd.DataFrame): The input DataFrame containing Coverage A limits.
        cov_a_factors (pd.DataFrame): The DataFrame containing CovA factors by peril.
        cov_a_addl_factors (pd.DataFrame): The DataFrame containing additional CovA factors by peril.
    Returns:
        pd.DataFrame: The updated input DataFrame with the calculated CovA factors.
    """
    if 'coverage_a_amt' not in input_df.columns:
        raise KeyError("coverage_a column is missing from the input data.")
    
    # Extract the base limit from the last row of the first column in CovAFactors
    base_limit = cov_a_factors['coverage_a_amt'].iloc[-1]
    
    # Extract the increment from the first row of the first column in CovAaddlFactors
    increment = cov_a_addl_factors['cov_a_addl_limit'].iloc[0]
    coverage_a_limits = input_df[coverage_a_amt]
    
    # Interpolate factors for each peril based on the CovA factors table
    perils = cov_a_factors.columns[1:]  # Assuming the first column is the limit and rest are perils
    for peril in perils:
        below_base_limit = coverage_a_limits <= base_limit
        above_base_limit = coverage_a_limits > base_limit
        
        # Create an empty array of the same shape as coverage_a_limits
        covafactor = np.zeros_like(coverage_a_limits, dtype=float)
        
        # Apply interpolation for limits <= base_limit
        covafactor[below_base_limit] = interpolate_factors(coverage_a_limits[below_base_limit], cov_a_factors, peril)
        
        # Apply additional factor calculation for limits > base_limit
        covafactor[above_base_limit] = calculate_above_base_limit_factors(coverage_a_limits[above_base_limit], cov_a_factors, cov_a_addl_factors, peril, base_limit, increment)

        # Apply custom rounding logic
        rounded_factors = custom_round(pd.Series(covafactor))

        # Assign the calculated factors to the DataFrame
        input_df[f'amount_of_insurance_{peril.lower()}_factor'] = rounded_factors
    return input_df

def interpolate_factors(limits, cov_a_factors, peril):
    """
    Ceiling lookup for limits less than or equal to the base limit.
    Returns the factor for the first table entry >= the given limit.
    Parameters:
        limits (pd.Series): Series of limits from the input DataFrame.
        cov_a_factors (pd.DataFrame): The CovA factors table.
        peril (str): The peril for which to calculate the factor.
    Returns:
        np.ndarray: The looked-up factors for the given limits.
    """
    limit_column = pd.to_numeric(cov_a_factors['coverage_a_amt'], errors='coerce').values
    factor_column = pd.to_numeric(cov_a_factors[peril], errors='coerce').values

    # Find the index of the first table entry >= limit (ceiling lookup)
    indices = np.searchsorted(limit_column, np.asarray(limits), side='left')
    indices = np.clip(indices, 0, len(factor_column) - 1)
    return factor_column[indices]

def calculate_above_base_limit_factors(limits, cov_a_factors, cov_a_addl_factors, peril, base_limit, increment):
    """
    Vectorized calculation for limits above the base limit, applying additional factors.
    Parameters:
        limits (pd.Series): Series of limits greater than the base limit.
        cov_a_factors (pd.DataFrame): The CovA factors table.
        cov_a_addl_factors (pd.DataFrame): The CovA additional factors table.
        peril (str): The peril for which to calculate the factor.
        base_limit (float): The dynamically extracted base limit.
        increment (float): The dynamically extracted increment.
    Returns:
        np.ndarray: The calculated factors for limits above the base limit.
    """
    # Interpolate the base factor for base_limit
    base_factor = interpolate_factors(pd.Series([base_limit] * len(limits)), cov_a_factors, peril)
    
    # Calculate the additional factor
    additional_factor = cov_a_addl_factors.loc[cov_a_addl_factors['cov_a_addl_limit'] == increment, peril].values[0]
    
    # Calculate the excess amount and apply the additional factor
    excess_amount = limits - base_limit
    additional_adjustment = (excess_amount / increment) * additional_factor
    
    # Return the final factor for each limit
    return base_factor + additional_adjustment

