import csv
import os
from io import StringIO

from util import (
    assert_dataset_response,
    assert_impute_response,
    assert_model_response,
)

import alchemite_apiclient as client
from alchemite_apiclient.extensions import await_trained


def test_vector(set_insecure_transport, api_models, api_datasets, example_dir):
    # Provide path to the dataset to train a model from
    vector_dataset_path = os.path.join(example_dir, "vector.csv")

    # Define names for the dataset and model
    dataset_name = "vector"
    model_name = "vector"
    vector_pairs = [["z", "t"]]

    with open(vector_dataset_path, "r", encoding="UTF-8") as file:
        data = file.read()
        reader = csv.reader(StringIO(data), delimiter=",")
        rows = [row for row in reader]
        row_count = len(rows) - 1
        column_headers = rows[0][1:]

    dataset = {
        "name": dataset_name,
        "row_count": row_count,  # Number of rows (not including column headers)
        "column_headers": column_headers,
        # No descriptors in this dataset so list of zeros
        "descriptor_columns": [0] * len(column_headers),
        "data": data,
        "vector_pairs": vector_pairs,
    }
    dataset_id = api_datasets.datasets_post(dataset=dataset)

    dataset_response = api_datasets.datasets_id_get(dataset_id)
    assert_dataset_response(
        dataset_response,
        dataset_name,
        column_headers,
        row_count,
        vector_pairs=vector_pairs,
    )

    # Create a model from this dataset
    model = {
        "name": model_name,
        "training_method": "alchemite",
        "training_dataset_id": dataset_id,
    }
    model_id = api_models.models_post(model=model)

    # Start training the model
    api_models.models_id_train_put(model_id, train_request={})
    await_trained(lambda: api_models.models_id_get(model_id))
    model_response = api_models.models_id_get(model_id)

    assert_model_response(
        model_response,
        model_name,
        dataset_id,
        column_headers,
    )

    # Impute the training dataset and write the output to a file
    impute_request = client.ImputeRequest(
        dataset_id=dataset_id,
        return_row_headers=True,
        return_column_headers=True,
    )
    impute_response = api_models.models_id_impute_put(
        model_id, impute_request=impute_request
    )
    assert_impute_response(impute_response, column_headers, True)
