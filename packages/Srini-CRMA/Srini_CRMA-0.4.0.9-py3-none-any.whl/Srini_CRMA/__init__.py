from Srini_CRMA.dataset_metadata import dataset_metadata
from Srini_CRMA.data_connectors import dataset_connectors
from Srini_CRMA.dashboard import dashboard_metadata
from Srini_CRMA.Limits import analytics_limits_metadata
from Srini_CRMA.object_fields import load_object_field_details
from Srini_CRMA.object_fields import dataset_connectors_source_objects
from Srini_CRMA.object_fields import data_connector_objects_fields
from Srini_CRMA.object_fields import replicated_objects
from Srini_CRMA.object_fields import replicated_fields
from Srini_CRMA.dataflow import dataflow_details
from Srini_CRMA.dataflow import dataflow_execution_details
from Srini_CRMA.dataflow import dataflow_nodes_execution
from Srini_CRMA.dataflow import load_dataflow_details
from Srini_CRMA.dataflow import load_dataflow_details
from Srini_CRMA.Folders import folder_details
from Srini_CRMA.dataflow_analysis import dataflow_analysis
from Srini_CRMA.dataset_fields import dataset_fields
from Srini_CRMA.upload_to_crma import upload_to_crma
from Srini_CRMA.assign_sf_login import assign_sf_login
from Srini_CRMA.Recipe import recipe_details
from Srini_CRMA.recipe_analysis import recipe_analysis
from datetime import datetime


def upload_all_crma_metadata(sf,in_upload_crma ,in_include_connector_field_analysis ,in_include_df_field_analysis ,in_include_recipe_field_analysis,in_datflow_list = None,in_recipe_list = None,):
    retrival_start_time = datetime.now().strftime("%H:%M:%S")
    print("Dataset Retrival Start Time", datetime.now().strftime("%H:%M:%S"))
    dataset_df = dataset_metadata(sf,in_upload_crma)
    print("Dataset Connector Retrival Start Time", datetime.now().strftime("%H:%M:%S"))
    data_connector_df = dataset_connectors(sf,in_upload_crma)
    print("Dashboard Start Time", datetime.now().strftime("%H:%M:%S"))
    dashboard_df = dashboard_metadata(sf,in_upload_crma)
    print("Analytics Limits Start Time", datetime.now().strftime("%H:%M:%S"))
    analytics_limits_df = analytics_limits_metadata(sf,in_upload_crma)
    print("Connector Related details Start Time", datetime.now().strftime("%H:%M:%S"))
    data_connector_objects_df_raw,data_connector_objects_df,data_connector_objects_fields_df,replicated_objects_df,replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df = load_object_field_details(sf,in_upload_crma,in_include_connector_field_analysis)
    print("Dataflow & Execution Related details Start Time", datetime.now().strftime("%H:%M:%S"))
    dataflow_df,dataflow_execution_df,dataflow_nodes_execution_df = load_dataflow_details(sf,in_upload_crma)
    print("Folders start Time", datetime.now().strftime("%H:%M:%S"))
    folders_df = folder_details(sf,in_upload_crma)
    print("Dataflow & Source Field Analysis Start time", datetime.now().strftime("%H:%M:%S"))
    dataflow_analysis_df,dataflow_source_objects_df,dataflow_target_datasets_df,dataflow_source_fields_df = dataflow_analysis(sf,dataflow_df,in_upload_crma,in_include_df_field_analysis=in_include_df_field_analysis,in_datflow_list=in_datflow_list)
    print("Dataflow target Dataset Fields Analysis Start time", datetime.now().strftime("%H:%M:%S"))
    dataset_date_df,dataset_dimension_df,dataset_measures_df,dataset_fields_df = dataset_fields(sf,dataflow_target_datasets_df,dataset_df,in_upload_crma) 
    print("Folder Start time", datetime.now().strftime("%H:%M:%S"))
    recipe_df = recipe_details(sf,'N')
    print("Folder End time", datetime.now().strftime("%H:%M:%S"))
    CRMA_final_recipe_analysis_df,recipe_source_objects_df,recipe_target_datasets_df,recipe_source_fields_df = recipe_analysis(sf,recipe_df,in_upload_crma = in_upload_crma,in_recipe_list=in_recipe_list,in_include_recipe_field_analysis = in_include_recipe_field_analysis)
    print("Execution completion time", datetime.now().strftime("%H:%M:%S"))
    return dataset_df,data_connector_df,dashboard_df,analytics_limits_df,data_connector_objects_df_raw,data_connector_objects_df,data_connector_objects_fields_df,replicated_objects_df,replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df,dataflow_df,dataflow_execution_df,dataflow_nodes_execution_df,folders_df,dataflow_analysis_df,dataflow_source_objects_df,dataflow_target_datasets_df,dataflow_source_fields_df,dataset_date_df,dataset_dimension_df,dataset_measures_df,dataset_fields_df,recipe_df,CRMA_final_recipe_analysis_df,recipe_source_objects_df,recipe_target_datasets_df,recipe_source_fields_df
    