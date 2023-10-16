'''
# AWS Data Solutions Framework
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
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_emrserverless as _aws_cdk_aws_emrserverless_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_glue as _aws_cdk_aws_glue_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import aws_cdk.aws_stepfunctions_tasks as _aws_cdk_aws_stepfunctions_tasks_ceddda9d
import aws_cdk.pipelines as _aws_cdk_pipelines_ceddda9d
import constructs as _constructs_77d1e7e8


class AccessLogsBucket(
    _aws_cdk_aws_s3_ceddda9d.Bucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.AccessLogsBucket",
):
    '''Amazon S3 Bucket configured with best-practices and smart defaults for storing S3 access logs.

    Default bucket name is ``accesslogs-<AWS_ACCOUNT_ID>-<AWS_REGION>-<UNIQUE_ID>``

    Example::

        import * as cdk from 'aws-cdk-lib';
        import { AccessLogsBucket } from 'aws-data-solutions-framework';
        
        const bucket = new AccessLogsBucket(this, 'AccessLogsBucket', {
         removalPolicy: RemovalPolicy.DESTROY,
        })
    '''

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
            type_hints = typing.get_type_hints(_typecheckingstub__6cd670a2e4f6f35ed3e5c5e824d5bff99861b579300bfab5042dade48d9e4813)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_aws_s3_ceddda9d.BucketProps(
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


class AnalyticsBucket(
    _aws_cdk_aws_s3_ceddda9d.Bucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.AnalyticsBucket",
):
    '''Amazon S3 Bucket configured with best-practices and defaults for analytics.

    The default bucket name is ``analytics-<AWS_ACCOUNT_ID>-<AWS_REGION>-<UNIQUE_ID>``
    See documentation TODO insert link

    Example::

        import * as cdk from 'aws-cdk-lib';
        import { AnalyticsBucket} from 'aws-data-solutions-framework';
        
        const exampleApp = new cdk.App();
        const stack = new cdk.Stack(exampleApp, 'AnalyticsBucketStack');
        
        // Set context value for global data removal policy (or set in cdk.json).
        stack.node.setContext('@aws-data-solutions-framework/removeDataOnDestroy', true);
        
        const encryptionKey = new Key(stack, 'DataKey', {
         removalPolicy: RemovalPolicy.DESTROY,
         enableKeyRotation: true,
        });
        
        new AnalyticsBucket(stack, 'MyAnalyticsBucket', {
         encryptionKey,
         removalPolicy: cdk.RemovalPolicy.DESTROY,
        });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
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
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``. An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption. - If not enabled, every object GET and PUT will cause an API call to KMS (with the attendant cost implications of that). - If enabled, S3 will use its own time-limited key instead. Only relevant, when Encryption is set to ``BucketEncryption.KMS`` or ``BucketEncryption.KMS_MANAGED``. Default: - false
        :param bucket_name: Physical name of this bucket. Default: - ``analytics-<AWS_ACCOUNT_ID>-<AWS_REGION>-<UNIQUE_ID>``
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_lock_default_retention: The default retention mode and rules for S3 Object Lock. Default retention can be configured after a bucket is created if the bucket already has object lock enabled. Enabling object lock for existing buckets is not supported. Default: no default retention period
        :param object_lock_enabled: Enable object lock on the bucket. Enabling object lock for existing buckets is not supported. Object lock must be enabled when the bucket is created. Default: false, unless objectLockDefaultRetention is set (then, true)
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. - @default - RETAIN (The bucket will be orphaned).
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false (unless object lock is enabled, then true)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acfe28de1a351d3b74ce12685045de02c577e5c7744874cf54a19363d72440cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AnalyticsBucketProps(
            encryption_key=encryption_key,
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            enforce_ssl=enforce_ssl,
            event_bridge_enabled=event_bridge_enabled,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
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
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="aws-dsf.AnalyticsBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "encryption_key": "encryptionKey",
        "access_control": "accessControl",
        "auto_delete_objects": "autoDeleteObjects",
        "block_public_access": "blockPublicAccess",
        "bucket_key_enabled": "bucketKeyEnabled",
        "bucket_name": "bucketName",
        "cors": "cors",
        "enforce_ssl": "enforceSSL",
        "event_bridge_enabled": "eventBridgeEnabled",
        "intelligent_tiering_configurations": "intelligentTieringConfigurations",
        "inventories": "inventories",
        "lifecycle_rules": "lifecycleRules",
        "metrics": "metrics",
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
    },
)
class AnalyticsBucketProps:
    def __init__(
        self,
        *,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
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
    ) -> None:
        '''Properties of the {@link AnalyticsBucket } construct.

        :param encryption_key: External KMS key to use for bucket encryption. The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``. An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``. Default: - If ``encryption`` is set to ``KMS`` and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption. - If not enabled, every object GET and PUT will cause an API call to KMS (with the attendant cost implications of that). - If enabled, S3 will use its own time-limited key instead. Only relevant, when Encryption is set to ``BucketEncryption.KMS`` or ``BucketEncryption.KMS_MANAGED``. Default: - false
        :param bucket_name: Physical name of this bucket. Default: - ``analytics-<AWS_ACCOUNT_ID>-<AWS_REGION>-<UNIQUE_ID>``
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_lock_default_retention: The default retention mode and rules for S3 Object Lock. Default retention can be configured after a bucket is created if the bucket already has object lock enabled. Enabling object lock for existing buckets is not supported. Default: no default retention period
        :param object_lock_enabled: Enable object lock on the bucket. Enabling object lock for existing buckets is not supported. Object lock must be enabled when the bucket is created. Default: false, unless objectLockDefaultRetention is set (then, true)
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. - @default - RETAIN (The bucket will be orphaned).
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false (unless object lock is enabled, then true)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85b197b6c67a05f3e6a882742f146f37555d0a9a6316895eaddd94ffc5a44a28)
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument auto_delete_objects", value=auto_delete_objects, expected_type=type_hints["auto_delete_objects"])
            check_type(argname="argument block_public_access", value=block_public_access, expected_type=type_hints["block_public_access"])
            check_type(argname="argument bucket_key_enabled", value=bucket_key_enabled, expected_type=type_hints["bucket_key_enabled"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument enforce_ssl", value=enforce_ssl, expected_type=type_hints["enforce_ssl"])
            check_type(argname="argument event_bridge_enabled", value=event_bridge_enabled, expected_type=type_hints["event_bridge_enabled"])
            check_type(argname="argument intelligent_tiering_configurations", value=intelligent_tiering_configurations, expected_type=type_hints["intelligent_tiering_configurations"])
            check_type(argname="argument inventories", value=inventories, expected_type=type_hints["inventories"])
            check_type(argname="argument lifecycle_rules", value=lifecycle_rules, expected_type=type_hints["lifecycle_rules"])
            check_type(argname="argument metrics", value=metrics, expected_type=type_hints["metrics"])
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
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "encryption_key": encryption_key,
        }
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

    @builtins.property
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        '''External KMS key to use for bucket encryption.

        The ``encryption`` property must be either not specified or set to ``KMS`` or ``DSSE``.
        An error will be emitted if ``encryption`` is set to ``UNENCRYPTED`` or ``S3_MANAGED``.

        :default:

        - If ``encryption`` is set to ``KMS`` and this property is undefined,
        a new KMS key will be created and associated with this bucket.
        '''
        result = self._values.get("encryption_key")
        assert result is not None, "Required property 'encryption_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, result)

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

        :default:

        - CloudFormation defaults will apply. New buckets and objects don't allow public access,
        but users can modify bucket policies or object permissions to allow public access
        '''
        result = self._values.get("block_public_access")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess], result)

    @builtins.property
    def bucket_key_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption.

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

        :default: - ``analytics-<AWS_ACCOUNT_ID>-<AWS_REGION>-<UNIQUE_ID>``
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cors(self) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]]:
        '''The CORS configuration of this bucket.

        :default: - No CORS configuration.
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.CorsRule]], result)

    @builtins.property
    def enforce_ssl(self) -> typing.Optional[builtins.bool]:
        '''Enforces SSL for requests.

        S3.5 of the AWS Foundational Security Best Practices Regarding S3.

        :default: false
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
        '''
        result = self._values.get("intelligent_tiering_configurations")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration]], result)

    @builtins.property
    def inventories(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.Inventory]]:
        '''The inventory configuration of the bucket.

        :default: - No inventory configuration
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
        '''
        result = self._values.get("metrics")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.BucketMetrics]], result)

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
        '''
        result = self._values.get("object_lock_default_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention], result)

    @builtins.property
    def object_lock_enabled(self) -> typing.Optional[builtins.bool]:
        '''Enable object lock on the bucket.

        Enabling object lock for existing buckets is not supported. Object lock must be
        enabled when the bucket is created.

        :default: false, unless objectLockDefaultRetention is set (then, true)
        '''
        result = self._values.get("object_lock_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def object_ownership(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership]:
        '''The objectOwnership of the bucket.

        :default: - No ObjectOwnership configuration, uploading account will own the object.
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

        - @default - RETAIN (The bucket will be orphaned).
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

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AnalyticsBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ApplicationStackFactory(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-dsf.ApplicationStackFactory",
):
    '''Abstract class that needs to be implemented to pass the application Stack to the CICD pipeline.

    Example::

        import { ApplicationStackFactory }
        import { CICDStage } from './application-stage';
        
        interface MyApplicationStackProps extends StackProps {
          readonly stage: CICDStage;
        }
        
        class MyApplicationStack extends Stack {
          constructor(scope: Stack, id: string, props?: MyApplicationStackProps) {
            super(scope, id, props);
            // stack logic goes here... and can be customized using props.stage
          }
        }
        
        class MyApplicationStackFactory extends ApplicationStackFactory {
          createStack(scope: Construct, stage: CICDStage): Stack {
            return new MyApplicationStack(scope, 'MyApplication', {
              stage: stage
            } as MyApplicationStackProps);
          }
        }
    '''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="createStack")
    @abc.abstractmethod
    def create_stack(
        self,
        scope: _constructs_77d1e7e8.Construct,
        stage: "CICDStage",
    ) -> _aws_cdk_ceddda9d.Stack:
        '''Abstract method that needs to be implemented to return the application Stack.

        :param scope: The scope to create the stack in.
        :param stage: The stage of the pipeline.
        '''
        ...


class _ApplicationStackFactoryProxy(ApplicationStackFactory):
    @jsii.member(jsii_name="createStack")
    def create_stack(
        self,
        scope: _constructs_77d1e7e8.Construct,
        stage: "CICDStage",
    ) -> _aws_cdk_ceddda9d.Stack:
        '''Abstract method that needs to be implemented to return the application Stack.

        :param scope: The scope to create the stack in.
        :param stage: The stage of the pipeline.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e60f52dd65bad14c1f26ca2aba2367ab2eb1c1b34add215e26177cd18aa1dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.invoke(self, "createStack", [scope, stage]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ApplicationStackFactory).__jsii_proxy_class__ = lambda : _ApplicationStackFactoryProxy


class ApplicationStage(
    _aws_cdk_ceddda9d.Stage,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.ApplicationStage",
):
    '''ApplicationStage class that creates a CDK Pipelines Stage from an ApplicationStackFactory.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_stack_factory: ApplicationStackFactory,
        stage: "CICDStage",
        outputs_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construct a new instance of the SparkCICDStage class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param application_stack_factory: The application Stack to deploy in the different CDK Pipelines Stages.
        :param stage: The Stage to deploy the SparkCICDStack in. Default: - No stage is passed to the application stack
        :param outputs_env: The list of values to create CfnOutputs. Default: - No CfnOutputs are created
        :param env: Default AWS environment (account/region) for ``Stack``s in this ``Stage``. Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing from its env will use the corresponding field given here. If either ``region`` or ``account``is is not configured for ``Stack`` (either on the ``Stack`` itself or on the containing ``Stage``), the Stack will be *environment-agnostic*. Environment-agnostic stacks can be deployed to any environment, may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups, will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environments should be configured on the ``Stack``s.
        :param outdir: The output directory into which to emit synthesized artifacts. Can only be specified if this stage is the root stage (the app). If this is specified and this stage is nested within another stage, an error will be thrown. Default: - for nested stages, outdir will be determined as a relative directory to the outdir of the app. For apps, if outdir is not specified, a temporary directory will be created.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param policy_validation_beta1: Validation plugins to run during synthesis. If any plugin reports any violation, synthesis will be interrupted and the report displayed to the user. Default: - no validation plugins are used
        :param stage_name: Name of this stage. Default: - Derived from the id.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f545a2c9269855f5a29fd2c49c15038dcd8a62aa7c82538e3de15c72d1a328)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationStageProps(
            application_stack_factory=application_stack_factory,
            stage=stage,
            outputs_env=outputs_env,
            env=env,
            outdir=outdir,
            permissions_boundary=permissions_boundary,
            policy_validation_beta1=policy_validation_beta1,
            stage_name=stage_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="stackOutputsEnv")
    def stack_outputs_env(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.CfnOutput]]:
        '''The list of CfnOutputs created by the CDK Stack.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.CfnOutput]], jsii.get(self, "stackOutputsEnv"))


@jsii.data_type(
    jsii_type="aws-dsf.ApplicationStageProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.StageProps],
    name_mapping={
        "env": "env",
        "outdir": "outdir",
        "permissions_boundary": "permissionsBoundary",
        "policy_validation_beta1": "policyValidationBeta1",
        "stage_name": "stageName",
        "application_stack_factory": "applicationStackFactory",
        "stage": "stage",
        "outputs_env": "outputsEnv",
    },
)
class ApplicationStageProps(_aws_cdk_ceddda9d.StageProps):
    def __init__(
        self,
        *,
        env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
        outdir: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
        policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        application_stack_factory: ApplicationStackFactory,
        stage: "CICDStage",
        outputs_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for SparkCICDStage class.

        :param env: Default AWS environment (account/region) for ``Stack``s in this ``Stage``. Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing from its env will use the corresponding field given here. If either ``region`` or ``account``is is not configured for ``Stack`` (either on the ``Stack`` itself or on the containing ``Stage``), the Stack will be *environment-agnostic*. Environment-agnostic stacks can be deployed to any environment, may not be able to take advantage of all features of the CDK. For example, they will not be able to use environmental context lookups, will not automatically translate Service Principals to the right format based on the environment's AWS partition, and other such enhancements. Default: - The environments should be configured on the ``Stack``s.
        :param outdir: The output directory into which to emit synthesized artifacts. Can only be specified if this stage is the root stage (the app). If this is specified and this stage is nested within another stage, an error will be thrown. Default: - for nested stages, outdir will be determined as a relative directory to the outdir of the app. For apps, if outdir is not specified, a temporary directory will be created.
        :param permissions_boundary: Options for applying a permissions boundary to all IAM Roles and Users created within this Stage. Default: - no permissions boundary is applied
        :param policy_validation_beta1: Validation plugins to run during synthesis. If any plugin reports any violation, synthesis will be interrupted and the report displayed to the user. Default: - no validation plugins are used
        :param stage_name: Name of this stage. Default: - Derived from the id.
        :param application_stack_factory: The application Stack to deploy in the different CDK Pipelines Stages.
        :param stage: The Stage to deploy the SparkCICDStack in. Default: - No stage is passed to the application stack
        :param outputs_env: The list of values to create CfnOutputs. Default: - No CfnOutputs are created
        '''
        if isinstance(env, dict):
            env = _aws_cdk_ceddda9d.Environment(**env)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8c976ea345f9836c305bfa275a198b91dcf105f5fc7544c827ea19a6d44fdc)
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument outdir", value=outdir, expected_type=type_hints["outdir"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policy_validation_beta1", value=policy_validation_beta1, expected_type=type_hints["policy_validation_beta1"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument application_stack_factory", value=application_stack_factory, expected_type=type_hints["application_stack_factory"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument outputs_env", value=outputs_env, expected_type=type_hints["outputs_env"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_stack_factory": application_stack_factory,
            "stage": stage,
        }
        if env is not None:
            self._values["env"] = env
        if outdir is not None:
            self._values["outdir"] = outdir
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policy_validation_beta1 is not None:
            self._values["policy_validation_beta1"] = policy_validation_beta1
        if stage_name is not None:
            self._values["stage_name"] = stage_name
        if outputs_env is not None:
            self._values["outputs_env"] = outputs_env

    @builtins.property
    def env(self) -> typing.Optional[_aws_cdk_ceddda9d.Environment]:
        '''Default AWS environment (account/region) for ``Stack``s in this ``Stage``.

        Stacks defined inside this ``Stage`` with either ``region`` or ``account`` missing
        from its env will use the corresponding field given here.

        If either ``region`` or ``account``is is not configured for ``Stack`` (either on
        the ``Stack`` itself or on the containing ``Stage``), the Stack will be
        *environment-agnostic*.

        Environment-agnostic stacks can be deployed to any environment, may not be
        able to take advantage of all features of the CDK. For example, they will
        not be able to use environmental context lookups, will not automatically
        translate Service Principals to the right format based on the environment's
        AWS partition, and other such enhancements.

        :default: - The environments should be configured on the ``Stack``s.

        Example::

            // Use a concrete account and region to deploy this Stage to
            new Stage(app, 'Stage1', {
              env: { account: '123456789012', region: 'us-east-1' },
            });
            
            // Use the CLI's current credentials to determine the target environment
            new Stage(app, 'Stage2', {
              env: { account: process.env.CDK_DEFAULT_ACCOUNT, region: process.env.CDK_DEFAULT_REGION },
            });
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Environment], result)

    @builtins.property
    def outdir(self) -> typing.Optional[builtins.str]:
        '''The output directory into which to emit synthesized artifacts.

        Can only be specified if this stage is the root stage (the app). If this is
        specified and this stage is nested within another stage, an error will be
        thrown.

        :default:

        - for nested stages, outdir will be determined as a relative
        directory to the outdir of the app. For apps, if outdir is not specified, a
        temporary directory will be created.
        '''
        result = self._values.get("outdir")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(
        self,
    ) -> typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary]:
        '''Options for applying a permissions boundary to all IAM Roles and Users created within this Stage.

        :default: - no permissions boundary is applied
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary], result)

    @builtins.property
    def policy_validation_beta1(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]]:
        '''Validation plugins to run during synthesis.

        If any plugin reports any violation,
        synthesis will be interrupted and the report displayed to the user.

        :default: - no validation plugins are used
        '''
        result = self._values.get("policy_validation_beta1")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''Name of this stage.

        :default: - Derived from the id.
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_stack_factory(self) -> ApplicationStackFactory:
        '''The application Stack to deploy in the different CDK Pipelines Stages.'''
        result = self._values.get("application_stack_factory")
        assert result is not None, "Required property 'application_stack_factory' is missing"
        return typing.cast(ApplicationStackFactory, result)

    @builtins.property
    def stage(self) -> "CICDStage":
        '''The Stage to deploy the SparkCICDStack in.

        :default: - No stage is passed to the application stack
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast("CICDStage", result)

    @builtins.property
    def outputs_env(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The list of values to create CfnOutputs.

        :default: - No CfnOutputs are created
        '''
        result = self._values.get("outputs_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-dsf.Architecture")
class Architecture(enum.Enum):
    '''Enum defining the CPU architecture type of the application, either  X86_64 or ARM64.'''

    X86_64 = "X86_64"
    ARM64 = "ARM64"


class BucketUtils(metaclass=jsii.JSIIMeta, jsii_type="aws-dsf.BucketUtils"):
    '''Utils for working with Amazon S3 buckets.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="generateUniqueBucketName")
    @builtins.classmethod
    def generate_unique_bucket_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        name: builtins.str,
    ) -> builtins.str:
        '''Generate a unique Amazon S3 bucket name based on the provided name, CDK construct ID and CDK construct scope.

        The bucket name is suffixed the AWS account ID, the AWS region and a unique 8 characters hash.
        The maximum length for name is 26 characters.

        :param scope: the current scope where the construct is created (generally ``this``).
        :param id: the CDK ID of the construct.
        :param name: the name of the bucket.

        :return: the unique Name for the bucket
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79d319717a1965981e8ded14af2ba7020f9d4782f3c604b4a2afb9073a77b0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "generateUniqueBucketName", [scope, id, name]))


@jsii.enum(jsii_type="aws-dsf.CICDStage")
class CICDStage(enum.Enum):
    '''The list of CICD Stages to deploy the SparkCICDStack.'''

    STAGING = "STAGING"
    PROD = "PROD"


class DataCatalogDatabase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.DataCatalogDatabase",
):
    '''An AWS Glue Data Catalog Database configured with the location and a crawler.

    Example::

        import * as cdk from 'aws-cdk-lib';
        import { DataCatalogDatabase } from 'aws-data-solutions-framework';
        
        const exampleApp = new cdk.App();
        const stack = new cdk.Stack(exampleApp, 'DataCatalogStack');
        
        new DataCatalogDatabase(stack, 'ExampleDatabase', {
           locationBucket: bucket,
           locationPrefix: '/databasePath',
           name: 'example-db'
        });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        location_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        location_prefix: builtins.str,
        name: builtins.str,
        auto_crawl: typing.Optional[builtins.bool] = None,
        auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        crawler_table_level_depth: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param location_bucket: S3 bucket where data is stored.
        :param location_prefix: Top level location wwhere table data is stored.
        :param name: Database name. Construct would add a randomize suffix as part of the name to prevent name collisions.
        :param auto_crawl: When enabled, this automatically creates a top level Glue Crawler that would run based on the defined schedule in the ``autoCrawlSchedule`` parameter. Default: True
        :param auto_crawl_schedule: The schedule when the Crawler would run. Default is once a day at 00:01h. Default: ``cron(1 0 * * ? *)``
        :param crawler_log_encryption_key: Encryption key used for Crawler logs. Default: Create a new key if none is provided
        :param crawler_table_level_depth: Directory depth where the table folders are located. This helps the crawler understand the layout of the folders in S3. Default: 3. The default value follows the structure: ``<bucket>/<databaseFolder>/<table1Folder>/``
        :param removal_policy: Policy to apply when the bucket is removed from this stack. - @default - RETAIN (The bucket will be orphaned).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fc7a60b58fe4f58e0bed3d8804410738c281f005eddcd657bf7b44db75c3f1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataCatalogDatabaseProps(
            location_bucket=location_bucket,
            location_prefix=location_prefix,
            name=name,
            auto_crawl=auto_crawl,
            auto_crawl_schedule=auto_crawl_schedule,
            crawler_log_encryption_key=crawler_log_encryption_key,
            crawler_table_level_depth=crawler_table_level_depth,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantReadOnlyAccess")
    def grant_read_only_access(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> _aws_cdk_aws_iam_ceddda9d.AddToPrincipalPolicyResult:
        '''Grants read access via identity based policy to the principal.

        This would attach an IAM policy to the principal allowing read access to the database and all its tables.

        :param principal: Principal to attach the database read access to.

        :return: ``AddToPrincipalPolicyResult``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec9e10691595dca6d589fd529c14b901cafb535d39e262d6d056a08c02401bc5)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.AddToPrincipalPolicyResult, jsii.invoke(self, "grantReadOnlyAccess", [principal]))

    @jsii.member(jsii_name="retrieveVersion")
    def retrieve_version(self) -> typing.Any:
        '''Retrieve ADSF package.json version.'''
        return typing.cast(typing.Any, jsii.invoke(self, "retrieveVersion", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_OWNED_TAG")
    def ADSF_OWNED_TAG(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_OWNED_TAG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_TRACKING_CODE")
    def ADSF_TRACKING_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_TRACKING_CODE"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> _aws_cdk_aws_glue_ceddda9d.CfnDatabase:
        '''The Glue database that's created.'''
        return typing.cast(_aws_cdk_aws_glue_ceddda9d.CfnDatabase, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''The Glue database name with the randomized suffix to prevent name collisions in the catalog.'''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="crawler")
    def crawler(self) -> typing.Optional[_aws_cdk_aws_glue_ceddda9d.CfnCrawler]:
        '''The Glue Crawler that is automatically created when ``autoCrawl`` is set to ``true`` (default value).

        This property can be undefined if ``autoCrawl`` is set to ``false``.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_glue_ceddda9d.CfnCrawler], jsii.get(self, "crawler"))

    @builtins.property
    @jsii.member(jsii_name="crawlerLogEncryptionKey")
    def crawler_log_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        '''KMS encryption key used by the Crawler.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], jsii.get(self, "crawlerLogEncryptionKey"))


@jsii.data_type(
    jsii_type="aws-dsf.DataCatalogDatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "location_bucket": "locationBucket",
        "location_prefix": "locationPrefix",
        "name": "name",
        "auto_crawl": "autoCrawl",
        "auto_crawl_schedule": "autoCrawlSchedule",
        "crawler_log_encryption_key": "crawlerLogEncryptionKey",
        "crawler_table_level_depth": "crawlerTableLevelDepth",
        "removal_policy": "removalPolicy",
    },
)
class DataCatalogDatabaseProps:
    def __init__(
        self,
        *,
        location_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        location_prefix: builtins.str,
        name: builtins.str,
        auto_crawl: typing.Optional[builtins.bool] = None,
        auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        crawler_table_level_depth: typing.Optional[jsii.Number] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''The Database catalog properties.

        :param location_bucket: S3 bucket where data is stored.
        :param location_prefix: Top level location wwhere table data is stored.
        :param name: Database name. Construct would add a randomize suffix as part of the name to prevent name collisions.
        :param auto_crawl: When enabled, this automatically creates a top level Glue Crawler that would run based on the defined schedule in the ``autoCrawlSchedule`` parameter. Default: True
        :param auto_crawl_schedule: The schedule when the Crawler would run. Default is once a day at 00:01h. Default: ``cron(1 0 * * ? *)``
        :param crawler_log_encryption_key: Encryption key used for Crawler logs. Default: Create a new key if none is provided
        :param crawler_table_level_depth: Directory depth where the table folders are located. This helps the crawler understand the layout of the folders in S3. Default: 3. The default value follows the structure: ``<bucket>/<databaseFolder>/<table1Folder>/``
        :param removal_policy: Policy to apply when the bucket is removed from this stack. - @default - RETAIN (The bucket will be orphaned).
        '''
        if isinstance(auto_crawl_schedule, dict):
            auto_crawl_schedule = _aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty(**auto_crawl_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9597c13111a5aeba355de3c6473722674812152ef9bc6cd18e154fe16acd9bc0)
            check_type(argname="argument location_bucket", value=location_bucket, expected_type=type_hints["location_bucket"])
            check_type(argname="argument location_prefix", value=location_prefix, expected_type=type_hints["location_prefix"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument auto_crawl", value=auto_crawl, expected_type=type_hints["auto_crawl"])
            check_type(argname="argument auto_crawl_schedule", value=auto_crawl_schedule, expected_type=type_hints["auto_crawl_schedule"])
            check_type(argname="argument crawler_log_encryption_key", value=crawler_log_encryption_key, expected_type=type_hints["crawler_log_encryption_key"])
            check_type(argname="argument crawler_table_level_depth", value=crawler_table_level_depth, expected_type=type_hints["crawler_table_level_depth"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location_bucket": location_bucket,
            "location_prefix": location_prefix,
            "name": name,
        }
        if auto_crawl is not None:
            self._values["auto_crawl"] = auto_crawl
        if auto_crawl_schedule is not None:
            self._values["auto_crawl_schedule"] = auto_crawl_schedule
        if crawler_log_encryption_key is not None:
            self._values["crawler_log_encryption_key"] = crawler_log_encryption_key
        if crawler_table_level_depth is not None:
            self._values["crawler_table_level_depth"] = crawler_table_level_depth
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def location_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''S3 bucket where data is stored.'''
        result = self._values.get("location_bucket")
        assert result is not None, "Required property 'location_bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def location_prefix(self) -> builtins.str:
        '''Top level location wwhere table data is stored.'''
        result = self._values.get("location_prefix")
        assert result is not None, "Required property 'location_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Database name.

        Construct would add a randomize suffix as part of the name to prevent name collisions.
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_crawl(self) -> typing.Optional[builtins.bool]:
        '''When enabled, this automatically creates a top level Glue Crawler that would run based on the defined schedule in the ``autoCrawlSchedule`` parameter.

        :default: True
        '''
        result = self._values.get("auto_crawl")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_crawl_schedule(
        self,
    ) -> typing.Optional[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty]:
        '''The schedule when the Crawler would run.

        Default is once a day at 00:01h.

        :default: ``cron(1 0 * * ? *)``
        '''
        result = self._values.get("auto_crawl_schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty], result)

    @builtins.property
    def crawler_log_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        '''Encryption key used for Crawler logs.

        :default: Create a new key if none is provided
        '''
        result = self._values.get("crawler_log_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], result)

    @builtins.property
    def crawler_table_level_depth(self) -> typing.Optional[jsii.Number]:
        '''Directory depth where the table folders are located.

        This helps the crawler understand the layout of the folders in S3.

        :default: 3. The default value follows the structure: ``<bucket>/<databaseFolder>/<table1Folder>/``
        '''
        result = self._values.get("crawler_table_level_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Policy to apply when the bucket is removed from this stack.

        - @default - RETAIN (The bucket will be orphaned).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataCatalogDatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLakeCatalog(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.DataLakeCatalog",
):
    '''Creates AWS Glue Catalog Database for each storage layer.

    Composed of 3 {@link DataCatalogDatabase} for Bronze, Silver, and Gold data.

    Example::

        import * as cdk from 'aws-cdk-lib';
        import { Key } from 'aws-cdk-lib/aws-kms';
        import { DataLakeCatalog, DataLakeStorage } from 'aws-data-solutions-framework';
        
        const exampleApp = new cdk.App();
        const stack = new cdk.Stack(exampleApp, 'DataCatalogStack');
        const storage = new DataLakeStorage(stack, "ExampleStorage");
        const logEncryptionKey = new Key(stack, 'LogEncryptionKey');
        const dataLakeCatalog = new DataLakeCatalog(stack, "ExampleDataLakeCatalog", {
          dataLakeStorage: storage,
          databaseName: "exampledb",
          crawlerLogEncryptionKey: logEncryptionKey
        })
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data_lake_storage: "DataLakeStorage",
        auto_crawl: typing.Optional[builtins.bool] = None,
        auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        database_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''Constructs a new instance of DataLakeCatalog.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param data_lake_storage: Location of data lake files.
        :param auto_crawl: When enabled, this automatically creates a top level Glue Crawler that would run based on the defined schedule in the ``autoCrawlSchedule`` parameter. Default: True
        :param auto_crawl_schedule: The schedule when the Crawler would run. Default is once a day at 00:01h. Default: ``cron(1 0 * * ? *)``
        :param crawler_log_encryption_key: Encryption key used for Crawler logs. Default: Create a new key if none is provided
        :param database_name: The name of the database in the Glue Data Catalog. This is also used as the prefix inside the data lake bucket. Default: Use the bucket name as the database name and / as the prefix
        :param removal_policy: Policy to apply when the bucket is removed from this stack. - @default - RETAIN (The bucket will be orphaned).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c9f62f44305087de500a1cd42feba2045289d23a52b548eac43a9ccbc36b4e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeCatalogProps(
            data_lake_storage=data_lake_storage,
            auto_crawl=auto_crawl,
            auto_crawl_schedule=auto_crawl_schedule,
            crawler_log_encryption_key=crawler_log_encryption_key,
            database_name=database_name,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="retrieveVersion")
    def retrieve_version(self) -> typing.Any:
        '''Retrieve ADSF package.json version.'''
        return typing.cast(typing.Any, jsii.invoke(self, "retrieveVersion", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_OWNED_TAG")
    def ADSF_OWNED_TAG(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_OWNED_TAG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_TRACKING_CODE")
    def ADSF_TRACKING_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_TRACKING_CODE"))

    @builtins.property
    @jsii.member(jsii_name="bronzeCatalogDatabase")
    def bronze_catalog_database(self) -> DataCatalogDatabase:
        return typing.cast(DataCatalogDatabase, jsii.get(self, "bronzeCatalogDatabase"))

    @builtins.property
    @jsii.member(jsii_name="goldCatalogDatabase")
    def gold_catalog_database(self) -> DataCatalogDatabase:
        return typing.cast(DataCatalogDatabase, jsii.get(self, "goldCatalogDatabase"))

    @builtins.property
    @jsii.member(jsii_name="silverCatalogDatabase")
    def silver_catalog_database(self) -> DataCatalogDatabase:
        return typing.cast(DataCatalogDatabase, jsii.get(self, "silverCatalogDatabase"))

    @builtins.property
    @jsii.member(jsii_name="crawlerLogEncryptionKey")
    def crawler_log_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], jsii.get(self, "crawlerLogEncryptionKey"))


@jsii.data_type(
    jsii_type="aws-dsf.DataLakeCatalogProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_lake_storage": "dataLakeStorage",
        "auto_crawl": "autoCrawl",
        "auto_crawl_schedule": "autoCrawlSchedule",
        "crawler_log_encryption_key": "crawlerLogEncryptionKey",
        "database_name": "databaseName",
        "removal_policy": "removalPolicy",
    },
)
class DataLakeCatalogProps:
    def __init__(
        self,
        *,
        data_lake_storage: "DataLakeStorage",
        auto_crawl: typing.Optional[builtins.bool] = None,
        auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        database_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''Properties for the DataLakeCatalog Construct.

        :param data_lake_storage: Location of data lake files.
        :param auto_crawl: When enabled, this automatically creates a top level Glue Crawler that would run based on the defined schedule in the ``autoCrawlSchedule`` parameter. Default: True
        :param auto_crawl_schedule: The schedule when the Crawler would run. Default is once a day at 00:01h. Default: ``cron(1 0 * * ? *)``
        :param crawler_log_encryption_key: Encryption key used for Crawler logs. Default: Create a new key if none is provided
        :param database_name: The name of the database in the Glue Data Catalog. This is also used as the prefix inside the data lake bucket. Default: Use the bucket name as the database name and / as the prefix
        :param removal_policy: Policy to apply when the bucket is removed from this stack. - @default - RETAIN (The bucket will be orphaned).
        '''
        if isinstance(auto_crawl_schedule, dict):
            auto_crawl_schedule = _aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty(**auto_crawl_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3aabdd1ab669297b207eab978305167ba45681c1169f69366712b0a83ec38a)
            check_type(argname="argument data_lake_storage", value=data_lake_storage, expected_type=type_hints["data_lake_storage"])
            check_type(argname="argument auto_crawl", value=auto_crawl, expected_type=type_hints["auto_crawl"])
            check_type(argname="argument auto_crawl_schedule", value=auto_crawl_schedule, expected_type=type_hints["auto_crawl_schedule"])
            check_type(argname="argument crawler_log_encryption_key", value=crawler_log_encryption_key, expected_type=type_hints["crawler_log_encryption_key"])
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_lake_storage": data_lake_storage,
        }
        if auto_crawl is not None:
            self._values["auto_crawl"] = auto_crawl
        if auto_crawl_schedule is not None:
            self._values["auto_crawl_schedule"] = auto_crawl_schedule
        if crawler_log_encryption_key is not None:
            self._values["crawler_log_encryption_key"] = crawler_log_encryption_key
        if database_name is not None:
            self._values["database_name"] = database_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def data_lake_storage(self) -> "DataLakeStorage":
        '''Location of data lake files.'''
        result = self._values.get("data_lake_storage")
        assert result is not None, "Required property 'data_lake_storage' is missing"
        return typing.cast("DataLakeStorage", result)

    @builtins.property
    def auto_crawl(self) -> typing.Optional[builtins.bool]:
        '''When enabled, this automatically creates a top level Glue Crawler that would run based on the defined schedule in the ``autoCrawlSchedule`` parameter.

        :default: True
        '''
        result = self._values.get("auto_crawl")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def auto_crawl_schedule(
        self,
    ) -> typing.Optional[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty]:
        '''The schedule when the Crawler would run.

        Default is once a day at 00:01h.

        :default: ``cron(1 0 * * ? *)``
        '''
        result = self._values.get("auto_crawl_schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty], result)

    @builtins.property
    def crawler_log_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        '''Encryption key used for Crawler logs.

        :default: Create a new key if none is provided
        '''
        result = self._values.get("crawler_log_encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], result)

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''The name of the database in the Glue Data Catalog.

        This is also used as the prefix inside the data lake bucket.

        :default: Use the bucket name as the database name and / as the prefix
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Policy to apply when the bucket is removed from this stack.

        - @default - RETAIN (The bucket will be orphaned).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeCatalogProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLakeStorage(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.DataLakeStorage",
):
    '''Creates the storage layer for a data lake, composed of 3 {@link AnalyticsBucket} for Bronze, Silver, and Gold data.

    See documentation TODO insert link.

    Example::

        import * as cdk from 'aws-cdk-lib';
        import { DataLakeStorage } from 'aws-data-solutions-framework';
        
        // Set the context value for global data removal policy
        stack.node.setContext('@aws-data-solutions-framework/removeDataOnDestroy', true);
        
        new DataLakeStorage(this, 'MyDataLakeStorage', {
         bronzeBucketName: 'my-bronze',
         bronzeBucketInfrequentAccessDelay: 90,
         bronzeBucketArchiveDelay: 180,
         silverBucketName: 'my-silver',
         silverBucketInfrequentAccessDelay: 180,
         silverBucketArchiveDelay: 360,
         goldBucketName: 'my-gold',
         goldBucketInfrequentAccessDelay: 180,
         goldBucketArchiveDelay: 360,
         removalPolicy: cdk.RemovalPolicy.DESTROY,
        });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bronze_bucket_archive_delay: typing.Optional[jsii.Number] = None,
        bronze_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        bronze_bucket_name: typing.Optional[builtins.str] = None,
        data_lake_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        gold_bucket_archive_delay: typing.Optional[jsii.Number] = None,
        gold_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        gold_bucket_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        silver_bucket_archive_delay: typing.Optional[jsii.Number] = None,
        silver_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        silver_bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construct a new instance of DataLakeStorage.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param bronze_bucket_archive_delay: Delay (in days) before archiving BRONZE data to frozen storage (Glacier storage class). Default: - Move objects to Glacier after 90 days.
        :param bronze_bucket_infrequent_access_delay: Delay (in days) before moving BRONZE data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 30 days.
        :param bronze_bucket_name: Name of the Bronze bucket. Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended). Default: - ``bronze-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        :param data_lake_key: The KMS Key used to encrypt all DataLakeStorage S3 buckets. Default: - A single KMS customer key is created.
        :param gold_bucket_archive_delay: Delay (in days) before archiving GOLD data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier.
        :param gold_bucket_infrequent_access_delay: Delay (in days) before moving GOLD data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days.
        :param gold_bucket_name: Name of the Gold bucket. Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended). Default: - ``gold-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        :param removal_policy: The removal policy when deleting the CDK resource. If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true. Otherwise, the removalPolicy is reverted to RETAIN. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param silver_bucket_archive_delay: Delay (in days) before archiving SILVER data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier.
        :param silver_bucket_infrequent_access_delay: Delay (in days) before moving SILVER data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days.
        :param silver_bucket_name: Name of the Silver bucket. Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended). Default: - ``silver-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd8415538052ebb4ea815fbf59792f64807d46258bcd13a36f0d38a21ef052b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataLakeStorageProps(
            bronze_bucket_archive_delay=bronze_bucket_archive_delay,
            bronze_bucket_infrequent_access_delay=bronze_bucket_infrequent_access_delay,
            bronze_bucket_name=bronze_bucket_name,
            data_lake_key=data_lake_key,
            gold_bucket_archive_delay=gold_bucket_archive_delay,
            gold_bucket_infrequent_access_delay=gold_bucket_infrequent_access_delay,
            gold_bucket_name=gold_bucket_name,
            removal_policy=removal_policy,
            silver_bucket_archive_delay=silver_bucket_archive_delay,
            silver_bucket_infrequent_access_delay=silver_bucket_infrequent_access_delay,
            silver_bucket_name=silver_bucket_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="retrieveVersion")
    def retrieve_version(self) -> typing.Any:
        '''Retrieve ADSF package.json version.'''
        return typing.cast(typing.Any, jsii.invoke(self, "retrieveVersion", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_OWNED_TAG")
    def ADSF_OWNED_TAG(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_OWNED_TAG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_TRACKING_CODE")
    def ADSF_TRACKING_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_TRACKING_CODE"))

    @builtins.property
    @jsii.member(jsii_name="accessLogsBucket")
    def access_logs_bucket(self) -> AccessLogsBucket:
        return typing.cast(AccessLogsBucket, jsii.get(self, "accessLogsBucket"))

    @builtins.property
    @jsii.member(jsii_name="bronzeBucket")
    def bronze_bucket(self) -> AnalyticsBucket:
        return typing.cast(AnalyticsBucket, jsii.get(self, "bronzeBucket"))

    @builtins.property
    @jsii.member(jsii_name="dataLakeKey")
    def data_lake_key(self) -> _aws_cdk_aws_kms_ceddda9d.Key:
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.Key, jsii.get(self, "dataLakeKey"))

    @builtins.property
    @jsii.member(jsii_name="goldBucket")
    def gold_bucket(self) -> AnalyticsBucket:
        return typing.cast(AnalyticsBucket, jsii.get(self, "goldBucket"))

    @builtins.property
    @jsii.member(jsii_name="silverBucket")
    def silver_bucket(self) -> AnalyticsBucket:
        return typing.cast(AnalyticsBucket, jsii.get(self, "silverBucket"))


@jsii.data_type(
    jsii_type="aws-dsf.DataLakeStorageProps",
    jsii_struct_bases=[],
    name_mapping={
        "bronze_bucket_archive_delay": "bronzeBucketArchiveDelay",
        "bronze_bucket_infrequent_access_delay": "bronzeBucketInfrequentAccessDelay",
        "bronze_bucket_name": "bronzeBucketName",
        "data_lake_key": "dataLakeKey",
        "gold_bucket_archive_delay": "goldBucketArchiveDelay",
        "gold_bucket_infrequent_access_delay": "goldBucketInfrequentAccessDelay",
        "gold_bucket_name": "goldBucketName",
        "removal_policy": "removalPolicy",
        "silver_bucket_archive_delay": "silverBucketArchiveDelay",
        "silver_bucket_infrequent_access_delay": "silverBucketInfrequentAccessDelay",
        "silver_bucket_name": "silverBucketName",
    },
)
class DataLakeStorageProps:
    def __init__(
        self,
        *,
        bronze_bucket_archive_delay: typing.Optional[jsii.Number] = None,
        bronze_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        bronze_bucket_name: typing.Optional[builtins.str] = None,
        data_lake_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
        gold_bucket_archive_delay: typing.Optional[jsii.Number] = None,
        gold_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        gold_bucket_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        silver_bucket_archive_delay: typing.Optional[jsii.Number] = None,
        silver_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
        silver_bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for the DataLakeStorage Construct.

        :param bronze_bucket_archive_delay: Delay (in days) before archiving BRONZE data to frozen storage (Glacier storage class). Default: - Move objects to Glacier after 90 days.
        :param bronze_bucket_infrequent_access_delay: Delay (in days) before moving BRONZE data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 30 days.
        :param bronze_bucket_name: Name of the Bronze bucket. Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended). Default: - ``bronze-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        :param data_lake_key: The KMS Key used to encrypt all DataLakeStorage S3 buckets. Default: - A single KMS customer key is created.
        :param gold_bucket_archive_delay: Delay (in days) before archiving GOLD data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier.
        :param gold_bucket_infrequent_access_delay: Delay (in days) before moving GOLD data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days.
        :param gold_bucket_name: Name of the Gold bucket. Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended). Default: - ``gold-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        :param removal_policy: The removal policy when deleting the CDK resource. If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true. Otherwise, the removalPolicy is reverted to RETAIN. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param silver_bucket_archive_delay: Delay (in days) before archiving SILVER data to frozen storage (Glacier storage class). Default: - Objects are not archived to Glacier.
        :param silver_bucket_infrequent_access_delay: Delay (in days) before moving SILVER data to cold storage (Infrequent Access storage class). Default: - Move objects to Infrequent Access after 90 days.
        :param silver_bucket_name: Name of the Silver bucket. Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended). Default: - ``silver-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5753d278e7d410a61c802eac9a9344c0ca8236941efbca8cc875cb7c4f16d19)
            check_type(argname="argument bronze_bucket_archive_delay", value=bronze_bucket_archive_delay, expected_type=type_hints["bronze_bucket_archive_delay"])
            check_type(argname="argument bronze_bucket_infrequent_access_delay", value=bronze_bucket_infrequent_access_delay, expected_type=type_hints["bronze_bucket_infrequent_access_delay"])
            check_type(argname="argument bronze_bucket_name", value=bronze_bucket_name, expected_type=type_hints["bronze_bucket_name"])
            check_type(argname="argument data_lake_key", value=data_lake_key, expected_type=type_hints["data_lake_key"])
            check_type(argname="argument gold_bucket_archive_delay", value=gold_bucket_archive_delay, expected_type=type_hints["gold_bucket_archive_delay"])
            check_type(argname="argument gold_bucket_infrequent_access_delay", value=gold_bucket_infrequent_access_delay, expected_type=type_hints["gold_bucket_infrequent_access_delay"])
            check_type(argname="argument gold_bucket_name", value=gold_bucket_name, expected_type=type_hints["gold_bucket_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument silver_bucket_archive_delay", value=silver_bucket_archive_delay, expected_type=type_hints["silver_bucket_archive_delay"])
            check_type(argname="argument silver_bucket_infrequent_access_delay", value=silver_bucket_infrequent_access_delay, expected_type=type_hints["silver_bucket_infrequent_access_delay"])
            check_type(argname="argument silver_bucket_name", value=silver_bucket_name, expected_type=type_hints["silver_bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bronze_bucket_archive_delay is not None:
            self._values["bronze_bucket_archive_delay"] = bronze_bucket_archive_delay
        if bronze_bucket_infrequent_access_delay is not None:
            self._values["bronze_bucket_infrequent_access_delay"] = bronze_bucket_infrequent_access_delay
        if bronze_bucket_name is not None:
            self._values["bronze_bucket_name"] = bronze_bucket_name
        if data_lake_key is not None:
            self._values["data_lake_key"] = data_lake_key
        if gold_bucket_archive_delay is not None:
            self._values["gold_bucket_archive_delay"] = gold_bucket_archive_delay
        if gold_bucket_infrequent_access_delay is not None:
            self._values["gold_bucket_infrequent_access_delay"] = gold_bucket_infrequent_access_delay
        if gold_bucket_name is not None:
            self._values["gold_bucket_name"] = gold_bucket_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if silver_bucket_archive_delay is not None:
            self._values["silver_bucket_archive_delay"] = silver_bucket_archive_delay
        if silver_bucket_infrequent_access_delay is not None:
            self._values["silver_bucket_infrequent_access_delay"] = silver_bucket_infrequent_access_delay
        if silver_bucket_name is not None:
            self._values["silver_bucket_name"] = silver_bucket_name

    @builtins.property
    def bronze_bucket_archive_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay (in days) before archiving BRONZE data to frozen storage (Glacier storage class).

        :default: - Move objects to Glacier after 90 days.
        '''
        result = self._values.get("bronze_bucket_archive_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bronze_bucket_infrequent_access_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay (in days) before moving BRONZE data to cold storage (Infrequent Access storage class).

        :default: - Move objects to Infrequent Access after 30 days.
        '''
        result = self._values.get("bronze_bucket_infrequent_access_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def bronze_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Bronze bucket.

        Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended).

        :default: - ``bronze-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        '''
        result = self._values.get("bronze_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def data_lake_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key]:
        '''The KMS Key used to encrypt all DataLakeStorage S3 buckets.

        :default: - A single KMS customer key is created.
        '''
        result = self._values.get("data_lake_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key], result)

    @builtins.property
    def gold_bucket_archive_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay (in days) before archiving GOLD data to frozen storage (Glacier storage class).

        :default: - Objects are not archived to Glacier.
        '''
        result = self._values.get("gold_bucket_archive_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gold_bucket_infrequent_access_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay (in days) before moving GOLD data to cold storage (Infrequent Access storage class).

        :default: - Move objects to Infrequent Access after 90 days.
        '''
        result = self._values.get("gold_bucket_infrequent_access_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gold_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Gold bucket.

        Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended).

        :default: - ``gold-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        '''
        result = self._values.get("gold_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy when deleting the CDK resource.

        If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true.
        Otherwise, the removalPolicy is reverted to RETAIN.

        :default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def silver_bucket_archive_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay (in days) before archiving SILVER data to frozen storage (Glacier storage class).

        :default: - Objects are not archived to Glacier.
        '''
        result = self._values.get("silver_bucket_archive_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def silver_bucket_infrequent_access_delay(self) -> typing.Optional[jsii.Number]:
        '''Delay (in days) before moving SILVER data to cold storage (Infrequent Access storage class).

        :default: - Move objects to Infrequent Access after 90 days.
        '''
        result = self._values.get("silver_bucket_infrequent_access_delay")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def silver_bucket_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Silver bucket.

        Use ``BucketUtils.generateUniqueBucketName()`` to generate a unique name (recommended).

        :default: - ``silver-<ACCOUNT_ID>-<REGION>-<UNIQUE_ID>`` will be used.
        '''
        result = self._values.get("silver_bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLakeStorageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-dsf.EmrRuntimeVersion")
class EmrRuntimeVersion(enum.Enum):
    '''Enum defining the EMR version as defined `here <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-6x.html>`_.'''

    V6_12 = "V6_12"
    V6_11_1 = "V6_11_1"
    V6_11 = "V6_11"
    V6_10_1 = "V6_10_1"
    V6_10 = "V6_10"
    V6_9 = "V6_9"
    V6_8 = "V6_8"
    V6_7 = "V6_7"
    V6_6 = "V6_6"
    V6_5 = "V6_5"
    V6_4 = "V6_4"
    V6_3 = "V6_3"
    V6_2 = "V6_2"
    V5_33 = "V5_33"
    V5_32 = "V5_32"


class PySparkApplicationPackage(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.PySparkApplicationPackage",
):
    '''A construct that takes your PySpark application, packages its virtual environment and uploads it along its entrypoint to an Amazon S3 bucket This construct requires Docker daemon installed locally to run.

    Example::

        let pysparkPacker = new PySparkApplicationPackage (stack, 'pysparkPacker', {
          pysparkApplicationName: 'my-pyspark',
          entrypointPath: '/Users/my-user/my-spark-job/app/app-pyspark.py',
          dependenciesFolder: '/Users/my-user/my-spark-job/app',
          removalPolicy: RemovalPolicy.DESTROY,
        });
        
        let sparkEnvConf: string = `--conf spark.archives=${pysparkPacker.virtualEnvironmentArchiveS3Uri} --conf spark.emr-serverless.driverEnv.PYSPARK_DRIVER_PYTHON=./environment/bin/python --conf spark.emr-serverless.driverEnv.PYSPARK_PYTHON=./environment/bin/python --conf spark.emr-serverless.executorEnv.PYSPARK_PYTHON=./environment/bin/python`
        
        new EmrServerlessSparkJob(stack, 'SparkJobServerless', {
          name: 'MyPySpark',
          applicationId: 'xxxxxxxxx',
          executionRoleArn: 'ROLE-ARN,
          executionTimeoutMinutes: 30,
          s3LogUri: 's3://s3-bucket/monitoring-logs',
          cloudWatchLogGroupName: 'my-pyspark-serverless-log',
          sparkSubmitEntryPoint: `${pysparkPacker.entrypointS3Uri}`,
          sparkSubmitParameters: `--conf spark.executor.instances=2 --conf spark.executor.memory=2G --conf spark.driver.memory=2G --conf spark.executor.cores=4 ${sparkEnvConf}`,
        } as EmrServerlessSparkJobProps);
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_name: builtins.str,
        entrypoint_path: builtins.str,
        artifacts_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        dependencies_folder: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        venv_archive_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param application_name: The name of the pyspark application. This name is used as a parent directory in s3 to store the entrypoint as well as virtual environment archive
        :param entrypoint_path: The source path in your code base where you have the entrypoint stored example ``~/my-project/src/entrypoint.py``.
        :param artifacts_bucket: The S3 bucket where to upload the artifacts of the Spark Job This is where the entry point and archive of the virtual environment will be stored. Default: - A bucket is created
        :param dependencies_folder: The source directory where you have ``requirements.txt`` or ``pyproject.toml`` that will install external AND internal Python packages. If your PySpark application has more than one Python file, you need to `package your Python project <https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_. This location must also have a ``Dockerfile`` that will `create a virtual environment and build an archive <https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/using-python-libraries.html#building-python-virtual-env>`_ out of it. Default: - No dependencies (internal or external) are packaged. Only the entrypoint can be used in the Spark Job.
        :param removal_policy: The removal policy when deleting the CDK resource. Resources like Amazon cloudwatch log or Amazon S3 bucket. If DESTROY is selected, the context value '@aws-data-solutions-framework/removeDataOnDestroy' in the 'cdk.json' or 'cdk.context.json' must be set to true. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param venv_archive_path: The path of the Python virtual environment archive generated in the Docker container. This is the output path used in the ``venv-pack -o`` command in your Dockerfile. Default: - No virtual environment archive is packaged. Only the entrypoint can be used in the Spark Job. It is required if the ``dependenciesFolder`` is provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9787f9e2305f0f39ba35d61392fb936c137d9ff78e91a7f4d10cf85a00329153)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PySparkApplicationPackageProps(
            application_name=application_name,
            entrypoint_path=entrypoint_path,
            artifacts_bucket=artifacts_bucket,
            dependencies_folder=dependencies_folder,
            removal_policy=removal_policy,
            venv_archive_path=venv_archive_path,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="retrieveVersion")
    def retrieve_version(self) -> typing.Any:
        '''Retrieve ADSF package.json version.'''
        return typing.cast(typing.Any, jsii.invoke(self, "retrieveVersion", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_OWNED_TAG")
    def ADSF_OWNED_TAG(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_OWNED_TAG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_TRACKING_CODE")
    def ADSF_TRACKING_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_TRACKING_CODE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ARTIFACTS_PREFIX")
    def ARTIFACTS_PREFIX(cls) -> builtins.str:
        '''The prefix used to store artifacts on the artifact bucket.'''
        return typing.cast(builtins.str, jsii.sget(cls, "ARTIFACTS_PREFIX"))

    @builtins.property
    @jsii.member(jsii_name="artifactsBucket")
    def artifacts_bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''The bucket storing the artifacts (entrypoint and virtual environment archive).'''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "artifactsBucket"))

    @builtins.property
    @jsii.member(jsii_name="assetUploadBucketRole")
    def asset_upload_bucket_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The role used by the BucketDeployment to upload the artifacts to an s3 bucket.

        In case you provide your own bucket for storing the artifacts (entrypoint and virtual environment archive),
        you must provide s3 write access to this role to upload the artifacts.
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "assetUploadBucketRole"))

    @builtins.property
    @jsii.member(jsii_name="entrypointS3Uri")
    def entrypoint_s3_uri(self) -> builtins.str:
        '''The S3 location where the entry point is saved in S3.

        You pass this location to your Spark job.
        '''
        return typing.cast(builtins.str, jsii.get(self, "entrypointS3Uri"))

    @builtins.property
    @jsii.member(jsii_name="sparkVenvConf")
    def spark_venv_conf(self) -> typing.Optional[builtins.str]:
        '''The Spark config containing the configuration of virtual environment archive with all dependencies.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sparkVenvConf"))

    @builtins.property
    @jsii.member(jsii_name="venvArchiveS3Uri")
    def venv_archive_s3_uri(self) -> typing.Optional[builtins.str]:
        '''The S3 location where the archive of the Python virtual environment with all dependencies is stored.

        You pass this location to your Spark job.
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "venvArchiveS3Uri"))


@jsii.data_type(
    jsii_type="aws-dsf.PySparkApplicationPackageProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "entrypoint_path": "entrypointPath",
        "artifacts_bucket": "artifactsBucket",
        "dependencies_folder": "dependenciesFolder",
        "removal_policy": "removalPolicy",
        "venv_archive_path": "venvArchivePath",
    },
)
class PySparkApplicationPackageProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        entrypoint_path: builtins.str,
        artifacts_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        dependencies_folder: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        venv_archive_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for the {PySparkApplicationPackage} construct.

        :param application_name: The name of the pyspark application. This name is used as a parent directory in s3 to store the entrypoint as well as virtual environment archive
        :param entrypoint_path: The source path in your code base where you have the entrypoint stored example ``~/my-project/src/entrypoint.py``.
        :param artifacts_bucket: The S3 bucket where to upload the artifacts of the Spark Job This is where the entry point and archive of the virtual environment will be stored. Default: - A bucket is created
        :param dependencies_folder: The source directory where you have ``requirements.txt`` or ``pyproject.toml`` that will install external AND internal Python packages. If your PySpark application has more than one Python file, you need to `package your Python project <https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_. This location must also have a ``Dockerfile`` that will `create a virtual environment and build an archive <https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/using-python-libraries.html#building-python-virtual-env>`_ out of it. Default: - No dependencies (internal or external) are packaged. Only the entrypoint can be used in the Spark Job.
        :param removal_policy: The removal policy when deleting the CDK resource. Resources like Amazon cloudwatch log or Amazon S3 bucket. If DESTROY is selected, the context value '@aws-data-solutions-framework/removeDataOnDestroy' in the 'cdk.json' or 'cdk.context.json' must be set to true. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param venv_archive_path: The path of the Python virtual environment archive generated in the Docker container. This is the output path used in the ``venv-pack -o`` command in your Dockerfile. Default: - No virtual environment archive is packaged. Only the entrypoint can be used in the Spark Job. It is required if the ``dependenciesFolder`` is provided.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95922462bacfe7c9bc74765ccd0278404efe4439f1e2bc491318a6d221a5ccb2)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument entrypoint_path", value=entrypoint_path, expected_type=type_hints["entrypoint_path"])
            check_type(argname="argument artifacts_bucket", value=artifacts_bucket, expected_type=type_hints["artifacts_bucket"])
            check_type(argname="argument dependencies_folder", value=dependencies_folder, expected_type=type_hints["dependencies_folder"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument venv_archive_path", value=venv_archive_path, expected_type=type_hints["venv_archive_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_name": application_name,
            "entrypoint_path": entrypoint_path,
        }
        if artifacts_bucket is not None:
            self._values["artifacts_bucket"] = artifacts_bucket
        if dependencies_folder is not None:
            self._values["dependencies_folder"] = dependencies_folder
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if venv_archive_path is not None:
            self._values["venv_archive_path"] = venv_archive_path

    @builtins.property
    def application_name(self) -> builtins.str:
        '''The name of the pyspark application.

        This name is used as a parent directory in s3 to store the entrypoint as well as virtual environment archive
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entrypoint_path(self) -> builtins.str:
        '''The source path in your code base where you have the entrypoint stored example ``~/my-project/src/entrypoint.py``.'''
        result = self._values.get("entrypoint_path")
        assert result is not None, "Required property 'entrypoint_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifacts_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''The S3 bucket where to upload the artifacts of the Spark Job This is where the entry point and archive of the virtual environment will be stored.

        :default: - A bucket is created
        '''
        result = self._values.get("artifacts_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def dependencies_folder(self) -> typing.Optional[builtins.str]:
        '''The source directory where you have ``requirements.txt`` or ``pyproject.toml`` that will install external AND internal Python packages. If your PySpark application has more than one Python file, you need to `package your Python project <https://packaging.python.org/en/latest/tutorials/packaging-projects/>`_. This location must also have a ``Dockerfile`` that will `create a virtual environment and build an archive <https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/using-python-libraries.html#building-python-virtual-env>`_ out of it.

        :default: - No dependencies (internal or external) are packaged. Only the entrypoint can be used in the Spark Job.
        '''
        result = self._values.get("dependencies_folder")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy when deleting the CDK resource.

        Resources like Amazon cloudwatch log or Amazon S3 bucket.
        If DESTROY is selected, the context value '@aws-data-solutions-framework/removeDataOnDestroy'
        in the 'cdk.json' or 'cdk.context.json' must be set to true.

        :default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def venv_archive_path(self) -> typing.Optional[builtins.str]:
        '''The path of the Python virtual environment archive generated in the Docker container.

        This is the output path used in the ``venv-pack -o`` command in your Dockerfile.

        :default: - No virtual environment archive is packaged. Only the entrypoint can be used in the Spark Job. It is required if the ``dependenciesFolder`` is provided.
        '''
        result = self._values.get("venv_archive_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PySparkApplicationPackageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SparkEmrCICDPipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.SparkEmrCICDPipeline",
):
    '''A CICD Pipeline that tests and deploys a Spark application in cross-account environments using CDK Pipelines.

    Example::

        const stack = new Stack();
        
        interface MyApplicationStackProps extends StackProps {
          readonly stage: CICDStage;
        }
        
        class MyApplicationStack extends Stack {
          constructor(scope: Stack, props?: MyApplicationStackProps) {
            super(scope, 'MyApplicationStack');
        *     const bucket = new Bucket(this, 'TestBucket', {
              autoDeleteObjects: true,
              removalPolicy: RemovalPolicy.DESTROY,
            });
            new CfnOutput(this, 'BucketName', { value: bucket.bucketName });
          }
        }
        
        class MyStackFactory implements ApplicationStackFactory {
          createStack(scope: Stack, stage: CICDStage): Stack {
            return new MyApplicationStack(scope, { stage });
          }
        }
        
        new SparkCICDPipeline(stack, 'TestConstruct', {
          sparkApplicationName: 'test',
          applicationStackFactory: new MyStackFactory(),
          cdkApplicationPath: 'cdk/',
          sparkApplicationPath: 'spark/',
          sparkImage: SparkImage.EMR_SERVERLESS_6_10,
          integTestScript: 'cdk/integ-test.sh',
          integTestEnv: {
            TEST_BUCKET: 'BucketName',
          },
        });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        application_stack_factory: ApplicationStackFactory,
        spark_application_name: builtins.str,
        cdk_application_path: typing.Optional[builtins.str] = None,
        integ_test_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        integ_test_permissions: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        integ_test_script: typing.Optional[builtins.str] = None,
        spark_application_path: typing.Optional[builtins.str] = None,
        spark_image: typing.Optional["SparkImage"] = None,
    ) -> None:
        '''Construct a new instance of the SparkCICDPipeline class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param application_stack_factory: The application Stack to deploy in the different CDK Pipelines Stages.
        :param spark_application_name: The name of the Spark application to be deployed.
        :param cdk_application_path: The path to the folder that contains the CDK Application. Default: - The root of the repository
        :param integ_test_env: The environment variables to create from the Application Stack and to pass to the integration tests. This is used to interact with resources created by the Application Stack from within the integration tests script. Key is the name of the environment variable to create. Value is generally a CfnOutput name from the Application Stack. Default: - No environment variables
        :param integ_test_permissions: The IAM policy statements to add permissions for running the integration tests. Default: - No permissions
        :param integ_test_script: The path to the Shell script that contains integration tests. Default: - No integration tests are run
        :param spark_application_path: The path to the folder that contains the Spark Application. Default: - The root of the repository
        :param spark_image: The EMR Spark image to use to run the unit tests. Default: - EMR v6.12 is used
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61487ab0fa5733da780f29da9f7ad67e2a4073d65d7a7e95e889454cc14e810e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SparkEmrCICDPipelineProps(
            application_stack_factory=application_stack_factory,
            spark_application_name=spark_application_name,
            cdk_application_path=cdk_application_path,
            integ_test_env=integ_test_env,
            integ_test_permissions=integ_test_permissions,
            integ_test_script=integ_test_script,
            spark_application_path=spark_application_path,
            spark_image=spark_image,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="retrieveVersion")
    def retrieve_version(self) -> typing.Any:
        '''Retrieve ADSF package.json version.'''
        return typing.cast(typing.Any, jsii.invoke(self, "retrieveVersion", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_OWNED_TAG")
    def ADSF_OWNED_TAG(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_OWNED_TAG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_TRACKING_CODE")
    def ADSF_TRACKING_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_TRACKING_CODE"))

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> _aws_cdk_pipelines_ceddda9d.CodePipeline:
        '''The CodePipeline created as part of the Spark CICD Pipeline.'''
        return typing.cast(_aws_cdk_pipelines_ceddda9d.CodePipeline, jsii.get(self, "pipeline"))


@jsii.data_type(
    jsii_type="aws-dsf.SparkEmrCICDPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_stack_factory": "applicationStackFactory",
        "spark_application_name": "sparkApplicationName",
        "cdk_application_path": "cdkApplicationPath",
        "integ_test_env": "integTestEnv",
        "integ_test_permissions": "integTestPermissions",
        "integ_test_script": "integTestScript",
        "spark_application_path": "sparkApplicationPath",
        "spark_image": "sparkImage",
    },
)
class SparkEmrCICDPipelineProps:
    def __init__(
        self,
        *,
        application_stack_factory: ApplicationStackFactory,
        spark_application_name: builtins.str,
        cdk_application_path: typing.Optional[builtins.str] = None,
        integ_test_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        integ_test_permissions: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        integ_test_script: typing.Optional[builtins.str] = None,
        spark_application_path: typing.Optional[builtins.str] = None,
        spark_image: typing.Optional["SparkImage"] = None,
    ) -> None:
        '''Properties for SparkEmrCICDPipeline class.

        :param application_stack_factory: The application Stack to deploy in the different CDK Pipelines Stages.
        :param spark_application_name: The name of the Spark application to be deployed.
        :param cdk_application_path: The path to the folder that contains the CDK Application. Default: - The root of the repository
        :param integ_test_env: The environment variables to create from the Application Stack and to pass to the integration tests. This is used to interact with resources created by the Application Stack from within the integration tests script. Key is the name of the environment variable to create. Value is generally a CfnOutput name from the Application Stack. Default: - No environment variables
        :param integ_test_permissions: The IAM policy statements to add permissions for running the integration tests. Default: - No permissions
        :param integ_test_script: The path to the Shell script that contains integration tests. Default: - No integration tests are run
        :param spark_application_path: The path to the folder that contains the Spark Application. Default: - The root of the repository
        :param spark_image: The EMR Spark image to use to run the unit tests. Default: - EMR v6.12 is used
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c44927b44f0aa19de886c8a2e3f54622c8f7e0468c357cf86380a5da2207a6)
            check_type(argname="argument application_stack_factory", value=application_stack_factory, expected_type=type_hints["application_stack_factory"])
            check_type(argname="argument spark_application_name", value=spark_application_name, expected_type=type_hints["spark_application_name"])
            check_type(argname="argument cdk_application_path", value=cdk_application_path, expected_type=type_hints["cdk_application_path"])
            check_type(argname="argument integ_test_env", value=integ_test_env, expected_type=type_hints["integ_test_env"])
            check_type(argname="argument integ_test_permissions", value=integ_test_permissions, expected_type=type_hints["integ_test_permissions"])
            check_type(argname="argument integ_test_script", value=integ_test_script, expected_type=type_hints["integ_test_script"])
            check_type(argname="argument spark_application_path", value=spark_application_path, expected_type=type_hints["spark_application_path"])
            check_type(argname="argument spark_image", value=spark_image, expected_type=type_hints["spark_image"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_stack_factory": application_stack_factory,
            "spark_application_name": spark_application_name,
        }
        if cdk_application_path is not None:
            self._values["cdk_application_path"] = cdk_application_path
        if integ_test_env is not None:
            self._values["integ_test_env"] = integ_test_env
        if integ_test_permissions is not None:
            self._values["integ_test_permissions"] = integ_test_permissions
        if integ_test_script is not None:
            self._values["integ_test_script"] = integ_test_script
        if spark_application_path is not None:
            self._values["spark_application_path"] = spark_application_path
        if spark_image is not None:
            self._values["spark_image"] = spark_image

    @builtins.property
    def application_stack_factory(self) -> ApplicationStackFactory:
        '''The application Stack to deploy in the different CDK Pipelines Stages.'''
        result = self._values.get("application_stack_factory")
        assert result is not None, "Required property 'application_stack_factory' is missing"
        return typing.cast(ApplicationStackFactory, result)

    @builtins.property
    def spark_application_name(self) -> builtins.str:
        '''The name of the Spark application to be deployed.'''
        result = self._values.get("spark_application_name")
        assert result is not None, "Required property 'spark_application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cdk_application_path(self) -> typing.Optional[builtins.str]:
        '''The path to the folder that contains the CDK Application.

        :default: - The root of the repository
        '''
        result = self._values.get("cdk_application_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integ_test_env(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The environment variables to create from the Application Stack and to pass to the integration tests.

        This is used to interact with resources created by the Application Stack from within the integration tests script.
        Key is the name of the environment variable to create. Value is generally a CfnOutput name from the Application Stack.

        :default: - No environment variables
        '''
        result = self._values.get("integ_test_env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def integ_test_permissions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        '''The IAM policy statements to add permissions for running the integration tests.

        :default: - No permissions
        '''
        result = self._values.get("integ_test_permissions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def integ_test_script(self) -> typing.Optional[builtins.str]:
        '''The path to the Shell script that contains integration tests.

        :default: - No integration tests are run
        '''
        result = self._values.get("integ_test_script")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_application_path(self) -> typing.Optional[builtins.str]:
        '''The path to the folder that contains the Spark Application.

        :default: - The root of the repository
        '''
        result = self._values.get("spark_application_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_image(self) -> typing.Optional["SparkImage"]:
        '''The EMR Spark image to use to run the unit tests.

        :default: - EMR v6.12 is used
        '''
        result = self._values.get("spark_image")
        return typing.cast(typing.Optional["SparkImage"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkEmrCICDPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-dsf.SparkEmrServerlessJobProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "name": "name",
        "spark_submit_entry_point": "sparkSubmitEntryPoint",
        "application_configuration": "applicationConfiguration",
        "cloud_watch_encryption_key_arn": "cloudWatchEncryptionKeyArn",
        "cloud_watch_log_group_name": "cloudWatchLogGroupName",
        "cloud_watch_log_group_stream_prefix": "cloudWatchLogGroupStreamPrefix",
        "cloud_watch_logtypes": "cloudWatchLogtypes",
        "execution_role_arn": "executionRoleArn",
        "execution_timeout_minutes": "executionTimeoutMinutes",
        "persistent_app_ui": "persistentAppUi",
        "persistent_app_ui_key_arn": "persistentAppUIKeyArn",
        "s3_log_uri": "s3LogUri",
        "s3_log_uri_key_arn": "s3LogUriKeyArn",
        "spark_submit_entry_point_arguments": "sparkSubmitEntryPointArguments",
        "spark_submit_parameters": "sparkSubmitParameters",
        "tags": "tags",
    },
)
class SparkEmrServerlessJobProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        name: builtins.str,
        spark_submit_entry_point: builtins.str,
        application_configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        cloud_watch_encryption_key_arn: typing.Optional[builtins.str] = None,
        cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
        cloud_watch_log_group_stream_prefix: typing.Optional[builtins.str] = None,
        cloud_watch_logtypes: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        execution_timeout_minutes: typing.Optional[jsii.Number] = None,
        persistent_app_ui: typing.Optional[builtins.bool] = None,
        persistent_app_ui_key_arn: typing.Optional[builtins.str] = None,
        s3_log_uri: typing.Optional[builtins.str] = None,
        s3_log_uri_key_arn: typing.Optional[builtins.str] = None,
        spark_submit_entry_point_arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
        spark_submit_parameters: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''Simplified configuration for the EMR Serverless Job.

        :param application_id: 
        :param name: 
        :param spark_submit_entry_point: 
        :param application_configuration: 
        :param cloud_watch_encryption_key_arn: 
        :param cloud_watch_log_group_name: 
        :param cloud_watch_log_group_stream_prefix: 
        :param cloud_watch_logtypes: 
        :param execution_role_arn: 
        :param execution_timeout_minutes: 
        :param persistent_app_ui: 
        :param persistent_app_ui_key_arn: 
        :param s3_log_uri: 
        :param s3_log_uri_key_arn: 
        :param spark_submit_entry_point_arguments: 
        :param spark_submit_parameters: 
        :param tags: 

        :default: ERROR

        :link: [https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_StartJobRun.html]

        Example::

            s3://BUCKET_NAME/
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80efcc15c6e084225d8c253e4300582e9838eacf574362a7fa2bdc678277b8d)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spark_submit_entry_point", value=spark_submit_entry_point, expected_type=type_hints["spark_submit_entry_point"])
            check_type(argname="argument application_configuration", value=application_configuration, expected_type=type_hints["application_configuration"])
            check_type(argname="argument cloud_watch_encryption_key_arn", value=cloud_watch_encryption_key_arn, expected_type=type_hints["cloud_watch_encryption_key_arn"])
            check_type(argname="argument cloud_watch_log_group_name", value=cloud_watch_log_group_name, expected_type=type_hints["cloud_watch_log_group_name"])
            check_type(argname="argument cloud_watch_log_group_stream_prefix", value=cloud_watch_log_group_stream_prefix, expected_type=type_hints["cloud_watch_log_group_stream_prefix"])
            check_type(argname="argument cloud_watch_logtypes", value=cloud_watch_logtypes, expected_type=type_hints["cloud_watch_logtypes"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument execution_timeout_minutes", value=execution_timeout_minutes, expected_type=type_hints["execution_timeout_minutes"])
            check_type(argname="argument persistent_app_ui", value=persistent_app_ui, expected_type=type_hints["persistent_app_ui"])
            check_type(argname="argument persistent_app_ui_key_arn", value=persistent_app_ui_key_arn, expected_type=type_hints["persistent_app_ui_key_arn"])
            check_type(argname="argument s3_log_uri", value=s3_log_uri, expected_type=type_hints["s3_log_uri"])
            check_type(argname="argument s3_log_uri_key_arn", value=s3_log_uri_key_arn, expected_type=type_hints["s3_log_uri_key_arn"])
            check_type(argname="argument spark_submit_entry_point_arguments", value=spark_submit_entry_point_arguments, expected_type=type_hints["spark_submit_entry_point_arguments"])
            check_type(argname="argument spark_submit_parameters", value=spark_submit_parameters, expected_type=type_hints["spark_submit_parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "name": name,
            "spark_submit_entry_point": spark_submit_entry_point,
        }
        if application_configuration is not None:
            self._values["application_configuration"] = application_configuration
        if cloud_watch_encryption_key_arn is not None:
            self._values["cloud_watch_encryption_key_arn"] = cloud_watch_encryption_key_arn
        if cloud_watch_log_group_name is not None:
            self._values["cloud_watch_log_group_name"] = cloud_watch_log_group_name
        if cloud_watch_log_group_stream_prefix is not None:
            self._values["cloud_watch_log_group_stream_prefix"] = cloud_watch_log_group_stream_prefix
        if cloud_watch_logtypes is not None:
            self._values["cloud_watch_logtypes"] = cloud_watch_logtypes
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if execution_timeout_minutes is not None:
            self._values["execution_timeout_minutes"] = execution_timeout_minutes
        if persistent_app_ui is not None:
            self._values["persistent_app_ui"] = persistent_app_ui
        if persistent_app_ui_key_arn is not None:
            self._values["persistent_app_ui_key_arn"] = persistent_app_ui_key_arn
        if s3_log_uri is not None:
            self._values["s3_log_uri"] = s3_log_uri
        if s3_log_uri_key_arn is not None:
            self._values["s3_log_uri_key_arn"] = s3_log_uri_key_arn
        if spark_submit_entry_point_arguments is not None:
            self._values["spark_submit_entry_point_arguments"] = spark_submit_entry_point_arguments
        if spark_submit_parameters is not None:
            self._values["spark_submit_parameters"] = spark_submit_parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> builtins.str:
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spark_submit_entry_point(self) -> builtins.str:
        result = self._values.get("spark_submit_entry_point")
        assert result is not None, "Required property 'spark_submit_entry_point' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_configuration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("application_configuration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def cloud_watch_encryption_key_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_watch_encryption_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_log_group_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_watch_log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_log_group_stream_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_watch_log_group_stream_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_logtypes(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_watch_logtypes")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("execution_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def persistent_app_ui(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("persistent_app_ui")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def persistent_app_ui_key_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("persistent_app_ui_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_log_uri(self) -> typing.Optional[builtins.str]:
        result = self._values.get("s3_log_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_log_uri_key_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("s3_log_uri_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_submit_entry_point_arguments(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("spark_submit_entry_point_arguments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def spark_submit_parameters(self) -> typing.Optional[builtins.str]:
        result = self._values.get("spark_submit_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkEmrServerlessJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SparkEmrServerlessRuntime(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.SparkEmrServerlessRuntime",
):
    '''A construct to create a Spark EMR Serverless Application, along with methods to create IAM roles having the least privilege.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        architecture: typing.Optional[Architecture] = None,
        auto_start_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.ImageConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        initial_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        maximum_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_label: typing.Optional[EmrRuntimeVersion] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        worker_type_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.WorkerTypeSpecificationInputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''
        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param name: The name of the application. The name must be less than 64 characters. *Pattern* : ``^[A-Za-z0-9._\\\\/#-]+$``
        :param architecture: The CPU architecture type of the application.
        :param auto_start_configuration: The configuration for an application to automatically start on job submission.
        :param auto_stop_configuration: The configuration for an application to automatically stop after a certain amount of time being idle.
        :param image_configuration: The image configuration.
        :param initial_capacity: The initial capacity of the application.
        :param maximum_capacity: The maximum capacity of the application. This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.
        :param network_configuration: The network configuration for customer VPC connectivity for the application. If no configuration is created, the a VPC with 3 public subnets and 3 private subnets is created The 3 public subnets and 3 private subnets are each created in an Availability Zone (AZ) The VPC has one NAT Gateway per AZ and an S3 endpoint Default: - a VPC and a security group are created, these are accessed as construct attribute.
        :param release_label: The EMR release version associated with the application. The EMR release can be found in this `documentation <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-6x.html>`_
        :param removal_policy: The removal policy when deleting the CDK resource. Resources like Amazon cloudwatch log or Amazon S3 bucket If DESTROY is selected, context value Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param worker_type_specifications: The container image to use in the application. If none is provided the application will use the base Amazon EMR Serverless image for the specified EMR release. This is an `example <https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/application-custom-image.html>`_ of usage
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__650e95755a31bcb91363c323fe5d83d024412ad7c12a701cc83640dd10b55ffa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SparkEmrServerlessRuntimeProps(
            name=name,
            architecture=architecture,
            auto_start_configuration=auto_start_configuration,
            auto_stop_configuration=auto_stop_configuration,
            image_configuration=image_configuration,
            initial_capacity=initial_capacity,
            maximum_capacity=maximum_capacity,
            network_configuration=network_configuration,
            release_label=release_label,
            removal_policy=removal_policy,
            worker_type_specifications=worker_type_specifications,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createExecutionRole")
    @builtins.classmethod
    def create_execution_role(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        execution_role_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
        iam_policy_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''A static method which will create an execution IAM role that can be assumed by EMR Serverless The method returns the role it creates.

        :param scope: the scope in which to create the role.
        :param id: passed to the IAM Role construct object.
        :param execution_role_policy_document: the inline policy document to attach to the role. These are IAM policies needed by the job. This parameter is mutually execlusive with iamPolicyName.
        :param iam_policy_name: the IAM policy name to attach to the role, this is mutually execlusive with executionRolePolicyDocument.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da17b882fc735554e5b0edce68bfb1566ec02e03ed3455c96bff6dd877d9897a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument execution_role_policy_document", value=execution_role_policy_document, expected_type=type_hints["execution_role_policy_document"])
            check_type(argname="argument iam_policy_name", value=iam_policy_name, expected_type=type_hints["iam_policy_name"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.sinvoke(cls, "createExecutionRole", [scope, id, execution_role_policy_document, iam_policy_name]))

    @jsii.member(jsii_name="grantStartJobExecution")
    @builtins.classmethod
    def grant_start_job_execution(
        cls,
        start_job_role: _aws_cdk_aws_iam_ceddda9d.IRole,
        execution_role_arn: typing.Sequence[builtins.str],
        application_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''A static method which will grant an IAM Role the right to start and monitor a job.

        The method will also attach an iam:PassRole permission limited to the IAM Job Execution roles passed

        :param start_job_role: the role that will call the start job api and which needs to have the iam:PassRole permission.
        :param execution_role_arn: the role used by EMR Serverless to access resources during the job execution.
        :param application_arns: the EMR Serverless aplication ARN, this is used by the method to limit the EMR Serverless applications the role can submit job to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d09ff2f77cd0eeb1fc5b48e1389cbe2a0d7b54723a488361373ebc237a1c22)
            check_type(argname="argument start_job_role", value=start_job_role, expected_type=type_hints["start_job_role"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument application_arns", value=application_arns, expected_type=type_hints["application_arns"])
        return typing.cast(None, jsii.sinvoke(cls, "grantStartJobExecution", [start_job_role, execution_role_arn, application_arns]))

    @jsii.member(jsii_name="grantStartExecution")
    def grant_start_execution(
        self,
        start_job_role: _aws_cdk_aws_iam_ceddda9d.IRole,
        execution_role_arn: builtins.str,
    ) -> None:
        '''A method which will grant an IAM Role the right to start and monitor a job.

        The method will also attach an iam:PassRole permission to limited to the IAM Job Execution roles passed.
        The excution role will be able to submit job to the EMR Serverless application created by the construct.

        :param start_job_role: the role that will call the start job api and which need to have the iam:PassRole permission.
        :param execution_role_arn: the role use by EMR Serverless to access resources during the job execution.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b614865d5ca419d9c0f5328e3fd6b73befd44f3616af7e3fd76b65255d766920)
            check_type(argname="argument start_job_role", value=start_job_role, expected_type=type_hints["start_job_role"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
        return typing.cast(None, jsii.invoke(self, "grantStartExecution", [start_job_role, execution_role_arn]))

    @jsii.member(jsii_name="retrieveVersion")
    def retrieve_version(self) -> typing.Any:
        '''Retrieve ADSF package.json version.'''
        return typing.cast(typing.Any, jsii.invoke(self, "retrieveVersion", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_OWNED_TAG")
    def ADSF_OWNED_TAG(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_OWNED_TAG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_TRACKING_CODE")
    def ADSF_TRACKING_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_TRACKING_CODE"))

    @builtins.property
    @jsii.member(jsii_name="applicationArn")
    def application_arn(self) -> builtins.str:
        '''The ARN of the EMR Serverless application, such as arn:aws:emr-serverless:us-east-1:123456789012:application/ab4rp1abcs8xz47n3x0example This is used to expose the ARN of the application to the user.'''
        return typing.cast(builtins.str, jsii.get(self, "applicationArn"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The id of the EMR Serverless application, such as ab4rp1abcs8xz47n3x0example This is used to expose the id of the application to the user.'''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @builtins.property
    @jsii.member(jsii_name="emrApplicationSecurityGroup")
    def emr_application_security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]:
        '''If no VPC is provided, one is created by default along with a security group attached to the EMR Serverless Application This attribute is used to expose the security group, if you provide your own security group through the {@link SparkEmrServerlessRuntimeProps} the attribute will be ``undefined``.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup], jsii.get(self, "emrApplicationSecurityGroup"))

    @builtins.property
    @jsii.member(jsii_name="s3GatewayVpcEndpoint")
    def s3_gateway_vpc_endpoint(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint]:
        '''If no VPC is provided, one is created by default This attribute is used to expose the Gateway Vpc Endpoint for Amazon S3 The attribute will be undefined if you provided the ``networkConfiguration`` through the {@link SparkEmrServerlessRuntimeProps}.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.GatewayVpcEndpoint], jsii.get(self, "s3GatewayVpcEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Vpc]:
        '''If no VPC is provided, one is created by default This attribute is used to expose the VPC, if you provide your own VPC through the {@link SparkEmrServerlessRuntimeProps} the attribute will be ``undefined``.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.Vpc], jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="aws-dsf.SparkEmrServerlessRuntimeProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "architecture": "architecture",
        "auto_start_configuration": "autoStartConfiguration",
        "auto_stop_configuration": "autoStopConfiguration",
        "image_configuration": "imageConfiguration",
        "initial_capacity": "initialCapacity",
        "maximum_capacity": "maximumCapacity",
        "network_configuration": "networkConfiguration",
        "release_label": "releaseLabel",
        "removal_policy": "removalPolicy",
        "worker_type_specifications": "workerTypeSpecifications",
    },
)
class SparkEmrServerlessRuntimeProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        architecture: typing.Optional[Architecture] = None,
        auto_start_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.ImageConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        initial_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        maximum_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        release_label: typing.Optional[EmrRuntimeVersion] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        worker_type_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.WorkerTypeSpecificationInputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for the {SparkRuntimeServerless} construct.

        :param name: The name of the application. The name must be less than 64 characters. *Pattern* : ``^[A-Za-z0-9._\\\\/#-]+$``
        :param architecture: The CPU architecture type of the application.
        :param auto_start_configuration: The configuration for an application to automatically start on job submission.
        :param auto_stop_configuration: The configuration for an application to automatically stop after a certain amount of time being idle.
        :param image_configuration: The image configuration.
        :param initial_capacity: The initial capacity of the application.
        :param maximum_capacity: The maximum capacity of the application. This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.
        :param network_configuration: The network configuration for customer VPC connectivity for the application. If no configuration is created, the a VPC with 3 public subnets and 3 private subnets is created The 3 public subnets and 3 private subnets are each created in an Availability Zone (AZ) The VPC has one NAT Gateway per AZ and an S3 endpoint Default: - a VPC and a security group are created, these are accessed as construct attribute.
        :param release_label: The EMR release version associated with the application. The EMR release can be found in this `documentation <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-6x.html>`_
        :param removal_policy: The removal policy when deleting the CDK resource. Resources like Amazon cloudwatch log or Amazon S3 bucket If DESTROY is selected, context value Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param worker_type_specifications: The container image to use in the application. If none is provided the application will use the base Amazon EMR Serverless image for the specified EMR release. This is an `example <https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/application-custom-image.html>`_ of usage
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28379121f70557d244a0691da885b789a630cf172d132cfb689d7540495ebb71)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auto_start_configuration", value=auto_start_configuration, expected_type=type_hints["auto_start_configuration"])
            check_type(argname="argument auto_stop_configuration", value=auto_stop_configuration, expected_type=type_hints["auto_stop_configuration"])
            check_type(argname="argument image_configuration", value=image_configuration, expected_type=type_hints["image_configuration"])
            check_type(argname="argument initial_capacity", value=initial_capacity, expected_type=type_hints["initial_capacity"])
            check_type(argname="argument maximum_capacity", value=maximum_capacity, expected_type=type_hints["maximum_capacity"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument worker_type_specifications", value=worker_type_specifications, expected_type=type_hints["worker_type_specifications"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_start_configuration is not None:
            self._values["auto_start_configuration"] = auto_start_configuration
        if auto_stop_configuration is not None:
            self._values["auto_stop_configuration"] = auto_stop_configuration
        if image_configuration is not None:
            self._values["image_configuration"] = image_configuration
        if initial_capacity is not None:
            self._values["initial_capacity"] = initial_capacity
        if maximum_capacity is not None:
            self._values["maximum_capacity"] = maximum_capacity
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if release_label is not None:
            self._values["release_label"] = release_label
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if worker_type_specifications is not None:
            self._values["worker_type_specifications"] = worker_type_specifications

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the application. The name must be less than 64 characters.

        *Pattern* : ``^[A-Za-z0-9._\\\\/#-]+$``
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[Architecture]:
        '''The CPU architecture type of the application.'''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[Architecture], result)

    @builtins.property
    def auto_start_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStartConfigurationProperty]]:
        '''The configuration for an application to automatically start on job submission.'''
        result = self._values.get("auto_start_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStartConfigurationProperty]], result)

    @builtins.property
    def auto_stop_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStopConfigurationProperty]]:
        '''The configuration for an application to automatically stop after a certain amount of time being idle.'''
        result = self._values.get("auto_stop_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStopConfigurationProperty]], result)

    @builtins.property
    def image_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.ImageConfigurationInputProperty]]:
        '''The image configuration.'''
        result = self._values.get("image_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.ImageConfigurationInputProperty]], result)

    @builtins.property
    def initial_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.InitialCapacityConfigKeyValuePairProperty]]]]:
        '''The initial capacity of the application.'''
        result = self._values.get("initial_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.List[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.InitialCapacityConfigKeyValuePairProperty]]]], result)

    @builtins.property
    def maximum_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.MaximumAllowedResourcesProperty]]:
        '''The maximum capacity of the application.

        This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.
        '''
        result = self._values.get("maximum_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.MaximumAllowedResourcesProperty]], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.NetworkConfigurationProperty]]:
        '''The network configuration for customer VPC connectivity for the application.

        If no configuration is created, the a VPC with 3 public subnets and 3 private subnets is created
        The 3 public subnets and 3 private subnets are each created in an Availability Zone (AZ)
        The VPC has one NAT Gateway per AZ and an S3 endpoint

        :default: - a VPC and a security group are created, these are accessed as construct attribute.
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.NetworkConfigurationProperty]], result)

    @builtins.property
    def release_label(self) -> typing.Optional[EmrRuntimeVersion]:
        '''The EMR release version associated with the application.

        The EMR release can be found in this `documentation <https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-release-6x.html>`_

        :see: EMR_DEFAULT_VERSION
        '''
        result = self._values.get("release_label")
        return typing.cast(typing.Optional[EmrRuntimeVersion], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy when deleting the CDK resource.

        Resources like Amazon cloudwatch log or Amazon S3 bucket
        If DESTROY is selected, context value

        :default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def worker_type_specifications(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.WorkerTypeSpecificationInputProperty]]]]:
        '''The container image to use in the application.

        If none is provided the application will use the base Amazon EMR Serverless image for the specified EMR release.
        This is an `example <https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/application-custom-image.html>`_ of usage
        '''
        result = self._values.get("worker_type_specifications")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, _aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.WorkerTypeSpecificationInputProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkEmrServerlessRuntimeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="aws-dsf.SparkImage")
class SparkImage(enum.Enum):
    '''The list of supported Spark images to use in the SparkCICDPipeline.'''

    EMR_6_12 = "EMR_6_12"
    EMR_6_11 = "EMR_6_11"
    EMR_6_10 = "EMR_6_10"
    EMR_6_9 = "EMR_6_9"


class SparkJob(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="aws-dsf.SparkJob",
):
    '''A base construct to run Spark Jobs Creates an AWS Step Functions State Machine that orchestrates the Spark Job.

    :see: EmrOnEksSparkJob for EMR On EKS implementation
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        tracking_tag: builtins.str,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    ) -> None:
        '''Constructs a new instance of the SparkJob class.

        :param scope: the Scope of the CDK Construct.
        :param id: the ID of the CDK Construct.
        :param tracking_tag: -
        :param removal_policy: The removal policy when deleting the CDK resource. If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true. Otherwise the removalPolicy is reverted to RETAIN. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param schedule: Schedule to run the Step Functions state machine.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1418d4f50fb877ff7647994fe2e2abc6d459071dbb415e2f663266c3237e055)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tracking_tag", value=tracking_tag, expected_type=type_hints["tracking_tag"])
        props = SparkJobProps(removal_policy=removal_policy, schedule=schedule)

        jsii.create(self.__class__, self, [scope, id, tracking_tag, props])

    @jsii.member(jsii_name="createCloudWatchLogsLogGroup")
    def _create_cloud_watch_logs_log_group(
        self,
        name: builtins.str,
        encryption_key_arn: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_logs_ceddda9d.LogGroup:
        '''Creates an encrypted CloudWatch Logs group to store the Spark job logs.

        :param name: CloudWatch Logs group name of cloudwatch log group to store the Spark job logs.
        :param encryption_key_arn: KMS Key ARN for encryption.

        :default: - Server-side encryption managed by CloudWatch Logs.

        :return: LogGroup CloudWatch Logs group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7998a3d6621fe869428f737ecd2fd7418d0a002a3fd457b4c0af9ca13d62e0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
        return typing.cast(_aws_cdk_aws_logs_ceddda9d.LogGroup, jsii.invoke(self, "createCloudWatchLogsLogGroup", [name, encryption_key_arn]))

    @jsii.member(jsii_name="createS3LogBucket")
    def _create_s3_log_bucket(
        self,
        s3_log_uri: typing.Optional[builtins.str] = None,
        encryption_key_arn: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''Creates or import an S3 bucket to store the logs of the Spark job.

        The bucket is created with SSE encryption (KMS managed or provided by user).

        :param s3_log_uri: S3 path to store the logs of the Spark job.
        :param encryption_key_arn: KMS Key ARN for encryption.

        :default: - Master KMS key of the account.

        :return: string S3 path to store the logs.

        Example::

            s3://<bucket-name>/
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c995e1c6ded7405cddd89784253155281f99e6543f07a4fbafdaa5c2684a695)
            check_type(argname="argument s3_log_uri", value=s3_log_uri, expected_type=type_hints["s3_log_uri"])
            check_type(argname="argument encryption_key_arn", value=encryption_key_arn, expected_type=type_hints["encryption_key_arn"])
        return typing.cast(builtins.str, jsii.invoke(self, "createS3LogBucket", [s3_log_uri, encryption_key_arn]))

    @jsii.member(jsii_name="createStateMachine")
    def _create_state_machine(
        self,
        job_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine:
        '''Creates a State Machine that orchestrates the Spark Job.

        This is a default implementation that can be overridden by the extending class.

        :param job_timeout: Timeout for the state machine.
        :param schedule: Schedule to run the state machine.

        :default: no schedule

        :return: StateMachine

        :defautl: 30 minutes
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661e0d9b9dee5b069bed1dae2610394a9c947e8824aaa763892c6d897e136fef)
            check_type(argname="argument job_timeout", value=job_timeout, expected_type=type_hints["job_timeout"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine, jsii.invoke(self, "createStateMachine", [job_timeout, schedule]))

    @jsii.member(jsii_name="grantExecutionRole")
    @abc.abstractmethod
    def _grant_execution_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''Grants the execution role to the Step Functions state machine.

        :param role: -
        '''
        ...

    @jsii.member(jsii_name="retrieveVersion")
    def retrieve_version(self) -> typing.Any:
        '''Retrieve ADSF package.json version.'''
        return typing.cast(typing.Any, jsii.invoke(self, "retrieveVersion", []))

    @jsii.member(jsii_name="returnJobFailTaskProps")
    @abc.abstractmethod
    def _return_job_fail_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.FailProps:
        '''Parameters for Step Functions task that fails the Spark job.

        :return: FailProps
        '''
        ...

    @jsii.member(jsii_name="returnJobMonitorTaskProps")
    @abc.abstractmethod
    def _return_job_monitor_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Parameters for Step Functions task that monitors the Spark job.

        :return: CallAwsServiceProps
        '''
        ...

    @jsii.member(jsii_name="returnJobStartTaskProps")
    @abc.abstractmethod
    def _return_job_start_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Parameters for Step Functions task that runs the Spark job.

        :return: CallAwsServiceProps
        '''
        ...

    @jsii.member(jsii_name="returnJobStatusCancelled")
    @abc.abstractmethod
    def _return_job_status_cancelled(self) -> builtins.str:
        '''Returns the status of the Spark job that is cancelled based on the GetJobRun API response.'''
        ...

    @jsii.member(jsii_name="returnJobStatusFailed")
    @abc.abstractmethod
    def _return_job_status_failed(self) -> builtins.str:
        '''Returns the status of the Spark job that failed based on the GetJobRun API response.

        :return: string
        '''
        ...

    @jsii.member(jsii_name="returnJobStatusSucceed")
    @abc.abstractmethod
    def _return_job_status_succeed(self) -> builtins.str:
        '''Returns the status of the Spark job that succeeded based on the GetJobRun API response.

        :return: string
        '''
        ...

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_OWNED_TAG")
    def ADSF_OWNED_TAG(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_OWNED_TAG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ADSF_TRACKING_CODE")
    def ADSF_TRACKING_CODE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "ADSF_TRACKING_CODE"))

    @builtins.property
    @jsii.member(jsii_name="cloudwatchGroup")
    def _cloudwatch_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup]:
        '''CloudWatch Logs Group for the Spark job logs.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup], jsii.get(self, "cloudwatchGroup"))

    @_cloudwatch_group.setter
    def _cloudwatch_group(
        self,
        value: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f33e28e9797394601192a928f4cb307dd4d8422f1e215b98c9c26bb9f3c81d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudwatchGroup", value)

    @builtins.property
    @jsii.member(jsii_name="s3LogBucket")
    def _s3_log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''S3 log bucket for the Spark job logs.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], jsii.get(self, "s3LogBucket"))

    @_s3_log_bucket.setter
    def _s3_log_bucket(
        self,
        value: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5d951ef036997c6f88bca2d19a3198d3770dbf7bfbc5b56f91a85453efdd593)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "s3LogBucket", value)

    @builtins.property
    @jsii.member(jsii_name="stateMachine")
    def state_machine(
        self,
    ) -> typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine]:
        '''Step Functions StateMachine created to orchestrate the Spark Job.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine], jsii.get(self, "stateMachine"))

    @state_machine.setter
    def state_machine(
        self,
        value: typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e0606d5957f6210ca926645cc86cf2622e957588d0b9fb2938803856d9cfd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stateMachine", value)


class _SparkJobProxy(SparkJob):
    @jsii.member(jsii_name="grantExecutionRole")
    def _grant_execution_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''Grants the execution role to the Step Functions state machine.

        :param role: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a041df026c0912d298b19efd093b69b490847214b6c4c9da520d99c43166d057)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "grantExecutionRole", [role]))

    @jsii.member(jsii_name="returnJobFailTaskProps")
    def _return_job_fail_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.FailProps:
        '''Parameters for Step Functions task that fails the Spark job.

        :return: FailProps
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.FailProps, jsii.invoke(self, "returnJobFailTaskProps", []))

    @jsii.member(jsii_name="returnJobMonitorTaskProps")
    def _return_job_monitor_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Parameters for Step Functions task that monitors the Spark job.

        :return: CallAwsServiceProps
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps, jsii.invoke(self, "returnJobMonitorTaskProps", []))

    @jsii.member(jsii_name="returnJobStartTaskProps")
    def _return_job_start_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Parameters for Step Functions task that runs the Spark job.

        :return: CallAwsServiceProps
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps, jsii.invoke(self, "returnJobStartTaskProps", []))

    @jsii.member(jsii_name="returnJobStatusCancelled")
    def _return_job_status_cancelled(self) -> builtins.str:
        '''Returns the status of the Spark job that is cancelled based on the GetJobRun API response.'''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusCancelled", []))

    @jsii.member(jsii_name="returnJobStatusFailed")
    def _return_job_status_failed(self) -> builtins.str:
        '''Returns the status of the Spark job that failed based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusFailed", []))

    @jsii.member(jsii_name="returnJobStatusSucceed")
    def _return_job_status_succeed(self) -> builtins.str:
        '''Returns the status of the Spark job that succeeded based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusSucceed", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SparkJob).__jsii_proxy_class__ = lambda : _SparkJobProxy


@jsii.data_type(
    jsii_type="aws-dsf.SparkJobProps",
    jsii_struct_bases=[],
    name_mapping={"removal_policy": "removalPolicy", "schedule": "schedule"},
)
class SparkJobProps:
    def __init__(
        self,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    ) -> None:
        '''Properties for the SparkJob construct.

        :param removal_policy: The removal policy when deleting the CDK resource. If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true. Otherwise the removalPolicy is reverted to RETAIN. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param schedule: Schedule to run the Step Functions state machine.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__319ed6eaa80f31c0f7b214156f94ef01bb26df312dd1cd2b592ab8eb59a3f1c5)
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy when deleting the CDK resource.

        If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true.
        Otherwise the removalPolicy is reverted to RETAIN.

        :default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''Schedule to run the Step Functions state machine.

        :see: Schedule
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.Schedule.html]
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SparkEmrEksJob(
    SparkJob,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.SparkEmrEksJob",
):
    '''A construct to run Spark Jobs using EMR on EKS.

    Creates a Step Functions State Machine that orchestrates the Spark Job.

    :default:

    ReleaseLabel: EMR version 6.12

    **Usage example**

    :see: SparkEmrEksJobProps parameters to be specified for the construct

    Example::

        const job = new SparkJob(stack, 'SparkJob', {
                 jobConfig:{
                      "Name": JsonPath.format('ge_profile-{}', JsonPath.uuid()),
                      "VirtualClusterId": "virtualClusterId",
                      "ExecutionRoleArn": "ROLE-ARN",
                      "JobDriver": {
                          "SparkSubmit": {
                              "EntryPoint": "s3://S3-BUCKET/pi.py",
                              "EntryPointArguments": [],
                              "SparkSubmitParameters": "--conf spark.executor.instances=2 --conf spark.executor.memory=2G --conf spark.driver.memory=2G --conf spark.executor.cores=4"
                          },
                      }
                 }
        } as EmrOnEksSparkJobApiProps);
        
        new cdk.CfnOutput(stack, 'SparkJobStateMachine', {
          value: job.stateMachine.stateMachineArn,
        });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union[typing.Union["SparkEmrEksJobApiProps", typing.Dict[builtins.str, typing.Any]], typing.Union["SparkEmrEksJobProps", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f32539b7e2c47d71a12823caefcb109ad1f9cabbd796d22f68c59a45061e968d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantExecutionRole")
    def _grant_execution_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''Grants the necessary permissions to the Step Functions StateMachine to be able to start EMR on EKS job.

        :param role: Step Functions StateMachine IAM role.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6eec87a3987c4a9ff90e0a5c23142dce11227cf574d3fffc3f371787dcbe26a)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "grantExecutionRole", [role]))

    @jsii.member(jsii_name="returnJobFailTaskProps")
    def _return_job_fail_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.FailProps:
        '''Returns the props for the Step Functions task that handles the failure  if the EMR Serverless job fails.

        :return: FailProps The error details of the failed Spark Job
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.FailProps, jsii.invoke(self, "returnJobFailTaskProps", []))

    @jsii.member(jsii_name="returnJobMonitorTaskProps")
    def _return_job_monitor_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Returns the props for the Step Functions CallAwsService Construct that checks the execution status of the Spark job.

        :return: CallAwsServiceProps

        :see: CallAwsService
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions_tasks.CallAwsService.html]
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps, jsii.invoke(self, "returnJobMonitorTaskProps", []))

    @jsii.member(jsii_name="returnJobStartTaskProps")
    def _return_job_start_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Returns the props for the Step Functions CallAwsService Construct that starts the Spark job, it calls the `StartJobRun API <https://docs.aws.amazon.com/emr-on-eks/latest/APIReference/API_StartJobRun.html>`_.

        :return: CallAwsServiceProps

        :see: CallAwsService
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions_tasks.CallAwsService.html]
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps, jsii.invoke(self, "returnJobStartTaskProps", []))

    @jsii.member(jsii_name="returnJobStatusCancelled")
    def _return_job_status_cancelled(self) -> builtins.str:
        '''Returns the status of the EMR Serverless job that is cancelled based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusCancelled", []))

    @jsii.member(jsii_name="returnJobStatusFailed")
    def _return_job_status_failed(self) -> builtins.str:
        '''Returns the status of the EMR on EKS job that failed based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusFailed", []))

    @jsii.member(jsii_name="returnJobStatusSucceed")
    def _return_job_status_succeed(self) -> builtins.str:
        '''Returns the status of the EMR on EKS job that succeeded  based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusSucceed", []))


@jsii.data_type(
    jsii_type="aws-dsf.SparkEmrEksJobApiProps",
    jsii_struct_bases=[SparkJobProps],
    name_mapping={
        "removal_policy": "removalPolicy",
        "schedule": "schedule",
        "job_config": "jobConfig",
        "execution_timeout_minutes": "executionTimeoutMinutes",
    },
)
class SparkEmrEksJobApiProps(SparkJobProps):
    def __init__(
        self,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        job_config: typing.Mapping[builtins.str, typing.Any],
        execution_timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Configuration for the EMR on EKS job.

        Use this interface when EmrOnEksSparkJobProps doesn't give you access to the configuration parameters you need.

        :param removal_policy: The removal policy when deleting the CDK resource. If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true. Otherwise the removalPolicy is reverted to RETAIN. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param schedule: Schedule to run the Step Functions state machine.
        :param job_config: EMR on EKS Job Configuration.
        :param execution_timeout_minutes: Job execution timeout in minutes. @default 30

        :link: [https://docs.aws.amazon.com/emr-on-eks/latest/APIReference/API_StartJobRun.html]
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2d7db25a1da2445441486c4ac7622d3dde1e724955d9c58a9f5600b56d9f00c)
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument job_config", value=job_config, expected_type=type_hints["job_config"])
            check_type(argname="argument execution_timeout_minutes", value=execution_timeout_minutes, expected_type=type_hints["execution_timeout_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_config": job_config,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if schedule is not None:
            self._values["schedule"] = schedule
        if execution_timeout_minutes is not None:
            self._values["execution_timeout_minutes"] = execution_timeout_minutes

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy when deleting the CDK resource.

        If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true.
        Otherwise the removalPolicy is reverted to RETAIN.

        :default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''Schedule to run the Step Functions state machine.

        :see: Schedule
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.Schedule.html]
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    @builtins.property
    def job_config(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''EMR on EKS Job Configuration.

        :link: [https://docs.aws.amazon.com/emr-on-eks/latest/APIReference/API_StartJobRun.html]
        '''
        result = self._values.get("job_config")
        assert result is not None, "Required property 'job_config' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    @builtins.property
    def execution_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''Job execution timeout in minutes.

        @default 30
        '''
        result = self._values.get("execution_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkEmrEksJobApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-dsf.SparkEmrEksJobProps",
    jsii_struct_bases=[SparkJobProps],
    name_mapping={
        "removal_policy": "removalPolicy",
        "schedule": "schedule",
        "execution_role_arn": "executionRoleArn",
        "name": "name",
        "spark_submit_entry_point": "sparkSubmitEntryPoint",
        "virtual_cluster_id": "virtualClusterId",
        "application_configuration": "applicationConfiguration",
        "cloud_watch_log_group_name": "cloudWatchLogGroupName",
        "cloud_watch_log_group_stream_prefix": "cloudWatchLogGroupStreamPrefix",
        "execution_timeout_minutes": "executionTimeoutMinutes",
        "max_retries": "maxRetries",
        "release_label": "releaseLabel",
        "s3_log_uri": "s3LogUri",
        "spark_submit_entry_point_arguments": "sparkSubmitEntryPointArguments",
        "spark_submit_parameters": "sparkSubmitParameters",
        "tags": "tags",
    },
)
class SparkEmrEksJobProps(SparkJobProps):
    def __init__(
        self,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        execution_role_arn: builtins.str,
        name: builtins.str,
        spark_submit_entry_point: builtins.str,
        virtual_cluster_id: builtins.str,
        application_configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
        cloud_watch_log_group_stream_prefix: typing.Optional[builtins.str] = None,
        execution_timeout_minutes: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        release_label: typing.Optional[builtins.str] = None,
        s3_log_uri: typing.Optional[builtins.str] = None,
        spark_submit_entry_point_arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
        spark_submit_parameters: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''Simplified configuration for the EMR Serverless Job.

        :param removal_policy: The removal policy when deleting the CDK resource. If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true. Otherwise the removalPolicy is reverted to RETAIN. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param schedule: Schedule to run the Step Functions state machine.
        :param execution_role_arn: 
        :param name: 
        :param spark_submit_entry_point: 
        :param virtual_cluster_id: 
        :param application_configuration: 
        :param cloud_watch_log_group_name: 
        :param cloud_watch_log_group_stream_prefix: 
        :param execution_timeout_minutes: 
        :param max_retries: 
        :param release_label: 
        :param s3_log_uri: 
        :param spark_submit_entry_point_arguments: 
        :param spark_submit_parameters: 
        :param tags: 

        :default: The name of the spark job.

        :link: (https://docs.aws.amazon.com/emr-on-eks/latest/APIReference/API_StartJobRun.html#emroneks-StartJobRun-request-tags)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bf09b1b5a5311cce03ff8bb4650e808b815061fe32e15015ef64856730e3d39)
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spark_submit_entry_point", value=spark_submit_entry_point, expected_type=type_hints["spark_submit_entry_point"])
            check_type(argname="argument virtual_cluster_id", value=virtual_cluster_id, expected_type=type_hints["virtual_cluster_id"])
            check_type(argname="argument application_configuration", value=application_configuration, expected_type=type_hints["application_configuration"])
            check_type(argname="argument cloud_watch_log_group_name", value=cloud_watch_log_group_name, expected_type=type_hints["cloud_watch_log_group_name"])
            check_type(argname="argument cloud_watch_log_group_stream_prefix", value=cloud_watch_log_group_stream_prefix, expected_type=type_hints["cloud_watch_log_group_stream_prefix"])
            check_type(argname="argument execution_timeout_minutes", value=execution_timeout_minutes, expected_type=type_hints["execution_timeout_minutes"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument s3_log_uri", value=s3_log_uri, expected_type=type_hints["s3_log_uri"])
            check_type(argname="argument spark_submit_entry_point_arguments", value=spark_submit_entry_point_arguments, expected_type=type_hints["spark_submit_entry_point_arguments"])
            check_type(argname="argument spark_submit_parameters", value=spark_submit_parameters, expected_type=type_hints["spark_submit_parameters"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "execution_role_arn": execution_role_arn,
            "name": name,
            "spark_submit_entry_point": spark_submit_entry_point,
            "virtual_cluster_id": virtual_cluster_id,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if schedule is not None:
            self._values["schedule"] = schedule
        if application_configuration is not None:
            self._values["application_configuration"] = application_configuration
        if cloud_watch_log_group_name is not None:
            self._values["cloud_watch_log_group_name"] = cloud_watch_log_group_name
        if cloud_watch_log_group_stream_prefix is not None:
            self._values["cloud_watch_log_group_stream_prefix"] = cloud_watch_log_group_stream_prefix
        if execution_timeout_minutes is not None:
            self._values["execution_timeout_minutes"] = execution_timeout_minutes
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if release_label is not None:
            self._values["release_label"] = release_label
        if s3_log_uri is not None:
            self._values["s3_log_uri"] = s3_log_uri
        if spark_submit_entry_point_arguments is not None:
            self._values["spark_submit_entry_point_arguments"] = spark_submit_entry_point_arguments
        if spark_submit_parameters is not None:
            self._values["spark_submit_parameters"] = spark_submit_parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy when deleting the CDK resource.

        If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true.
        Otherwise the removalPolicy is reverted to RETAIN.

        :default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''Schedule to run the Step Functions state machine.

        :see: Schedule
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.Schedule.html]
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    @builtins.property
    def execution_role_arn(self) -> builtins.str:
        result = self._values.get("execution_role_arn")
        assert result is not None, "Required property 'execution_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spark_submit_entry_point(self) -> builtins.str:
        result = self._values.get("spark_submit_entry_point")
        assert result is not None, "Required property 'spark_submit_entry_point' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def virtual_cluster_id(self) -> builtins.str:
        result = self._values.get("virtual_cluster_id")
        assert result is not None, "Required property 'virtual_cluster_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def application_configuration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("application_configuration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def cloud_watch_log_group_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_watch_log_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_watch_log_group_stream_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("cloud_watch_log_group_stream_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_timeout_minutes(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("execution_timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def release_label(self) -> typing.Optional[builtins.str]:
        result = self._values.get("release_label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_log_uri(self) -> typing.Optional[builtins.str]:
        result = self._values.get("s3_log_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def spark_submit_entry_point_arguments(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("spark_submit_entry_point_arguments")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def spark_submit_parameters(self) -> typing.Optional[builtins.str]:
        result = self._values.get("spark_submit_parameters")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkEmrEksJobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SparkEmrServerlessJob(
    SparkJob,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-dsf.SparkEmrServerlessJob",
):
    '''A construct to run Spark Jobs using EMR Serverless.

    creates a State Machine that orchestrates the Spark Job.

    :default:

    ClientToken: universally unique identifier (v4 UUID) generated using random numbers

    **Usage example**

    :see: SparkEmrServerlessJobProps parameters to be specified for the construct

    Example::

        const myFileSystemPolicy = new PolicyDocument({
          statements: [new PolicyStatement({
            actions: [
              's3:GetObject',
            ],
            resources: ['*'],
          })],
        });
        
        
        const myExecutionRole = SparkRuntimeServerless.createExecutionRole(stack, 'execRole1', myFileSystemPolicy);
        const applicationId = "APPLICATION_ID";
        const job = new SparkJob(stack, 'SparkJob', {
                 jobConfig:{
                      "Name": JsonPath.format('ge_profile-{}', JsonPath.uuid()),
                      "ApplicationId": applicationId,
                      "ExecutionRoleArn": myExecutionRole.roleArn,
                      "JobDriver": {
                          "SparkSubmit": {
                              "EntryPoint": "s3://S3-BUCKET/pi.py",
                              "EntryPointArguments": [],
                              "SparkSubmitParameters": "--conf spark.executor.instances=2 --conf spark.executor.memory=2G --conf spark.driver.memory=2G --conf spark.executor.cores=4"
                          },
                      }
                 }
        } as EmrServerlessSparkJobApiProps);
        
        new cdk.CfnOutput(stack, 'SparkJobStateMachine', {
          value: job.stateMachine.stateMachineArn,
        });
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Union[typing.Union["SparkEmrServerlessJobApiProps", typing.Dict[builtins.str, typing.Any]], typing.Union[SparkEmrServerlessJobProps, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e68c9f2b57d72d43b81a47c2ef94ff46489e9e54bcc7840f076cb7d87f3ed300)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantExecutionRole")
    def _grant_execution_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''Grants the necessary permissions to the Step Functions StateMachine to be able to start EMR Serverless job.

        :param role: Step Functions StateMachine IAM role.

        :see: SparkRuntimeServerless.grantJobExecution
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773098c03f67ddb1e1fcaab21ff5c63aac32b60626703e7b55320c7103cb42da)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "grantExecutionRole", [role]))

    @jsii.member(jsii_name="returnJobFailTaskProps")
    def _return_job_fail_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.FailProps:
        '''Returns the props for the step function task that handles the failure if the EMR Serverless job fails.

        :return: FailProps The error details of the failed Spark Job
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.FailProps, jsii.invoke(self, "returnJobFailTaskProps", []))

    @jsii.member(jsii_name="returnJobMonitorTaskProps")
    def _return_job_monitor_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Returns the props for the Step Functions CallAwsService Construct that checks the execution status of the Spark job, it calls the `GetJobRun API <https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_GetJobRun.html>`_.

        :return: CallAwsServiceProps

        :see: CallAwsService
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions_tasks.CallAwsService.html]
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps, jsii.invoke(self, "returnJobMonitorTaskProps", []))

    @jsii.member(jsii_name="returnJobStartTaskProps")
    def _return_job_start_task_props(
        self,
    ) -> _aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps:
        '''Returns the props for the Step Functions CallAwsService Construct that starts the Spark job, it calls the `StartJobRun API <https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_StartJobRun.html>`_.

        :return: CallAwsServiceProps

        :see: CallAwsService
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_stepfunctions_tasks.CallAwsService.html]
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_tasks_ceddda9d.CallAwsServiceProps, jsii.invoke(self, "returnJobStartTaskProps", []))

    @jsii.member(jsii_name="returnJobStatusCancelled")
    def _return_job_status_cancelled(self) -> builtins.str:
        '''Returns the status of the EMR Serverless job that is cancelled based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusCancelled", []))

    @jsii.member(jsii_name="returnJobStatusFailed")
    def _return_job_status_failed(self) -> builtins.str:
        '''Returns the status of the EMR Serverless job that failed based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusFailed", []))

    @jsii.member(jsii_name="returnJobStatusSucceed")
    def _return_job_status_succeed(self) -> builtins.str:
        '''Returns the status of the EMR Serverless job that succeeded based on the GetJobRun API response.

        :return: string
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "returnJobStatusSucceed", []))

    @builtins.property
    @jsii.member(jsii_name="sparkJobExecutionRole")
    def spark_job_execution_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Spark Job execution role.

        Use this property to add additional IAM permissions if necessary.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "sparkJobExecutionRole"))

    @spark_job_execution_role.setter
    def spark_job_execution_role(
        self,
        value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03e61df5ada036074c4d0512ac4b5e63558d6440cd037881048f6a7d4cbd77ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sparkJobExecutionRole", value)


@jsii.data_type(
    jsii_type="aws-dsf.SparkEmrServerlessJobApiProps",
    jsii_struct_bases=[SparkJobProps],
    name_mapping={
        "removal_policy": "removalPolicy",
        "schedule": "schedule",
        "job_config": "jobConfig",
    },
)
class SparkEmrServerlessJobApiProps(SparkJobProps):
    def __init__(
        self,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        job_config: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''Configuration for the EMR Serverless Job API.

        Use this interface when EmrServerlessJobProps doesn't give you access to the configuration parameters you need.

        :param removal_policy: The removal policy when deleting the CDK resource. If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true. Otherwise the removalPolicy is reverted to RETAIN. Default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        :param schedule: Schedule to run the Step Functions state machine.
        :param job_config: EMR Serverless Job Configuration.

        :link: [https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_StartJobRun.html]
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff96c9f1bffa46ebb525272f14cc5c627a60933325ee19f1beecdb6293abd45c)
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument job_config", value=job_config, expected_type=type_hints["job_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_config": job_config,
        }
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''The removal policy when deleting the CDK resource.

        If DESTROY is selected, context value ``@aws-data-solutions-framework/removeDataOnDestroy`` needs to be set to true.
        Otherwise the removalPolicy is reverted to RETAIN.

        :default: - The resources are not deleted (``RemovalPolicy.RETAIN``).
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''Schedule to run the Step Functions state machine.

        :see: Schedule
        :link: [https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_events.Schedule.html]
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    @builtins.property
    def job_config(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''EMR Serverless Job Configuration.

        :link: [https://docs.aws.amazon.com/emr-serverless/latest/APIReference/API_StartJobRun.html]
        '''
        result = self._values.get("job_config")
        assert result is not None, "Required property 'job_config' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.Any], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkEmrServerlessJobApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AccessLogsBucket",
    "AnalyticsBucket",
    "AnalyticsBucketProps",
    "ApplicationStackFactory",
    "ApplicationStage",
    "ApplicationStageProps",
    "Architecture",
    "BucketUtils",
    "CICDStage",
    "DataCatalogDatabase",
    "DataCatalogDatabaseProps",
    "DataLakeCatalog",
    "DataLakeCatalogProps",
    "DataLakeStorage",
    "DataLakeStorageProps",
    "EmrRuntimeVersion",
    "PySparkApplicationPackage",
    "PySparkApplicationPackageProps",
    "SparkEmrCICDPipeline",
    "SparkEmrCICDPipelineProps",
    "SparkEmrEksJob",
    "SparkEmrEksJobApiProps",
    "SparkEmrEksJobProps",
    "SparkEmrServerlessJob",
    "SparkEmrServerlessJobApiProps",
    "SparkEmrServerlessJobProps",
    "SparkEmrServerlessRuntime",
    "SparkEmrServerlessRuntimeProps",
    "SparkImage",
    "SparkJob",
    "SparkJobProps",
]

publication.publish()

def _typecheckingstub__6cd670a2e4f6f35ed3e5c5e824d5bff99861b579300bfab5042dade48d9e4813(
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

def _typecheckingstub__acfe28de1a351d3b74ce12685045de02c577e5c7744874cf54a19363d72440cd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    auto_delete_objects: typing.Optional[builtins.bool] = None,
    block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
    bucket_key_enabled: typing.Optional[builtins.bool] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
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
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85b197b6c67a05f3e6a882742f146f37555d0a9a6316895eaddd94ffc5a44a28(
    *,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    auto_delete_objects: typing.Optional[builtins.bool] = None,
    block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
    bucket_key_enabled: typing.Optional[builtins.bool] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
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
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e60f52dd65bad14c1f26ca2aba2367ab2eb1c1b34add215e26177cd18aa1dd(
    scope: _constructs_77d1e7e8.Construct,
    stage: CICDStage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f545a2c9269855f5a29fd2c49c15038dcd8a62aa7c82538e3de15c72d1a328(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_stack_factory: ApplicationStackFactory,
    stage: CICDStage,
    outputs_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8c976ea345f9836c305bfa275a198b91dcf105f5fc7544c827ea19a6d44fdc(
    *,
    env: typing.Optional[typing.Union[_aws_cdk_ceddda9d.Environment, typing.Dict[builtins.str, typing.Any]]] = None,
    outdir: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[_aws_cdk_ceddda9d.PermissionsBoundary] = None,
    policy_validation_beta1: typing.Optional[typing.Sequence[_aws_cdk_ceddda9d.IPolicyValidationPluginBeta1]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    application_stack_factory: ApplicationStackFactory,
    stage: CICDStage,
    outputs_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79d319717a1965981e8ded14af2ba7020f9d4782f3c604b4a2afb9073a77b0b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fc7a60b58fe4f58e0bed3d8804410738c281f005eddcd657bf7b44db75c3f1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    location_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    location_prefix: builtins.str,
    name: builtins.str,
    auto_crawl: typing.Optional[builtins.bool] = None,
    auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    crawler_table_level_depth: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec9e10691595dca6d589fd529c14b901cafb535d39e262d6d056a08c02401bc5(
    principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9597c13111a5aeba355de3c6473722674812152ef9bc6cd18e154fe16acd9bc0(
    *,
    location_bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    location_prefix: builtins.str,
    name: builtins.str,
    auto_crawl: typing.Optional[builtins.bool] = None,
    auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    crawler_table_level_depth: typing.Optional[jsii.Number] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c9f62f44305087de500a1cd42feba2045289d23a52b548eac43a9ccbc36b4e9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_lake_storage: DataLakeStorage,
    auto_crawl: typing.Optional[builtins.bool] = None,
    auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    database_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3aabdd1ab669297b207eab978305167ba45681c1169f69366712b0a83ec38a(
    *,
    data_lake_storage: DataLakeStorage,
    auto_crawl: typing.Optional[builtins.bool] = None,
    auto_crawl_schedule: typing.Optional[typing.Union[_aws_cdk_aws_glue_ceddda9d.CfnCrawler.ScheduleProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    crawler_log_encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    database_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd8415538052ebb4ea815fbf59792f64807d46258bcd13a36f0d38a21ef052b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bronze_bucket_archive_delay: typing.Optional[jsii.Number] = None,
    bronze_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    bronze_bucket_name: typing.Optional[builtins.str] = None,
    data_lake_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    gold_bucket_archive_delay: typing.Optional[jsii.Number] = None,
    gold_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    gold_bucket_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    silver_bucket_archive_delay: typing.Optional[jsii.Number] = None,
    silver_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    silver_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5753d278e7d410a61c802eac9a9344c0ca8236941efbca8cc875cb7c4f16d19(
    *,
    bronze_bucket_archive_delay: typing.Optional[jsii.Number] = None,
    bronze_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    bronze_bucket_name: typing.Optional[builtins.str] = None,
    data_lake_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.Key] = None,
    gold_bucket_archive_delay: typing.Optional[jsii.Number] = None,
    gold_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    gold_bucket_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    silver_bucket_archive_delay: typing.Optional[jsii.Number] = None,
    silver_bucket_infrequent_access_delay: typing.Optional[jsii.Number] = None,
    silver_bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9787f9e2305f0f39ba35d61392fb936c137d9ff78e91a7f4d10cf85a00329153(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_name: builtins.str,
    entrypoint_path: builtins.str,
    artifacts_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    dependencies_folder: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    venv_archive_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95922462bacfe7c9bc74765ccd0278404efe4439f1e2bc491318a6d221a5ccb2(
    *,
    application_name: builtins.str,
    entrypoint_path: builtins.str,
    artifacts_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    dependencies_folder: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    venv_archive_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61487ab0fa5733da780f29da9f7ad67e2a4073d65d7a7e95e889454cc14e810e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    application_stack_factory: ApplicationStackFactory,
    spark_application_name: builtins.str,
    cdk_application_path: typing.Optional[builtins.str] = None,
    integ_test_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    integ_test_permissions: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    integ_test_script: typing.Optional[builtins.str] = None,
    spark_application_path: typing.Optional[builtins.str] = None,
    spark_image: typing.Optional[SparkImage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c44927b44f0aa19de886c8a2e3f54622c8f7e0468c357cf86380a5da2207a6(
    *,
    application_stack_factory: ApplicationStackFactory,
    spark_application_name: builtins.str,
    cdk_application_path: typing.Optional[builtins.str] = None,
    integ_test_env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    integ_test_permissions: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    integ_test_script: typing.Optional[builtins.str] = None,
    spark_application_path: typing.Optional[builtins.str] = None,
    spark_image: typing.Optional[SparkImage] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80efcc15c6e084225d8c253e4300582e9838eacf574362a7fa2bdc678277b8d(
    *,
    application_id: builtins.str,
    name: builtins.str,
    spark_submit_entry_point: builtins.str,
    application_configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    cloud_watch_encryption_key_arn: typing.Optional[builtins.str] = None,
    cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
    cloud_watch_log_group_stream_prefix: typing.Optional[builtins.str] = None,
    cloud_watch_logtypes: typing.Optional[builtins.str] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    execution_timeout_minutes: typing.Optional[jsii.Number] = None,
    persistent_app_ui: typing.Optional[builtins.bool] = None,
    persistent_app_ui_key_arn: typing.Optional[builtins.str] = None,
    s3_log_uri: typing.Optional[builtins.str] = None,
    s3_log_uri_key_arn: typing.Optional[builtins.str] = None,
    spark_submit_entry_point_arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
    spark_submit_parameters: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650e95755a31bcb91363c323fe5d83d024412ad7c12a701cc83640dd10b55ffa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    auto_start_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.ImageConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initial_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    maximum_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_label: typing.Optional[EmrRuntimeVersion] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    worker_type_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.WorkerTypeSpecificationInputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da17b882fc735554e5b0edce68bfb1566ec02e03ed3455c96bff6dd877d9897a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    execution_role_policy_document: typing.Optional[_aws_cdk_aws_iam_ceddda9d.PolicyDocument] = None,
    iam_policy_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d09ff2f77cd0eeb1fc5b48e1389cbe2a0d7b54723a488361373ebc237a1c22(
    start_job_role: _aws_cdk_aws_iam_ceddda9d.IRole,
    execution_role_arn: typing.Sequence[builtins.str],
    application_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b614865d5ca419d9c0f5328e3fd6b73befd44f3616af7e3fd76b65255d766920(
    start_job_role: _aws_cdk_aws_iam_ceddda9d.IRole,
    execution_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28379121f70557d244a0691da885b789a630cf172d132cfb689d7540495ebb71(
    *,
    name: builtins.str,
    architecture: typing.Optional[Architecture] = None,
    auto_start_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    image_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.ImageConfigurationInputProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initial_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Sequence[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    maximum_capacity: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    release_label: typing.Optional[EmrRuntimeVersion] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    worker_type_specifications: typing.Optional[typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_ceddda9d.IResolvable, typing.Union[_aws_cdk_aws_emrserverless_ceddda9d.CfnApplication.WorkerTypeSpecificationInputProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1418d4f50fb877ff7647994fe2e2abc6d459071dbb415e2f663266c3237e055(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    tracking_tag: builtins.str,
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7998a3d6621fe869428f737ecd2fd7418d0a002a3fd457b4c0af9ca13d62e0(
    name: builtins.str,
    encryption_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c995e1c6ded7405cddd89784253155281f99e6543f07a4fbafdaa5c2684a695(
    s3_log_uri: typing.Optional[builtins.str] = None,
    encryption_key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661e0d9b9dee5b069bed1dae2610394a9c947e8824aaa763892c6d897e136fef(
    job_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f33e28e9797394601192a928f4cb307dd4d8422f1e215b98c9c26bb9f3c81d2(
    value: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5d951ef036997c6f88bca2d19a3198d3770dbf7bfbc5b56f91a85453efdd593(
    value: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98e0606d5957f6210ca926645cc86cf2622e957588d0b9fb2938803856d9cfd3(
    value: typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a041df026c0912d298b19efd093b69b490847214b6c4c9da520d99c43166d057(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__319ed6eaa80f31c0f7b214156f94ef01bb26df312dd1cd2b592ab8eb59a3f1c5(
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32539b7e2c47d71a12823caefcb109ad1f9cabbd796d22f68c59a45061e968d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[typing.Union[SparkEmrEksJobApiProps, typing.Dict[builtins.str, typing.Any]], typing.Union[SparkEmrEksJobProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6eec87a3987c4a9ff90e0a5c23142dce11227cf574d3fffc3f371787dcbe26a(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2d7db25a1da2445441486c4ac7622d3dde1e724955d9c58a9f5600b56d9f00c(
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    job_config: typing.Mapping[builtins.str, typing.Any],
    execution_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf09b1b5a5311cce03ff8bb4650e808b815061fe32e15015ef64856730e3d39(
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    execution_role_arn: builtins.str,
    name: builtins.str,
    spark_submit_entry_point: builtins.str,
    virtual_cluster_id: builtins.str,
    application_configuration: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    cloud_watch_log_group_name: typing.Optional[builtins.str] = None,
    cloud_watch_log_group_stream_prefix: typing.Optional[builtins.str] = None,
    execution_timeout_minutes: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    release_label: typing.Optional[builtins.str] = None,
    s3_log_uri: typing.Optional[builtins.str] = None,
    spark_submit_entry_point_arguments: typing.Optional[typing.Sequence[builtins.str]] = None,
    spark_submit_parameters: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e68c9f2b57d72d43b81a47c2ef94ff46489e9e54bcc7840f076cb7d87f3ed300(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Union[typing.Union[SparkEmrServerlessJobApiProps, typing.Dict[builtins.str, typing.Any]], typing.Union[SparkEmrServerlessJobProps, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773098c03f67ddb1e1fcaab21ff5c63aac32b60626703e7b55320c7103cb42da(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03e61df5ada036074c4d0512ac4b5e63558d6440cd037881048f6a7d4cbd77ca(
    value: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff96c9f1bffa46ebb525272f14cc5c627a60933325ee19f1beecdb6293abd45c(
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    job_config: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass
