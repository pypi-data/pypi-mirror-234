import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma


def initialize_dataset_variables():
    CRMA_Datasets_df = pd.DataFrame()
    dataset_details_df = pd.DataFrame()
    next_page_response_df = pd.DataFrame()
    temp_details_df = pd.DataFrame()
    api = "/services/data/v57.0/wave/datasets?sort=Mru&pageSize=200"
    dataset_api_name = 'CRMA_Dataset'
    dataset_label_name = 'CRMA Dataset'
    return CRMA_Datasets_df,dataset_details_df,next_page_response_df,temp_details_df,temp_details_df,api,dataset_api_name,dataset_label_name

def dataset_metadata(sf,in_upload_crma):
    # api = '/services/data/v57.0/wave/datasets?sort=Mru&pageSize=200'
    # # dataset_rest_response = get_api_response(api)
    # dataset_details = dataset_rest_response['datasets']
    # dataset_details_df = pd.DataFrame(dataset_details)
    # dataset_details_df['Created_by_name'] = [x.get('name', 0) for x in dataset_details_df['createdBy']]
    # dataset_details_df['Created_by_id'] = [x.get('id', 0) for x in dataset_details_df['createdBy']]
    # dataset_details_df['folder_name'] = [x.get('name', 0) for x in dataset_details_df['folder']]
    # dataset_details_df['folder_id'] = [x.get('id', 0) for x in dataset_details_df['folder']]
    # CRMA_Datasets_df= dataset_details_df[['folder_id','folder_name','id','name','label','type','datasetType','dataRefreshDate','visibility','Created_by_id','Created_by_name','visibility']]
    # return CRMA_Datasets_df,dataset_rest_response
    CRMA_Datasets_df,dataset_details_df,next_page_response_df,temp_details_df,temp_details_df,api,dataset_api_name,dataset_label_name = initialize_dataset_variables()
    while(api is not None):
        # print(api)
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['datasets']
        temp_details_df = pd.DataFrame(temp_details)
        temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
        temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
        temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
        temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']]    
        dataset_details_df = pd.concat([dataset_details_df,temp_details_df],axis=0)
        # dataset_details_df = dataset_details_df.append(temp_details_df)
        # print(len(dataset_details_df))
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    CRMA_Datasets_df= dataset_details_df[['folder_id','folder_name','id','name','label','currentVersionId','type','datasetType','dataRefreshDate','visibility','Created_by_id','Created_by_name']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_Datasets_df,dataset_api_name,dataset_label_name)
    return CRMA_Datasets_df