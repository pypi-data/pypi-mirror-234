import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma


def initialize_dataconnector_variables():
    api = "/services/data/v57.0/wave/dataConnectors"
    dataset_connectors_details_df = pd.DataFrame()
    api_name = 'CRMA_Data_connectors'
    label_name = 'CRMA Data Connectors'
    return api,dataset_connectors_details_df,api_name,label_name

def dataset_connectors(sf,in_upload_crma):
    api,dataset_connectors_details_df,api_name,label_name = initialize_dataconnector_variables()
    while(api is not None):
        # print("Within While")
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['dataConnectors']
        temp_details_df = pd.DataFrame(temp_details)
        temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
        temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
        dataset_connectors_details_df = pd.concat([dataset_connectors_details_df,temp_details_df],axis=0)
        #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    CRM_dataconnectors_df = dataset_connectors_details_df[['connectorType','id','label','name','description','Created_by_id','Created_by_name','url','ingestionSchedule']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRM_dataconnectors_df,api_name,label_name)
    return CRM_dataconnectors_df