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
from Srini_CRMA.upload_all_crma_metadata import upload_all_crma_metadata
from datetime import datetime
import pandas as pd
import os

    
def upload_all_crma_metadata(sf,in_upload_crma):
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
    data_connector_objects_df,data_connector_objects_fields_df,replicated_objects_df,replicated_datasets_all_fields_df,replicated_dataset_CRMA_fields_df = load_object_field_details(sf,in_upload_crma)
    print("Dataflow & Execution Related details Start Time", datetime.now().strftime("%H:%M:%S"))
    dataflow_df,dataflow_execution_df,dataflow_nodes_execution_df = load_dataflow_details(sf,in_upload_crma)
    print("Folders start Time", datetime.now().strftime("%H:%M:%S"))
    folder_df = folder_details(sf,in_upload_crma)
    print("Dataflow & Source Field Analysis Start time", datetime.now().strftime("%H:%M:%S"))
    dataflow_analysis_df,dataflow_source_objects_df,dataflow_target_datasets_df,dataflow_source_fields_df = dataflow_analysis(sf,dataflow_df,in_upload_crma)
    print("Dataflow target Dataset Fields Analysis Start time", datetime.now().strftime("%H:%M:%S"))
    dataset_date_df,dataset_dimension_df,dataset_measures_df,dataset_fields_df = dataset_fields(sf,dataflow_target_datasets_df,dataset_df,in_upload_crma) 
    print("Execution completion time", datetime.now().strftime("%H:%M:%S"))
    dataframes_dict = {'dataset_df': dataset_df, 'data_connector_df': data_connector_df,'dashboard_df':dashboard_df,'analytics_limits_df':analytics_limits_df,
                   'data_connector_objects_df':data_connector_objects_df,
                   'data_connector_objects_fields_df':data_connector_objects_fields_df,
                   'data_connector_objects_df_raw':data_connector_objects_df_raw,'replicated_objects_df':replicated_objects_df,'replicated_datasets_all_fields_df':replicated_datasets_all_fields_df,
                   'replicated_dataset_CRMA_fields_df':replicated_dataset_CRMA_fields_df,'dataflow_df':dataflow_df,
                   'dataflow_execution_df':dataflow_execution_df,
                   'dataflow_nodes_execution_df':dataflow_nodes_execution_df,
                   'folder_df':folder_df,
                   'dataflow_analysis_df':dataflow_analysis_df,
                   'dataflow_source_objects_df':dataflow_source_objects_df,
                   'dataflow_target_datasets_df':dataflow_target_datasets_df,
                   'dataflow_source_fields_df':dataflow_source_fields_df,
                   'dataset_date_df':dataset_date_df,
                   'dataset_dimension_df':dataset_dimension_df,
                   'dataset_measures_df':dataset_measures_df,
                   'dataset_fields_df':dataset_fields_df
                    }
    excel_file_name = 'output_file.xlsx'
    writer = pd.ExcelWriter(excel_file_name)

    # Write each dataframe to a separate sheet in the Excel file
    for sheet_name, dataframe in dataframes_dict.items():
        dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
        # The below creates separate csv files
        #file_name = sheet_name+'.csv'
        #dataframe.to_csv(file_name, sep=',')
    # Save and close the Excel writer
    current_directory = os.getcwd()
    print("Excel file saved at:", os.path.join(current_directory, excel_file_name))
    writer.save()
    writer.close()
    