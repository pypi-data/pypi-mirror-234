# BillingSubscriptionUsageOverrideItem

Override to billing-usage job, including minimum-commit. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metric** | **str** | The stripe metric (e.g. active_users) to override | [optional] 
**min_quantity** | **int** | Usage reported is max(min_quantity, actual_quantity) This provides a committed-usage.  | [optional] 
**max_quantity** | **int** | Usage reported is min(max_quantity, actual_quantity). This provides a cap, not-to-exceed.  | [optional] 
**step_size** | **int, none_type** | If set, the usage is stepped by this amount (e.g. rounded up to a multiple of this bounder).  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


