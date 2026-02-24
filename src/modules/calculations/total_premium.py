
import pandas as pd

def total_premium_excluding_fees_calc(input_df):
    # List of premium columns to sum
    premium_columns = ['base_prem', 'cov_e_prem', 'cov_f_prem', 'solar_panel_prem', 'sh_prem',
                       'structures_property_prem', 'home_sharing_prem', 'incr_pp_prem', 'sch_pp_prem',
                       'la_prem', 'fungi_prem', 'golf_cart_prem', 'water_backup_prem', 'animal_liab_prem',
                       'screen_encl_prem', 'eb_prem', 'pi_prem', 'home_comp_prem','edoc_credit']
    
    # Calculate total premium excluding fees in a vectorized way
    input_df['total_prem_xfees'] = input_df[premium_columns].sum(axis=1).astype(float).round(2)
    
    return input_df
