from __future__ import print_function

import csv
import json
from io import StringIO

import alchemite_apiclient as client
import matplotlib.pyplot as plt
from alchemite_apiclient.extensions import (Configuration, await_job,
                                            await_trained)

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

#### Configuration ####
# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Provide path to the dataset to train a model from
dataset_file = "steels.csv"
optimize_args = "optimize_args_steel.json"
suggest_args = "suggest_additional_args_steel.json"

# Define names for the dataset and model (they do not have to be unique)
dataset_name = "steels"
model_name = "steels"
#######################

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})")
print("------------------------------------------")

############################################################################
### Upload dataset with POST /datasets
############################################################################

with open(dataset_file, "r", encoding="UTF-8") as file:
    data = file.read()
    reader = csv.reader(StringIO(data), delimiter=",")
    rows = [row for row in reader]
    row_count = len(rows) - 1
    column_headers = rows[0][1:]
descriptor_columns = [0] * len(column_headers)

dataset = {
    "name": dataset_name,
    "row_count": row_count,
    "column_headers": column_headers,
    "descriptor_columns": descriptor_columns,
    "data": data,
}
dataset_id = api_datasets.datasets_post(dataset=dataset)
print("Uploaded dataset:", dataset_id)

############################################################################
### Train model on dataset
############################################################################

model = {
    "name": model_name,
    "training_method": "alchemite",  # Must always be 'alchemite' right now
    "training_dataset_id": dataset_id,  # The ID of the dataset to train the model pn
}
model_id = api_models.models_post(model=model)
print("Created model record ID:", model_id)

# Start training the model using default hyperparameters and no validation
response = api_models.models_id_train_put(
    model_id, train_request={}
)
print("Train response:", response)

# Wait until the model has finished training
model = await_trained(lambda: api_models.models_id_get(model_id))

############################################################################
### Make a suggest additional request
############################################################################
print("\n--- Suggest-additional ---")

# Get suggest additional input arguments
with open(suggest_args, encoding="UTF-8") as f:
    suggest_additional_args = json.load(f)

# Send suggest_additional request
suggest_additional_job_id = api_models.models_id_suggest_additional_post(
    model_id, **suggest_additional_args
)
print("suggest_additional job ID:", suggest_additional_job_id)

# Wait until the suggest_additional job has finished
def get_suggest_additional_job_metadata():
    return api_models.models_id_suggest_additional_job_id_get(
        model_id, job_id=suggest_additional_job_id
    )


suggest_additional_job = await_job(get_suggest_additional_job_metadata)

############################################################################
### Make an optimize request
############################################################################
print("\n--- Optimize ---")

# Get optimize input arguments
with open(optimize_args, encoding="UTF-8") as f:
    optimize_args = json.load(f)

# Send optimize request
optimize_job_id = api_models.models_id_optimize_post(model_id, **optimize_args)
print("Optimize job ID:", optimize_job_id)

# Wait until the optimize job has finished
def get_optimize_job_metadata():
    return api_models.models_id_optimize_job_id_get(
        model_id, job_id=optimize_job_id
    )


optimize_job = await_job(get_optimize_job_metadata)

############################################################################
### Reduce the dataset down to a visualisable amount of dimensions
############################################################################
print("\n--- Dimensionality Reduduction ---\n")

reduction_data_types = ["dataset", "optimize", "suggest-additional"]
colours = ["black", "green", "gold"]

for reduction_data_type, colour in zip(reduction_data_types, colours):
    # Build dimensionality reduction request
    print(f"Reducing using {reduction_data_type}...")
    dimensionality_reduction_request = {
        "reductionData": {
            "modelID": model_id,
            "reductionDataType": reduction_data_type,
            "columnType": "all columns",
        },
        "reductionMethod": {
            "method": "UMAP",
            "dimensions": 2,
            "numNeighbours": 5,
            "minimumDistance": 0.5,
        },
    }
    dimensionality_reduction_response = (
        api_datasets.datasets_id_dimensionality_reduction_put(
            dataset_id,
            dimensionality_reduction_request=dimensionality_reduction_request,
        )
    )
    # Plot the points
    plot_points = dimensionality_reduction_response.reduction_coordinates
    x = plot_points["x"]
    y = plot_points["y"]
    metadata = dimensionality_reduction_response.reduction_metadata
    plt.scatter(x, y, color=colour)

plt.show()
