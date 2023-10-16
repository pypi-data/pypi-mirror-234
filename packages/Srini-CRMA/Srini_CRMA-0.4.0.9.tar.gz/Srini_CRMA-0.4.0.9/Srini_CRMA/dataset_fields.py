import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from Srini_CRMA.data_connectors import dataset_connectors

def initialize_dataset_fields():
    api = "/services/data/v57.0/wave/datasets"
    datasets_fields_df = pd.DataFrame()
    date_df = pd.DataFrame()
    dimension_df = pd.DataFrame()
    measures_df = pd.DataFrame()
    # carma_dataflow_list = ['CARMA','CARMA_CSL']
    # carma_dataflow_df = dataflow_df[dataflow_df['name'].isin(carma_dataflow_list)]
    dummy_datasets_fields_df = OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    dataset_fields_api_name = 'CRMA_DF_Dataset_Fields'
    dataset_fields_label_name = 'CRMA DF Dataset Fields'
    dataset_date_fields_api_name = 'CRMA_DF_Date_Fields'
    dataset_date_fields_label_name = 'CRMA DF Date Fields'
    dataset_dimension_fields_api_name = 'CRMA_DF_Dimension_Fields'
    dataset_dimension_fields_label_name = 'CRMA DF Dimension Fields'
    dataset_measure_fields_api_name = 'CRMA_DF_Measure_Fields'
    dataset_measure_fields_label_name = 'CRMA DF Measure Fields'
    return api,datasets_fields_df,date_df,dimension_df,measures_df,dummy_datasets_fields_df,dataset_fields_api_name,dataset_fields_label_name,dataset_date_fields_api_name,dataset_date_fields_label_name,dataset_dimension_fields_api_name,dataset_dimension_fields_label_name,dataset_measure_fields_api_name,dataset_measure_fields_label_name

def dataset_fields(sf,in_dataflow_target_datasets_df,in_dataset_df,in_upload_crma):
    api,datasets_fields_df,date_df,dimension_df,measures_df,dummy_datasets_fields_df,dataset_fields_api_name,dataset_fields_label_name,dataset_date_fields_api_name,dataset_date_fields_label_name,dataset_dimension_fields_api_name,dataset_dimension_fields_label_name,dataset_measure_fields_api_name,dataset_measure_fields_label_name = initialize_dataset_fields()
    dataflow_target_datasets_df = in_dataflow_target_datasets_df
    dataset_df = in_dataset_df
    # print('here')
    dataflow_target_datasets_df = dataflow_target_datasets_df.merge(dataset_df[['id','name','currentVersionId']],left_on='alias' ,right_on='name',how = 'left',suffixes=('', '_dataset'))
    source_fields_list = ['id','name','currentVersionId']
    Target_fields_list = ['dataset_id','dataset_name','dataset_currentVersionId']
    # replicated_objects_id = replicated_objects_df['id']
    for index, row in dataflow_target_datasets_df.iterrows():
        # "/services/data/v57.0/wave/datasets/0Fbt0000000I4ovCAC/versions/0FcBZ000000AE3J0AW/xmds/system"
        # print(api)
        # print(row['id'])
        # print(row['currentVersionId'])
        connector_api = api+"/"+row['id']+"/versions/"+row['currentVersionId']+"/xmds/system?sort=Mru&pageSize=200"
        #print(row['id']+"/"+row['currentVersionId'])
        while(connector_api is not None):
            # print("At beginning of", connector_api)
            temp_rest_response = sf.query_more(connector_api, True)
            temp_details_dates = temp_rest_response['dates']
            temp_details_dimensions = temp_rest_response['dimensions']
            temp_details_measures = temp_rest_response['measures']
            temp_details_dates_df = pd.DataFrame(temp_details_dates)
            temp_details_dimensions_df = pd.DataFrame(temp_details_dimensions)
            temp_details_measures_df = pd.DataFrame(temp_details_measures)
            # temp_df = pd.DataFrame(temp_rest_response)
            # print(temp_df)
            # temp_details_df = pd.DataFrame(list(temp_df['nodes']))
            # print("here 3 ")
            temp_details_dates_df['field_type'] = "Date"
            temp_details_dimensions_df['field_type'] = "Dimension"
            temp_details_measures_df['field_type'] = "Measures"
            temp_details_dates_df['xmd_type'] = "system"
            temp_details_dimensions_df['xmd_type'] = "system"
            temp_details_measures_df['xmd_type'] = "system"
            temp_details_dates_df[Target_fields_list] = row[source_fields_list]
            temp_details_dimensions_df[Target_fields_list] = row[source_fields_list]
            temp_details_measures_df[Target_fields_list] = row[source_fields_list]
            # temp_details_df['Data_Connector_id'] = [x.get('id', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_name'] = [x.get('name', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['Data_Connector_label'] = [x.get('label', 0) for x in temp_details_df['dataConnector']]
            # temp_details_df['api'] = connector_api
            # print(row['jobType'])
            # temp_details_df[Target_fields_list] = row[source_fields_list]
            # temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
            # temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
            # temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
            # # assign empty dictionary else the process fails while using the get function.
            # temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
            # temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
            # datasets_fields_df['dataset_name'] = row['label']
            # datasets_fields_df = pd.concat([datasets_fields_df,temp_details_dates_df,temp_details_dimensions_df,temp_details_measures_df],axis=0)
            # print('COncat 1')
            date_df = pd.concat([date_df,temp_details_dates_df],axis=0)
            # print('COncat 2')
            dimension_df = pd.concat([dimension_df,temp_details_dimensions_df],axis=0)
            # print('COncat 3')
            measures_df = pd.concat([measures_df,temp_details_measures_df],axis=0)
            # print('COncat 4')
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
    final_measures_df = measures_df[['dataset_id','dataset_name','dataset_currentVersionId','field','label','fullyQualifiedName','xmd_type','field_type','showInExplorer']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,final_measures_df,dataset_measure_fields_api_name,dataset_measure_fields_label_name)

    final_dimension_df = dimension_df[['dataset_id','dataset_name','dataset_currentVersionId','field','label','fullyQualifiedName','xmd_type','field_type','showInExplorer']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,final_dimension_df,dataset_dimension_fields_api_name,dataset_dimension_fields_label_name)

    final_date_df = date_df[['dataset_id','dataset_name','dataset_currentVersionId','alias','label','fullyQualifiedName','xmd_type','field_type','showInExplorer']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,final_date_df,dataset_date_fields_api_name,dataset_date_fields_label_name)
    
    final_dataset_fields_df = pd.concat([final_date_df,final_dimension_df,final_measures_df],axis=0).sort_values(by=['dataset_name','label'])
    # CRMA_dataflow_nodes_execution_df = dataflow_nodes_execution_df[['dataflow_execution_id','dataflow_jobType','dataflow_label','dataflow_startDate','id','label','name','nodeType','message','startDate','status','duration','input_rows_processed_count','output_rows_processed_count','output_rows_failed_count']]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,final_dataset_fields_df,dataset_fields_api_name,dataset_fields_label_name)    
    
    
    
    return final_date_df,final_dimension_df,final_measures_df,final_dataset_fields_df