import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict


def initialize_dashboard_variables():
    api = "/services/data/v57.0/wave/dashboards"
    dashboard_details_df = pd.DataFrame()
    dummy_dataset_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Dashboards'
    label_name = 'CRMA Dashboards'
    return api,dashboard_details_df,dummy_dataset_dict,api_name,label_name

def dashboard_metadata(sf,in_upload_crma):
    api,dashboard_details_df,dummy_dataset_dict,api_name,label_name = initialize_dashboard_variables()
    while(api is not None):
        # print("Within While")
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['dashboards']
        temp_details_df = pd.DataFrame(temp_details)
        temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
        temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
        temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
        temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
        temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
        # assign empty dictionary else the process fails while using the get function.
        temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
        temp_details_df['dataset_id'] = [x.get('id', 'NO DATASETS') for x in temp_details_df['datasets']] 
        temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
        dashboard_details_df = pd.concat([dashboard_details_df,temp_details_df],axis=0)
        #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    CRMA_Dashboard_df = dashboard_details_df[['type','assetSharingUrl','url','folder_id','folder_name','id','name','label','description','datasets','dataset_id','dataset_name','createdDate','refreshDate','templateSourceId','templateAssetSourceName','Created_by_id','Created_by_name','visibility']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_Dashboard_df,api_name,label_name)
    return CRMA_Dashboard_df