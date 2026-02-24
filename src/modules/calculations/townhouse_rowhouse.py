import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def townhouse_rowhouse_factor_calc(input_df, dataframes, input_attributes):
    # From the array of dataframes, get the relevant df 
    townhouse_rowhouse_df = dataframes.get('townhouse_rowhouse_df')
    # townhouse_rowhouse_group_df = dataframes.get('townhouse_rowhouse_group_df')
    #townhouse_rowhouse_df['Units Within Fire Division'] = townhouse_rowhouse_df['Units Within Fire Division'].replace(" & ","to",regex=True)
    
    units_in_fire_division   = find_input_attribute(input_attributes, 'units_in_fire_division')
    protection_class      = find_input_attribute(input_attributes, 'protection_class')
    # input_df['fire_category'] = np.where(input_df[units_in_fire_division] >= 5,'5+',input_df[units_in_fire_division].astype(str))
    # townhouse_rowhouse_group_df['# of Units'] = townhouse_rowhouse_group_df['# of Units'].astype(str)
    # input_df['fire_category'] = input_df['fire_category'].astype(str)

    # Ensure data types match for merge
    townhouse_rowhouse_df['units_in_fire_division'] = townhouse_rowhouse_df['units_in_fire_division'].astype(str)
    townhouse_rowhouse_df['protection_class'] = townhouse_rowhouse_df['protection_class'].astype(str)
    input_df[units_in_fire_division] = input_df[units_in_fire_division].astype(str)
    input_df[protection_class] = input_df[protection_class].astype(str)

    input_df = pd.merge(input_df, 
                        townhouse_rowhouse_df,
                        how='left', 
                        left_on=[units_in_fire_division,protection_class], 
                        right_on=['units_in_fire_division','protection_class'])
    # Rename columns after the merge
    input_df.rename(columns={
        'aop': 'townhouse_rowhouse_aop_factor', 
        'nhw': 'townhouse_rowhouse_nhw_factor', 
        'hur': 'townhouse_rowhouse_hur_factor'
    }, inplace=True)

    # Incase any missing lookups,Fill missing values for AOP, NHW, HUR with 1
    input_df['townhouse_rowhouse_aop_factor'].fillna(1, inplace=True)
    input_df['townhouse_rowhouse_nhw_factor'].fillna(1, inplace=True)
    input_df['townhouse_rowhouse_hur_factor'].fillna(1, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['units_in_fire_division'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['units_in_fire_division'].isna(), 
                                     input_df['error_msg']+','+'Invalid Units Within Fire Division', 
                                     input_df['error_msg'])
    
    # Drop extra columns from the merge
    # input_df.drop(columns=['units_fire_category','Units Within Fire Division', 'Protection Class'], inplace=True)

    return input_df