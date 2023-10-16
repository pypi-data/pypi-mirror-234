import pandas as pd
from Srini_CRMA.upload_to_crma import upload_to_crma
from collections import OrderedDict
from Srini_CRMA.data_connectors import dataset_connectors
from datetime import datetime

def initialize_recipe_analysis(in_recipe_df,recipe_filter_list = None):
    api = "/services/data/v57.0/wave/recipes"
    recipe_df = in_recipe_df
    recipe_analysis_df = pd.DataFrame()
    recipe_list_df = pd.DataFrame()
    recipe_list = recipe_filter_list
    # print(1)
    # dataflow_analysis_df = pd.DataFrame()
    if recipe_filter_list is not None:
        # print(dataflow_list)
        recipe_list_df = recipe_df[recipe_df['name'].isin(recipe_list)]
    #dataflow_list = ['CA','CACSL']
    #dataflow_list = ['Ecosystem','Master','']
    #dataflow_df = dataflow_df[dataflow_df['name'].isin(dataflow_list)]
    #dataflow_df = in_dataflow_df
    # print(dataflow_list_df)
    dummy_recipe_analysis_dict =  OrderedDict([
    ('id','NA'),
    ('label','NO DATASETS'),
    ('name','NO DATASETS'),
    ('url','NA')
    ])
    recipe_analysis_api_name = 'CRMA_Recipe_Analysis'
    recipe_analysis_label_name = 'CRMA Recipe Analysis'
    recipe_source_objects_api_name = 'CRMA_Recipe_Source_Objects'
    recipe_source_objects_label_name = 'CRMA Recipe Source Objects'
    recipe_target_datasets_api_name = 'CRMA_Recipe_Target_Datasets'
    recipe_target_datasets_label_name = 'CRMA Recipe Target Datasets'
    recipe_source_objects_fields_api_name = 'CRMA_Recipe_Source_Objects_Fields'
    recipe_source_objects_fields_label_name = 'CRMA Recipe Source Objects Fields'
    return api,recipe_list_df,recipe_analysis_df,dummy_recipe_analysis_dict,recipe_analysis_api_name,recipe_analysis_label_name,recipe_source_objects_api_name,recipe_source_objects_label_name,recipe_target_datasets_api_name,recipe_target_datasets_label_name,recipe_source_objects_fields_api_name,recipe_source_objects_fields_label_name


def recipe_source_objects(in_recipe_analysis_df):
    recipe_analysis_df = in_recipe_analysis_df
    filter_recs =  (recipe_analysis_df.action =='load') & (recipe_analysis_df.node_param =='dataset')
    recipe_source_objects_df = recipe_analysis_df[filter_recs][['recipe_id','recipe_name','recipe_label','node_name','value']]
    recipe_source_objects_df = recipe_source_objects_df.rename(columns={'value':'object_name'})
    recipe_source_objects_df['connection_name'] = [x.get('connectionName', 0) for x in recipe_source_objects_df['object_name']]
    recipe_source_objects_df['Object_API_Name'] = [x.get('label', 0) for x in recipe_source_objects_df['object_name']]
    recipe_source_objects_df['Object_Label_Name'] = [x.get('sourceObjectName', 0) for x in recipe_source_objects_df['object_name']]
    recipe_source_objects_df['type'] = [x.get('type', 0) for x in recipe_source_objects_df['object_name']]
    return recipe_source_objects_df


def recipe_target_datasets(in_recipe_analysis_df):
    recipe_analysis_df = in_recipe_analysis_df
    filter_recs =  (recipe_analysis_df.action =='save') & (recipe_analysis_df.node_param =='dataset')
    recipe_datasets_df = recipe_analysis_df[filter_recs][['recipe_id','recipe_name','recipe_label','node_param','node_name','value']]
    recipe_datasets_df = recipe_datasets_df.rename(columns={'value':'object_name'})
    recipe_datasets_pivot_df = recipe_datasets_df.pivot(index=['recipe_id','recipe_name','recipe_label','node_name'],columns='node_param',values='object_name').reset_index()
    recipe_datasets_pivot_df['folderName'] = [x.get('folderName', 0) for x in recipe_datasets_pivot_df['dataset']]
    recipe_datasets_pivot_df['Dataset_API_Name'] = [x.get('label', 0) for x in recipe_datasets_pivot_df['dataset']]
    recipe_datasets_pivot_df['Dataset_Label_Name'] = [x.get('name', 0) for x in recipe_datasets_pivot_df['dataset']]
    recipe_datasets_pivot_df['type'] = [x.get('type', 0) for x in recipe_datasets_pivot_df['dataset']]
    return recipe_datasets_pivot_df


def recipe_source_fields(in_recipe_analysis_df):
    recipe_analysis_df = in_recipe_analysis_df
    filter_recs =  (recipe_analysis_df.action =='load') & (recipe_analysis_df.node_param =='fields')
    temp_recipe_source_fields_df = recipe_analysis_df[filter_recs][['recipe_id','recipe_name','recipe_label','node_param','node_name','value']]
    temp_recipe_source_fields_df = temp_recipe_source_fields_df.rename(columns={'value':'object_name'})
    temp_recipe_source_fields_pivot_df = temp_recipe_source_fields_df.pivot(index=['recipe_id','recipe_name','recipe_label','node_name'],columns='node_param',values='object_name').reset_index()
    temp_recipe_source_fields_pivot_df = temp_recipe_source_fields_pivot_df.explode('fields')
    temp_recipe_source_fields_pivot_df['field_name'] = [x.get('name', 0) for x in temp_recipe_source_fields_pivot_df['fields']]
    return temp_recipe_source_fields_pivot_df



def recipe_analysis(sf,in_recipe_df,in_upload_crma,in_recipe_list = None,in_include_recipe_field_analysis = None):
    api,recipe_list_df,recipe_analysis_df,dummy_recipe_analysis_dict,recipe_analysis_api_name,recipe_analysis_label_name,recipe_source_objects_api_name,recipe_source_objects_label_name,recipe_target_datasets_api_name,recipe_target_datasets_label_name,recipe_source_objects_fields_api_name,recipe_source_objects_fields_label_name = initialize_recipe_analysis(in_recipe_df,recipe_filter_list =in_recipe_list )
    recipe_source_fields_df = recipe_analysis_df
    source_fields_list = ['id','name','label']
    Target_fields_list = ['recipe_id','recipe_name','recipe_label']
    # replicated_objects_id = replicated_objects_df['id']
    for index, row in recipe_list_df.iterrows():
        connector_api = api+"/"+row['id']+"?format=R3"
        print(connector_api)
        while(connector_api is not None):
            # print("At beginning of", row['id'])
            temp_rest_response = sf.query_more(connector_api, True)
            #print(temp_rest_response)
            temp_details = temp_rest_response['recipeDefinition']['nodes']
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

            temp_details_node_name = temp_rest_response['recipeDefinition']['ui']['nodes']
            temp_details_node_name_df = pd.DataFrame(temp_details_node_name)
            temp_details_node_name_transpose_df = temp_details_node_name_df.transpose().reset_index()
            temp_details_node_name_transpose_df = temp_details_node_name_transpose_df.rename(columns={'index':'node_ui_name'})
            temp_details_node_name_transpose_df = temp_details_node_name_transpose_df[['node_ui_name','label']]
            temp_details_node_name_transpose_df = temp_details_node_name_transpose_df.rename(columns={'label':'node_ui_label'})
            temp_details_transpose_df = pd.merge(temp_details_transpose_df,temp_details_node_name_transpose_df,left_on='node_name', right_on='node_ui_name', how='left')

            # temp_details_df['Created_by_name'] = [x.get('name', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['Created_by_id'] = [x.get('id', 0) for x in temp_details_df['createdBy']]
            # temp_details_df['folder_name'] = [x.get('name', 'NO FOLDER') for x in temp_details_df['folder']]
            # temp_details_df['folder_id'] = [x.get('id', 0) for x in temp_details_df['folder']] 
            # temp_details_df = pd.DataFrame(temp_details_df.explode('datasets'))
            # # assign empty dictionary else the process fails while using the get function.
            # temp_details_df['datasets'] = temp_details_df['datasets'].apply(lambda x: dummy_dataset_dict if x != x else x)
            # temp_details_df['dataset_name'] = [x.get('name', 'NO DATASETS') for x in temp_details_df['datasets']]   
            recipe_analysis_df = pd.concat([recipe_analysis_df,temp_details_transpose_df],axis=0)
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
    recipe_analysis_df = recipe_analysis_df[['api','recipe_id','recipe_name','recipe_label','action','node_name','parameters','node_param','value','node_ui_name','node_ui_label']]
    print("Recipe Analyis Start Time", datetime.now().strftime("%H:%M:%S"))
    CRMA_final_recipe_analysis_df = recipe_analysis_df[~recipe_analysis_df['value'].isna()]
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,CRMA_final_recipe_analysis_df,recipe_analysis_api_name,recipe_analysis_label_name)  
        # print(1)  
    print("Recipe source object Start Time", datetime.now().strftime("%H:%M:%S"))
    recipe_source_objects_df = recipe_source_objects(CRMA_final_recipe_analysis_df)
    if (in_upload_crma == 'Y'):
        upload_to_crma(sf,recipe_source_objects_df,recipe_source_objects_api_name,recipe_source_objects_label_name)
        # print(1)  
    print("Recipe target datasets Start Time", datetime.now().strftime("%H:%M:%S"))
    recipe_target_datasets_df = recipe_target_datasets(CRMA_final_recipe_analysis_df)
    if (in_upload_crma == 'Y'):
        # print(1)
        upload_to_crma(sf,recipe_target_datasets_df,recipe_target_datasets_api_name,recipe_target_datasets_label_name)   
    if (in_include_recipe_field_analysis == 'Y'):
        print("Recipe Source fields Start Time", datetime.now().strftime("%H:%M:%S"))
        recipe_source_fields_df = recipe_source_fields(CRMA_final_recipe_analysis_df)
        if (in_upload_crma == 'Y'):
            # print(1)
            upload_to_crma(sf,recipe_source_fields_df,recipe_source_objects_fields_api_name,recipe_source_objects_fields_label_name)  
    return CRMA_final_recipe_analysis_df,recipe_source_objects_df,recipe_target_datasets_df,recipe_source_fields_df
