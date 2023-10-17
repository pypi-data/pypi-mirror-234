# DatasetChunk

Metadata for a chunk of an upload

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**chunk_number** | **int** |  | 
**row_count** | **int** | The number of rows in the chunk array, not including column headers. | 
**column_count** | **int** | The number of columns in the chunk array, not including row headers. | 
**created_at** | **int** | The Unix Timestamp in seconds when PUT /datasets/{id}/chunks/{chunk_number} was called. If &#x60;0&#x60; (Unix system time zero) then creation timestamp unavailable. This can happen for older dataset chunks.  | [optional] [readonly] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


