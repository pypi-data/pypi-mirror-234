import alchemite_apiclient as client
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()
api_default = client.DefaultApi(client.ApiClient(configuration))
api_models = client.ModelsApi(client.ApiClient(configuration))

#### Configuration ####
# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# The ID of the model to export
model_id = "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
#######################

# Check we can access the API by getting the version number from GET /version
api_response = api_default.version_get()
print("------ API & Python Client Versions ------")
print(api_response)
print(f"Python client version: {client.__version__} (latest: {api_response['api_definition_version']})")
print("------------------------------------------")

### Export model
# - This zip file contains the model and its metadata.  The zip file does not
# contain the training dataset itself, although it may contain some summary
# statistics about the model's training dataset (eg. min, max, mean)
model_file = api_models.models_id_export_get(model_id)
with open("exported_model.zip", "wb") as f, model_file:
    f.write(model_file.read())


### Import model
# - If a model with the same ID already exists then a new ID will be created
# for the imported model
# - If the user importing the model is not the same user who uploaded the training
# dataset then they will not be able to access that dataset.  Therefore certain
# functions in the Platform that use the training dataset, like the Data
# Explorer won't work for them.  However, functions that just use the model,
# like the prediction and optimization pages, will work.
with open("exported_model.zip", "rb") as f:
    new_model_id = api_models.models_import_post(body=f)

# Get the metadata for the model we just imported
model_metadata = api_models.models_id_get(new_model_id)
print(model_metadata)
