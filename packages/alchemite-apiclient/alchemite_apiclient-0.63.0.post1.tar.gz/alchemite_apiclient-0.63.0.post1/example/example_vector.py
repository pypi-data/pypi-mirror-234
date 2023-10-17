from __future__ import print_function

import csv
from io import StringIO

import matplotlib.pyplot as plt
import pandas as pd

import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration, await_trained

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))
api_datasets = client.DatasetsApi(client.ApiClient(configuration))

### Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

dataset_file = "vector.csv"
dataset_name = "vector"
model_name = "vector"
vector_pairs = [["z", "t"]]
output_impute_file = "output_impute_vector.csv"

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})")
print("------------------------------------------")

############################################################################
### Upload a dataset
############################################################################
with open(dataset_file, "r", encoding="UTF-8") as file:
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
print("dataset ID:", dataset_id)

############################################################################
### Get the metadata about this dataset
############################################################################
dataset_metadata = api_datasets.datasets_id_get(dataset_id)
print("\n--- dataset metadata ---")
print(dataset_metadata)

############################################################################
### Create a model from this dataset
############################################################################
# POST the model
model = {
    "name": model_name,
    "training_method": "alchemite",
    "training_dataset_id": dataset_id,
}
model_id = api_models.models_post(model=model)
print("model ID:", model_id)

############################################################################
### Start training the model
############################################################################
# No hyperparameter optimisation, therefore default hyperparameters used
response = api_models.models_id_train_put(model_id, train_request={})
print(response)
model = await_trained(lambda: api_models.models_id_get(model_id))

############################################################################
### Get the model metadata
############################################################################
model = api_models.models_id_get(model_id)
print("\n--- model metadata ---")
print(model)

training_column_headers = model.training_column_headers

############################################################################
### Print hyperparameters
############################################################################
print("\n--- Hyperparameters ---")
print(model.training_hyperparameters)

############################################################################
### Impute the training dataset and write the output to a file
############################################################################
impute_request = client.ImputeRequest(
    # We can provide the ID of a dataset to be imputed, rather than
    # uploading the dataset itself.
    dataset_id=dataset_id,
    # Set return_row_headers=True so that the first column of the returned
    # CSV with imputed data are actually row headers.
    return_row_headers=True,
    return_column_headers=True,
)
response = api_models.models_id_impute_put(
    model_id, impute_request=impute_request
)
with open(output_impute_file, "w", encoding="UTF-8") as f:
    f.write(response)

############################################################################
### Use imputed file for plotting
############################################################################

imputed_data = pd.read_csv(output_impute_file, index_col=0)

fig = plt.figure()
ax = plt.axes(projection="3d")

x_col = "x"
y_col = "t"
z_col = "z"

for x, y, z in zip(
    imputed_data[x_col], imputed_data[y_col], imputed_data[z_col]
):
    max_length = max([len(str(i).split(";")) for i in [x, y, z]])
    if isinstance(x, str):
        x = [float(i) if len(i) != 0 else 0 for i in x.split(";")]
        assert len(x) == max_length
    else:
        x = [x] * max_length
    if isinstance(y, str):
        y = [float(i) if len(i) != 0 else 0 for i in y.split(";")]
        assert len(y) == max_length
    else:
        y = [y] * max_length
    if isinstance(z, str):
        z = [float(i) if len(i) != 0 else 0 for i in z.split(";")]
        assert len(z) == max_length
    else:
        z = [z] * max_length

    ax.scatter3D(x, y, z)
    ax.plot3D(x, y, z)

ax.set_xlabel(x_col)
ax.set_ylabel(y_col)
ax.set_zlabel(z_col)
plt.title("Example Vector Plot")
plt.show()
