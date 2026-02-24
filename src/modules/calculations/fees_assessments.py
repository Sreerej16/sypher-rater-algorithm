import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def fees_assessments_calc(input_df, dataframes):
    """
    Copies fees/assessments from the reference sheet into input_df.
    If Percent of Premium is provided, calculates based on total_premium.
    """

    # Get the reference sheet
    fees_assessments_df = dataframes.get('fees_assessments_df')
    
    for _, row in fees_assessments_df.iterrows():
        fee_name = row["fee"]
        amount = row.get("amount")
        percent = row.get("percent_of_premium")

        if pd.notna(amount):  
            # Fixed fee
            input_df[fee_name] = amount
        elif pd.notna(percent):  
            # Percent of premium → calculate
            input_df[fee_name] = np.round(input_df['total_excl_fees_premium'] * percent, 2)
        else:
            # If both are NaN, set to 0
            input_df[fee_name] = 0

    return input_df
