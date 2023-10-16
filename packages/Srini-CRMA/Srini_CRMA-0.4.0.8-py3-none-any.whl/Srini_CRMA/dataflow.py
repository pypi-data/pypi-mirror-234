import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from Srini_CRMA.data_connectors import dataset_connectors
from datetime import datetime


def initialize_dataflow_variables():
    api = "/services/data/v57.0/wave/dataflows"
    dataflow_df = pd.DataFrame()
    dummy_dataflow_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Dataflow'
    label_name = 'CRMA Dataflow'
    return api,dataflow_df,dummy_dataflow_dict,api_name,label_name


def dataflow_details(sf,in_upload_crma):
    api,dataflow_df,dummy_dataflow_dict,api_name,label_name = initialize_dataflow_variables()
    while(api is not None):
        # print("Within While")
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['dataflows']
        temp_details_df = pd.DataFrame(temp_details)
        # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('description', 0) for x in temp_details_df['connector']]
        dataflow_df = pd.concat([dataflow_df,temp_details_df],axis=0)
        #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    CRMA_dataflow_df = dataflow_df[['id','label','name','url','description','emailNotificationLevel','historiesUrl']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_dataflow_df,api_name,label_name)
    return CRMA_dataflow_df


def initialize_dataflow_execution_variables():
    api = "/services/data/v57.0/wave/dataflowjobs"
    dataflow_execution_df = pd.DataFrame()
    dummy_dataflow_execution_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Dataflow_jobs'
    label_name = 'CRMA Dataflow Jobs'
    return api,dataflow_execution_df,dummy_dataflow_execution_dict,api_name,label_name


def dataflow_execution_details(sf,in_upload_crma):
    api,dataflow_execution_df,dummy_dataflow_execution_dict,api_name,label_name = initialize_dataflow_execution_variables()
    while(api is not None):
        # print("Within While")
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['dataflowJobs']
        temp_details_df = pd.DataFrame(temp_details)
        if 'message' in temp_details_df.columns:
            a = 1
        else:
            temp_details_df['message'] = ''
        # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['connector']]
        # temp_details_df['Data_Connector_label'] = [x.get('description', 0) for x in temp_details_df['connector']]
        dataflow_execution_df = pd.concat([dataflow_execution_df,temp_details_df],axis=0)
        #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    CRMA_dataflow_execution_df = dataflow_execution_df[['id','jobType','label','startDate','duration','executedDate','waitTime','progress','message','retryCount']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_dataflow_execution_df,api_name,label_name)
    return CRMA_dataflow_execution_df


def initialize_dataflow_nodes_execution_variables():
    api = "/services/data/v57.0/wave/dataflowjobs"
    dataflow_nodes_execution_df = pd.DataFrame()
    dummy_dataflow_node_execution_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Dataflow_job_node'
    label_name = 'CRMA Dataflow job node'
    return api,dataflow_nodes_execution_df,dummy_dataflow_node_execution_dict,api_name,label_name


def dataflow_nodes_execution(sf,in_dataflow_execution_df,in_upload_crma):
    api,dataflow_nodes_execution_df,dummy_dataflow_node_execution_dict,api_name,label_name = initialize_dataflow_nodes_execution_variables()
    dataflow_execution_df = in_dataflow_execution_df
    source_fields_list = ['id','jobType','label','startDate']
    Target_fields_list = ['dataflow_execution_id','dataflow_jobType','dataflow_label','dataflow_startDate']
    # replicated_objects_id = replicated_objects_df['id']
    for index, row in dataflow_execution_df.iterrows():
        connector_api = api+"/"+row['id']+"/nodes?sort=Mru&pageSize=200"
        # print(connector_api)
        # print(row['label'])
        while(connector_api is not None):
            # print("At beginning of", connector_api)
            temp_rest_response = sf.query_more(connector_api, True)
            # print("here 1 ")
            # temp_details = temp_rest_response['nodes']
            temp_df = pd.DataFrame(temp_rest_response)
            # print(temp_df)
            temp_details_df = pd.DataFrame(list(temp_df['nodes']))
            if temp_details_df.empty == True:
                break
            # print("here 3 ")
            temp_details_df['input_rows_processed_count'] = [x.get('processedCount', 0) for x in temp_details_df['inputRows']]
            temp_details_df['output_rows_failed_count'] = [x.get('failedCount', 0) for x in temp_details_df['outputRows']]
            temp_details_df['output_rows_processed_count'] = [x.get('processedCount', 0) for x in temp_details_df['outputRows']]
            if 'message' in temp_details_df.columns:
                a = 1
            else:
                temp_details_df['message'] = ''
            # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['dataConnector']]
            temp_details_df['api'] = connector_api
            # print(row['jobType'])
            temp_details_df[Target_fields_list] = row[source_fields_list]
            # temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
            # temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
            # temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
            # # assign empty dictionary else the process fails while using the get function.
            # temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
            # temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
            dataflow_nodes_execution_df = pd.concat([dataflow_nodes_execution_df,temp_details_df],axis=0)
            #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
            key_exists = temp_rest_response.get('nextPageUrl') 
            # print("before if")
            if (key_exists is not None):
                connector_api = temp_rest_response['nextPageUrl']
                # print(api , "inside if)")
            else:
                connector_api = key_exists
                # print("iside else",api)
            # print("Next API",connector_api)
    # CRMA_data_connector_objects_df_raw = data_connector_objects_df[['api','temp_x','Data_Connector_id','Data_Connector_name','Data_Connector_label','name','url','replicated','accessDeniedReason','accessible','dataPreviewUrl','fieldsUrl']]
    # print("Final")
    # print(dataflow_nodes_execution_df.dtypes)
    CRMA_dataflow_nodes_execution_df = dataflow_nodes_execution_df[['dataflow_execution_id','dataflow_jobType','dataflow_label','dataflow_startDate','id','label','name','nodeType','message','startDate','status','duration','input_rows_processed_count','output_rows_processed_count','output_rows_failed_count']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_dataflow_nodes_execution_df,api_name,label_name)
    return CRMA_dataflow_nodes_execution_df

def load_dataflow_details(sf,in_upload_crma):
    print("Dataflow Start Time", datetime.now().strftime("%H:%M:%S"))
    CRMA_dataflow_df = dataflow_details(sf,in_upload_crma)
    print("Dataflow execution start Time", datetime.now().strftime("%H:%M:%S"))
    CRMA_dataflow_execution_df = dataflow_execution_details(sf,in_upload_crma)
    print("Dataflow nodes execution start Time", datetime.now().strftime("%H:%M:%S"))
    CRMA_dataflow_nodes_execution_df = dataflow_nodes_execution(sf,CRMA_dataflow_execution_df,in_upload_crma)
    return CRMA_dataflow_df,CRMA_dataflow_execution_df,CRMA_dataflow_nodes_execution_df
    

    