'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-secure-bucket?style=flat-square)](https://github.com/yicr/aws-secure-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.SecureBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-secure-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-secure-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-secure-bucket?sort=semver&style=flat-square)](https://github.com/yicr/aws-secure-bucket/releases)

# AWS Secure Bucket

This is a Simple S3 Secure Bucket.

* Bucket Access Control is Private
* Public Read Access is false
* Enforce SSL
* All Block public access
* Require encryption

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-bucket
# or
yarn add @gammarer/aws-secure-bucket
```

### Python

```shell
pip install gammarer.aws-secure-bucket
```

### C# / .Net

```shell
dotnet add package Gammarer.CDK.AWS.SecureBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-bucket</artifactId>
</dependency>
```

## Example

### TypeScript

```python
import { SecureBucket } from '@gammarer/aws-secure-bucket';

const bucket = new SecureBucket(stack, 'SecureBucket', {
  bucketName: 'example-secure-bucket',
});
```
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

import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class SecureBucket(
    _aws_cdk_aws_s3_ceddda9d.Bucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-secure-bucket.SecureBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        encryption: typing.Optional["SecureBucketEncryption"] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        object_ownership: typing.Optional["SecureObjectOwnership"] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: 
        :param encryption: 
        :param event_bridge_enabled: 
        :param lifecycle_rules: 
        :param object_ownership: 
        :param versioned: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a9ff962f293bb283ec66531dc0679a4e67d2992d4afdf4872f1d50ad349807)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecureBucketProps(
            bucket_name=bucket_name,
            encryption=encryption,
            event_bridge_enabled=event_bridge_enabled,
            lifecycle_rules=lifecycle_rules,
            object_ownership=object_ownership,
            versioned=versioned,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.enum(jsii_type="@gammarer/aws-secure-bucket.SecureBucketEncryption")
class SecureBucketEncryption(enum.Enum):
    KMS_MANAGED = "KMS_MANAGED"
    '''Server-side KMS encryption with a master key managed by KMS.'''
    S3_MANAGED = "S3_MANAGED"
    '''Server-side encryption with a master key managed by S3.'''


@jsii.data_type(
    jsii_type="@gammarer/aws-secure-bucket.SecureBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "encryption": "encryption",
        "event_bridge_enabled": "eventBridgeEnabled",
        "lifecycle_rules": "lifecycleRules",
        "object_ownership": "objectOwnership",
        "versioned": "versioned",
    },
)
class SecureBucketProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[SecureBucketEncryption] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        object_ownership: typing.Optional["SecureObjectOwnership"] = None,
        versioned: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param encryption: 
        :param event_bridge_enabled: 
        :param lifecycle_rules: 
        :param object_ownership: 
        :param versioned: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92a51c4f23f233d427763f097323e6e19c625d60e5d6ba65125bac4d98dc3683)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument event_bridge_enabled", value=event_bridge_enabled, expected_type=type_hints["event_bridge_enabled"])
            check_type(argname="argument lifecycle_rules", value=lifecycle_rules, expected_type=type_hints["lifecycle_rules"])
            check_type(argname="argument object_ownership", value=object_ownership, expected_type=type_hints["object_ownership"])
            check_type(argname="argument versioned", value=versioned, expected_type=type_hints["versioned"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if encryption is not None:
            self._values["encryption"] = encryption
        if event_bridge_enabled is not None:
            self._values["event_bridge_enabled"] = event_bridge_enabled
        if lifecycle_rules is not None:
            self._values["lifecycle_rules"] = lifecycle_rules
        if object_ownership is not None:
            self._values["object_ownership"] = object_ownership
        if versioned is not None:
            self._values["versioned"] = versioned

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(self) -> typing.Optional[SecureBucketEncryption]:
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[SecureBucketEncryption], result)

    @builtins.property
    def event_bridge_enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("event_bridge_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lifecycle_rules(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.LifecycleRule]]:
        result = self._values.get("lifecycle_rules")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_s3_ceddda9d.LifecycleRule]], result)

    @builtins.property
    def object_ownership(self) -> typing.Optional["SecureObjectOwnership"]:
        result = self._values.get("object_ownership")
        return typing.cast(typing.Optional["SecureObjectOwnership"], result)

    @builtins.property
    def versioned(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("versioned")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@gammarer/aws-secure-bucket.SecureObjectOwnership")
class SecureObjectOwnership(enum.Enum):
    '''The ObjectOwnership of the bucket.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/about-object-ownership.html
    '''

    BUCKET_OWNER_ENFORCED = "BUCKET_OWNER_ENFORCED"
    '''ACLs are disabled, and the bucket owner automatically owns and has full control over every object in the bucket.

    ACLs no longer affect permissions to data in the S3 bucket.
    The bucket uses policies to define access control.
    '''
    BUCKET_OWNER_PREFERRED = "BUCKET_OWNER_PREFERRED"
    '''Objects uploaded to the bucket change ownership to the bucket owner .'''
    OBJECT_WRITER = "OBJECT_WRITER"
    '''The uploading account will own the object.'''


__all__ = [
    "SecureBucket",
    "SecureBucketEncryption",
    "SecureBucketProps",
    "SecureObjectOwnership",
]

publication.publish()

def _typecheckingstub__96a9ff962f293bb283ec66531dc0679a4e67d2992d4afdf4872f1d50ad349807(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[SecureBucketEncryption] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_ownership: typing.Optional[SecureObjectOwnership] = None,
    versioned: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92a51c4f23f233d427763f097323e6e19c625d60e5d6ba65125bac4d98dc3683(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[SecureBucketEncryption] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    object_ownership: typing.Optional[SecureObjectOwnership] = None,
    versioned: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
