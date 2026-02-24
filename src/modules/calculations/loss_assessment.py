import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def loss_assessment_factor_calc(input_df,dataframes, input_attributes):

    loss_assessment_coverage = find_input_attribute(input_attributes, 'loss_assessment_coverage')
    
    loss_assessment_df   = dataframes.get('loss_assessment_df')
    
    if input_df['loss_assessment_coverage'].isna().any():
        input_df['loss_assessment_premium'] = pd.NA
        return input_df
    
    input_df[loss_assessment_coverage]   = input_df[loss_assessment_coverage].astype(str)
    loss_assessment_df["loss_assessment_coverage"] = loss_assessment_df["loss_assessment_coverage"].astype(str)

    input_df             = pd.merge(input_df,
                                    loss_assessment_df ,
                                    how = 'left',
                                    left_on = loss_assessment_coverage,
                                    right_on= "loss_assessment_coverage"
                                    )
    
    input_df['loss_assessment_premium'].fillna(0, inplace=True)

    # Mark invalid lookups where the merge didn't find a match - this is not working right since None is converting to nan and causing error.
    input_df['invalid_lookup'] = np.where(input_df['loss_assessment_coverage'].isna(), True, input_df['invalid_lookup'])
    
    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['loss_assessment_coverage'].isna(), 
                                     input_df['error_msg']+','+'Invalid loss assessment premium', 
                                     input_df['error_msg'])
    

    return input_df