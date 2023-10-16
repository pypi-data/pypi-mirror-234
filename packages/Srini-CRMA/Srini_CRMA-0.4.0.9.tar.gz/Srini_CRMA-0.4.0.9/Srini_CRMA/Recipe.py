import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from Srini_CRMA.data_connectors import dataset_connectors
from datetime import datetime


def initialize_recipe_variables():
    api = "/services/data/v57.0/wave/recipes"
    recipe_df = pd.DataFrame()
    dummy_recipe_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Recipe'
    label_name = 'CRMA Recipe'
    return api,recipe_df,dummy_recipe_dict,api_name,label_name


def recipe_details(sf,in_upload_crma):
    api,recipe_df,dummy_recipe_dict,api_name,label_name = initialize_recipe_variables()
    while(api is not None):
        # print("Within While")
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['recipes']
        temp_details_df = pd.DataFrame(temp_details)
        # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('description', 0) for x in temp_details_df['connector']]
        recipe_df = pd.concat([recipe_df,temp_details_df],axis=0)
        #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    CRMA_recipe_df = recipe_df[['id', 'label','name','fileUrl','targetDataflowId']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_recipe_df,api_name,label_name)
    return CRMA_recipe_df


