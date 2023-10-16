import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict

def initialize_folder_variables():
    api = "/services/data/v57.0/wave/folders"
    folders_df = pd.DataFrame()
    dummy_folder_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_folders'
    label_name = 'CRMA folders'
    return api,folders_df,dummy_folder_dict,api_name,label_name

def folder_details(sf,in_upload_crma):
    api,folders_df,dummy_dataflow_execution_dict,api_name,label_name = initialize_folder_variables()
    while(api is not None):
        # print("Within While")
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['folders']
        temp_details_df = pd.DataFrame(temp_details)
        # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('description', 0) for x in temp_details_df['connector']]
        folders_df = pd.concat([folders_df,temp_details_df],axis=0)
        #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    CRMA_folders_df = folders_df[['id','name','label','assetSharingUrl','canBeSharedExternally','featuredAssets','isPinned','lastModifiedDate','permissions','shares','type','url','usageUrl']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_folders_df,api_name,label_name)
    return CRMA_folders_df