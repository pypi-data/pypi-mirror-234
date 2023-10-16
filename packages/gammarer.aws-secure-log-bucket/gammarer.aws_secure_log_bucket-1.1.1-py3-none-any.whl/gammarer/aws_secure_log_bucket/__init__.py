'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-secure-log-bucket?style=flat-square)](https://github.com/yicr/aws-secure-log-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-log-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-log-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-log-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-log-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureLogBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.SecureLogBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-log-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-log-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-secure-log-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-secure-log-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-secure-log-bucket?sort=semver&style=flat-square)](https://github.com/yicr/aws-secure-log-bucket/releases)

# AWS Secure Log Bucket

secure multiple transition phases in a single lifecycle policy bucket.

## Lifecycle rule

The storage class will be changed with the following lifecycle configuration.

| Storage Class       | Defaul transition after days |
| ------------------- |------------------------------|
| INFREQUENT_ACCESS   | 60 days                      |
| INTELLIGENT_TIERING | 120 days                     |
| GLACIER             | 180 days                     |
| DEEP_ARCHIVE        | 360 days                     |

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-log-bucket
# or
yarn add @gammarer/aws-secure-log-bucket
```

### Python

```shell
pip install gammarer.aws-secure-log-bucket
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.SecureLogBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-log-bucket</artifactId>
</dependency>
```

## Example

```python
import { SecureLogBucket } from '@gammarer/aws-secure-log-bucket';

new SecureLogBucket(stack, 'SecureLogBucket');
```

## License

This project is licensed under the Apache-2.0 License.
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

import constructs as _constructs_77d1e7e8
import gammarer.aws_secure_bucket as _gammarer_aws_secure_bucket_909c3804


class SecureLogBucket(
    _gammarer_aws_secure_bucket_909c3804.SecureBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-secure-log-bucket.SecureLogBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        change_class_transition: typing.Optional[typing.Union["StorageClassTransitionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: 
        :param change_class_transition: 
        :param object_ownership: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb12e1976e8afae652d701babe69093b337a18cbccc030d127e9039bb0eff2bc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecureLogBucketProps(
            bucket_name=bucket_name,
            change_class_transition=change_class_transition,
            object_ownership=object_ownership,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-secure-log-bucket.SecureLogBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "change_class_transition": "changeClassTransition",
        "object_ownership": "objectOwnership",
    },
)
class SecureLogBucketProps:
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        change_class_transition: typing.Optional[typing.Union["StorageClassTransitionProperty", typing.Dict[builtins.str, typing.Any]]] = None,
        object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param change_class_transition: 
        :param object_ownership: 
        '''
        if isinstance(change_class_transition, dict):
            change_class_transition = StorageClassTransitionProperty(**change_class_transition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9fab2b5b81cd538da92e3b69da78bb9d073d38fd49e4c33fa058cfd65801e9)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument change_class_transition", value=change_class_transition, expected_type=type_hints["change_class_transition"])
            check_type(argname="argument object_ownership", value=object_ownership, expected_type=type_hints["object_ownership"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if change_class_transition is not None:
            self._values["change_class_transition"] = change_class_transition
        if object_ownership is not None:
            self._values["object_ownership"] = object_ownership

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_class_transition(
        self,
    ) -> typing.Optional["StorageClassTransitionProperty"]:
        result = self._values.get("change_class_transition")
        return typing.cast(typing.Optional["StorageClassTransitionProperty"], result)

    @builtins.property
    def object_ownership(
        self,
    ) -> typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership]:
        result = self._values.get("object_ownership")
        return typing.cast(typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureLogBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarer/aws-secure-log-bucket.StorageClassTransitionProperty",
    jsii_struct_bases=[],
    name_mapping={
        "deep_archive_days": "deepArchiveDays",
        "glacier_days": "glacierDays",
        "infrequent_access_days": "infrequentAccessDays",
        "intelligent_tiering_days": "intelligentTieringDays",
    },
)
class StorageClassTransitionProperty:
    def __init__(
        self,
        *,
        deep_archive_days: jsii.Number,
        glacier_days: jsii.Number,
        infrequent_access_days: jsii.Number,
        intelligent_tiering_days: jsii.Number,
    ) -> None:
        '''
        :param deep_archive_days: 
        :param glacier_days: 
        :param infrequent_access_days: 
        :param intelligent_tiering_days: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ef1c319d62223cf48cd6d89af33a4982d9f21b0d9cbcd90eaa564e79c4bff1)
            check_type(argname="argument deep_archive_days", value=deep_archive_days, expected_type=type_hints["deep_archive_days"])
            check_type(argname="argument glacier_days", value=glacier_days, expected_type=type_hints["glacier_days"])
            check_type(argname="argument infrequent_access_days", value=infrequent_access_days, expected_type=type_hints["infrequent_access_days"])
            check_type(argname="argument intelligent_tiering_days", value=intelligent_tiering_days, expected_type=type_hints["intelligent_tiering_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deep_archive_days": deep_archive_days,
            "glacier_days": glacier_days,
            "infrequent_access_days": infrequent_access_days,
            "intelligent_tiering_days": intelligent_tiering_days,
        }

    @builtins.property
    def deep_archive_days(self) -> jsii.Number:
        result = self._values.get("deep_archive_days")
        assert result is not None, "Required property 'deep_archive_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def glacier_days(self) -> jsii.Number:
        result = self._values.get("glacier_days")
        assert result is not None, "Required property 'glacier_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def infrequent_access_days(self) -> jsii.Number:
        result = self._values.get("infrequent_access_days")
        assert result is not None, "Required property 'infrequent_access_days' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def intelligent_tiering_days(self) -> jsii.Number:
        result = self._values.get("intelligent_tiering_days")
        assert result is not None, "Required property 'intelligent_tiering_days' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StorageClassTransitionProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecureLogBucket",
    "SecureLogBucketProps",
    "StorageClassTransitionProperty",
]

publication.publish()

def _typecheckingstub__cb12e1976e8afae652d701babe69093b337a18cbccc030d127e9039bb0eff2bc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    change_class_transition: typing.Optional[typing.Union[StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9fab2b5b81cd538da92e3b69da78bb9d073d38fd49e4c33fa058cfd65801e9(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    change_class_transition: typing.Optional[typing.Union[StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ef1c319d62223cf48cd6d89af33a4982d9f21b0d9cbcd90eaa564e79c4bff1(
    *,
    deep_archive_days: jsii.Number,
    glacier_days: jsii.Number,
    infrequent_access_days: jsii.Number,
    intelligent_tiering_days: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
