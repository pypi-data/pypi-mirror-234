import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from Srini_CRMA.data_connectors import dataset_connectors
from datetime import datetime

def initialize_dataflow_analysis(in_dataflow_df,dataflow_filter_list = None):
    api = "/services/data/v57.0/wave/dataflows"
    dataflow_df = in_dataflow_df
    dataflow_analysis_df = pd.DataFrame()
    dataflow_list_df = pd.DataFrame()
    dataflow_list = dataflow_filter_list
    # print(1)
    # dataflow_analysis_df = pd.DataFrame()
    if dataflow_filter_list is not None:
        # print(dataflow_list)
        dataflow_list_df = dataflow_df[dataflow_df['name'].isin(dataflow_list)]
    #dataflow_list = ['CA','CACSL']
    #dataflow_list = ['Ecosystem','Master','']
    #dataflow_df = dataflow_df[dataflow_df['name'].isin(dataflow_list)]
    #dataflow_df = in_dataflow_df
    # print(dataflow_list_df)
    dummy_dataflow_analysis_dict =  OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    df_analysis_api_name = 'CRMA_Dataflow_Analysis'
    df_analysis_label_name = 'CRMA Dataflow Analysis'
    dataflow_source_objects_api_name = 'CRMA_Dataflow_Source_Objects'
    dataflow_source_objects_label_name = 'CRMA Dataflow Source Objects'
    dataflow_target_datasets_api_name = 'CRMA_Dataflow_Target_Datasets'
    dataflow_target_datasets_label_name = 'CRMA Dataflow Target Datasets'
    dataflow_source_objects_fields_api_name = 'CRMA_Dataflow_Source_Objects_Fields'
    dataflow_source_objects_fields_label_name = 'CRMA Dataflow Source Objects Fields'
    return api,dataflow_list_df,dataflow_analysis_df,dummy_dataflow_analysis_dict,df_analysis_api_name,df_analysis_label_name,dataflow_source_objects_api_name,dataflow_source_objects_label_name,dataflow_target_datasets_api_name,dataflow_target_datasets_label_name,dataflow_source_objects_fields_api_name,dataflow_source_objects_fields_label_name

def dataflow_source_objects(in_dataflow_analysis_df):
    dataflow_analysis_df = in_dataflow_analysis_df
    filter_recs =  (dataflow_analysis_df.action =='sfdcDigest') & (dataflow_analysis_df.node_param =='object')
    dataflow_source_objects_df = dataflow_analysis_df[filter_recs][['dataflow_id','dataflow_name','dataflow_label','node_name','value']]
    dataflow_source_objects_df = dataflow_source_objects_df.rename(columns={'value':'object_name'})
    return dataflow_source_objects_df


def dataflow_target_datasets(in_dataflow_analysis_df):
    dataflow_analysis_df = in_dataflow_analysis_df
    filter_recs =  (dataflow_analysis_df.action =='sfdcRegister') & (dataflow_analysis_df.node_param.isin(['alias','name']))
    dataflow_datasets_df = dataflow_analysis_df[filter_recs][['dataflow_id','dataflow_name','dataflow_label','node_param','node_name','value']]
    dataflow_datasets_df = dataflow_datasets_df.rename(columns={'value':'object_name'})
    dataflow_datasets_pivot_df = dataflow_datasets_df.pivot(index=['dataflow_id','dataflow_name','dataflow_label','node_name'],columns='node_param',values='object_name').reset_index()
    return dataflow_datasets_pivot_df


def dataflow_source_fields(in_dataflow_analysis_df):
    dataflow_analysis_df = in_dataflow_analysis_df
    filter_recs =  (dataflow_analysis_df.action =='sfdcDigest') & (dataflow_analysis_df.node_param.isin(['object','fields']))
    temp_dataflow_source_fields_df = dataflow_analysis_df[filter_recs][['dataflow_id','dataflow_name','dataflow_label','node_param','node_name','value']]
    temp_dataflow_source_fields_df = temp_dataflow_source_fields_df.rename(columns={'value':'object_name'})
    temp_dataflow_source_fields_pivot_df = temp_dataflow_source_fields_df.pivot(index=['dataflow_id','dataflow_name','dataflow_label','node_name'],columns='node_param',values='object_name').reset_index()
    temp_dataflow_source_fields_pivot_df = temp_dataflow_source_fields_pivot_df.explode('fields')
    temp_dataflow_source_fields_pivot_df['field_name'] = [x.get('name', 0) for x in temp_dataflow_source_fields_pivot_df['fields']]
    return temp_dataflow_source_fields_pivot_df


def dataflow_analysis(sf,in_dataflow_df,in_upload_crma,in_datflow_list = None,in_include_df_field_analysis = None):
    api,dataflow_list_df,dataflow_analysis_df,dummy_dataflow_analysis_dict,df_analysis_api_name,df_analysis_label_name,dataflow_source_objects_api_name,dataflow_source_objects_label_name,dataflow_target_datasets_api_name,dataflow_target_datasets_label_name,dataflow_source_objects_fields_api_name,dataflow_source_objects_fields_label_name = initialize_dataflow_analysis(in_dataflow_df,dataflow_filter_list =in_datflow_list )
    dataflow_source_fields_df = dataflow_analysis_df
    source_fields_list = ['id','name','label']
    Target_fields_list = ['dataflow_id','dataflow_name','dataflow_label']
    # replicated_objects_id = replicated_objects_df['id']
    for index, row in dataflow_list_df.iterrows():
        connector_api = api+"/"+row['id']
        # print(connector_api)
        while(connector_api is not None):
            # print("At beginning of", row['id'])
            temp_rest_response = sf.query_more(connector_api, True)
            #print(temp_rest_response)
            temp_details = temp_rest_response['definition']
            temp_details_df = pd.DataFrame(temp_details)
            temp_details_transpose_df = temp_details_df.transpose().reset_index()
            temp_details_transpose_df = temp_details_transpose_df.rename(columns={'index':'node_name'})
            #print("1")
            temp_details_transpose_df = temp_details_transpose_df.join(temp_details_transpose_df.parameters.apply(pd.Series),how='left',lsuffix="_left", rsuffix="_right")
            #print("2")
            temp_details_transpose_df = pd.melt(temp_details_transpose_df, id_vars=['action','node_name', 'parameters'], var_name='node_param', value_name='value')
            #print("3")
            # print("here 3 ")
            # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['dataConnector']]
            temp_details_transpose_df['api'] = connector_api
            # print(row['jobType'])
            temp_details_transpose_df[Target_fields_list] = row[source_fields_list]
            # temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
            # temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
            # temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
            # # assign empty dictionary else the process fails while using the get function.
            # temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
            # temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
            dataflow_analysis_df = pd.concat([dataflow_analysis_df,temp_details_transpose_df],axis=0)
            #print("4")
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
    dataflow_analysis_df = dataflow_analysis_df[['api','dataflow_id','dataflow_name','dataflow_label','action','node_name','parameters','node_param','value']]
    print("Dataflow Analyis Start Time", datetime.now().strftime("%H:%M:%S"))
    CRMA_final_dataflow_analysis_df = dataflow_analysis_df[~dataflow_analysis_df['value'].isna()]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_final_dataflow_analysis_df,df_analysis_api_name,df_analysis_label_name)    
    print("Dataflow source object Start Time", datetime.now().strftime("%H:%M:%S"))
    dataflow_source_objects_df = dataflow_source_objects(CRMA_final_dataflow_analysis_df)
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,dataflow_source_objects_df,dataflow_source_objects_api_name,dataflow_source_objects_label_name)
    print("Dataflow target datasets Start Time", datetime.now().strftime("%H:%M:%S"))
    dataflow_target_datasets_df = dataflow_target_datasets(CRMA_final_dataflow_analysis_df)
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,dataflow_target_datasets_df,dataflow_target_datasets_api_name,dataflow_target_datasets_label_name)   
    if (in_include_df_field_analysis == 'Y'):
        print("Dataflow Source fields Start Time", datetime.now().strftime("%H:%M:%S"))
        dataflow_source_fields_df = dataflow_source_fields(CRMA_final_dataflow_analysis_df)
        if (in_upload_crma == 'Y'):
            upload_to_crma(sf,dataflow_source_fields_df,dataflow_source_objects_fields_api_name,dataflow_source_objects_fields_label_name)  
    return CRMA_final_dataflow_analysis_df,dataflow_source_objects_df,dataflow_target_datasets_df,dataflow_source_fields_df