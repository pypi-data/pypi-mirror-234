import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from Srini_CRMA.data_connectors import dataset_connectors
from datetime import datetime


def initialize_data_connector_objects_variables():
    api = "/services/data/v57.0/wave/dataConnectors"
    data_connector_objects_df = pd.DataFrame()
    dummy_connector_objects_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Data_connector_objects'
    label_name = 'CRMA Data connector objects'
    return api,data_connector_objects_df,dummy_connector_objects_dict,api_name,label_name

def dataset_connectors_source_objects(sf,in_data_connector_df,in_upload_crma):
    api,data_connector_objects_df,dummy_connector_objects_dict,api_name,label_name = initialize_data_connector_objects_variables()
    data_connector_df = in_data_connector_df
    data_connector_id = data_connector_df['id']
    for x in data_connector_id:
        connector_api = api+"/"+x+"/sourceObjects?sort=Mru&pageSize=200"
        # print(connector_api)
        while(connector_api is not None):
            #print("At beginning of", x)
            temp_rest_response = sf.query_more(connector_api, True)
            temp_details = temp_rest_response['sourceObjects']
            temp_details_df = pd.DataFrame(temp_details)
            temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['dataConnector']]
            temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['dataConnector']]
            temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['dataConnector']]
            temp_details_df['api'] = connector_api
            temp_details_df['temp_x'] = x
            # temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
            # temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
            # temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
            # # assign empty dictionary else the process fails while using the get function.
            # temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
            # temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
            data_connector_objects_df = pd.concat([data_connector_objects_df,temp_details_df],axis=0)
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
    CRMA_data_connector_objects_df_raw = data_connector_objects_df[['api','temp_x','Data_Connector_id','Data_Connector_name','Data_Connector_label','name','url','replicated','accessDeniedReason','accessible','dataPreviewUrl','fieldsUrl']]
    CRMA_data_connector_objects_df = data_connector_objects_df[['Data_Connector_id','Data_Connector_name','Data_Connector_label','name','replicated']].loc[(data_connector_objects_df['replicated']==True)]
    #if (in_upload_crma == 'Y'):
    #    upload_to_crma(sf,CRMA_data_connector_objects_df,api_name,label_name)
    return CRMA_data_connector_objects_df_raw,CRMA_data_connector_objects_df

def initialize_data_connector_objects_fields_variables():
    api = "/services/data/v57.0/wave/dataConnectors"
    data_connector_objects_df = pd.DataFrame()
    data_connector_objects_fields_df = pd.DataFrame()
    dummy_connector_objects_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Data_connector_objects_fields'
    label_name = 'CRMA Data connector objects fields'
    return api,data_connector_objects_df,data_connector_objects_fields_df,dummy_connector_objects_dict,api_name,label_name

def data_connector_objects_fields(sf,in_data_connector_objects_df,in_upload_crma):
    api,data_connector_objects_df,data_connector_objects_fields_df,dummy_connector_objects_dict,api_name,label_name = initialize_data_connector_objects_fields_variables()
    data_connector_objects_df = in_data_connector_objects_df
    source_fields_list = ['api', 'temp_x', 'Data_Connector_id', 'Data_Connector_name','Data_Connector_label', 'name', 'url', 'replicated','accessDeniedReason', 'accessible', 'dataPreviewUrl', 'fieldsUrl']
    Target_fields_list = ['data_connector_api', 'temp_x', 'Data_Connector_id', 'Data_Connector_name','Data_Connector_label', 'object_name', 'object_url', 'object_replicated','object_accessDeniedReason', 'object_accessible', 'object_dataPreviewUrl', 'object_fieldsUrl']
    # replicated_objects_id = replicated_objects_df['id']
    for index, row in data_connector_objects_df.iterrows():
        connector_api = api+"/"+row['Data_Connector_id']+'/'+'sourceObjects'+'/'+row['name']+"/fields?sort=Mru&pageSize=200"
        #print(connector_api)
        while(connector_api is not None):
            #print("At beginning of", row['Data_Connector_id']+'/'+row['name'])
            temp_rest_response = sf.query_more(connector_api, True)
            temp_details = temp_rest_response['fields']
            temp_details_df = pd.DataFrame(temp_details)
            # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['dataConnector']]
            temp_details_df['api'] = connector_api
            temp_details_df[Target_fields_list] = row[source_fields_list]
            # temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
            # temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
            # temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
            # # assign empty dictionary else the process fails while using the get function.
            # temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
            # temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
            data_connector_objects_fields_df = pd.concat([data_connector_objects_fields_df,temp_details_df],axis=0)
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
    CRMA_data_connector_objects_fields_df = data_connector_objects_fields_df[['data_connector_api','temp_x','Data_Connector_id','Data_Connector_name','Data_Connector_label','object_name','object_url','object_replicated','object_accessDeniedReason',
    'object_accessible','object_dataPreviewUrl','object_fieldsUrl','label','name','fieldType','multiValue','precision','defaultValue','scale','format','accessDeniedReason','accessible']]
    #CRMA_replicated_datasets_all_fields_df = data_connector_objects_fields_df[['Data_Connector_id','Data_Connector_name','Data_Connector_label','object_id','object_name','rowLevelSharing','sourceObjectName','status','type','url','passThroughFilter','replicationDataflowId','name','label','fieldType','multiValue','precision','skipped','defaultValue','format','api','scale','multiValueSeparator']]
    #replicated_dataset_CRMA_fields_df = CRMA_replicated_datasets_all_fields_df[CRMA_replicated_datasets_all_fields_df['skipped'] == False]
    #if (in_upload_crma == 'Y'):
    #    upload_to_crma(sf,CRMA_data_connector_objects_fields_df,api_name,label_name)
    return CRMA_data_connector_objects_fields_df

def initialize_replicated_objects_variables():
    api = "/services/data/v57.0/wave/replicateddatasets"
    replicated_objects_df = pd.DataFrame()
    dummy_replicated_objects_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    api_name = 'CRMA_Data_connector_replicated_objects'
    label_name = 'CRMA Data connector replicated objects'
    return api,replicated_objects_df,dummy_replicated_objects_dict,api_name,label_name

def replicated_objects(sf,in_upload_crma):
    api,replicated_objects_df,dummy_replicated_objects_dict,api_name,label_name = initialize_replicated_objects_variables()
    while(api is not None):
        # print("Within While")
        temp_rest_response = sf.query_more(api, True)
        temp_details = temp_rest_response['replicatedDatasets']
        temp_details_df = pd.DataFrame(temp_details)
        temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['connector']]
        temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['connector']]
        temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['connector']]
        temp_details_df['Data_Connector_label'] = [x.get('description', 0) for x in temp_details_df['connector']]
        if 'passThroughFilter' in temp_details_df.columns:
            a = 1
        else:
            temp_details_df['passThroughFilter'] = ''
        replicated_objects_df = pd.concat([replicated_objects_df,temp_details_df],axis=0)
        #  api = temp_rest_response.get('temp_rest_response',temp_rest_response['nextPageUrl'])
        key_exists = temp_rest_response.get('nextPageUrl') 
        # print("before if")
        if (key_exists is not None):
            api = temp_rest_response['nextPageUrl']
            # print(api , "inside if)")
        else:
            api = key_exists
            # print("iside else",api)
    #columns = ['Data_Connector_id','Data_Connector_name','Data_Connector_label','id','label','name','replicationDataflowId','rowLevelSharing', 'sourceObjectName','status','type','url','passThroughFilter']
    columns = ['Data_Connector_id','Data_Connector_name','Data_Connector_label','id','label','name','replicationDataflowId', 'sourceObjectName','status','type','url','passThroughFilter']
    CRMA_replicated_objects_df = replicated_objects_df[columns]
    #if (in_upload_crma == 'Y'):
    #    upload_to_crma(sf,CRMA_replicated_objects_df,api_name,label_name)
    return CRMA_replicated_objects_df

def initialize_replicated_fields_variables():
    api = "/services/data/v57.0/wave/replicateddatasets"
    replicated_datasets_all_fields_df = pd.DataFrame()
    replicated_dataset_CRMA_fields_df = pd.DataFrame()
    dummy_replicated_fields_dict = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    rep_api_name = 'CRMA_Data_connector_replicated_objects_fields'
    rep_label_name = 'CRMA Data connector replicated objects fields'
    all_api_name = 'CRMA_Data_connector_all_objects_fields'
    all_label_name = 'CRMA Data connector all objects fields'   
    return api,replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df,dummy_replicated_fields_dict,rep_api_name,rep_label_name,all_api_name,all_label_name

def replicated_fields(sf,in_replicated_objects_df,in_upload_crma):
    api,replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df,dummy_replicated_fields_dict,rep_api_name,rep_label_name,all_api_name,all_label_name = initialize_replicated_fields_variables()
    replicated_objects_df = in_replicated_objects_df
    #source_fields_list = ['Data_Connector_id','Data_Connector_name','Data_Connector_label','id','label','name','replicationDataflowId','rowLevelSharing','sourceObjectName','status','type','url','passThroughFilter']
    #Target_fields_list = ['Data_Connector_id','Data_Connector_name','Data_Connector_label','object_id','object_label','object_name','replicationDataflowId','rowLevelSharing','sourceObjectName','status','type','url','passThroughFilter']
    source_fields_list = ['Data_Connector_id','Data_Connector_name','Data_Connector_label','id','label','name','replicationDataflowId','sourceObjectName','status','type','url','passThroughFilter']
    Target_fields_list = ['Data_Connector_id','Data_Connector_name','Data_Connector_label','object_id','object_label','object_name','replicationDataflowId','sourceObjectName','status','type','url','passThroughFilter']
    # replicated_objects_id = replicated_objects_df['id']
    for index, row in replicated_objects_df.iterrows():
        connector_api = api+"/"+row['id']+"/fields?sort=Mru&pageSize=200"
        #print(row['id'])
        while(connector_api is not None):
            # print("At beginning of", connector_api)
            temp_rest_response = sf.query_more(connector_api, True)
            temp_details = temp_rest_response['fields']
            temp_details_df = pd.DataFrame(temp_details)
            # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['dataConnector']]
            temp_details_df['api'] = connector_api
            temp_details_df[Target_fields_list] = row[source_fields_list]
            # temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
            # temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
            # temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
            # # assign empty dictionary else the process fails while using the get function.
            # temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
            # temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
            replicated_datasets_all_fields_df = pd.concat([replicated_datasets_all_fields_df,temp_details_df],axis=0)
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
    #CRMA_replicated_datasets_all_fields_df = replicated_datasets_all_fields_df[['Data_Connector_id','Data_Connector_name','Data_Connector_label','object_id','object_name','rowLevelSharing','sourceObjectName','status','type','url','passThroughFilter','replicationDataflowId','name','label','fieldType','multiValue','precision','skipped','defaultValue','format','api','scale','multiValueSeparator']]
    CRMA_replicated_datasets_all_fields_df = replicated_datasets_all_fields_df[['Data_Connector_id','Data_Connector_name','Data_Connector_label','object_id','object_name','sourceObjectName','status','type','url','passThroughFilter','replicationDataflowId','name','label','fieldType','multiValue','precision','skipped','defaultValue','format','api','scale']]
    replicated_dataset_CRMA_fields_df = CRMA_replicated_datasets_all_fields_df[CRMA_replicated_datasets_all_fields_df['skipped'] == False]
    #if (in_upload_crma == 'Y'):
    #    upload_to_crma(sf,CRMA_replicated_datasets_all_fields_df,all_api_name,all_label_name)
    #    upload_to_crma(sf,replicated_dataset_CRMA_fields_df,rep_api_name,rep_label_name)
    return CRMA_replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df

def load_object_field_details(sf,in_upload_crma,in_include_connector_field_analysis):
    dataset_connectors_df = dataset_connectors(sf,in_upload_crma)
    api,data_connector_objects_df,dummy_connector_objects_dict,api_name,label_name = initialize_data_connector_objects_variables()
    CRMA_data_connector_objects_fields_df = data_connector_objects_df
    CRMA_replicated_datasets_all_fields_df = data_connector_objects_df
    replicated_dataset_CRMA_fields_df = data_connector_objects_df
    print("Data Connector Objects Start Time", datetime.now().strftime("%H:%M:%S"))
    CRMA_data_connector_objects_df_raw,CRMA_data_connector_objects_df = dataset_connectors_source_objects(sf,dataset_connectors_df,in_upload_crma)
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_data_connector_objects_df,api_name,label_name)
    api,data_connector_objects_df,data_connector_objects_fields_df,dummy_connector_objects_dict,api_name,label_name = initialize_data_connector_objects_fields_variables()
    if (in_include_connector_field_analysis == 'Y'):
        print("Data Connector Objects Fields Start Time", datetime.now().strftime("%H:%M:%S"))
        CRMA_data_connector_objects_fields_df = data_connector_objects_fields(sf,CRMA_data_connector_objects_df_raw,in_upload_crma)
        if (in_upload_crma == 'Y'):
            upload_to_crma(sf,CRMA_data_connector_objects_fields_df,api_name,label_name)
    api,replicated_objects_df,dummy_replicated_objects_dict,api_name,label_name = initialize_replicated_objects_variables()
    print("Replicated Object Start Time", datetime.now().strftime("%H:%M:%S"))
    CRMA_replicated_objects_df = replicated_objects(sf,in_upload_crma)
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_replicated_objects_df,api_name,label_name)
    api,replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df,dummy_replicated_fields_dict,rep_api_name,rep_label_name,all_api_name,all_label_name = initialize_replicated_fields_variables()
    if (in_include_connector_field_analysis == 'Y'):
        print("Replicated Object Fields Start Time", datetime.now().strftime("%H:%M:%S"))
        CRMA_replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df = replicated_fields(sf,CRMA_replicated_objects_df,in_upload_crma)
        if (in_upload_crma == 'Y'):
            upload_to_crma(sf,CRMA_replicated_datasets_all_fields_df,all_api_name,all_label_name)
            upload_to_crma(sf,replicated_dataset_CRMA_fields_df,rep_api_name,rep_label_name)
    return CRMA_data_connector_objects_df_raw,CRMA_data_connector_objects_df,CRMA_data_connector_objects_fields_df,CRMA_replicated_objects_df,CRMA_replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df

    

    