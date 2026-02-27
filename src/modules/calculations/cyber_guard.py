import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def cyber_guard_factor_calc(input_df, dataframes, input_attributes):
    cyber_guard_coverage = find_input_attribute(input_attributes, 'cyber_guard_coverage')
    cyber_guard_df = dataframes.get('cyber_guard_df')

    if input_df['cyber_guard_coverage'].isna().any():
        input_df['cyber_guard_premium'] = pd.NA
        return input_df

    cyber_guard_df['package'] = cyber_guard_df['package'].astype(str)
    input_df[cyber_guard_coverage] = input_df[cyber_guard_coverage].astype(str)

    input_df = pd.merge(input_df,
                        cyber_guard_df,
                        how='left',
                        left_on=cyber_guard_coverage,
                        right_on='package')

    input_df.rename(columns={'premium': 'cyber_guard_premium'}, inplace=True)

    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['package'].isna(), True, input_df['invalid_lookup'])

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['package'].isna(),
                                     input_df['error_msg'] + ',' + 'Invalid cyber guard coverage',
                                     input_df['error_msg'])

    input_df.drop(columns=['package'], inplace=True)
    input_df['cyber_guard_premium'].fillna(0, inplace=True)

    return input_df
