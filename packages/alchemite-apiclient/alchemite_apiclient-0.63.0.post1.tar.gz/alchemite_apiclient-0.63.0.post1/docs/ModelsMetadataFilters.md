# ModelsMetadataFilters

Filter models based on model attributes. Note that currently each filter is AND'ed. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the model. Will return models with names containing a subset of this value | [optional] 
**status** | [**ModelStatus**](ModelStatus.md) |  | [optional] 
**validation_metric** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**validation_method** | [**ModelValidationMethods**](ModelValidationMethods.md) |  | [optional] 
**virtual_training** | **bool** | Whether the model underwent virtual training or not | [optional] 
**virtual_experiment_validation** | **bool** | Whether the model underwent virtual experiment validation or not | [optional] 
**training_completion_time** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**training_method_version** | **str** | Alchemite version used to train the model | [optional] 
**groups** | **[str]** | Groups the model has been shared with | [optional] 
**created_at** | [**NumericalFilter**](NumericalFilter.md) |  | [optional] 
**tags** | **[str]** | Tags that the model contains | [optional] 
**search** | **str** | Will search over all valid fields for the model and return any models that contain the provided key | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


