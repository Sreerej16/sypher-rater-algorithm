import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def increased_spec_limits_factor_calc(input_df,dataframes, input_attributes):
    
    #incr_pp_limit=find_input_attribute(input_attributes, 'incr_pp_limit')
    jewel_watch_fur=find_input_attribute(input_attributes, 'jewel_watch_fur')
    silver_gold_pewt=find_input_attribute(input_attributes, 'silver_gold_pewt')
    increased_spec_limits_df = dataframes.get('increased_spec_limits_df')

    if input_df[[jewel_watch_fur, silver_gold_pewt]].isna().all(axis=1).any():
        input_df['increased_spec_limits_premium'] = pd.NA
        return input_df
    
    input_df['jew_watch_fur_fact'] = increased_spec_limits_df.loc[increased_spec_limits_df['personal_property']=='jewel_watch_fur','rate_per_$500'].values[0]
    input_df['sil_gol_pew_fact']   = increased_spec_limits_df.loc[(increased_spec_limits_df['personal_property']=='silver_gold_pewt'),'rate_per_$500'].values[0]
    '''input_df['increased_spec_limits_premium'] = np.where(input_df[incr_pp_limit] == 'Included',
                                                 (((input_df[incr_pp_limit_jew_fur]/500)*input_df['jew_watch_fur_fact']))+((input_df[incr_pp_limit_silver_gold]/500)*input_df['sil_gol_pew_fact']).astype(float).round(2),
                                                 0)'''
    #input_df['increased_spec_limits_premium'] = (((input_df[incr_pp_limit_jew_fur]/500)*input_df['jew_watch_fur_fact']))+((input_df[incr_pp_limit_silver_gold]/500)*input_df['sil_gol_pew_fact']).astype(float).round(2)
    
    
   # Convert incr_pp_limit_jew_fur and incr_pp_limit_silver_gold to numeric, invalid parsing will be set to NaN
    input_df[jewel_watch_fur] = pd.to_numeric(input_df[jewel_watch_fur], errors='coerce')
    input_df[silver_gold_pewt] = pd.to_numeric(input_df[silver_gold_pewt], errors='coerce')

    # Now apply your logic with np.where
    increased_spec_limit = np.where(
        input_df[jewel_watch_fur].isna(),
        np.where(
            input_df[silver_gold_pewt].isna(),
            0,  # If both are 'No Increased Limit'
            ((input_df[silver_gold_pewt] / 500) * input_df['sil_gol_pew_fact'])
        ),
        np.where(
            input_df[silver_gold_pewt].isna(),
            ((input_df[jewel_watch_fur] / 500) * input_df['jew_watch_fur_fact']),
            (((input_df[jewel_watch_fur] / 500) * input_df['jew_watch_fur_fact']) + 
            ((input_df[silver_gold_pewt] / 500) * input_df['sil_gol_pew_fact']))
        )
    )

    input_df['increased_spec_limits_premium'] = np.where(
        (increased_spec_limit % 1) < 0.5,
        np.floor(increased_spec_limit),
        np.ceil(increased_spec_limit)
    ).astype(int)

    return input_df