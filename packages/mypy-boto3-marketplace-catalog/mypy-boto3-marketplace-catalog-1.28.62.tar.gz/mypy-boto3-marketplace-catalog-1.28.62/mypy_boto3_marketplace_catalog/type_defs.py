"""
Type annotations for marketplace-catalog service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_marketplace_catalog/type_defs/)

Usage::

    ```python
    from mypy_boto3_marketplace_catalog.type_defs import CancelChangeSetRequestRequestTypeDef

    data: CancelChangeSetRequestRequestTypeDef = ...
    ```
"""
import sys
from typing import Any, Dict, List, Mapping, Sequence

from .literals import ChangeStatusType, FailureCodeType, OwnershipTypeType, SortOrderType

if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "CancelChangeSetRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "ChangeSetSummaryListItemTypeDef",
    "EntityTypeDef",
    "ErrorDetailTypeDef",
    "TagTypeDef",
    "DeleteResourcePolicyRequestRequestTypeDef",
    "DescribeChangeSetRequestRequestTypeDef",
    "DescribeEntityRequestRequestTypeDef",
    "EntitySummaryTypeDef",
    "FilterTypeDef",
    "GetResourcePolicyRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "SortTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "PutResourcePolicyRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "CancelChangeSetResponseTypeDef",
    "DescribeEntityResponseTypeDef",
    "GetResourcePolicyResponseTypeDef",
    "StartChangeSetResponseTypeDef",
    "ListChangeSetsResponseTypeDef",
    "ChangeSummaryTypeDef",
    "ChangeTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "ListEntitiesResponseTypeDef",
    "ListChangeSetsRequestListChangeSetsPaginateTypeDef",
    "ListChangeSetsRequestRequestTypeDef",
    "ListEntitiesRequestListEntitiesPaginateTypeDef",
    "ListEntitiesRequestRequestTypeDef",
    "DescribeChangeSetResponseTypeDef",
    "StartChangeSetRequestRequestTypeDef",
)

CancelChangeSetRequestRequestTypeDef = TypedDict(
    "CancelChangeSetRequestRequestTypeDef",
    {
        "Catalog": str,
        "ChangeSetId": str,
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

ChangeSetSummaryListItemTypeDef = TypedDict(
    "ChangeSetSummaryListItemTypeDef",
    {
        "ChangeSetId": NotRequired[str],
        "ChangeSetArn": NotRequired[str],
        "ChangeSetName": NotRequired[str],
        "StartTime": NotRequired[str],
        "EndTime": NotRequired[str],
        "Status": NotRequired[ChangeStatusType],
        "EntityIdList": NotRequired[List[str]],
        "FailureCode": NotRequired[FailureCodeType],
    },
)

EntityTypeDef = TypedDict(
    "EntityTypeDef",
    {
        "Type": str,
        "Identifier": NotRequired[str],
    },
)

ErrorDetailTypeDef = TypedDict(
    "ErrorDetailTypeDef",
    {
        "ErrorCode": NotRequired[str],
        "ErrorMessage": NotRequired[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

DeleteResourcePolicyRequestRequestTypeDef = TypedDict(
    "DeleteResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

DescribeChangeSetRequestRequestTypeDef = TypedDict(
    "DescribeChangeSetRequestRequestTypeDef",
    {
        "Catalog": str,
        "ChangeSetId": str,
    },
)

DescribeEntityRequestRequestTypeDef = TypedDict(
    "DescribeEntityRequestRequestTypeDef",
    {
        "Catalog": str,
        "EntityId": str,
    },
)

EntitySummaryTypeDef = TypedDict(
    "EntitySummaryTypeDef",
    {
        "Name": NotRequired[str],
        "EntityType": NotRequired[str],
        "EntityId": NotRequired[str],
        "EntityArn": NotRequired[str],
        "LastModifiedDate": NotRequired[str],
        "Visibility": NotRequired[str],
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": NotRequired[str],
        "ValueList": NotRequired[Sequence[str]],
    },
)

GetResourcePolicyRequestRequestTypeDef = TypedDict(
    "GetResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)

SortTypeDef = TypedDict(
    "SortTypeDef",
    {
        "SortBy": NotRequired[str],
        "SortOrder": NotRequired[SortOrderType],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
    },
)

PutResourcePolicyRequestRequestTypeDef = TypedDict(
    "PutResourcePolicyRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Policy": str,
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

CancelChangeSetResponseTypeDef = TypedDict(
    "CancelChangeSetResponseTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeEntityResponseTypeDef = TypedDict(
    "DescribeEntityResponseTypeDef",
    {
        "EntityType": str,
        "EntityIdentifier": str,
        "EntityArn": str,
        "LastModifiedDate": str,
        "Details": str,
        "DetailsDocument": Dict[str, Any],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

GetResourcePolicyResponseTypeDef = TypedDict(
    "GetResourcePolicyResponseTypeDef",
    {
        "Policy": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartChangeSetResponseTypeDef = TypedDict(
    "StartChangeSetResponseTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChangeSetsResponseTypeDef = TypedDict(
    "ListChangeSetsResponseTypeDef",
    {
        "ChangeSetSummaryList": List[ChangeSetSummaryListItemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ChangeSummaryTypeDef = TypedDict(
    "ChangeSummaryTypeDef",
    {
        "ChangeType": NotRequired[str],
        "Entity": NotRequired[EntityTypeDef],
        "Details": NotRequired[str],
        "DetailsDocument": NotRequired[Dict[str, Any]],
        "ErrorDetailList": NotRequired[List[ErrorDetailTypeDef]],
        "ChangeName": NotRequired[str],
    },
)

ChangeTypeDef = TypedDict(
    "ChangeTypeDef",
    {
        "ChangeType": str,
        "Entity": EntityTypeDef,
        "EntityTags": NotRequired[Sequence[TagTypeDef]],
        "Details": NotRequired[str],
        "DetailsDocument": NotRequired[Mapping[str, Any]],
        "ChangeName": NotRequired[str],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "ResourceArn": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ListEntitiesResponseTypeDef = TypedDict(
    "ListEntitiesResponseTypeDef",
    {
        "EntitySummaryList": List[EntitySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ListChangeSetsRequestListChangeSetsPaginateTypeDef = TypedDict(
    "ListChangeSetsRequestListChangeSetsPaginateTypeDef",
    {
        "Catalog": str,
        "FilterList": NotRequired[Sequence[FilterTypeDef]],
        "Sort": NotRequired[SortTypeDef],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListChangeSetsRequestRequestTypeDef = TypedDict(
    "ListChangeSetsRequestRequestTypeDef",
    {
        "Catalog": str,
        "FilterList": NotRequired[Sequence[FilterTypeDef]],
        "Sort": NotRequired[SortTypeDef],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ListEntitiesRequestListEntitiesPaginateTypeDef = TypedDict(
    "ListEntitiesRequestListEntitiesPaginateTypeDef",
    {
        "Catalog": str,
        "EntityType": str,
        "FilterList": NotRequired[Sequence[FilterTypeDef]],
        "Sort": NotRequired[SortTypeDef],
        "OwnershipType": NotRequired[OwnershipTypeType],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListEntitiesRequestRequestTypeDef = TypedDict(
    "ListEntitiesRequestRequestTypeDef",
    {
        "Catalog": str,
        "EntityType": str,
        "FilterList": NotRequired[Sequence[FilterTypeDef]],
        "Sort": NotRequired[SortTypeDef],
        "NextToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "OwnershipType": NotRequired[OwnershipTypeType],
    },
)

DescribeChangeSetResponseTypeDef = TypedDict(
    "DescribeChangeSetResponseTypeDef",
    {
        "ChangeSetId": str,
        "ChangeSetArn": str,
        "ChangeSetName": str,
        "StartTime": str,
        "EndTime": str,
        "Status": ChangeStatusType,
        "FailureCode": FailureCodeType,
        "FailureDescription": str,
        "ChangeSet": List[ChangeSummaryTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartChangeSetRequestRequestTypeDef = TypedDict(
    "StartChangeSetRequestRequestTypeDef",
    {
        "Catalog": str,
        "ChangeSet": Sequence[ChangeTypeDef],
        "ChangeSetName": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "ChangeSetTags": NotRequired[Sequence[TagTypeDef]],
    },
)
