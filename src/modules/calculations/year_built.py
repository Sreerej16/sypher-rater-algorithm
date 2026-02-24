import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def year_built_calc(input_df,dataframes, input_attributes):
    # Find the input attributes that are needed for lookup
    year_built = find_input_attribute(input_attributes, 'year_built')

    # Load the year built lookup DataFrame
    year_built_df = dataframes.get("year_built_df")
    year_built_df['year_built_ref'] = year_built_df['year_built_ref'].astype(str)

    # Apply year built category based on ranges
    input_df['Year_built_val'] = np.where(input_df[year_built] >= 2012, '2012 and Newer',
                                np.where(input_df[year_built] <= 1950, '1950 and Older',
                                input_df[year_built].astype(str)))
    
    # Merge input_df with year_built_df on 'Year_built_val'
    input_df = pd.merge(input_df, year_built_df, how='left', left_on='Year_built_val', right_on='year_built_ref')
    
    # Rename columns for the AOP, NHW, and HUR factors
    input_df.rename(columns={'aop': 'year_built_aop_factor', 'nhw': 'year_built_nhw_factor', 'hur': 'year_built_hur_factor'}, inplace=True)
    
    # Fill missing values with defaults for year built columns
    input_df['year_built_aop_factor'].fillna(1, inplace=True)
    input_df['year_built_nhw_factor'].fillna(1, inplace=True)
    input_df['year_built_hur_factor'].fillna(1, inplace=True)
    
    # Mark invalid lookups where the 'Year Built' wasn't found
    input_df['invalid_lookup'] = np.where(input_df['year_built_ref'].isna(), True, input_df['invalid_lookup']==True)

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['year_built_ref'].isna(),
                                    input_df['error_msg']+','+'Invalid Year Built',
                                    input_df['error_msg'])

    # Drop extra columns after the merge if needed
    input_df.drop(columns=['Year_built_val'], inplace=True)

    return input_df

