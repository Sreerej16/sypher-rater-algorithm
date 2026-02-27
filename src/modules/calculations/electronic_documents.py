import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute


def electronic_documents_factor_calc(input_df,dataframes, input_attributes):
    edoc=find_input_attribute(input_attributes, 'edoc')
    electronic_documents_df = dataframes.get('electronic_documents_df')

    input_df = pd.merge(input_df,
                        electronic_documents_df ,
                        how='left',
                        left_on=edoc,
                        right_on = 'electronic_documents'
                        )
    
    # Rename columns after the merge
    input_df.rename(columns={
        'credit': 'electronic_documents_credit_premium'
    }, inplace=True)
    print(input_df)
    # Fill missing columns after the merge with default values
    input_df['electronic_documents_credit_premium'].fillna(0, inplace=True)

    # Mark invalid lookups where the merge didn't find a match 
    input_df['invalid_lookup'] = np.where(input_df['electronic_documents'].isna(), True, input_df['invalid_lookup'])

    # Update the Error Message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['electronic_documents'].isna(),
                                     input_df['error_msg']+','+'Invalid edoc',
                                     input_df['error_msg'])

    return input_df