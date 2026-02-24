import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def golf_cart_factor_calc(input_df,dataframes, input_attributes):
    
    golf_cart_coverage=find_input_attribute(input_attributes, 'golf_cart_coverage')
    
    golf_cart_df   = dataframes.get('golf_cart_df')

    if input_df['golf_cart_coverage'].isna().any():
        input_df['golf_cart_premium'] = pd.NA
        return input_df
    
    golf_cart_df['golf_cart_coverage'] = np.where(
    (golf_cart_df['property_limit'] == 'excl') & (golf_cart_df['liability_limit'] == 'excl'),
    'excl',
    np.where(
        (golf_cart_df['property_limit'] != 'excl') & (golf_cart_df['liability_limit'] == 'excl'),
        golf_cart_df['property_limit'].astype(str) + '_phy_dam' + '_0_liab',
        golf_cart_df['property_limit'].astype(str) + '_phy_dam_' + golf_cart_df['liability_limit'].astype(str) + '_liab'
    )
)

    input_df[golf_cart_coverage] = input_df[golf_cart_coverage].astype(str)
    input_df[golf_cart_coverage] = input_df[golf_cart_coverage].str.replace(',', '')
    input_df = pd.merge(input_df,
                        golf_cart_df[['golf_cart_coverage','golf_cart_premium']],
                        how = 'left',
                        left_on = golf_cart_coverage,
                        right_on = 'golf_cart_coverage')
    

    input_df['golf_cart_premium'].fillna(0, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['golf_cart_coverage'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['golf_cart_coverage'].isna(), 
                                     input_df['error_msg']+','+'Invalid golf cart  limit ', 
                                     input_df['error_msg'])
    


    return input_df