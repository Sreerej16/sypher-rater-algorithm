import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute

def sink_hole_factor_calc(input_df,dataframes, input_attributes):
    location_zipcode   = find_input_attribute(input_attributes, 'location_zipcode')
    sinkhole_loss_coverage = find_input_attribute(input_attributes, 'sinkhole_loss_coverage')
    sinkhole_terr_surcharge_df = dataframes.get('sinkhole_terr_surcharge_df')
    sinkhole_deductible_df     = dataframes.get('sinkhole_deductible_df')
    base_rates_df              = dataframes.get('base_rates_df')

    if input_df['sinkhole_loss_coverage'].isna().any():
        input_df['sinkhole_premium'] = pd.NA
        return input_df

    input_df                   = pd.merge(input_df,
                                          base_rates_df[['location_zipcode','sinkhole_territory']],
                                          how="left",
                                          left_on = location_zipcode,
                                          right_on = "location_zipcode")
    input_df['sinkhole_territory'].fillna('s05', inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['location_zipcode'].isna(), True, input_df['invalid_lookup'])
    input_df['error_msg'] = np.where(input_df['location_zipcode'].isna(), 
                                     'Invalid Zip code....', 
                                     input_df['error_msg'])
    #input_df.drop('location_zipcode',inplace =True)
    input_df                   = pd.merge(input_df,
                                          sinkhole_terr_surcharge_df,
                                          how      ='left',
                                          left_on  = 'sinkhole_territory',
                                          right_on = 'sinkhole_territory')
    
    input_df['sinkhole_territory_surcharge_factor'].fillna(1, inplace=True)
    input_df['invalid_lookup'] = np.where(input_df['sinkhole_territory_surcharge_factor'].isna(), True, input_df['invalid_lookup'])
    input_df['error_msg'] = np.where(input_df['sinkhole_territory_surcharge_factor'].isna(), 
                                     input_df['error_msg']+','+'Invalid Sink Hole territory', 
                                     input_df['error_msg'])
   

    input_df['sinkhole_deductible'] = sinkhole_deductible_df.loc[sinkhole_deductible_df['sinkhole_deductible']==0.1,'sinkhole_deductible_factor'].values[0]

    input_df['sinkhole_premium'] = np.where(input_df[sinkhole_loss_coverage] == 'incl',
                                             input_df[['base_rates_aop_factor', 'amount_of_insurance_aop_factor', 'sinkhole_territory_surcharge_factor', 'sinkhole_deductible']].prod(axis=1).astype(float).round(0),
                                             0)
    return input_df



    


