# alchemite_apiclient.ModelDatasetApi

All URIs are relative to *https://alchemiteapi.intellegens.ai/v0*

Method | HTTP request | Description
------------- | ------------- | -------------
[**models_id_dataset_chunks_chunk_number_delete**](ModelDatasetApi.md#models_id_dataset_chunks_chunk_number_delete) | **DELETE** /models/{id}/dataset/chunks/{chunk_number} | Delete a chunk
[**models_id_dataset_chunks_chunk_number_get**](ModelDatasetApi.md#models_id_dataset_chunks_chunk_number_get) | **GET** /models/{id}/dataset/chunks/{chunk_number} | Get a chunk&#39;s metadata
[**models_id_dataset_chunks_chunk_number_put**](ModelDatasetApi.md#models_id_dataset_chunks_chunk_number_put) | **PUT** /models/{id}/dataset/chunks/{chunk_number} | Upload a chunk of the dataset&#39;s rows
[**models_id_dataset_chunks_delete**](ModelDatasetApi.md#models_id_dataset_chunks_delete) | **DELETE** /models/{id}/dataset/chunks | Restart uploading a dataset
[**models_id_dataset_chunks_get**](ModelDatasetApi.md#models_id_dataset_chunks_get) | **GET** /models/{id}/dataset/chunks | List the metadata for every chunk of a model&#39;s training dataset
[**models_id_dataset_delete**](ModelDatasetApi.md#models_id_dataset_delete) | **DELETE** /models/{id}/dataset | Delete a model&#39;s training dataset
[**models_id_dataset_download_get**](ModelDatasetApi.md#models_id_dataset_download_get) | **GET** /models/{id}/dataset/download | Download a dataset
[**models_id_dataset_get**](ModelDatasetApi.md#models_id_dataset_get) | **GET** /models/{id}/dataset | Get the metadata of a model&#39;s training dataset
[**models_id_dataset_post**](ModelDatasetApi.md#models_id_dataset_post) | **POST** /models/{id}/dataset | Upload or start uploading a dataset for a model to train on
[**models_id_dataset_put**](ModelDatasetApi.md#models_id_dataset_put) | **PUT** /models/{id}/dataset | Set existing dataset as model&#39;s training dataset
[**models_id_dataset_uploaded_post**](ModelDatasetApi.md#models_id_dataset_uploaded_post) | **POST** /models/{id}/dataset/uploaded | Finish uploading a dataset


# **models_id_dataset_chunks_chunk_number_delete**
> models_id_dataset_chunks_chunk_number_delete(id, chunk_number)

Delete a chunk

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    chunk_number = 1 # int | An integer which identifies this chunk of data

    # example passing only required values which don't have defaults set
    try:
        # Delete a chunk
        api_instance.models_id_dataset_chunks_chunk_number_delete(id, chunk_number)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_chunks_chunk_number_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **chunk_number** | **int**| An integer which identifies this chunk of data |

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Chunk deleted |  -  |
**400** | Invalid model ID |  -  |
**404** | The chunk number, model ID or dataset associated with this model has not been found or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_chunks_chunk_number_get**
> DatasetChunk models_id_dataset_chunks_chunk_number_get(id, chunk_number)

Get a chunk's metadata

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.dataset_chunk import DatasetChunk
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    chunk_number = 1 # int | An integer which identifies this chunk of data

    # example passing only required values which don't have defaults set
    try:
        # Get a chunk's metadata
        api_response = api_instance.models_id_dataset_chunks_chunk_number_get(id, chunk_number)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_chunks_chunk_number_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **chunk_number** | **int**| An integer which identifies this chunk of data |

### Return type

[**DatasetChunk**](DatasetChunk.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning chunk metadata |  -  |
**400** | Invalid model ID |  -  |
**404** | The chunk number, model ID or dataset associated with this model has not been found or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_chunks_chunk_number_put**
> models_id_dataset_chunks_chunk_number_put(id, chunk_number)

Upload a chunk of the dataset's rows

Upload a subset of rows from the full dataset as a CSV file with row and column headers.  If a chunk with this chunkNumber already exists then replace it.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    chunk_number = 1 # int | An integer which identifies this chunk of data
    body = open('/path/to/file', 'rb') # file_type |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Upload a chunk of the dataset's rows
        api_instance.models_id_dataset_chunks_chunk_number_put(id, chunk_number)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_chunks_chunk_number_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Upload a chunk of the dataset's rows
        api_instance.models_id_dataset_chunks_chunk_number_put(id, chunk_number, body=body)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_chunks_chunk_number_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **chunk_number** | **int**| An integer which identifies this chunk of data |
 **body** | **file_type**|  | [optional]

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: text/csv
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Chunk uploaded |  -  |
**400** | Bad request, eg. CSV malformed or missing column headers |  -  |
**404** | The chunk number, model ID or dataset associated with this model has not been found or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_chunks_delete**
> models_id_dataset_chunks_delete(id)

Restart uploading a dataset

Delete all the chunks associated with this dataset upload

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Restart uploading a dataset
        api_instance.models_id_dataset_chunks_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_chunks_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Deleted all chunks in this upload |  -  |
**400** | Invalid model ID |  -  |
**404** | The model ID or the dataset associated with this model was not found or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_chunks_get**
> [DatasetChunk] models_id_dataset_chunks_get(id)

List the metadata for every chunk of a model's training dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.dataset_chunk import DatasetChunk
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # List the metadata for every chunk of a model's training dataset
        api_response = api_instance.models_id_dataset_chunks_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_chunks_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

[**[DatasetChunk]**](DatasetChunk.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning list of chunk metadata for this upload |  -  |
**400** | Invalid model ID |  -  |
**404** | Either the model ID was not found, no dataset is associated with this model or the dataset has already been uploaded. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_delete**
> models_id_dataset_delete(id)

Delete a model's training dataset

Delete the dataset used to train this model.  If the dataset has not yet been fully uploaded this will also delete all chunks of this dataset already uploaded.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Delete a model's training dataset
        api_instance.models_id_dataset_delete(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_delete: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Dataset deleted |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found or no dataset is associated with this model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_download_get**
> file_type models_id_dataset_download_get(id)

Download a dataset

Download the dataset as a CSV file.  The columns may not be in the same order as they were given at upload.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Download a dataset
        api_response = api_instance.models_id_dataset_download_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_download_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

**file_type**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/csv, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning dataset |  -  |
**400** | Invalid model ID |  -  |
**404** | The model ID or the dataset associated with this model was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_get**
> Dataset models_id_dataset_get(id)

Get the metadata of a model's training dataset

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.dataset import Dataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Get the metadata of a model's training dataset
        api_response = api_instance.models_id_dataset_get(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_get: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

[**Dataset**](Dataset.md)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Returning dataset metadata |  -  |
**400** | Invalid model ID |  -  |
**404** | Model ID not found or no dataset is associated with this model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_post**
> str models_id_dataset_post(id)

Upload or start uploading a dataset for a model to train on

Create a dataset for the model to train on and return the dataset ID. If the 'data' parameter is not given in the JSON request body then it will be assumed that the data is to be uploaded later in chunks.  In this case the parameter 'status' in the dataset metadata will be set to 'uploading'. If data is provided, the status will be set to 'pending' while the dataset is ingested into the datastore. When finished, the final status the dataset enters will be 'uploaded'.  If the model already has a dataset associated with it then a new dataset will be created which becomes the dataset that the model will be trained against in the future (ie. the 'trainingDatasetId' parameter of the model will be the new dataset's ID).  The old dataset will not be deleted and will have the same dataset ID as before.  The new dataset must have at least all the column headers present in the dataset used to train the model originally and they must be in the same order.  Columns may be added in the new dataset to the right of the original columns.  However, given input values in these new columns will not be used when predicting missing values in old columns.  Rows may be added and/or removed in the new dataset.  If the model has already been trained then the 'status' parameter in the model metadata will be set to 'stale' indicating that it must be trained on the dataset given here before it can be used again.  > It is not possible to change a model's training dataset after the model is trained for models with trainingMethodVersion > 20230302. > For older models this functionality is deprecated and will be removed in a future release. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.dataset import Dataset
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    dataset = Dataset(
        name="name_example",
        tags=[
            "tags_example",
        ],
        notes="notes_example",
        revises_id="00112233-4455-6677-8899-aabbccddeeff",
        row_count=1,
        column_headers=["C","Ni","Si","Young's modulus","Resistivity"],
        categorical_columns=[
            CategoricalColumn(
                name="name_example",
                values=None,
            ),
        ],
        descriptor_columns=[1,1,1,0,0],
        auto_detect_complete_columns=False,
        complete_columns=[1,0,1,0,0],
        calculated_columns=[
            DatasetCalculatedColumns(
                name="name_example",
                expression=CalColExpression(),
            ),
        ],
        measurement_groups=[1,2,3,1,4],
        data=''',C,Ni,Si,Young's modulus,Resistivity
Carbon steel 1,0.105,0,0,209.9,14.4
Carbon steel 2,0.2,,0,,17
Low alloy steel,,0,0.25,206.4,22.40
''',
        vector_pairs=[["time","temperature"],["distance","strength"]],
    ) # Dataset |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Upload or start uploading a dataset for a model to train on
        api_response = api_instance.models_id_dataset_post(id)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_post: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Upload or start uploading a dataset for a model to train on
        api_response = api_instance.models_id_dataset_post(id, dataset=dataset)
        pprint(api_response)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **dataset** | [**Dataset**](Dataset.md)|  | [optional]

### Return type

**str**

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain, application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Dataset created.  Returning the dataset ID. |  -  |
**400** | Invalid model ID |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found |  -  |
**409** | Conflict due to the column headers in this dataset and the dataset used to train the model not matching |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_put**
> models_id_dataset_put(id)

Set existing dataset as model's training dataset

Sets the dataset that the model will train to an existing dataset corresponding to the given dataset ID.  If the model already has a training dataset associated with it then the old dataset will not be deleted and will have the same dataset ID as before.  The new dataset must have at least all the column headers present in the dataset used to train the model originally and they must be in the same order.  Columns may be added in the new dataset to the right of the original columns.  However, given input values in these new columns will not be used when predicting missing values in old columns.  Rows may be added and/or removed in the new dataset.  If the model has already been trained then the 'status' parameter in the model metadata will be set to 'stale' indicating that it must be trained on the dataset given here before it can be used again.  > It is not possible to change a model's training dataset after the model is trained for models with trainingMethodVersion > 20230302. > For older models this functionality is deprecated and will be removed in a future release. 

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from alchemite_apiclient.model.models_dataset_put_request import ModelsDatasetPutRequest
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.
    models_dataset_put_request = ModelsDatasetPutRequest(
        training_dataset_id="training_dataset_id_example",
    ) # ModelsDatasetPutRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Set existing dataset as model's training dataset
        api_instance.models_id_dataset_put(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_put: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Set existing dataset as model's training dataset
        api_instance.models_id_dataset_put(id, models_dataset_put_request=models_dataset_put_request)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_put: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |
 **models_dataset_put_request** | [**ModelsDatasetPutRequest**](ModelsDatasetPutRequest.md)|  | [optional]

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Training dataset assigned |  -  |
**400** | Invalid model ID |  -  |
**401** | Licence expired |  -  |
**404** | Model ID not found |  -  |
**409** | Conflict due to the column headers in this dataset and the dataset used to train the model not matching |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **models_id_dataset_uploaded_post**
> models_id_dataset_uploaded_post(id)

Finish uploading a dataset

Collate all the uploaded chunks into the final dataset.  This will set the status of the dataset to 'uploaded'.

### Example

* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):
* OAuth Authentication (oauth):

```python
import time
import alchemite_apiclient
from alchemite_apiclient.api import model_dataset_api
from alchemite_apiclient.model.error import Error
from pprint import pprint
from alchemite_apiclient.extensions import Configuration

configuration = Configuration()

# Provide path to the JSON containing your credentials
configuration.credentials = "credentials.json"

# Please see readme for details about the contents of credentials.json
# Enter a context with an instance of the API client
with alchemite_apiclient.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = model_dataset_api.ModelDatasetApi(api_client)
    id = "00112233-4455-6677-8899-aabbccddeeff" # str | Unique identifier for the model.

    # example passing only required values which don't have defaults set
    try:
        # Finish uploading a dataset
        api_instance.models_id_dataset_uploaded_post(id)
    except alchemite_apiclient.ApiException as e:
        print("Exception when calling ModelDatasetApi->models_id_dataset_uploaded_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**| Unique identifier for the model. |

### Return type

void (empty response body)

### Authorization

[oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth), [oauth](../README.md#oauth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Dataset successfully collated |  -  |
**400** | Invalid model ID |  -  |
**404** | The model ID or the dataset associated with this model was not found or the dataset has already been uploaded. |  -  |
**409** | Conflict.  This may be due to the column headers in this dataset and the dataset used to train the model not matching, the dataset dimensions not matching those specified at dataset creation or the values in two or more chunks conflicting. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

