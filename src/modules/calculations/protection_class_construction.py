import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def protection_class_construction_factor_calc(input_df, dataframes, input_attributes):
    # From the array of dataframes, get the relevant df 
    protection_class_df = dataframes.get("protection_class_construction_df")
    protection_class = find_input_attribute(input_attributes, 'protection_class')
    construction_type = find_input_attribute(input_attributes, 'construction_type')
    input_df[protection_class] = input_df[protection_class].astype(str)
    protection_class_df['Protection Class'] = protection_class_df['Protection Class'].astype(str)
    # Merge input_df with protection_class_df on 'Protection_Class' and 'construction_type'
    input_df = pd.merge(input_df, protection_class_df, how='left', 
                        left_on=['protection_class', 'construction_type'], 
                        right_on=['protection_class', 'construction_type'])
    # Rename columns after the merge
    input_df.rename(columns={'aop': 'protection_class_construction_aop',
                             'nhw': 'protection_class_construction_nhw',
                             'hur': 'protection_class_construction_hur'}, inplace=True)
    # Fill missing values with defaults for protection class columns
    input_df['protection_class_construction_aop'].fillna(1, inplace=True)
    input_df['protection_class_construction_nhw'].fillna(1, inplace=True)
    input_df['protection_class_construction_hur'].fillna(1, inplace=True)
    
    # Mark invalid lookups where protection class and construction type weren't found
    input_df['invalid_lookup'] = np.where(input_df['protection_class'].isna(), True, input_df['invalid_lookup'])
    
    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['protection_class'].isna(), 
                                     input_df['error_msg']+','+'Invalid Protection Class', 
                                     input_df['error_msg'])
    
    # Drop extra columns from the merge if needed
    # input_df.drop(columns=['Protection Class', 'Construction Type'], inplace=True)
    
    return input_df