import base64


def upload_to_crma(sf,in_dataframe,in_dataset_name,in_dateset_label):
    # df_bytes = in_dataframe.to_csv(index=False).encode('utf-8')
    # df_base64 = base64.b64encode(df_bytes).decode('utf-8')
    # res_header = sf.InsightsExternalData.create({
    #     'Format': 'Csv',
    #     'EdgemartAlias': in_dataset_name,
    #     'EdgemartLabel': in_dateset_label,
    #     'FileName': in_dataset_name,
    #     'Operation': 'Overwrite',
    #     'Action': 'None'
    # })
    # header_id = res_header.get('id')
    # res_data = sf.InsightsExternalDataPart.create({
    #             'DataFile': df_base64,
    #             'InsightsExternalDataId': header_id,
    #             'PartNumber': '1'
    #         })
    # res_proc = sf.InsightsExternalData.update(header_id, {
    # 'Action': 'Process'
    #     }) 
    df_bytes = in_dataframe.to_csv(index=False).encode('utf-8')
    dataset_size_mb = len(df_bytes) / (1024 * 1024)  # Convert to MB
    if dataset_size_mb <= 10:
        df_bytes = in_dataframe.to_csv(index=False).encode('utf-8')
        df_base64 = base64.b64encode(df_bytes).decode('utf-8')
        res_header = sf.InsightsExternalData.create({
            'Format': 'Csv',
            'EdgemartAlias': in_dataset_name,
            'EdgemartLabel': in_dateset_label,
            'FileName': in_dataset_name,
            'Operation': 'Overwrite',
            'Action': 'None'
        })
        header_id = res_header.get('id')
        res_data = sf.InsightsExternalDataPart.create({
                'DataFile': df_base64,
                'InsightsExternalDataId': header_id,
                'PartNumber': '1'
        })
        res_proc = sf.InsightsExternalData.update(header_id, {
            'Action': 'Process'
        }) 
    else:
        max_chunk_size_mb = 10
        num_chunks = (dataset_size_mb // max_chunk_size_mb) + 1
        chunk_size = len(in_dataframe) // num_chunks
        for i in range(num_chunks):
            chunk = in_dataframe.iloc[i * chunk_size: (i + 1) * chunk_size]
            chunk_bytes = chunk.to_csv(index=False).encode('utf-8')
            df_base64 = base64.b64encode(chunk_bytes).decode('utf-8')
            res_header = sf.InsightsExternalData.create({
            'Format': 'Csv',
            'EdgemartAlias': in_dataset_name,
            'EdgemartLabel': in_dateset_label,
            'FileName': in_dataset_name,
            'Operation': 'Overwrite',
            'Action': 'None'
            })
            header_id = res_header.get('id')
            res_data = sf.InsightsExternalDataPart.create({
                    'DataFile': df_base64,
                    'InsightsExternalDataId': header_id,
                    'PartNumber': i + 1
            })
            res_proc = sf.InsightsExternalData.update(header_id, {
                'Action': 'Process'
            })
