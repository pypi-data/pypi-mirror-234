'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class AzIdToNameMapping(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-multi-account-az-mapping.AzIdToNameMapping",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        az_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_code: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Code] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        ssm_parameter_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param az_ids: The target AZ IDs for mapping. Defaults to values for 3 zones in us-east-1. Default: ['use1-az2', 'use1-az4', 'use1-az6']
        :param lambda_code: The lambda function code to use for the custom resource. For most use cases this should be left as the default, but in cases where the custom resource needs to be deployed through something like CloudFormation StackSets you may need to source the lambda function code from S3 or some other location because the CDK cant upload the local code to the correct asset location for the StackSet target accounts. You can use the included ``AzIdToNameMappingFunctionCodeCache`` class to cache the lambda function code in S3 and create a cross account access policy to allow the StackSet target accounts to access the code. Default: - default lambda function code
        :param log_retention: The number of days to retain log events in CloudWatch logs. Defaults to 30 days. Default: logs.RetentionDays.ONE_MONTH
        :param ssm_parameter_prefix: The prefix to use for the SSM parameter names. Defaults to ``/az-mapping/``. Default: '/az-mapping/'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8e01f1331094aea4f29fcdf1c20c5b0d4600dafd77865a5c3bfc70a4779f1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AzIdToNameMappingProps(
            az_ids=az_ids,
            lambda_code=lambda_code,
            log_retention=log_retention,
            ssm_parameter_prefix=ssm_parameter_prefix,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="mapping")
    def mapping(self) -> builtins.str:
        '''The resulting mapping of AZ IDs to names.'''
        return typing.cast(builtins.str, jsii.get(self, "mapping"))


class AzIdToNameMappingFunctionCodeCache(
    _aws_cdk_aws_s3_ceddda9d.Bucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-multi-account-az-mapping.AzIdToNameMappingFunctionCodeCache",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
        minimum_tls_version: typing.Optional[jsii.Number] = None,
        notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
        object_lock_enabled: typing.Optional[builtins.bool] = None,
        object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
        website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption. - If not enabled, every object GET and PUT will cause an API call to KMS (with the attendant cost implications of that). - If enabled, S3 will use its own time-limited key instead. Only relevant, when Encryption is set to ``BucketEncryption.KMS`` or ``BucketEncryption.KMS_MANAGED``. Default: - false
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``KMS`` if ``encryptionKey`` is specified, or ``UNENCRYPTED`` otherwise. But if ``UNENCRYPTED`` is specified, the bucket will be encrypted as ``S3_MANAGED`` automatically.
        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``. An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param minimum_tls_version: Enforces minimum TLS version for requests. Requires ``enforceSSL`` to be enabled. Default: No minimum TLS version is enforced.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_lock_default_retention: The default retention mode and rules for S3 Object Lock. Default retention can be configured after a bucket is created if the bucket already has object lock enabled. Enabling object lock for existing buckets is not supported. Default: no default retention period
        :param object_lock_enabled: Enable object lock on the bucket. Enabling object lock for existing buckets is not supported. Object lock must be enabled when the bucket is created. Default: false, unless objectLockDefaultRetention is set (then, true)
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false (unless object lock is enabled, then true)
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0286c5a0bb3bbd367d20438a3255377055c5be754bfa7c2b12a0e7fe181b7319)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AzIdToNameMappingFunctionCodeCacheProps(
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            event_bridge_enabled=event_bridge_enabled,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            minimum_tls_version=minimum_tls_version,
            notifications_handler_role=notifications_handler_role,
            object_lock_default_retention=object_lock_default_retention,
            object_lock_enabled=object_lock_enabled,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            transfer_acceleration=transfer_acceleration,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAccountAccessPolicy")
    def add_account_access_policy(
        self,
        principal_account_id: builtins.str,
        principal_org_id: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult:
        '''Add access to the specified accounts to get the lambda function code from the bucket.

        :param principal_account_id: The account ID to add access for.
        :param principal_org_id: (Optional) The organization ID to require for the account accessing the bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57887c79ec80538fb4240ebc0f5773350c590c2f67e62641da25a7271b394351)
            check_type(argname="argument principal_account_id", value=principal_account_id, expected_type=type_hints["principal_account_id"])
            check_type(argname="argument principal_org_id", value=principal_org_id, expected_type=type_hints["principal_org_id"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult, jsii.invoke(self, "addAccountAccessPolicy", [principal_account_id, principal_org_id]))

    @jsii.member(jsii_name="addOrgOuAccessPolicy")
    def add_org_ou_access_policy(
        self,
        principal_org_paths: typing.Sequence[builtins.str],
    ) -> _aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult:
        '''Add access to the specified organizational units to get the lambda function code from the bucket.

        :param principal_org_paths: The organizational unit paths to add access for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f30fd0263fdf8f4be5544afc4fa397c3a320aefb1359face6d8cb4dc1ba65f)
            check_type(argname="argument principal_org_paths", value=principal_org_paths, expected_type=type_hints["principal_org_paths"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult, jsii.invoke(self, "addOrgOuAccessPolicy", [principal_org_paths]))

    @jsii.member(jsii_name="addOrgWideAccessPolicy")
    def add_org_wide_access_policy(
        self,
        principal_org_id: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult:
        '''Add access to the whole organization to get the lambda function code from the bucket.

        :param principal_org_id: The organization ID to require for any accounts accessing the bucket.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18f613feeeb6bdb710f8340efe63f8f5cf66f75a986b1d13bb978b1500473f9)
            check_type(argname="argument principal_org_id", value=principal_org_id, expected_type=type_hints["principal_org_id"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult, jsii.invoke(self, "addOrgWideAccessPolicy", [principal_org_id]))

    @builtins.property
    @jsii.member(jsii_name="lambdaCode")
    def lambda_code(self) -> _aws_cdk_aws_lambda_ceddda9d.Code:
        '''The lambda.Code object that represents the contents of the bucket.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Code, jsii.get(self, "lambdaCode"))


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-multi-account-az-mapping.AzIdToNameMappingFunctionCodeCacheProps",
    jsii_struct_bases=[_aws_cdk_aws_s3_ceddda9d.BucketProps],
    name_mapping={
        "access_control": "accessControl",
        "auto_delete_objects": "autoDeleteObjects",
        "block_public_access": "blockPublicAccess",
        "bucket_key_enabled": "bucketKeyEnabled",
        "bucket_name": "bucketName",
        "cors": "cors",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "enforce_ssl": "enforceSSL",
        "event_bridge_enabled": "eventBridgeEnabled",
        "intelligent_tiering_configurations": "intelligentTieringConfigurations",
        "inventories": "inventories",
        "lifecycle_rules": "lifecycleRules",
        "metrics": "metrics",
        "minimum_tls_version": "minimumTLSVersion",
        "notifications_handler_role": "notificationsHandlerRole",
        "object_lock_default_retention": "objectLockDefaultRetention",
        "object_lock_enabled": "objectLockEnabled",
        "object_ownership": "objectOwnership",
        "public_read_access": "publicReadAccess",
        "removal_policy": "removalPolicy",
        "server_access_logs_bucket": "serverAccessLogsBucket",
        "server_access_logs_prefix": "serverAccessLogsPrefix",
        "transfer_acceleration": "transferAcceleration",
        "versioned": "versioned",
        "website_error_document": "websiteErrorDocument",
        "website_index_document": "websiteIndexDocument",
        "website_redirect": "websiteRedirect",
        "website_routing_rules": "websiteRoutingRules",
    },
)
class AzIdToNameMappingFunctionCodeCacheProps(_aws_cdk_aws_s3_ceddda9d.BucketProps):
    def __init__(
        self,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
        minimum_tls_version: typing.Optional[jsii.Number] = None,
        notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
        object_lock_enabled: typing.Optional[builtins.bool] = None,
        object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
        website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption. - If not enabled, every object GET and PUT will cause an API call to KMS (with the attendant cost implications of that). - If enabled, S3 will use its own time-limited key instead. Only relevant, when Encryption is set to ``BucketEncryption.KMS`` or ``BucketEncryption.KMS_MANAGED``. Default: - false
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``KMS`` if ``encryptionKey`` is specified, or ``UNENCRYPTED`` otherwise. But if ``UNENCRYPTED`` is specified, the bucket will be encrypted as ``S3_MANAGED`` automatically.
        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``. An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param minimum_tls_version: Enforces minimum TLS version for requests. Requires ``enforceSSL`` to be enabled. Default: No minimum TLS version is enforced.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_lock_default_retention: The default retention mode and rules for S3 Object Lock. Default retention can be configured after a bucket is created if the bucket already has object lock enabled. Enabling object lock for existing buckets is not supported. Default: no default retention period
        :param object_lock_enabled: Enable object lock on the bucket. Enabling object lock for existing buckets is not supported. Object lock must be enabled when the bucket is created. Default: false, unless objectLockDefaultRetention is set (then, true)
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false (unless object lock is enabled, then true)
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.
        '''
        if isinstance(website_redirect, dict):
            website_redirect = _aws_cdk_aws_s3_ceddda9d.RedirectTarget(**website_redirect)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b89de7e5433dd290acdfe05af4fbf8cd5750d22052a2fb662e2b13166af413)
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument auto_delete_objects", value=auto_delete_objects, expected_type=type_hints["auto_delete_objects"])
            check_type(argname="argument block_public_access", value=block_public_access, expected_type=type_hints["block_public_access"])
            check_type(argname="argument bucket_key_enabled", value=bucket_key_enabled, expected_type=type_hints["bucket_key_enabled"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument enforce_ssl", value=enforce_ssl, expected_type=type_hints["enforce_ssl"])
            check_type(argname="argument event_bridge_enabled", value=event_bridge_enabled, expected_type=type_hints["event_bridge_enabled"])
            check_type(argname="argument intelligent_tiering_configurations", value=intelligent_tiering_configurations, expected_type=type_hints["intelligent_tiering_configurations"])
            check_type(argname="argument inventories", value=inventories, expected_type=type_hints["inventories"])
            check_type(argname="argument lifecycle_rules", value=lifecycle_rules, expected_type=type_hints["lifecycle_rules"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
            check_type(argname="argument minimum_tls_version", value=minimum_tls_version, expected_type=type_hints["minimum_tls_version"])
            check_type(argname="argument notifications_handler_role", value=notifications_handler_role, expected_type=type_hints["notifications_handler_role"])
            check_type(argname="argument object_lock_default_retention", value=object_lock_default_retention, expected_type=type_hints["object_lock_default_retention"])
            check_type(argname="argument object_lock_enabled", value=object_lock_enabled, expected_type=type_hints["object_lock_enabled"])
            check_type(argname="argument object_ownership", value=object_ownership, expected_type=type_hints["object_ownership"])
            check_type(argname="argument public_read_access", value=public_read_access, expected_type=type_hints["public_read_access"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument server_access_logs_bucket", value=server_access_logs_bucket, expected_type=type_hints["server_access_logs_bucket"])
            check_type(argname="argument server_access_logs_prefix", value=server_access_logs_prefix, expected_type=type_hints["server_access_logs_prefix"])
            check_type(argname="argument transfer_acceleration", value=transfer_acceleration, expected_type=type_hints["transfer_acceleration"])
            check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
            check_type(argname="argument website_error_document", value=website_error_document, expected_type=type_hints["website_error_document"])
            check_type(argname="argument website_index_document", value=website_index_document, expected_type=type_hints["website_index_document"])
            check_type(argname="argument website_redirect", value=website_redirect, expected_type=type_hints["website_redirect"])
            check_type(argname="argument website_routing_rules", value=website_routing_rules, expected_type=type_hints["website_routing_rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if access_control is not None:
            self._values["access_control"] = access_control
        if auto_delete_objects is not None:
            self._values["auto_delete_objects"] = auto_delete_objects
        if block_public_access is not None:
            self._values["block_public_access"] = block_public_access
        if bucket_key_enabled is not None:
            self._values["bucket_key_enabled"] = bucket_key_enabled
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if cors is not None:
            self._values["cors"] = cors
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if enforce_ssl is not None:
            self._values["enforce_ssl"] = enforce_ssl
        if event_bridge_enabled is not None:
            self._values["event_bridge_enabled"] = event_bridge_enabled
        if intelligent_tiering_configurations is not None:
            self._values["intelligent_tiering_configurations"] = intelligent_tiering_configurations
        if inventories is not None:
            self._values["inventories"] = inventories
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if metrics is not None:
            self._values["metrics"] = metrics
        if minimum_tls_version is not None:
            self._values["minimum_tls_version"] = minimum_tls_version
        if notifications_handler_role is not None:
            self._values["notifications_handler_role"] = notifications_handler_role
        if object_lock_default_retention is not None:
            self._values["object_lock_default_retention"] = object_lock_default_retention
        if object_lock_enabled is not None:
            self._values["object_lock_enabled"] = object_lock_enabled
        if object_ownership is not None:
            self._values["object_ownership"] = object_ownership
        if public_read_access is not None:
            self._values["public_read_access"] = public_read_access
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if server_access_logs_bucket is not None:
            self._values["server_access_logs_bucket"] = server_access_logs_bucket
        if server_access_logs_prefix is not None:
            self._values["server_access_logs_prefix"] = server_access_logs_prefix
        if transfer_acceleration is not None:
            self._values["transfer_acceleration"] = transfer_acceleration
        if versioned is not None:
            self._values["versioned"] = versioned
        if website_error_document is not None:
            self._values["website_error_document"] = website_error_document
        if website_index_document is not None:
            self._values["website_index_document"] = website_index_document
        if website_redirect is not None:
            self._values["website_redirect"] = website_redirect
        if website_routing_rules is not None:
            self._values["website_routing_rules"] = website_routing_rules

    @builtins.property
    def access_control(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl]:
        '''Specifies a canned ACL that grants predefined permissions to the bucket.

        :default: BucketAccessControl.PRIVATE
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl], result)

    @builtins.property
    def auto_delete_objects(self) -> typing.Optional[builtins.bool]:
        '''Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted.

        Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``.

        **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``,
        switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to
        all objects in the bucket being deleted. Be sure to update your bucket resources
        by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``.

        :default: false
        '''
        result = self._values.get("auto_delete_objects")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def block_public_access(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess]:
        '''The block public access configuration of this bucket.

        :default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
        '''
        result = self._values.get("block_public_access")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess], result)

    @builtins.property
    def bucket_key_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether Amazon S3 should use its own intermediary key to generate data keys.

        Only relevant when using KMS for encryption.

        - If not enabled, every object GET and PUT will cause an API call to KMS (with the
          attendant cost implications of that).
        - If enabled, S3 will use its own time-limited key instead.

        Only relevant, when Encryption is set to ``BucketEncryption.KMS`` or ``BucketEncryption.KMS_MANAGED``.

        :default: - false
        '''
        result = self._values.get("bucket_key_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''Physical name of this bucket.

        :default: - Assigned by CloudFormation (recommended).
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(self) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]]:
        '''The CORS configuration of this bucket.

        :default: - No CORS configuration.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-cors.html
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]], result)

    @builtins.property
    def encryption(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption]:
        '''The kind of server-side encryption to apply to this bucket.

        If you choose KMS, you can specify a KMS key via ``encryptionKey``. If
        encryption key is not specified, a key will automatically be created.

        :default:

        - ``KMS`` if ``encryptionKey`` is specified, or ``UNENCRYPTED`` otherwise.
        But if ``UNENCRYPTED`` is specified, the bucket will be encrypted as ``S3_MANAGED`` automatically.
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''External KMS key to use for bucket encryption.

        The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``.
        An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``.

        :default:

        - If ``encryption`` is set to ``KMS`` and this property is undefined,
        a new KMS key will be created and associated with this bucket.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def enforce_ssl(self) -> typing.Optional[builtins.bool]:
        '''Enforces SSL for requests.

        S3.5 of the AWS Foundational Security Best Practices Regarding S3.

        :default: false

        :see: https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-ssl-requests-only.html
        '''
        result = self._values.get("enforce_ssl")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_bridge_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether this bucket should send notifications to Amazon EventBridge or not.

        :default: false
        '''
        result = self._values.get("event_bridge_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def intelligent_tiering_configurations(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration]]:
        '''Inteligent Tiering Configurations.

        :default: No Intelligent Tiiering Configurations.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/intelligent-tiering.html
        '''
        result = self._values.get("intelligent_tiering_configurations")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration]], result)

    @builtins.property
    def inventories(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.Inventory]]:
        '''The inventory configuration of the bucket.

        :default: - No inventory configuration

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-inventory.html
        '''
        result = self._values.get("inventories")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.Inventory]], result)

    @builtins.property
    def lifecycle_rules(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.LifecycleRule]]:
        '''Rules that define how Amazon S3 manages objects during their lifetime.

        :default: - No lifecycle rules.
        '''
        result = self._values.get("lifecycle_rules")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.LifecycleRule]], result)

    @builtins.property
    def metrics(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.BucketMetrics]]:
        '''The metrics configuration of this bucket.

        :default: - No metrics configuration.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-s3-bucket-metricsconfiguration.html
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.BucketMetrics]], result)

    @builtins.property
    def minimum_tls_version(self) -> typing.Optional[jsii.Number]:
        '''Enforces minimum TLS version for requests.

        Requires ``enforceSSL`` to be enabled.

        :default: No minimum TLS version is enforced.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html#example-object-tls-version
        '''
        result = self._values.get("minimum_tls_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notifications_handler_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The role to be used by the notifications handler.

        :default: - a new role will be created.
        '''
        result = self._values.get("notifications_handler_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def object_lock_default_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention]:
        '''The default retention mode and rules for S3 Object Lock.

        Default retention can be configured after a bucket is created if the bucket already
        has object lock enabled. Enabling object lock for existing buckets is not supported.

        :default: no default retention period

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html#object-lock-bucket-config-enable
        '''
        result = self._values.get("object_lock_default_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention], result)

    @builtins.property
    def object_lock_enabled(self) -> typing.Optional[builtins.bool]:
        '''Enable object lock on the bucket.

        Enabling object lock for existing buckets is not supported. Object lock must be
        enabled when the bucket is created.

        :default: false, unless objectLockDefaultRetention is set (then, true)

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock-overview.html#object-lock-bucket-config-enable
        '''
        result = self._values.get("object_lock_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def object_ownership(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership]:
        '''The objectOwnership of the bucket.

        :default: - No ObjectOwnership configuration, uploading account will own the object.

        :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/about-object-ownership.html
        '''
        result = self._values.get("object_ownership")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership], result)

    @builtins.property
    def public_read_access(self) -> typing.Optional[builtins.bool]:
        '''Grants public read access to all objects in the bucket.

        Similar to calling ``bucket.grantPublicAccess()``

        :default: false
        '''
        result = self._values.get("public_read_access")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Policy to apply when the bucket is removed from this stack.

        :default: - The bucket will be orphaned.
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def server_access_logs_bucket(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''Destination bucket for the server access logs.

        :default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        '''
        result = self._values.get("server_access_logs_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def server_access_logs_prefix(self) -> typing.Optional[builtins.str]:
        '''Optional log file prefix to use for the bucket's access logs.

        If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix.

        :default: - No log file prefix
        '''
        result = self._values.get("server_access_logs_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transfer_acceleration(self) -> typing.Optional[builtins.bool]:
        '''Whether this bucket should have transfer acceleration turned on or not.

        :default: false
        '''
        result = self._values.get("transfer_acceleration")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def versioned(self) -> typing.Optional[builtins.bool]:
        '''Whether this bucket should have versioning turned on or not.

        :default: false (unless object lock is enabled, then true)
        '''
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def website_error_document(self) -> typing.Optional[builtins.str]:
        '''The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set.

        :default: - No error document.
        '''
        result = self._values.get("website_error_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website_index_document(self) -> typing.Optional[builtins.str]:
        '''The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket.

        :default: - No index document.
        '''
        result = self._values.get("website_index_document")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def website_redirect(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.RedirectTarget]:
        '''Specifies the redirect behavior of all requests to a website endpoint of a bucket.

        If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules".

        :default: - No redirection.
        '''
        result = self._values.get("website_redirect")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.RedirectTarget], result)

    @builtins.property
    def website_routing_rules(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.RoutingRule]]:
        '''Rules that define when a redirect is applied and the redirect behavior.

        :default: - No redirection rules.
        '''
        result = self._values.get("website_routing_rules")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.RoutingRule]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzIdToNameMappingFunctionCodeCacheProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@renovosolutions/cdk-library-multi-account-az-mapping.AzIdToNameMappingProps",
    jsii_struct_bases=[],
    name_mapping={
        "az_ids": "azIds",
        "lambda_code": "lambdaCode",
        "log_retention": "logRetention",
        "ssm_parameter_prefix": "ssmParameterPrefix",
    },
)
class AzIdToNameMappingProps:
    def __init__(
        self,
        *,
        az_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        lambda_code: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Code] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        ssm_parameter_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The properties of a new AZ ID to name mapping.

        :param az_ids: The target AZ IDs for mapping. Defaults to values for 3 zones in us-east-1. Default: ['use1-az2', 'use1-az4', 'use1-az6']
        :param lambda_code: The lambda function code to use for the custom resource. For most use cases this should be left as the default, but in cases where the custom resource needs to be deployed through something like CloudFormation StackSets you may need to source the lambda function code from S3 or some other location because the CDK cant upload the local code to the correct asset location for the StackSet target accounts. You can use the included ``AzIdToNameMappingFunctionCodeCache`` class to cache the lambda function code in S3 and create a cross account access policy to allow the StackSet target accounts to access the code. Default: - default lambda function code
        :param log_retention: The number of days to retain log events in CloudWatch logs. Defaults to 30 days. Default: logs.RetentionDays.ONE_MONTH
        :param ssm_parameter_prefix: The prefix to use for the SSM parameter names. Defaults to ``/az-mapping/``. Default: '/az-mapping/'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c15575ce63eee4acf10333bc7c3ac0aabb639dfb8e41183cddd7e624e1931e)
            check_type(argname="argument az_ids", value=az_ids, expected_type=type_hints["az_ids"])
            check_type(argname="argument lambda_code", value=lambda_code, expected_type=type_hints["lambda_code"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument ssm_parameter_prefix", value=ssm_parameter_prefix, expected_type=type_hints["ssm_parameter_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if az_ids is not None:
            self._values["az_ids"] = az_ids
        if lambda_code is not None:
            self._values["lambda_code"] = lambda_code
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if ssm_parameter_prefix is not None:
            self._values["ssm_parameter_prefix"] = ssm_parameter_prefix

    @builtins.property
    def az_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The target AZ IDs for mapping.

        Defaults to values for 3 zones in us-east-1.

        :default: ['use1-az2', 'use1-az4', 'use1-az6']
        '''
        result = self._values.get("az_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def lambda_code(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Code]:
        '''The lambda function code to use for the custom resource.

        For most use cases this should be left as the default, but
        in cases where the custom resource needs to be deployed through
        something like CloudFormation StackSets you may need to source
        the lambda function code from S3 or some other location because
        the CDK cant upload the local code to the correct asset location
        for the StackSet target accounts.

        You can use the included ``AzIdToNameMappingFunctionCodeCache`` class to
        cache the lambda function code in S3 and create a cross
        account access policy to allow the StackSet target accounts
        to access the code.

        :default: - default lambda function code
        '''
        result = self._values.get("lambda_code")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Code], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''The number of days to retain log events in CloudWatch logs.

        Defaults to 30 days.

        :default: logs.RetentionDays.ONE_MONTH
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def ssm_parameter_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix to use for the SSM parameter names.

        Defaults to ``/az-mapping/``.

        :default: '/az-mapping/'
        '''
        result = self._values.get("ssm_parameter_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzIdToNameMappingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AzIdToNameMapping",
    "AzIdToNameMappingFunctionCodeCache",
    "AzIdToNameMappingFunctionCodeCacheProps",
    "AzIdToNameMappingProps",
]

publication.publish()

def _typecheckingstub__7f8e01f1331094aea4f29fcdf1c20c5b0d4600dafd77865a5c3bfc70a4779f1e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    az_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_code: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Code] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ssm_parameter_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0286c5a0bb3bbd367d20438a3255377055c5be754bfa7c2b12a0e7fe181b7319(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    auto_delete_objects: typing.Optional[builtins.bool] = None,
    block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
    bucket_key_enabled: typing.Optional[builtins.bool] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_tls_version: typing.Optional[jsii.Number] = None,
    notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
    object_lock_enabled: typing.Optional[builtins.bool] = None,
    object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
    public_read_access: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    server_access_logs_prefix: typing.Optional[builtins.str] = None,
    transfer_acceleration: typing.Optional[builtins.bool] = None,
    versioned: typing.Optional[builtins.bool] = None,
    website_error_document: typing.Optional[builtins.str] = None,
    website_index_document: typing.Optional[builtins.str] = None,
    website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57887c79ec80538fb4240ebc0f5773350c590c2f67e62641da25a7271b394351(
    principal_account_id: builtins.str,
    principal_org_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f30fd0263fdf8f4be5544afc4fa397c3a320aefb1359face6d8cb4dc1ba65f(
    principal_org_paths: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18f613feeeb6bdb710f8340efe63f8f5cf66f75a986b1d13bb978b1500473f9(
    principal_org_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b89de7e5433dd290acdfe05af4fbf8cd5750d22052a2fb662e2b13166af413(
    *,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    auto_delete_objects: typing.Optional[builtins.bool] = None,
    block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
    bucket_key_enabled: typing.Optional[builtins.bool] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
    minimum_tls_version: typing.Optional[jsii.Number] = None,
    notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
    object_lock_enabled: typing.Optional[builtins.bool] = None,
    object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
    public_read_access: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    server_access_logs_prefix: typing.Optional[builtins.str] = None,
    transfer_acceleration: typing.Optional[builtins.bool] = None,
    versioned: typing.Optional[builtins.bool] = None,
    website_error_document: typing.Optional[builtins.str] = None,
    website_index_document: typing.Optional[builtins.str] = None,
    website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c15575ce63eee4acf10333bc7c3ac0aabb639dfb8e41183cddd7e624e1931e(
    *,
    az_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    lambda_code: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Code] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    ssm_parameter_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
