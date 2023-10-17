from io import StringIO

import pandas as pd


def test_download(
    set_insecure_transport,
    api_datasets,
    steels_dataset,
):
    dataset_id_to_download = steels_dataset
    dataset_response = api_datasets.datasets_id_get(dataset_id_to_download)
    column_headers = dataset_response["column_headers"]
    row_count = dataset_response["row_count"]

    download_response = api_datasets.datasets_id_download_get(
        dataset_id_to_download, _preload_content=False
    )
    download_data = StringIO(download_response.data.decode())
    df = pd.read_csv(download_data, index_col=0)

    assert set(column_headers) == set(df.columns)
    assert row_count == len(df.index)
