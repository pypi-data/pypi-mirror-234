# StandaloneRuleTreeSpec

Definition of a StandaloneRuleTree. The spec contains a tree, which recursively defines a tree of rules. Name is used to help with human identificaction of the rule, but is not necessary. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | [**StandaloneRuleName**](StandaloneRuleName.md) |  | 
**tree** | [**StandaloneRuleTreeNode**](StandaloneRuleTreeNode.md) |  | 
**org_id** | **str** | Unique identifier | 
**description** | **str** | A description of the purpose of the StandaloneRuleTree. Use this to provide more context for why the rule exists, any complexities or decisions related to it, etc.  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


