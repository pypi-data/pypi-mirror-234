"""
Type annotations for fsx service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/type_defs/)

Usage::

    ```python
    from mypy_boto3_fsx.type_defs import ActiveDirectoryBackupAttributesTypeDef

    data: ActiveDirectoryBackupAttributesTypeDef = ...
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Sequence

from .literals import (
    AdministrativeActionTypeType,
    AliasLifecycleType,
    AutocommitPeriodTypeType,
    AutoImportPolicyTypeType,
    BackupLifecycleType,
    BackupTypeType,
    DataCompressionTypeType,
    DataRepositoryLifecycleType,
    DataRepositoryTaskFilterNameType,
    DataRepositoryTaskLifecycleType,
    DataRepositoryTaskTypeType,
    DiskIopsConfigurationModeType,
    DriveCacheTypeType,
    EventTypeType,
    FileCacheLifecycleType,
    FileSystemLifecycleType,
    FileSystemMaintenanceOperationType,
    FileSystemTypeType,
    FilterNameType,
    FlexCacheEndpointTypeType,
    InputOntapVolumeTypeType,
    LustreAccessAuditLogLevelType,
    LustreDeploymentTypeType,
    OntapDeploymentTypeType,
    OntapVolumeTypeType,
    OpenZFSCopyStrategyType,
    OpenZFSDataCompressionTypeType,
    OpenZFSDeploymentTypeType,
    OpenZFSQuotaTypeType,
    PrivilegedDeleteType,
    ResourceTypeType,
    RestoreOpenZFSVolumeOptionType,
    RetentionPeriodTypeType,
    SecurityStyleType,
    SnaplockTypeType,
    SnapshotFilterNameType,
    SnapshotLifecycleType,
    StatusType,
    StorageTypeType,
    StorageVirtualMachineLifecycleType,
    StorageVirtualMachineRootVolumeSecurityStyleType,
    StorageVirtualMachineSubtypeType,
    TieringPolicyNameType,
    VolumeFilterNameType,
    VolumeLifecycleType,
    VolumeTypeType,
    WindowsAccessAuditLogLevelType,
    WindowsDeploymentTypeType,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 12):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired
if sys.version_info >= (3, 12):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "ActiveDirectoryBackupAttributesTypeDef",
    "AdministrativeActionFailureDetailsTypeDef",
    "AliasTypeDef",
    "AssociateFileSystemAliasesRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "AutoExportPolicyTypeDef",
    "AutoImportPolicyTypeDef",
    "AutocommitPeriodTypeDef",
    "BackupFailureDetailsTypeDef",
    "TagTypeDef",
    "CancelDataRepositoryTaskRequestRequestTypeDef",
    "CompletionReportTypeDef",
    "FileCacheLustreMetadataConfigurationTypeDef",
    "LustreLogCreateConfigurationTypeDef",
    "LustreRootSquashConfigurationTypeDef",
    "DiskIopsConfigurationTypeDef",
    "SelfManagedActiveDirectoryConfigurationTypeDef",
    "WindowsAuditLogCreateConfigurationTypeDef",
    "TieringPolicyTypeDef",
    "CreateOpenZFSOriginSnapshotConfigurationTypeDef",
    "OpenZFSUserOrGroupQuotaTypeDef",
    "DataRepositoryFailureDetailsTypeDef",
    "DataRepositoryTaskFailureDetailsTypeDef",
    "DataRepositoryTaskFilterTypeDef",
    "DataRepositoryTaskStatusTypeDef",
    "DeleteBackupRequestRequestTypeDef",
    "DeleteDataRepositoryAssociationRequestRequestTypeDef",
    "DeleteFileCacheRequestRequestTypeDef",
    "DeleteSnapshotRequestRequestTypeDef",
    "DeleteStorageVirtualMachineRequestRequestTypeDef",
    "DeleteVolumeOpenZFSConfigurationTypeDef",
    "FilterTypeDef",
    "PaginatorConfigTypeDef",
    "DescribeFileCachesRequestRequestTypeDef",
    "DescribeFileSystemAliasesRequestRequestTypeDef",
    "DescribeFileSystemsRequestRequestTypeDef",
    "SnapshotFilterTypeDef",
    "StorageVirtualMachineFilterTypeDef",
    "VolumeFilterTypeDef",
    "DisassociateFileSystemAliasesRequestRequestTypeDef",
    "DurationSinceLastAccessTypeDef",
    "FileCacheFailureDetailsTypeDef",
    "FileCacheNFSConfigurationTypeDef",
    "LustreLogConfigurationTypeDef",
    "FileSystemEndpointTypeDef",
    "FileSystemFailureDetailsTypeDef",
    "LifecycleTransitionReasonTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "OpenZFSClientConfigurationTypeDef",
    "OpenZFSOriginSnapshotConfigurationTypeDef",
    "ReleaseFileSystemNfsV3LocksRequestRequestTypeDef",
    "RestoreVolumeFromSnapshotRequestRequestTypeDef",
    "RetentionPeriodTypeDef",
    "SelfManagedActiveDirectoryAttributesTypeDef",
    "SelfManagedActiveDirectoryConfigurationUpdatesTypeDef",
    "StartMisconfiguredStateRecoveryRequestRequestTypeDef",
    "SvmEndpointTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFileCacheLustreConfigurationTypeDef",
    "UpdateSnapshotRequestRequestTypeDef",
    "WindowsAuditLogConfigurationTypeDef",
    "AssociateFileSystemAliasesResponseTypeDef",
    "CancelDataRepositoryTaskResponseTypeDef",
    "CreateFileSystemFromBackupResponseTypeDef",
    "CreateFileSystemResponseTypeDef",
    "DeleteBackupResponseTypeDef",
    "DeleteDataRepositoryAssociationResponseTypeDef",
    "DeleteFileCacheResponseTypeDef",
    "DeleteSnapshotResponseTypeDef",
    "DeleteStorageVirtualMachineResponseTypeDef",
    "DescribeFileSystemAliasesResponseTypeDef",
    "DisassociateFileSystemAliasesResponseTypeDef",
    "ReleaseFileSystemNfsV3LocksResponseTypeDef",
    "RestoreVolumeFromSnapshotResponseTypeDef",
    "StartMisconfiguredStateRecoveryResponseTypeDef",
    "UpdateFileSystemResponseTypeDef",
    "NFSDataRepositoryConfigurationTypeDef",
    "S3DataRepositoryConfigurationTypeDef",
    "CopyBackupRequestRequestTypeDef",
    "CreateBackupRequestRequestTypeDef",
    "CreateSnapshotRequestRequestTypeDef",
    "DeleteFileSystemLustreConfigurationTypeDef",
    "DeleteFileSystemLustreResponseTypeDef",
    "DeleteFileSystemOpenZFSConfigurationTypeDef",
    "DeleteFileSystemOpenZFSResponseTypeDef",
    "DeleteFileSystemWindowsConfigurationTypeDef",
    "DeleteFileSystemWindowsResponseTypeDef",
    "DeleteVolumeOntapConfigurationTypeDef",
    "DeleteVolumeOntapResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "CreateFileCacheLustreConfigurationTypeDef",
    "CreateFileSystemLustreConfigurationTypeDef",
    "UpdateFileSystemLustreConfigurationTypeDef",
    "CreateFileSystemOntapConfigurationTypeDef",
    "OpenZFSFileSystemConfigurationTypeDef",
    "UpdateFileSystemOntapConfigurationTypeDef",
    "UpdateFileSystemOpenZFSConfigurationTypeDef",
    "CreateSvmActiveDirectoryConfigurationTypeDef",
    "CreateFileSystemWindowsConfigurationTypeDef",
    "DataRepositoryConfigurationTypeDef",
    "DescribeDataRepositoryTasksRequestRequestTypeDef",
    "DescribeBackupsRequestRequestTypeDef",
    "DescribeDataRepositoryAssociationsRequestRequestTypeDef",
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    "DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef",
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    "DescribeSnapshotsRequestRequestTypeDef",
    "DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef",
    "DescribeStorageVirtualMachinesRequestRequestTypeDef",
    "DescribeVolumesRequestDescribeVolumesPaginateTypeDef",
    "DescribeVolumesRequestRequestTypeDef",
    "ReleaseConfigurationTypeDef",
    "FileCacheDataRepositoryAssociationTypeDef",
    "FileCacheLustreConfigurationTypeDef",
    "FileSystemEndpointsTypeDef",
    "SnapshotTypeDef",
    "OpenZFSNfsExportTypeDef",
    "SnaplockRetentionPeriodTypeDef",
    "SvmActiveDirectoryConfigurationTypeDef",
    "UpdateFileSystemWindowsConfigurationTypeDef",
    "UpdateSvmActiveDirectoryConfigurationTypeDef",
    "SvmEndpointsTypeDef",
    "UpdateFileCacheRequestRequestTypeDef",
    "WindowsFileSystemConfigurationTypeDef",
    "CreateDataRepositoryAssociationRequestRequestTypeDef",
    "DataRepositoryAssociationTypeDef",
    "UpdateDataRepositoryAssociationRequestRequestTypeDef",
    "DeleteFileSystemRequestRequestTypeDef",
    "DeleteFileSystemResponseTypeDef",
    "DeleteVolumeRequestRequestTypeDef",
    "DeleteVolumeResponseTypeDef",
    "CreateStorageVirtualMachineRequestRequestTypeDef",
    "LustreFileSystemConfigurationTypeDef",
    "CreateDataRepositoryTaskRequestRequestTypeDef",
    "DataRepositoryTaskTypeDef",
    "CreateFileCacheRequestRequestTypeDef",
    "FileCacheCreatingTypeDef",
    "FileCacheTypeDef",
    "OntapFileSystemConfigurationTypeDef",
    "CreateSnapshotResponseTypeDef",
    "DescribeSnapshotsResponseTypeDef",
    "UpdateSnapshotResponseTypeDef",
    "CreateOpenZFSVolumeConfigurationTypeDef",
    "OpenZFSCreateRootVolumeConfigurationTypeDef",
    "OpenZFSVolumeConfigurationTypeDef",
    "UpdateOpenZFSVolumeConfigurationTypeDef",
    "CreateSnaplockConfigurationTypeDef",
    "SnaplockConfigurationTypeDef",
    "UpdateSnaplockConfigurationTypeDef",
    "UpdateFileSystemRequestRequestTypeDef",
    "UpdateStorageVirtualMachineRequestRequestTypeDef",
    "StorageVirtualMachineTypeDef",
    "CreateDataRepositoryAssociationResponseTypeDef",
    "DescribeDataRepositoryAssociationsResponseTypeDef",
    "UpdateDataRepositoryAssociationResponseTypeDef",
    "CreateDataRepositoryTaskResponseTypeDef",
    "DescribeDataRepositoryTasksResponseTypeDef",
    "CreateFileCacheResponseTypeDef",
    "DescribeFileCachesResponseTypeDef",
    "UpdateFileCacheResponseTypeDef",
    "FileSystemTypeDef",
    "CreateFileSystemOpenZFSConfigurationTypeDef",
    "CreateOntapVolumeConfigurationTypeDef",
    "OntapVolumeConfigurationTypeDef",
    "UpdateOntapVolumeConfigurationTypeDef",
    "CreateStorageVirtualMachineResponseTypeDef",
    "DescribeStorageVirtualMachinesResponseTypeDef",
    "UpdateStorageVirtualMachineResponseTypeDef",
    "DescribeFileSystemsResponseTypeDef",
    "CreateFileSystemFromBackupRequestRequestTypeDef",
    "CreateFileSystemRequestRequestTypeDef",
    "CreateVolumeFromBackupRequestRequestTypeDef",
    "CreateVolumeRequestRequestTypeDef",
    "VolumeTypeDef",
    "UpdateVolumeRequestRequestTypeDef",
    "AdministrativeActionTypeDef",
    "BackupTypeDef",
    "CreateVolumeFromBackupResponseTypeDef",
    "CreateVolumeResponseTypeDef",
    "DescribeVolumesResponseTypeDef",
    "UpdateVolumeResponseTypeDef",
    "CopyBackupResponseTypeDef",
    "CreateBackupResponseTypeDef",
    "DescribeBackupsResponseTypeDef",
)

ActiveDirectoryBackupAttributesTypeDef = TypedDict(
    "ActiveDirectoryBackupAttributesTypeDef",
    {
        "DomainName": NotRequired[str],
        "ActiveDirectoryId": NotRequired[str],
        "ResourceARN": NotRequired[str],
    },
)

AdministrativeActionFailureDetailsTypeDef = TypedDict(
    "AdministrativeActionFailureDetailsTypeDef",
    {
        "Message": NotRequired[str],
    },
)

AliasTypeDef = TypedDict(
    "AliasTypeDef",
    {
        "Name": NotRequired[str],
        "Lifecycle": NotRequired[AliasLifecycleType],
    },
)

AssociateFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "AssociateFileSystemAliasesRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "Aliases": Sequence[str],
        "ClientRequestToken": NotRequired[str],
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

AutoExportPolicyTypeDef = TypedDict(
    "AutoExportPolicyTypeDef",
    {
        "Events": NotRequired[Sequence[EventTypeType]],
    },
)

AutoImportPolicyTypeDef = TypedDict(
    "AutoImportPolicyTypeDef",
    {
        "Events": NotRequired[Sequence[EventTypeType]],
    },
)

AutocommitPeriodTypeDef = TypedDict(
    "AutocommitPeriodTypeDef",
    {
        "Type": AutocommitPeriodTypeType,
        "Value": NotRequired[int],
    },
)

BackupFailureDetailsTypeDef = TypedDict(
    "BackupFailureDetailsTypeDef",
    {
        "Message": NotRequired[str],
    },
)

TagTypeDef = TypedDict(
    "TagTypeDef",
    {
        "Key": str,
        "Value": str,
    },
)

CancelDataRepositoryTaskRequestRequestTypeDef = TypedDict(
    "CancelDataRepositoryTaskRequestRequestTypeDef",
    {
        "TaskId": str,
    },
)

CompletionReportTypeDef = TypedDict(
    "CompletionReportTypeDef",
    {
        "Enabled": bool,
        "Path": NotRequired[str],
        "Format": NotRequired[Literal["REPORT_CSV_20191124"]],
        "Scope": NotRequired[Literal["FAILED_FILES_ONLY"]],
    },
)

FileCacheLustreMetadataConfigurationTypeDef = TypedDict(
    "FileCacheLustreMetadataConfigurationTypeDef",
    {
        "StorageCapacity": int,
    },
)

LustreLogCreateConfigurationTypeDef = TypedDict(
    "LustreLogCreateConfigurationTypeDef",
    {
        "Level": LustreAccessAuditLogLevelType,
        "Destination": NotRequired[str],
    },
)

LustreRootSquashConfigurationTypeDef = TypedDict(
    "LustreRootSquashConfigurationTypeDef",
    {
        "RootSquash": NotRequired[str],
        "NoSquashNids": NotRequired[List[str]],
    },
)

DiskIopsConfigurationTypeDef = TypedDict(
    "DiskIopsConfigurationTypeDef",
    {
        "Mode": NotRequired[DiskIopsConfigurationModeType],
        "Iops": NotRequired[int],
    },
)

SelfManagedActiveDirectoryConfigurationTypeDef = TypedDict(
    "SelfManagedActiveDirectoryConfigurationTypeDef",
    {
        "DomainName": str,
        "UserName": str,
        "Password": str,
        "DnsIps": Sequence[str],
        "OrganizationalUnitDistinguishedName": NotRequired[str],
        "FileSystemAdministratorsGroup": NotRequired[str],
    },
)

WindowsAuditLogCreateConfigurationTypeDef = TypedDict(
    "WindowsAuditLogCreateConfigurationTypeDef",
    {
        "FileAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
        "FileShareAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
        "AuditLogDestination": NotRequired[str],
    },
)

TieringPolicyTypeDef = TypedDict(
    "TieringPolicyTypeDef",
    {
        "CoolingPeriod": NotRequired[int],
        "Name": NotRequired[TieringPolicyNameType],
    },
)

CreateOpenZFSOriginSnapshotConfigurationTypeDef = TypedDict(
    "CreateOpenZFSOriginSnapshotConfigurationTypeDef",
    {
        "SnapshotARN": str,
        "CopyStrategy": OpenZFSCopyStrategyType,
    },
)

OpenZFSUserOrGroupQuotaTypeDef = TypedDict(
    "OpenZFSUserOrGroupQuotaTypeDef",
    {
        "Type": OpenZFSQuotaTypeType,
        "Id": int,
        "StorageCapacityQuotaGiB": int,
    },
)

DataRepositoryFailureDetailsTypeDef = TypedDict(
    "DataRepositoryFailureDetailsTypeDef",
    {
        "Message": NotRequired[str],
    },
)

DataRepositoryTaskFailureDetailsTypeDef = TypedDict(
    "DataRepositoryTaskFailureDetailsTypeDef",
    {
        "Message": NotRequired[str],
    },
)

DataRepositoryTaskFilterTypeDef = TypedDict(
    "DataRepositoryTaskFilterTypeDef",
    {
        "Name": NotRequired[DataRepositoryTaskFilterNameType],
        "Values": NotRequired[Sequence[str]],
    },
)

DataRepositoryTaskStatusTypeDef = TypedDict(
    "DataRepositoryTaskStatusTypeDef",
    {
        "TotalCount": NotRequired[int],
        "SucceededCount": NotRequired[int],
        "FailedCount": NotRequired[int],
        "LastUpdatedTime": NotRequired[datetime],
        "ReleasedCapacity": NotRequired[int],
    },
)

DeleteBackupRequestRequestTypeDef = TypedDict(
    "DeleteBackupRequestRequestTypeDef",
    {
        "BackupId": str,
        "ClientRequestToken": NotRequired[str],
    },
)

DeleteDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "DeleteDataRepositoryAssociationRequestRequestTypeDef",
    {
        "AssociationId": str,
        "ClientRequestToken": NotRequired[str],
        "DeleteDataInFileSystem": NotRequired[bool],
    },
)

DeleteFileCacheRequestRequestTypeDef = TypedDict(
    "DeleteFileCacheRequestRequestTypeDef",
    {
        "FileCacheId": str,
        "ClientRequestToken": NotRequired[str],
    },
)

DeleteSnapshotRequestRequestTypeDef = TypedDict(
    "DeleteSnapshotRequestRequestTypeDef",
    {
        "SnapshotId": str,
        "ClientRequestToken": NotRequired[str],
    },
)

DeleteStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "DeleteStorageVirtualMachineRequestRequestTypeDef",
    {
        "StorageVirtualMachineId": str,
        "ClientRequestToken": NotRequired[str],
    },
)

DeleteVolumeOpenZFSConfigurationTypeDef = TypedDict(
    "DeleteVolumeOpenZFSConfigurationTypeDef",
    {
        "Options": NotRequired[Sequence[Literal["DELETE_CHILD_VOLUMES_AND_SNAPSHOTS"]]],
    },
)

FilterTypeDef = TypedDict(
    "FilterTypeDef",
    {
        "Name": NotRequired[FilterNameType],
        "Values": NotRequired[Sequence[str]],
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

DescribeFileCachesRequestRequestTypeDef = TypedDict(
    "DescribeFileCachesRequestRequestTypeDef",
    {
        "FileCacheIds": NotRequired[Sequence[str]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

DescribeFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "DescribeFileSystemAliasesRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "ClientRequestToken": NotRequired[str],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

DescribeFileSystemsRequestRequestTypeDef = TypedDict(
    "DescribeFileSystemsRequestRequestTypeDef",
    {
        "FileSystemIds": NotRequired[Sequence[str]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

SnapshotFilterTypeDef = TypedDict(
    "SnapshotFilterTypeDef",
    {
        "Name": NotRequired[SnapshotFilterNameType],
        "Values": NotRequired[Sequence[str]],
    },
)

StorageVirtualMachineFilterTypeDef = TypedDict(
    "StorageVirtualMachineFilterTypeDef",
    {
        "Name": NotRequired[Literal["file-system-id"]],
        "Values": NotRequired[Sequence[str]],
    },
)

VolumeFilterTypeDef = TypedDict(
    "VolumeFilterTypeDef",
    {
        "Name": NotRequired[VolumeFilterNameType],
        "Values": NotRequired[Sequence[str]],
    },
)

DisassociateFileSystemAliasesRequestRequestTypeDef = TypedDict(
    "DisassociateFileSystemAliasesRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "Aliases": Sequence[str],
        "ClientRequestToken": NotRequired[str],
    },
)

DurationSinceLastAccessTypeDef = TypedDict(
    "DurationSinceLastAccessTypeDef",
    {
        "Unit": NotRequired[Literal["DAYS"]],
        "Value": NotRequired[int],
    },
)

FileCacheFailureDetailsTypeDef = TypedDict(
    "FileCacheFailureDetailsTypeDef",
    {
        "Message": NotRequired[str],
    },
)

FileCacheNFSConfigurationTypeDef = TypedDict(
    "FileCacheNFSConfigurationTypeDef",
    {
        "Version": Literal["NFS3"],
        "DnsIps": NotRequired[Sequence[str]],
    },
)

LustreLogConfigurationTypeDef = TypedDict(
    "LustreLogConfigurationTypeDef",
    {
        "Level": LustreAccessAuditLogLevelType,
        "Destination": NotRequired[str],
    },
)

FileSystemEndpointTypeDef = TypedDict(
    "FileSystemEndpointTypeDef",
    {
        "DNSName": NotRequired[str],
        "IpAddresses": NotRequired[List[str]],
    },
)

FileSystemFailureDetailsTypeDef = TypedDict(
    "FileSystemFailureDetailsTypeDef",
    {
        "Message": NotRequired[str],
    },
)

LifecycleTransitionReasonTypeDef = TypedDict(
    "LifecycleTransitionReasonTypeDef",
    {
        "Message": NotRequired[str],
    },
)

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

OpenZFSClientConfigurationTypeDef = TypedDict(
    "OpenZFSClientConfigurationTypeDef",
    {
        "Clients": str,
        "Options": List[str],
    },
)

OpenZFSOriginSnapshotConfigurationTypeDef = TypedDict(
    "OpenZFSOriginSnapshotConfigurationTypeDef",
    {
        "SnapshotARN": NotRequired[str],
        "CopyStrategy": NotRequired[OpenZFSCopyStrategyType],
    },
)

ReleaseFileSystemNfsV3LocksRequestRequestTypeDef = TypedDict(
    "ReleaseFileSystemNfsV3LocksRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "ClientRequestToken": NotRequired[str],
    },
)

RestoreVolumeFromSnapshotRequestRequestTypeDef = TypedDict(
    "RestoreVolumeFromSnapshotRequestRequestTypeDef",
    {
        "VolumeId": str,
        "SnapshotId": str,
        "ClientRequestToken": NotRequired[str],
        "Options": NotRequired[Sequence[RestoreOpenZFSVolumeOptionType]],
    },
)

RetentionPeriodTypeDef = TypedDict(
    "RetentionPeriodTypeDef",
    {
        "Type": RetentionPeriodTypeType,
        "Value": NotRequired[int],
    },
)

SelfManagedActiveDirectoryAttributesTypeDef = TypedDict(
    "SelfManagedActiveDirectoryAttributesTypeDef",
    {
        "DomainName": NotRequired[str],
        "OrganizationalUnitDistinguishedName": NotRequired[str],
        "FileSystemAdministratorsGroup": NotRequired[str],
        "UserName": NotRequired[str],
        "DnsIps": NotRequired[List[str]],
    },
)

SelfManagedActiveDirectoryConfigurationUpdatesTypeDef = TypedDict(
    "SelfManagedActiveDirectoryConfigurationUpdatesTypeDef",
    {
        "UserName": NotRequired[str],
        "Password": NotRequired[str],
        "DnsIps": NotRequired[Sequence[str]],
        "DomainName": NotRequired[str],
        "OrganizationalUnitDistinguishedName": NotRequired[str],
        "FileSystemAdministratorsGroup": NotRequired[str],
    },
)

StartMisconfiguredStateRecoveryRequestRequestTypeDef = TypedDict(
    "StartMisconfiguredStateRecoveryRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "ClientRequestToken": NotRequired[str],
    },
)

SvmEndpointTypeDef = TypedDict(
    "SvmEndpointTypeDef",
    {
        "DNSName": NotRequired[str],
        "IpAddresses": NotRequired[List[str]],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "TagKeys": Sequence[str],
    },
)

UpdateFileCacheLustreConfigurationTypeDef = TypedDict(
    "UpdateFileCacheLustreConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": NotRequired[str],
    },
)

UpdateSnapshotRequestRequestTypeDef = TypedDict(
    "UpdateSnapshotRequestRequestTypeDef",
    {
        "Name": str,
        "SnapshotId": str,
        "ClientRequestToken": NotRequired[str],
    },
)

WindowsAuditLogConfigurationTypeDef = TypedDict(
    "WindowsAuditLogConfigurationTypeDef",
    {
        "FileAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
        "FileShareAccessAuditLogLevel": WindowsAccessAuditLogLevelType,
        "AuditLogDestination": NotRequired[str],
    },
)

AssociateFileSystemAliasesResponseTypeDef = TypedDict(
    "AssociateFileSystemAliasesResponseTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CancelDataRepositoryTaskResponseTypeDef = TypedDict(
    "CancelDataRepositoryTaskResponseTypeDef",
    {
        "Lifecycle": DataRepositoryTaskLifecycleType,
        "TaskId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFileSystemFromBackupResponseTypeDef = TypedDict(
    "CreateFileSystemFromBackupResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFileSystemResponseTypeDef = TypedDict(
    "CreateFileSystemResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteBackupResponseTypeDef = TypedDict(
    "DeleteBackupResponseTypeDef",
    {
        "BackupId": str,
        "Lifecycle": BackupLifecycleType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteDataRepositoryAssociationResponseTypeDef = TypedDict(
    "DeleteDataRepositoryAssociationResponseTypeDef",
    {
        "AssociationId": str,
        "Lifecycle": DataRepositoryLifecycleType,
        "DeleteDataInFileSystem": bool,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteFileCacheResponseTypeDef = TypedDict(
    "DeleteFileCacheResponseTypeDef",
    {
        "FileCacheId": str,
        "Lifecycle": FileCacheLifecycleType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteSnapshotResponseTypeDef = TypedDict(
    "DeleteSnapshotResponseTypeDef",
    {
        "SnapshotId": str,
        "Lifecycle": SnapshotLifecycleType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteStorageVirtualMachineResponseTypeDef = TypedDict(
    "DeleteStorageVirtualMachineResponseTypeDef",
    {
        "StorageVirtualMachineId": str,
        "Lifecycle": StorageVirtualMachineLifecycleType,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFileSystemAliasesResponseTypeDef = TypedDict(
    "DescribeFileSystemAliasesResponseTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DisassociateFileSystemAliasesResponseTypeDef = TypedDict(
    "DisassociateFileSystemAliasesResponseTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

ReleaseFileSystemNfsV3LocksResponseTypeDef = TypedDict(
    "ReleaseFileSystemNfsV3LocksResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

RestoreVolumeFromSnapshotResponseTypeDef = TypedDict(
    "RestoreVolumeFromSnapshotResponseTypeDef",
    {
        "VolumeId": str,
        "Lifecycle": VolumeLifecycleType,
        "AdministrativeActions": List["AdministrativeActionTypeDef"],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

StartMisconfiguredStateRecoveryResponseTypeDef = TypedDict(
    "StartMisconfiguredStateRecoveryResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFileSystemResponseTypeDef = TypedDict(
    "UpdateFileSystemResponseTypeDef",
    {
        "FileSystem": "FileSystemTypeDef",
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

NFSDataRepositoryConfigurationTypeDef = TypedDict(
    "NFSDataRepositoryConfigurationTypeDef",
    {
        "Version": Literal["NFS3"],
        "DnsIps": NotRequired[List[str]],
        "AutoExportPolicy": NotRequired[AutoExportPolicyTypeDef],
    },
)

S3DataRepositoryConfigurationTypeDef = TypedDict(
    "S3DataRepositoryConfigurationTypeDef",
    {
        "AutoImportPolicy": NotRequired[AutoImportPolicyTypeDef],
        "AutoExportPolicy": NotRequired[AutoExportPolicyTypeDef],
    },
)

CopyBackupRequestRequestTypeDef = TypedDict(
    "CopyBackupRequestRequestTypeDef",
    {
        "SourceBackupId": str,
        "ClientRequestToken": NotRequired[str],
        "SourceRegion": NotRequired[str],
        "KmsKeyId": NotRequired[str],
        "CopyTags": NotRequired[bool],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

CreateBackupRequestRequestTypeDef = TypedDict(
    "CreateBackupRequestRequestTypeDef",
    {
        "FileSystemId": NotRequired[str],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "VolumeId": NotRequired[str],
    },
)

CreateSnapshotRequestRequestTypeDef = TypedDict(
    "CreateSnapshotRequestRequestTypeDef",
    {
        "Name": str,
        "VolumeId": str,
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

DeleteFileSystemLustreConfigurationTypeDef = TypedDict(
    "DeleteFileSystemLustreConfigurationTypeDef",
    {
        "SkipFinalBackup": NotRequired[bool],
        "FinalBackupTags": NotRequired[Sequence[TagTypeDef]],
    },
)

DeleteFileSystemLustreResponseTypeDef = TypedDict(
    "DeleteFileSystemLustreResponseTypeDef",
    {
        "FinalBackupId": NotRequired[str],
        "FinalBackupTags": NotRequired[List[TagTypeDef]],
    },
)

DeleteFileSystemOpenZFSConfigurationTypeDef = TypedDict(
    "DeleteFileSystemOpenZFSConfigurationTypeDef",
    {
        "SkipFinalBackup": NotRequired[bool],
        "FinalBackupTags": NotRequired[Sequence[TagTypeDef]],
        "Options": NotRequired[Sequence[Literal["DELETE_CHILD_VOLUMES_AND_SNAPSHOTS"]]],
    },
)

DeleteFileSystemOpenZFSResponseTypeDef = TypedDict(
    "DeleteFileSystemOpenZFSResponseTypeDef",
    {
        "FinalBackupId": NotRequired[str],
        "FinalBackupTags": NotRequired[List[TagTypeDef]],
    },
)

DeleteFileSystemWindowsConfigurationTypeDef = TypedDict(
    "DeleteFileSystemWindowsConfigurationTypeDef",
    {
        "SkipFinalBackup": NotRequired[bool],
        "FinalBackupTags": NotRequired[Sequence[TagTypeDef]],
    },
)

DeleteFileSystemWindowsResponseTypeDef = TypedDict(
    "DeleteFileSystemWindowsResponseTypeDef",
    {
        "FinalBackupId": NotRequired[str],
        "FinalBackupTags": NotRequired[List[TagTypeDef]],
    },
)

DeleteVolumeOntapConfigurationTypeDef = TypedDict(
    "DeleteVolumeOntapConfigurationTypeDef",
    {
        "SkipFinalBackup": NotRequired[bool],
        "FinalBackupTags": NotRequired[Sequence[TagTypeDef]],
        "BypassSnaplockEnterpriseRetention": NotRequired[bool],
    },
)

DeleteVolumeOntapResponseTypeDef = TypedDict(
    "DeleteVolumeOntapResponseTypeDef",
    {
        "FinalBackupId": NotRequired[str],
        "FinalBackupTags": NotRequired[List[TagTypeDef]],
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "Tags": List[TagTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "ResourceARN": str,
        "Tags": Sequence[TagTypeDef],
    },
)

CreateFileCacheLustreConfigurationTypeDef = TypedDict(
    "CreateFileCacheLustreConfigurationTypeDef",
    {
        "PerUnitStorageThroughput": int,
        "DeploymentType": Literal["CACHE_1"],
        "MetadataConfiguration": FileCacheLustreMetadataConfigurationTypeDef,
        "WeeklyMaintenanceStartTime": NotRequired[str],
    },
)

CreateFileSystemLustreConfigurationTypeDef = TypedDict(
    "CreateFileSystemLustreConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "ImportPath": NotRequired[str],
        "ExportPath": NotRequired[str],
        "ImportedFileChunkSize": NotRequired[int],
        "DeploymentType": NotRequired[LustreDeploymentTypeType],
        "AutoImportPolicy": NotRequired[AutoImportPolicyTypeType],
        "PerUnitStorageThroughput": NotRequired[int],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "AutomaticBackupRetentionDays": NotRequired[int],
        "CopyTagsToBackups": NotRequired[bool],
        "DriveCacheType": NotRequired[DriveCacheTypeType],
        "DataCompressionType": NotRequired[DataCompressionTypeType],
        "LogConfiguration": NotRequired[LustreLogCreateConfigurationTypeDef],
        "RootSquashConfiguration": NotRequired[LustreRootSquashConfigurationTypeDef],
    },
)

UpdateFileSystemLustreConfigurationTypeDef = TypedDict(
    "UpdateFileSystemLustreConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "AutomaticBackupRetentionDays": NotRequired[int],
        "AutoImportPolicy": NotRequired[AutoImportPolicyTypeType],
        "DataCompressionType": NotRequired[DataCompressionTypeType],
        "LogConfiguration": NotRequired[LustreLogCreateConfigurationTypeDef],
        "RootSquashConfiguration": NotRequired[LustreRootSquashConfigurationTypeDef],
    },
)

CreateFileSystemOntapConfigurationTypeDef = TypedDict(
    "CreateFileSystemOntapConfigurationTypeDef",
    {
        "DeploymentType": OntapDeploymentTypeType,
        "ThroughputCapacity": int,
        "AutomaticBackupRetentionDays": NotRequired[int],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "EndpointIpAddressRange": NotRequired[str],
        "FsxAdminPassword": NotRequired[str],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
        "PreferredSubnetId": NotRequired[str],
        "RouteTableIds": NotRequired[Sequence[str]],
        "WeeklyMaintenanceStartTime": NotRequired[str],
    },
)

OpenZFSFileSystemConfigurationTypeDef = TypedDict(
    "OpenZFSFileSystemConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": NotRequired[int],
        "CopyTagsToBackups": NotRequired[bool],
        "CopyTagsToVolumes": NotRequired[bool],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "DeploymentType": NotRequired[OpenZFSDeploymentTypeType],
        "ThroughputCapacity": NotRequired[int],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
        "RootVolumeId": NotRequired[str],
        "PreferredSubnetId": NotRequired[str],
        "EndpointIpAddressRange": NotRequired[str],
        "RouteTableIds": NotRequired[List[str]],
        "EndpointIpAddress": NotRequired[str],
    },
)

UpdateFileSystemOntapConfigurationTypeDef = TypedDict(
    "UpdateFileSystemOntapConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": NotRequired[int],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "FsxAdminPassword": NotRequired[str],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
        "ThroughputCapacity": NotRequired[int],
        "AddRouteTableIds": NotRequired[Sequence[str]],
        "RemoveRouteTableIds": NotRequired[Sequence[str]],
    },
)

UpdateFileSystemOpenZFSConfigurationTypeDef = TypedDict(
    "UpdateFileSystemOpenZFSConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": NotRequired[int],
        "CopyTagsToBackups": NotRequired[bool],
        "CopyTagsToVolumes": NotRequired[bool],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "ThroughputCapacity": NotRequired[int],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
        "AddRouteTableIds": NotRequired[Sequence[str]],
        "RemoveRouteTableIds": NotRequired[Sequence[str]],
    },
)

CreateSvmActiveDirectoryConfigurationTypeDef = TypedDict(
    "CreateSvmActiveDirectoryConfigurationTypeDef",
    {
        "NetBiosName": str,
        "SelfManagedActiveDirectoryConfiguration": NotRequired[
            SelfManagedActiveDirectoryConfigurationTypeDef
        ],
    },
)

CreateFileSystemWindowsConfigurationTypeDef = TypedDict(
    "CreateFileSystemWindowsConfigurationTypeDef",
    {
        "ThroughputCapacity": int,
        "ActiveDirectoryId": NotRequired[str],
        "SelfManagedActiveDirectoryConfiguration": NotRequired[
            SelfManagedActiveDirectoryConfigurationTypeDef
        ],
        "DeploymentType": NotRequired[WindowsDeploymentTypeType],
        "PreferredSubnetId": NotRequired[str],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "AutomaticBackupRetentionDays": NotRequired[int],
        "CopyTagsToBackups": NotRequired[bool],
        "Aliases": NotRequired[Sequence[str]],
        "AuditLogConfiguration": NotRequired[WindowsAuditLogCreateConfigurationTypeDef],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
    },
)

DataRepositoryConfigurationTypeDef = TypedDict(
    "DataRepositoryConfigurationTypeDef",
    {
        "Lifecycle": NotRequired[DataRepositoryLifecycleType],
        "ImportPath": NotRequired[str],
        "ExportPath": NotRequired[str],
        "ImportedFileChunkSize": NotRequired[int],
        "AutoImportPolicy": NotRequired[AutoImportPolicyTypeType],
        "FailureDetails": NotRequired[DataRepositoryFailureDetailsTypeDef],
    },
)

DescribeDataRepositoryTasksRequestRequestTypeDef = TypedDict(
    "DescribeDataRepositoryTasksRequestRequestTypeDef",
    {
        "TaskIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[DataRepositoryTaskFilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

DescribeBackupsRequestRequestTypeDef = TypedDict(
    "DescribeBackupsRequestRequestTypeDef",
    {
        "BackupIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

DescribeDataRepositoryAssociationsRequestRequestTypeDef = TypedDict(
    "DescribeDataRepositoryAssociationsRequestRequestTypeDef",
    {
        "AssociationIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

DescribeBackupsRequestDescribeBackupsPaginateTypeDef = TypedDict(
    "DescribeBackupsRequestDescribeBackupsPaginateTypeDef",
    {
        "BackupIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[FilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef = TypedDict(
    "DescribeFileSystemsRequestDescribeFileSystemsPaginateTypeDef",
    {
        "FileSystemIds": NotRequired[Sequence[str]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

ListTagsForResourceRequestListTagsForResourcePaginateTypeDef = TypedDict(
    "ListTagsForResourceRequestListTagsForResourcePaginateTypeDef",
    {
        "ResourceARN": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeSnapshotsRequestRequestTypeDef = TypedDict(
    "DescribeSnapshotsRequestRequestTypeDef",
    {
        "SnapshotIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[SnapshotFilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef = TypedDict(
    "DescribeStorageVirtualMachinesRequestDescribeStorageVirtualMachinesPaginateTypeDef",
    {
        "StorageVirtualMachineIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[StorageVirtualMachineFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeStorageVirtualMachinesRequestRequestTypeDef = TypedDict(
    "DescribeStorageVirtualMachinesRequestRequestTypeDef",
    {
        "StorageVirtualMachineIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[StorageVirtualMachineFilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

DescribeVolumesRequestDescribeVolumesPaginateTypeDef = TypedDict(
    "DescribeVolumesRequestDescribeVolumesPaginateTypeDef",
    {
        "VolumeIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[VolumeFilterTypeDef]],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)

DescribeVolumesRequestRequestTypeDef = TypedDict(
    "DescribeVolumesRequestRequestTypeDef",
    {
        "VolumeIds": NotRequired[Sequence[str]],
        "Filters": NotRequired[Sequence[VolumeFilterTypeDef]],
        "MaxResults": NotRequired[int],
        "NextToken": NotRequired[str],
    },
)

ReleaseConfigurationTypeDef = TypedDict(
    "ReleaseConfigurationTypeDef",
    {
        "DurationSinceLastAccess": NotRequired[DurationSinceLastAccessTypeDef],
    },
)

FileCacheDataRepositoryAssociationTypeDef = TypedDict(
    "FileCacheDataRepositoryAssociationTypeDef",
    {
        "FileCachePath": str,
        "DataRepositoryPath": str,
        "DataRepositorySubdirectories": NotRequired[Sequence[str]],
        "NFS": NotRequired[FileCacheNFSConfigurationTypeDef],
    },
)

FileCacheLustreConfigurationTypeDef = TypedDict(
    "FileCacheLustreConfigurationTypeDef",
    {
        "PerUnitStorageThroughput": NotRequired[int],
        "DeploymentType": NotRequired[Literal["CACHE_1"]],
        "MountName": NotRequired[str],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "MetadataConfiguration": NotRequired[FileCacheLustreMetadataConfigurationTypeDef],
        "LogConfiguration": NotRequired[LustreLogConfigurationTypeDef],
    },
)

FileSystemEndpointsTypeDef = TypedDict(
    "FileSystemEndpointsTypeDef",
    {
        "Intercluster": NotRequired[FileSystemEndpointTypeDef],
        "Management": NotRequired[FileSystemEndpointTypeDef],
    },
)

SnapshotTypeDef = TypedDict(
    "SnapshotTypeDef",
    {
        "ResourceARN": NotRequired[str],
        "SnapshotId": NotRequired[str],
        "Name": NotRequired[str],
        "VolumeId": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "Lifecycle": NotRequired[SnapshotLifecycleType],
        "LifecycleTransitionReason": NotRequired[LifecycleTransitionReasonTypeDef],
        "Tags": NotRequired[List[TagTypeDef]],
        "AdministrativeActions": NotRequired[List["AdministrativeActionTypeDef"]],
    },
)

OpenZFSNfsExportTypeDef = TypedDict(
    "OpenZFSNfsExportTypeDef",
    {
        "ClientConfigurations": List[OpenZFSClientConfigurationTypeDef],
    },
)

SnaplockRetentionPeriodTypeDef = TypedDict(
    "SnaplockRetentionPeriodTypeDef",
    {
        "DefaultRetention": RetentionPeriodTypeDef,
        "MinimumRetention": RetentionPeriodTypeDef,
        "MaximumRetention": RetentionPeriodTypeDef,
    },
)

SvmActiveDirectoryConfigurationTypeDef = TypedDict(
    "SvmActiveDirectoryConfigurationTypeDef",
    {
        "NetBiosName": NotRequired[str],
        "SelfManagedActiveDirectoryConfiguration": NotRequired[
            SelfManagedActiveDirectoryAttributesTypeDef
        ],
    },
)

UpdateFileSystemWindowsConfigurationTypeDef = TypedDict(
    "UpdateFileSystemWindowsConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "AutomaticBackupRetentionDays": NotRequired[int],
        "ThroughputCapacity": NotRequired[int],
        "SelfManagedActiveDirectoryConfiguration": NotRequired[
            SelfManagedActiveDirectoryConfigurationUpdatesTypeDef
        ],
        "AuditLogConfiguration": NotRequired[WindowsAuditLogCreateConfigurationTypeDef],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
    },
)

UpdateSvmActiveDirectoryConfigurationTypeDef = TypedDict(
    "UpdateSvmActiveDirectoryConfigurationTypeDef",
    {
        "SelfManagedActiveDirectoryConfiguration": NotRequired[
            SelfManagedActiveDirectoryConfigurationUpdatesTypeDef
        ],
        "NetBiosName": NotRequired[str],
    },
)

SvmEndpointsTypeDef = TypedDict(
    "SvmEndpointsTypeDef",
    {
        "Iscsi": NotRequired[SvmEndpointTypeDef],
        "Management": NotRequired[SvmEndpointTypeDef],
        "Nfs": NotRequired[SvmEndpointTypeDef],
        "Smb": NotRequired[SvmEndpointTypeDef],
    },
)

UpdateFileCacheRequestRequestTypeDef = TypedDict(
    "UpdateFileCacheRequestRequestTypeDef",
    {
        "FileCacheId": str,
        "ClientRequestToken": NotRequired[str],
        "LustreConfiguration": NotRequired[UpdateFileCacheLustreConfigurationTypeDef],
    },
)

WindowsFileSystemConfigurationTypeDef = TypedDict(
    "WindowsFileSystemConfigurationTypeDef",
    {
        "ActiveDirectoryId": NotRequired[str],
        "SelfManagedActiveDirectoryConfiguration": NotRequired[
            SelfManagedActiveDirectoryAttributesTypeDef
        ],
        "DeploymentType": NotRequired[WindowsDeploymentTypeType],
        "RemoteAdministrationEndpoint": NotRequired[str],
        "PreferredSubnetId": NotRequired[str],
        "PreferredFileServerIp": NotRequired[str],
        "ThroughputCapacity": NotRequired[int],
        "MaintenanceOperationsInProgress": NotRequired[List[FileSystemMaintenanceOperationType]],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "AutomaticBackupRetentionDays": NotRequired[int],
        "CopyTagsToBackups": NotRequired[bool],
        "Aliases": NotRequired[List[AliasTypeDef]],
        "AuditLogConfiguration": NotRequired[WindowsAuditLogConfigurationTypeDef],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
    },
)

CreateDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "CreateDataRepositoryAssociationRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "DataRepositoryPath": str,
        "FileSystemPath": NotRequired[str],
        "BatchImportMetaDataOnCreate": NotRequired[bool],
        "ImportedFileChunkSize": NotRequired[int],
        "S3": NotRequired[S3DataRepositoryConfigurationTypeDef],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

DataRepositoryAssociationTypeDef = TypedDict(
    "DataRepositoryAssociationTypeDef",
    {
        "AssociationId": NotRequired[str],
        "ResourceARN": NotRequired[str],
        "FileSystemId": NotRequired[str],
        "Lifecycle": NotRequired[DataRepositoryLifecycleType],
        "FailureDetails": NotRequired[DataRepositoryFailureDetailsTypeDef],
        "FileSystemPath": NotRequired[str],
        "DataRepositoryPath": NotRequired[str],
        "BatchImportMetaDataOnCreate": NotRequired[bool],
        "ImportedFileChunkSize": NotRequired[int],
        "S3": NotRequired[S3DataRepositoryConfigurationTypeDef],
        "Tags": NotRequired[List[TagTypeDef]],
        "CreationTime": NotRequired[datetime],
        "FileCacheId": NotRequired[str],
        "FileCachePath": NotRequired[str],
        "DataRepositorySubdirectories": NotRequired[List[str]],
        "NFS": NotRequired[NFSDataRepositoryConfigurationTypeDef],
    },
)

UpdateDataRepositoryAssociationRequestRequestTypeDef = TypedDict(
    "UpdateDataRepositoryAssociationRequestRequestTypeDef",
    {
        "AssociationId": str,
        "ClientRequestToken": NotRequired[str],
        "ImportedFileChunkSize": NotRequired[int],
        "S3": NotRequired[S3DataRepositoryConfigurationTypeDef],
    },
)

DeleteFileSystemRequestRequestTypeDef = TypedDict(
    "DeleteFileSystemRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "ClientRequestToken": NotRequired[str],
        "WindowsConfiguration": NotRequired[DeleteFileSystemWindowsConfigurationTypeDef],
        "LustreConfiguration": NotRequired[DeleteFileSystemLustreConfigurationTypeDef],
        "OpenZFSConfiguration": NotRequired[DeleteFileSystemOpenZFSConfigurationTypeDef],
    },
)

DeleteFileSystemResponseTypeDef = TypedDict(
    "DeleteFileSystemResponseTypeDef",
    {
        "FileSystemId": str,
        "Lifecycle": FileSystemLifecycleType,
        "WindowsResponse": DeleteFileSystemWindowsResponseTypeDef,
        "LustreResponse": DeleteFileSystemLustreResponseTypeDef,
        "OpenZFSResponse": DeleteFileSystemOpenZFSResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DeleteVolumeRequestRequestTypeDef = TypedDict(
    "DeleteVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
        "ClientRequestToken": NotRequired[str],
        "OntapConfiguration": NotRequired[DeleteVolumeOntapConfigurationTypeDef],
        "OpenZFSConfiguration": NotRequired[DeleteVolumeOpenZFSConfigurationTypeDef],
    },
)

DeleteVolumeResponseTypeDef = TypedDict(
    "DeleteVolumeResponseTypeDef",
    {
        "VolumeId": str,
        "Lifecycle": VolumeLifecycleType,
        "OntapResponse": DeleteVolumeOntapResponseTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "CreateStorageVirtualMachineRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "Name": str,
        "ActiveDirectoryConfiguration": NotRequired[CreateSvmActiveDirectoryConfigurationTypeDef],
        "ClientRequestToken": NotRequired[str],
        "SvmAdminPassword": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "RootVolumeSecurityStyle": NotRequired[StorageVirtualMachineRootVolumeSecurityStyleType],
    },
)

LustreFileSystemConfigurationTypeDef = TypedDict(
    "LustreFileSystemConfigurationTypeDef",
    {
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DataRepositoryConfiguration": NotRequired[DataRepositoryConfigurationTypeDef],
        "DeploymentType": NotRequired[LustreDeploymentTypeType],
        "PerUnitStorageThroughput": NotRequired[int],
        "MountName": NotRequired[str],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "AutomaticBackupRetentionDays": NotRequired[int],
        "CopyTagsToBackups": NotRequired[bool],
        "DriveCacheType": NotRequired[DriveCacheTypeType],
        "DataCompressionType": NotRequired[DataCompressionTypeType],
        "LogConfiguration": NotRequired[LustreLogConfigurationTypeDef],
        "RootSquashConfiguration": NotRequired[LustreRootSquashConfigurationTypeDef],
    },
)

CreateDataRepositoryTaskRequestRequestTypeDef = TypedDict(
    "CreateDataRepositoryTaskRequestRequestTypeDef",
    {
        "Type": DataRepositoryTaskTypeType,
        "FileSystemId": str,
        "Report": CompletionReportTypeDef,
        "Paths": NotRequired[Sequence[str]],
        "ClientRequestToken": NotRequired[str],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "CapacityToRelease": NotRequired[int],
        "ReleaseConfiguration": NotRequired[ReleaseConfigurationTypeDef],
    },
)

DataRepositoryTaskTypeDef = TypedDict(
    "DataRepositoryTaskTypeDef",
    {
        "TaskId": str,
        "Lifecycle": DataRepositoryTaskLifecycleType,
        "Type": DataRepositoryTaskTypeType,
        "CreationTime": datetime,
        "StartTime": NotRequired[datetime],
        "EndTime": NotRequired[datetime],
        "ResourceARN": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "FileSystemId": NotRequired[str],
        "Paths": NotRequired[List[str]],
        "FailureDetails": NotRequired[DataRepositoryTaskFailureDetailsTypeDef],
        "Status": NotRequired[DataRepositoryTaskStatusTypeDef],
        "Report": NotRequired[CompletionReportTypeDef],
        "CapacityToRelease": NotRequired[int],
        "FileCacheId": NotRequired[str],
        "ReleaseConfiguration": NotRequired[ReleaseConfigurationTypeDef],
    },
)

CreateFileCacheRequestRequestTypeDef = TypedDict(
    "CreateFileCacheRequestRequestTypeDef",
    {
        "FileCacheType": Literal["LUSTRE"],
        "FileCacheTypeVersion": str,
        "StorageCapacity": int,
        "SubnetIds": Sequence[str],
        "ClientRequestToken": NotRequired[str],
        "SecurityGroupIds": NotRequired[Sequence[str]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "CopyTagsToDataRepositoryAssociations": NotRequired[bool],
        "KmsKeyId": NotRequired[str],
        "LustreConfiguration": NotRequired[CreateFileCacheLustreConfigurationTypeDef],
        "DataRepositoryAssociations": NotRequired[
            Sequence[FileCacheDataRepositoryAssociationTypeDef]
        ],
    },
)

FileCacheCreatingTypeDef = TypedDict(
    "FileCacheCreatingTypeDef",
    {
        "OwnerId": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "FileCacheId": NotRequired[str],
        "FileCacheType": NotRequired[Literal["LUSTRE"]],
        "FileCacheTypeVersion": NotRequired[str],
        "Lifecycle": NotRequired[FileCacheLifecycleType],
        "FailureDetails": NotRequired[FileCacheFailureDetailsTypeDef],
        "StorageCapacity": NotRequired[int],
        "VpcId": NotRequired[str],
        "SubnetIds": NotRequired[List[str]],
        "NetworkInterfaceIds": NotRequired[List[str]],
        "DNSName": NotRequired[str],
        "KmsKeyId": NotRequired[str],
        "ResourceARN": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "CopyTagsToDataRepositoryAssociations": NotRequired[bool],
        "LustreConfiguration": NotRequired[FileCacheLustreConfigurationTypeDef],
        "DataRepositoryAssociationIds": NotRequired[List[str]],
    },
)

FileCacheTypeDef = TypedDict(
    "FileCacheTypeDef",
    {
        "OwnerId": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "FileCacheId": NotRequired[str],
        "FileCacheType": NotRequired[Literal["LUSTRE"]],
        "FileCacheTypeVersion": NotRequired[str],
        "Lifecycle": NotRequired[FileCacheLifecycleType],
        "FailureDetails": NotRequired[FileCacheFailureDetailsTypeDef],
        "StorageCapacity": NotRequired[int],
        "VpcId": NotRequired[str],
        "SubnetIds": NotRequired[List[str]],
        "NetworkInterfaceIds": NotRequired[List[str]],
        "DNSName": NotRequired[str],
        "KmsKeyId": NotRequired[str],
        "ResourceARN": NotRequired[str],
        "LustreConfiguration": NotRequired[FileCacheLustreConfigurationTypeDef],
        "DataRepositoryAssociationIds": NotRequired[List[str]],
    },
)

OntapFileSystemConfigurationTypeDef = TypedDict(
    "OntapFileSystemConfigurationTypeDef",
    {
        "AutomaticBackupRetentionDays": NotRequired[int],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "DeploymentType": NotRequired[OntapDeploymentTypeType],
        "EndpointIpAddressRange": NotRequired[str],
        "Endpoints": NotRequired[FileSystemEndpointsTypeDef],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
        "PreferredSubnetId": NotRequired[str],
        "RouteTableIds": NotRequired[List[str]],
        "ThroughputCapacity": NotRequired[int],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "FsxAdminPassword": NotRequired[str],
    },
)

CreateSnapshotResponseTypeDef = TypedDict(
    "CreateSnapshotResponseTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeSnapshotsResponseTypeDef = TypedDict(
    "DescribeSnapshotsResponseTypeDef",
    {
        "Snapshots": List[SnapshotTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateSnapshotResponseTypeDef = TypedDict(
    "UpdateSnapshotResponseTypeDef",
    {
        "Snapshot": SnapshotTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateOpenZFSVolumeConfigurationTypeDef = TypedDict(
    "CreateOpenZFSVolumeConfigurationTypeDef",
    {
        "ParentVolumeId": str,
        "StorageCapacityReservationGiB": NotRequired[int],
        "StorageCapacityQuotaGiB": NotRequired[int],
        "RecordSizeKiB": NotRequired[int],
        "DataCompressionType": NotRequired[OpenZFSDataCompressionTypeType],
        "CopyTagsToSnapshots": NotRequired[bool],
        "OriginSnapshot": NotRequired[CreateOpenZFSOriginSnapshotConfigurationTypeDef],
        "ReadOnly": NotRequired[bool],
        "NfsExports": NotRequired[Sequence[OpenZFSNfsExportTypeDef]],
        "UserAndGroupQuotas": NotRequired[Sequence[OpenZFSUserOrGroupQuotaTypeDef]],
    },
)

OpenZFSCreateRootVolumeConfigurationTypeDef = TypedDict(
    "OpenZFSCreateRootVolumeConfigurationTypeDef",
    {
        "RecordSizeKiB": NotRequired[int],
        "DataCompressionType": NotRequired[OpenZFSDataCompressionTypeType],
        "NfsExports": NotRequired[Sequence[OpenZFSNfsExportTypeDef]],
        "UserAndGroupQuotas": NotRequired[Sequence[OpenZFSUserOrGroupQuotaTypeDef]],
        "CopyTagsToSnapshots": NotRequired[bool],
        "ReadOnly": NotRequired[bool],
    },
)

OpenZFSVolumeConfigurationTypeDef = TypedDict(
    "OpenZFSVolumeConfigurationTypeDef",
    {
        "ParentVolumeId": NotRequired[str],
        "VolumePath": NotRequired[str],
        "StorageCapacityReservationGiB": NotRequired[int],
        "StorageCapacityQuotaGiB": NotRequired[int],
        "RecordSizeKiB": NotRequired[int],
        "DataCompressionType": NotRequired[OpenZFSDataCompressionTypeType],
        "CopyTagsToSnapshots": NotRequired[bool],
        "OriginSnapshot": NotRequired[OpenZFSOriginSnapshotConfigurationTypeDef],
        "ReadOnly": NotRequired[bool],
        "NfsExports": NotRequired[List[OpenZFSNfsExportTypeDef]],
        "UserAndGroupQuotas": NotRequired[List[OpenZFSUserOrGroupQuotaTypeDef]],
        "RestoreToSnapshot": NotRequired[str],
        "DeleteIntermediateSnaphots": NotRequired[bool],
        "DeleteClonedVolumes": NotRequired[bool],
    },
)

UpdateOpenZFSVolumeConfigurationTypeDef = TypedDict(
    "UpdateOpenZFSVolumeConfigurationTypeDef",
    {
        "StorageCapacityReservationGiB": NotRequired[int],
        "StorageCapacityQuotaGiB": NotRequired[int],
        "RecordSizeKiB": NotRequired[int],
        "DataCompressionType": NotRequired[OpenZFSDataCompressionTypeType],
        "NfsExports": NotRequired[Sequence[OpenZFSNfsExportTypeDef]],
        "UserAndGroupQuotas": NotRequired[Sequence[OpenZFSUserOrGroupQuotaTypeDef]],
        "ReadOnly": NotRequired[bool],
    },
)

CreateSnaplockConfigurationTypeDef = TypedDict(
    "CreateSnaplockConfigurationTypeDef",
    {
        "SnaplockType": SnaplockTypeType,
        "AuditLogVolume": NotRequired[bool],
        "AutocommitPeriod": NotRequired[AutocommitPeriodTypeDef],
        "PrivilegedDelete": NotRequired[PrivilegedDeleteType],
        "RetentionPeriod": NotRequired[SnaplockRetentionPeriodTypeDef],
        "VolumeAppendModeEnabled": NotRequired[bool],
    },
)

SnaplockConfigurationTypeDef = TypedDict(
    "SnaplockConfigurationTypeDef",
    {
        "AuditLogVolume": NotRequired[bool],
        "AutocommitPeriod": NotRequired[AutocommitPeriodTypeDef],
        "PrivilegedDelete": NotRequired[PrivilegedDeleteType],
        "RetentionPeriod": NotRequired[SnaplockRetentionPeriodTypeDef],
        "SnaplockType": NotRequired[SnaplockTypeType],
        "VolumeAppendModeEnabled": NotRequired[bool],
    },
)

UpdateSnaplockConfigurationTypeDef = TypedDict(
    "UpdateSnaplockConfigurationTypeDef",
    {
        "AuditLogVolume": NotRequired[bool],
        "AutocommitPeriod": NotRequired[AutocommitPeriodTypeDef],
        "PrivilegedDelete": NotRequired[PrivilegedDeleteType],
        "RetentionPeriod": NotRequired[SnaplockRetentionPeriodTypeDef],
        "VolumeAppendModeEnabled": NotRequired[bool],
    },
)

UpdateFileSystemRequestRequestTypeDef = TypedDict(
    "UpdateFileSystemRequestRequestTypeDef",
    {
        "FileSystemId": str,
        "ClientRequestToken": NotRequired[str],
        "StorageCapacity": NotRequired[int],
        "WindowsConfiguration": NotRequired[UpdateFileSystemWindowsConfigurationTypeDef],
        "LustreConfiguration": NotRequired[UpdateFileSystemLustreConfigurationTypeDef],
        "OntapConfiguration": NotRequired[UpdateFileSystemOntapConfigurationTypeDef],
        "OpenZFSConfiguration": NotRequired[UpdateFileSystemOpenZFSConfigurationTypeDef],
        "StorageType": NotRequired[StorageTypeType],
    },
)

UpdateStorageVirtualMachineRequestRequestTypeDef = TypedDict(
    "UpdateStorageVirtualMachineRequestRequestTypeDef",
    {
        "StorageVirtualMachineId": str,
        "ActiveDirectoryConfiguration": NotRequired[UpdateSvmActiveDirectoryConfigurationTypeDef],
        "ClientRequestToken": NotRequired[str],
        "SvmAdminPassword": NotRequired[str],
    },
)

StorageVirtualMachineTypeDef = TypedDict(
    "StorageVirtualMachineTypeDef",
    {
        "ActiveDirectoryConfiguration": NotRequired[SvmActiveDirectoryConfigurationTypeDef],
        "CreationTime": NotRequired[datetime],
        "Endpoints": NotRequired[SvmEndpointsTypeDef],
        "FileSystemId": NotRequired[str],
        "Lifecycle": NotRequired[StorageVirtualMachineLifecycleType],
        "Name": NotRequired[str],
        "ResourceARN": NotRequired[str],
        "StorageVirtualMachineId": NotRequired[str],
        "Subtype": NotRequired[StorageVirtualMachineSubtypeType],
        "UUID": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "LifecycleTransitionReason": NotRequired[LifecycleTransitionReasonTypeDef],
        "RootVolumeSecurityStyle": NotRequired[StorageVirtualMachineRootVolumeSecurityStyleType],
    },
)

CreateDataRepositoryAssociationResponseTypeDef = TypedDict(
    "CreateDataRepositoryAssociationResponseTypeDef",
    {
        "Association": DataRepositoryAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataRepositoryAssociationsResponseTypeDef = TypedDict(
    "DescribeDataRepositoryAssociationsResponseTypeDef",
    {
        "Associations": List[DataRepositoryAssociationTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateDataRepositoryAssociationResponseTypeDef = TypedDict(
    "UpdateDataRepositoryAssociationResponseTypeDef",
    {
        "Association": DataRepositoryAssociationTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateDataRepositoryTaskResponseTypeDef = TypedDict(
    "CreateDataRepositoryTaskResponseTypeDef",
    {
        "DataRepositoryTask": DataRepositoryTaskTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeDataRepositoryTasksResponseTypeDef = TypedDict(
    "DescribeDataRepositoryTasksResponseTypeDef",
    {
        "DataRepositoryTasks": List[DataRepositoryTaskTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFileCacheResponseTypeDef = TypedDict(
    "CreateFileCacheResponseTypeDef",
    {
        "FileCache": FileCacheCreatingTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFileCachesResponseTypeDef = TypedDict(
    "DescribeFileCachesResponseTypeDef",
    {
        "FileCaches": List[FileCacheTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateFileCacheResponseTypeDef = TypedDict(
    "UpdateFileCacheResponseTypeDef",
    {
        "FileCache": FileCacheTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

FileSystemTypeDef = TypedDict(
    "FileSystemTypeDef",
    {
        "OwnerId": NotRequired[str],
        "CreationTime": NotRequired[datetime],
        "FileSystemId": NotRequired[str],
        "FileSystemType": NotRequired[FileSystemTypeType],
        "Lifecycle": NotRequired[FileSystemLifecycleType],
        "FailureDetails": NotRequired[FileSystemFailureDetailsTypeDef],
        "StorageCapacity": NotRequired[int],
        "StorageType": NotRequired[StorageTypeType],
        "VpcId": NotRequired[str],
        "SubnetIds": NotRequired[List[str]],
        "NetworkInterfaceIds": NotRequired[List[str]],
        "DNSName": NotRequired[str],
        "KmsKeyId": NotRequired[str],
        "ResourceARN": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "WindowsConfiguration": NotRequired[WindowsFileSystemConfigurationTypeDef],
        "LustreConfiguration": NotRequired[LustreFileSystemConfigurationTypeDef],
        "AdministrativeActions": NotRequired[List["AdministrativeActionTypeDef"]],
        "OntapConfiguration": NotRequired[OntapFileSystemConfigurationTypeDef],
        "FileSystemTypeVersion": NotRequired[str],
        "OpenZFSConfiguration": NotRequired[OpenZFSFileSystemConfigurationTypeDef],
    },
)

CreateFileSystemOpenZFSConfigurationTypeDef = TypedDict(
    "CreateFileSystemOpenZFSConfigurationTypeDef",
    {
        "DeploymentType": OpenZFSDeploymentTypeType,
        "ThroughputCapacity": int,
        "AutomaticBackupRetentionDays": NotRequired[int],
        "CopyTagsToBackups": NotRequired[bool],
        "CopyTagsToVolumes": NotRequired[bool],
        "DailyAutomaticBackupStartTime": NotRequired[str],
        "WeeklyMaintenanceStartTime": NotRequired[str],
        "DiskIopsConfiguration": NotRequired[DiskIopsConfigurationTypeDef],
        "RootVolumeConfiguration": NotRequired[OpenZFSCreateRootVolumeConfigurationTypeDef],
        "PreferredSubnetId": NotRequired[str],
        "EndpointIpAddressRange": NotRequired[str],
        "RouteTableIds": NotRequired[Sequence[str]],
    },
)

CreateOntapVolumeConfigurationTypeDef = TypedDict(
    "CreateOntapVolumeConfigurationTypeDef",
    {
        "SizeInMegabytes": int,
        "StorageVirtualMachineId": str,
        "JunctionPath": NotRequired[str],
        "SecurityStyle": NotRequired[SecurityStyleType],
        "StorageEfficiencyEnabled": NotRequired[bool],
        "TieringPolicy": NotRequired[TieringPolicyTypeDef],
        "OntapVolumeType": NotRequired[InputOntapVolumeTypeType],
        "SnapshotPolicy": NotRequired[str],
        "CopyTagsToBackups": NotRequired[bool],
        "SnaplockConfiguration": NotRequired[CreateSnaplockConfigurationTypeDef],
    },
)

OntapVolumeConfigurationTypeDef = TypedDict(
    "OntapVolumeConfigurationTypeDef",
    {
        "FlexCacheEndpointType": NotRequired[FlexCacheEndpointTypeType],
        "JunctionPath": NotRequired[str],
        "SecurityStyle": NotRequired[SecurityStyleType],
        "SizeInMegabytes": NotRequired[int],
        "StorageEfficiencyEnabled": NotRequired[bool],
        "StorageVirtualMachineId": NotRequired[str],
        "StorageVirtualMachineRoot": NotRequired[bool],
        "TieringPolicy": NotRequired[TieringPolicyTypeDef],
        "UUID": NotRequired[str],
        "OntapVolumeType": NotRequired[OntapVolumeTypeType],
        "SnapshotPolicy": NotRequired[str],
        "CopyTagsToBackups": NotRequired[bool],
        "SnaplockConfiguration": NotRequired[SnaplockConfigurationTypeDef],
    },
)

UpdateOntapVolumeConfigurationTypeDef = TypedDict(
    "UpdateOntapVolumeConfigurationTypeDef",
    {
        "JunctionPath": NotRequired[str],
        "SecurityStyle": NotRequired[SecurityStyleType],
        "SizeInMegabytes": NotRequired[int],
        "StorageEfficiencyEnabled": NotRequired[bool],
        "TieringPolicy": NotRequired[TieringPolicyTypeDef],
        "SnapshotPolicy": NotRequired[str],
        "CopyTagsToBackups": NotRequired[bool],
        "SnaplockConfiguration": NotRequired[UpdateSnaplockConfigurationTypeDef],
    },
)

CreateStorageVirtualMachineResponseTypeDef = TypedDict(
    "CreateStorageVirtualMachineResponseTypeDef",
    {
        "StorageVirtualMachine": StorageVirtualMachineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeStorageVirtualMachinesResponseTypeDef = TypedDict(
    "DescribeStorageVirtualMachinesResponseTypeDef",
    {
        "StorageVirtualMachines": List[StorageVirtualMachineTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateStorageVirtualMachineResponseTypeDef = TypedDict(
    "UpdateStorageVirtualMachineResponseTypeDef",
    {
        "StorageVirtualMachine": StorageVirtualMachineTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeFileSystemsResponseTypeDef = TypedDict(
    "DescribeFileSystemsResponseTypeDef",
    {
        "FileSystems": List[FileSystemTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateFileSystemFromBackupRequestRequestTypeDef = TypedDict(
    "CreateFileSystemFromBackupRequestRequestTypeDef",
    {
        "BackupId": str,
        "SubnetIds": Sequence[str],
        "ClientRequestToken": NotRequired[str],
        "SecurityGroupIds": NotRequired[Sequence[str]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "WindowsConfiguration": NotRequired[CreateFileSystemWindowsConfigurationTypeDef],
        "LustreConfiguration": NotRequired[CreateFileSystemLustreConfigurationTypeDef],
        "StorageType": NotRequired[StorageTypeType],
        "KmsKeyId": NotRequired[str],
        "FileSystemTypeVersion": NotRequired[str],
        "OpenZFSConfiguration": NotRequired[CreateFileSystemOpenZFSConfigurationTypeDef],
        "StorageCapacity": NotRequired[int],
    },
)

CreateFileSystemRequestRequestTypeDef = TypedDict(
    "CreateFileSystemRequestRequestTypeDef",
    {
        "FileSystemType": FileSystemTypeType,
        "StorageCapacity": int,
        "SubnetIds": Sequence[str],
        "ClientRequestToken": NotRequired[str],
        "StorageType": NotRequired[StorageTypeType],
        "SecurityGroupIds": NotRequired[Sequence[str]],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "KmsKeyId": NotRequired[str],
        "WindowsConfiguration": NotRequired[CreateFileSystemWindowsConfigurationTypeDef],
        "LustreConfiguration": NotRequired[CreateFileSystemLustreConfigurationTypeDef],
        "OntapConfiguration": NotRequired[CreateFileSystemOntapConfigurationTypeDef],
        "FileSystemTypeVersion": NotRequired[str],
        "OpenZFSConfiguration": NotRequired[CreateFileSystemOpenZFSConfigurationTypeDef],
    },
)

CreateVolumeFromBackupRequestRequestTypeDef = TypedDict(
    "CreateVolumeFromBackupRequestRequestTypeDef",
    {
        "BackupId": str,
        "Name": str,
        "ClientRequestToken": NotRequired[str],
        "OntapConfiguration": NotRequired[CreateOntapVolumeConfigurationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
    },
)

CreateVolumeRequestRequestTypeDef = TypedDict(
    "CreateVolumeRequestRequestTypeDef",
    {
        "VolumeType": VolumeTypeType,
        "Name": str,
        "ClientRequestToken": NotRequired[str],
        "OntapConfiguration": NotRequired[CreateOntapVolumeConfigurationTypeDef],
        "Tags": NotRequired[Sequence[TagTypeDef]],
        "OpenZFSConfiguration": NotRequired[CreateOpenZFSVolumeConfigurationTypeDef],
    },
)

VolumeTypeDef = TypedDict(
    "VolumeTypeDef",
    {
        "CreationTime": NotRequired[datetime],
        "FileSystemId": NotRequired[str],
        "Lifecycle": NotRequired[VolumeLifecycleType],
        "Name": NotRequired[str],
        "OntapConfiguration": NotRequired[OntapVolumeConfigurationTypeDef],
        "ResourceARN": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "VolumeId": NotRequired[str],
        "VolumeType": NotRequired[VolumeTypeType],
        "LifecycleTransitionReason": NotRequired[LifecycleTransitionReasonTypeDef],
        "AdministrativeActions": NotRequired[List["AdministrativeActionTypeDef"]],
        "OpenZFSConfiguration": NotRequired[OpenZFSVolumeConfigurationTypeDef],
    },
)

UpdateVolumeRequestRequestTypeDef = TypedDict(
    "UpdateVolumeRequestRequestTypeDef",
    {
        "VolumeId": str,
        "ClientRequestToken": NotRequired[str],
        "OntapConfiguration": NotRequired[UpdateOntapVolumeConfigurationTypeDef],
        "Name": NotRequired[str],
        "OpenZFSConfiguration": NotRequired[UpdateOpenZFSVolumeConfigurationTypeDef],
    },
)

AdministrativeActionTypeDef = TypedDict(
    "AdministrativeActionTypeDef",
    {
        "AdministrativeActionType": NotRequired[AdministrativeActionTypeType],
        "ProgressPercent": NotRequired[int],
        "RequestTime": NotRequired[datetime],
        "Status": NotRequired[StatusType],
        "TargetFileSystemValues": NotRequired[Dict[str, Any]],
        "FailureDetails": NotRequired[AdministrativeActionFailureDetailsTypeDef],
        "TargetVolumeValues": NotRequired[Dict[str, Any]],
        "TargetSnapshotValues": NotRequired[Dict[str, Any]],
    },
)

BackupTypeDef = TypedDict(
    "BackupTypeDef",
    {
        "BackupId": str,
        "Lifecycle": BackupLifecycleType,
        "Type": BackupTypeType,
        "CreationTime": datetime,
        "FileSystem": "FileSystemTypeDef",
        "FailureDetails": NotRequired[BackupFailureDetailsTypeDef],
        "ProgressPercent": NotRequired[int],
        "KmsKeyId": NotRequired[str],
        "ResourceARN": NotRequired[str],
        "Tags": NotRequired[List[TagTypeDef]],
        "DirectoryInformation": NotRequired[ActiveDirectoryBackupAttributesTypeDef],
        "OwnerId": NotRequired[str],
        "SourceBackupId": NotRequired[str],
        "SourceBackupRegion": NotRequired[str],
        "ResourceType": NotRequired[ResourceTypeType],
        "Volume": NotRequired[VolumeTypeDef],
    },
)

CreateVolumeFromBackupResponseTypeDef = TypedDict(
    "CreateVolumeFromBackupResponseTypeDef",
    {
        "Volume": VolumeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateVolumeResponseTypeDef = TypedDict(
    "CreateVolumeResponseTypeDef",
    {
        "Volume": VolumeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeVolumesResponseTypeDef = TypedDict(
    "DescribeVolumesResponseTypeDef",
    {
        "Volumes": List[VolumeTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

UpdateVolumeResponseTypeDef = TypedDict(
    "UpdateVolumeResponseTypeDef",
    {
        "Volume": VolumeTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CopyBackupResponseTypeDef = TypedDict(
    "CopyBackupResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

CreateBackupResponseTypeDef = TypedDict(
    "CreateBackupResponseTypeDef",
    {
        "Backup": BackupTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

DescribeBackupsResponseTypeDef = TypedDict(
    "DescribeBackupsResponseTypeDef",
    {
        "Backups": List[BackupTypeDef],
        "NextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
