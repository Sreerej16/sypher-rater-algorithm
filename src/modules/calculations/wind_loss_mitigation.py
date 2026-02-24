import pandas as pd
import numpy as np
from utils.json_handler import find_input_attribute
def wind_loss_mitigation_factor_calc(input_df, dataframes, input_attributes):
    wlm_new_df = dataframes.get('wind_loss_mitigation_new_df')
    wlm_old_df = dataframes.get('wind_loss_mitigation_old_df')
    wlm_op_new_df = dataframes.get('wind_loss_mitigation_op_new_df')
    wlm_op_old_df = dataframes.get('wind_loss_mitigation_op_old_df')
    # Masks for new and old construction
    year_built           = find_input_attribute(input_attributes, 'year_built')
    roof_cover             = find_input_attribute(input_attributes, 'roof_cover')
    terrain                     = find_input_attribute(input_attributes, 'terrain')
    roof_deck_attachment        = find_input_attribute(input_attributes, 'roof_deck_attachment')
    fbc_wind_speed              = find_input_attribute(input_attributes, 'fbc_wind_speed')
    internal_pressure_design    = find_input_attribute(input_attributes, 'internal_pressure_design')
    windborne_debris_region                        = find_input_attribute(input_attributes, 'windborne_debris_region')
    roof_to_wall_attachment        = find_input_attribute(input_attributes, 'roof_to_wall_attachment')
    roof_shape                  = find_input_attribute(input_attributes, 'roof_shape')
    secondary_water_resistance                         = find_input_attribute(input_attributes, 'secondary_water_resistance')
    opening_protection          = find_input_attribute(input_attributes, 'opening_protection')

    new_construction_mask = input_df[year_built] >= 2002
    old_construction_mask = input_df[year_built] < 2002

    # Create new DataFrame for new construction
    new_constr_df = input_df[new_construction_mask].copy()
    wlm_new_df['fbc_wind_speed'].fillna('n/a',inplace=True)
    new_constr_df['fbc_wind_speed'] = new_constr_df[fbc_wind_speed].astype(str)
    wlm_new_df['fbc_wind_speed'] = wlm_new_df['fbc_wind_speed'].astype(str)

    # Update FBC_Wind_Speed based on conditions
    new_constr_df['fbc_wind_speed_category'] = np.where(new_constr_df[terrain] == 'hvhz',
                                               'n/a',
                                               np.where(new_constr_df[roof_cover ] == 'reinf_concrete',
                                                        'any',
                                                        new_constr_df[fbc_wind_speed]))
    #new_constr_df[roof_deck_attachment].fillna('Other',inplace=True)
    new_constr_df[opening_protection].fillna('none',inplace=True)
    # Update Opening Protection and Roof Shape
    '''new_constr_df['opening_protection_category'] = np.where(new_constr_df['opening_protection'].isin(['Basic', 'Hurricane']),
                                                        'Yes',
                                                    'No')'''
    wlm_op_new_df['opening_protection'].fillna('none',inplace=True)
    new_constr_df    = pd.merge(new_constr_df,
                                wlm_op_new_df,
                                how = 'left',
                                left_on = opening_protection,
                                right_on = 'opening_protection'
                                )
    
    # new_constr_df.drop(columns=['Opening Protection'],inplace= True)
    # new_constr_df.rename(columns={'Opening Protection Category': 'opening_protection_category'}, inplace=True)
    new_constr_df['opening_protection_category'] = np.where(new_constr_df[terrain] == 'hvhz',
                                                            'yes',
                                                            new_constr_df['opening_protection_category'])
    new_constr_df['roof_shape_category'] = np.where(new_constr_df[roof_shape] == 'flat',
                                           'hip',
                                           np.where(new_constr_df[roof_shape] == 'gable',
                                                    'other',
                                                    new_constr_df[roof_shape]))
    new_constr_df['roof_shape_category'] = np.where(new_constr_df[roof_cover]=='reinf_concrete',
                                                    'hip',
                                                    new_constr_df['roof_shape_category'])
    new_constr_df['swr_category']        = np.where(new_constr_df[roof_cover]=='reinf_concrete',
                                                    'yes',
                                                    new_constr_df[secondary_water_resistance])
    conditions = [
    new_constr_df['roof_cover'] == 'reinf_concrete',
    new_constr_df['roof_cover'].isin(['fbc_equivalent', 'non_fbc_equivalent', 'other'])]
    choices = ['reinf_concrete', 'other']

    new_constr_df['roof_cover_type_category'] = np.select(conditions, choices, default='Unknown')
    # Merge new construction DataFrame
    merged_new_df = pd.merge(new_constr_df,
                             wlm_new_df,
                             how='left',
                             left_on=[terrain,'roof_cover_type_category','fbc_wind_speed_category',internal_pressure_design,windborne_debris_region,'roof_shape_category','swr_category','opening_protection_category'],
                             right_on=['terrain','roof_cover','fbc_wind_speed','internal_pressure_design','windborne_debris_region','roof_shape','secondary_water_resistance','opening_protection'])
    
    # Create new DataFrame for old construction
    #merged_new_df = merged_new_df.reindex(new_constr_df.index)
    old_constr_df = input_df[old_construction_mask].copy()
    old_constr_df[opening_protection].fillna('none',inplace=True)
    wlm_old_df['opening_protection'].fillna('none', inplace=True)
    wlm_op_old_df['opening_protection'].fillna('none',inplace=True)
    wlm_op_old_df['opening_protection_category'].fillna('none',inplace=True)
    old_constr_df = pd.merge(old_constr_df,
                             wlm_op_old_df,
                             how= 'left',
                             left_on = opening_protection,
                             right_on ='opening_protection')
    # old_constr_df.drop(columns=['Opening Protection'],inplace= True)
    # old_constr_df.rename(columns={'Opening Protection Category': 'opening_protection_category'}, inplace=True)
    # Update Roof Shape for old construction
    old_constr_df['roof_shape_category'] = np.where(old_constr_df[roof_shape] == 'flat',
                                           'hip',
                                           np.where(old_constr_df[roof_shape] == 'gable',
                                                    'other',
                                                    old_constr_df[roof_shape]))
    old_constr_df['roof_deck_attachment_category'] = np.where(old_constr_df[roof_cover] == 'reinf_concrete',
                                                              'reinf_concrete',
                                                              old_constr_df[roof_deck_attachment])
    old_constr_df['swr_category']    = np.where(old_constr_df[roof_cover] == 'reinf_concrete',
                                                              'yes',
                                                              old_constr_df[secondary_water_resistance])
    old_constr_df['roof_to_wall_attachment_category'] = np.where(old_constr_df[roof_cover] == 'reinf_concrete',
                                                              'reinf_concrete',
                                                              old_constr_df[roof_to_wall_attachment])
    # Ensure no NaNs in 'Opening Protection' column
    
    
    old_constr_df['roof_cover_type_category'] = np.where(old_constr_df[roof_cover] == 'other',
                                                         'non_fbc_equivalent',
                                                         old_constr_df[roof_cover]
                                                         )
    # Merge old construction DataFrame
    merged_old_df = pd.merge(old_constr_df,
                             wlm_old_df,
                             how='left',
                             left_on=['roof_cover_type_category',terrain,'roof_deck_attachment_category','roof_to_wall_attachment_category','roof_shape_category','swr_category','opening_protection_category'],
                             right_on=['roof_cover','terrain','roof_deck_attachment','roof_to_wall_attachment','roof_shape','secondary_water_resistance','opening_protection'])

    # Implement fallback strategy for missing lookups
    if 'nhw_&_hur' in merged_old_df.columns and merged_old_df['nhw_&_hur'].isna().sum() > 0:
        # Strategy: Use terrain and roof_cover based average for unmatched records
        fallback_df = merged_old_df[merged_old_df['nhw_&_hur'].isna()].copy()

        if not fallback_df.empty:
            fallback_merge = pd.merge(
                fallback_df[['roof_cover_type_category', terrain]],
                wlm_old_df.groupby(['roof_cover', 'terrain'])['nhw_&_hur'].mean().reset_index(),
                how='left',
                left_on=['roof_cover_type_category', terrain],
                right_on=['roof_cover', 'terrain']
            )

            # Update merged_old_df with fallback values where available
            mask = merged_old_df['nhw_&_hur'].isna()
            if len(fallback_merge) > 0 and 'nhw_&_hur' in fallback_merge.columns:
                merged_old_df.loc[mask, 'nhw_&_hur'] = fallback_merge['nhw_&_hur'].values

    # Initialize a new DataFrame to hold results with the same structure as input_df
    input_df.loc[old_construction_mask, 'wind_loss_mitigation_aop_factor'] = 1
    input_df.loc[old_construction_mask, 'wind_loss_mitigation_nhw_factor'] = merged_old_df['nhw_&_hur'].values
    input_df.loc[old_construction_mask, 'wind_loss_mitigation_hur_factor'] = merged_old_df['nhw_&_hur'].values
    input_df.loc[old_construction_mask, 'terrain'] = merged_old_df['terrain'].values
    input_df.loc[new_construction_mask, 'wind_loss_mitigation_aop_factor'] = 1
    input_df.loc[new_construction_mask, 'wind_loss_mitigation_nhw_factor'] = merged_new_df['nhw_&_hur'].values
    input_df.loc[new_construction_mask, 'wind_loss_mitigation_hur_factor'] = merged_new_df['nhw_&_hur'].values
    input_df.loc[new_construction_mask, 'terrain'] = merged_new_df['terrain'].values

    input_df['wind_loss_mitigation_aop_factor']  =  input_df['wind_loss_mitigation_aop_factor'].round(3)
    input_df['wind_loss_mitigation_nhw_factor']  =  input_df['wind_loss_mitigation_nhw_factor'].round(3)
    input_df['wind_loss_mitigation_hur_factor']  =  input_df['wind_loss_mitigation_hur_factor'].round(3)
    
    input_df['wind_loss_mitigation_aop_factor'].fillna(1, inplace=True)
    input_df['wind_loss_mitigation_nhw_factor'].fillna(1, inplace=True)
    input_df['wind_loss_mitigation_hur_factor'].fillna(1, inplace=True)
    # Mark invalid lookups where the merge didn't find a match
    input_df['invalid_lookup'] = np.where(input_df['terrain'].isna(), True,input_df['invalid_lookup']==True )

    # Optionally, convert to boolean True/False
    input_df['invalid_lookup'] = input_df['invalid_lookup'].astype(bool)

    # Update the error message only if 'invalid_lookup' is True
    input_df['error_msg'] = np.where(input_df['terrain'].isna(),
                                      input_df['error_msg']+','+"Invalid windloss mitigation factors...",
                                      input_df['error_msg'] )
    # input_df.drop(columns=['Terrain'],inplace=True)
    return input_df
