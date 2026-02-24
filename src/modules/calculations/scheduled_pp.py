import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def scheduled_pp_factor_calc(input_df, dataframes, input_attributes):
    # Retrieve the 'scheduled_pp_df' DataFrame from the dataframes dictionary
    scheduled_pp_df = dataframes.get('scheduled_pp_df')

    # Create a mapping of property categories to their respective column names
    property_mapping = {
        'antiques': find_input_attribute(input_attributes, 'antiques'),
        'bicycles': find_input_attribute(input_attributes, 'bicycles'),
        'cameras_proj_equip': find_input_attribute(input_attributes, 'cameras_proj_equip'),
        'coins': find_input_attribute(input_attributes, 'coins'),
        'stamps': find_input_attribute(input_attributes, 'stamps'),
        'art_incl_br': find_input_attribute(input_attributes, 'art_incl_br'),
        'art_not_incl_br': find_input_attribute(input_attributes, 'art_not_incl_br'),
        'furs': find_input_attribute(input_attributes, 'furs'),
        'golf_equip': find_input_attribute(input_attributes, 'golf_equip'),
        'other_sport_equip': find_input_attribute(input_attributes, 'other_sport_equip'),
        'guns_fired': find_input_attribute(input_attributes, 'guns_fired'),
        'guns_coll': find_input_attribute(input_attributes, 'guns_coll'),
        'jewelry': find_input_attribute(input_attributes, 'jewelry'),
        'misc_pers_prop': find_input_attribute(input_attributes, 'misc_pers_prop'),
        'musical_ins': find_input_attribute(input_attributes, 'musical_ins'),
        'silver_gold_pewt': find_input_attribute(input_attributes, 'silverware')
    }

    if input_df[list(property_mapping.values())].isna().all(axis=1).any():
        input_df['scheduled_pp_premium'] = pd.NA
        return input_df

    #sch_pp= find_input_attribute(input_attributes, 'sch_pp')
    # Create a DataFrame of rates with default values
    rates = scheduled_pp_df.set_index('scheduled_personal_property')['rate_per_$100'].reindex(property_mapping.keys(), fill_value=0)

    # Calculate the premiums in a single loop
    for category, column in property_mapping.items():
        input_df[f'{column}_premium'] = (input_df[column] / 100) * rates[category]

    # Sum all the calculated premiums into one column
    scheduled_pp_sum = input_df[[f'{column}_premium' for column in property_mapping.values()]].sum(axis=1).astype(float)

    input_df['scheduled_pp_premium'] = np.where(
        (scheduled_pp_sum % 1) < 0.5,
        np.floor(scheduled_pp_sum),
        np.ceil(scheduled_pp_sum)
    ).astype(int)

    # Apply conditional logic for 'sch_pp' column
    '''input_df['scheduled_pp_premium'] = np.where(input_df[sch_pp] == 'Included', 
                                                input_df['scheduled_pp_premium'], 0)'''

    return input_df

