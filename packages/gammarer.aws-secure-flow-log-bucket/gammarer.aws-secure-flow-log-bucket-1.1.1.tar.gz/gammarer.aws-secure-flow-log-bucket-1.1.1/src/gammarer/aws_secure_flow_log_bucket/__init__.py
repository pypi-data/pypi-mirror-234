'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-secure-flow-log-bucket?style=flat-square)](https://github.com/yicr/aws-secure-flow-log-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-flow-log-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-flow-log-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-flow-log-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-flow-log-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureFlowLogBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.SecureFlowLogBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-flow-log-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-flow-log-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-secure-flow-log-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-secure-flow-log-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-secure-flow-log-bucket?sort=semver&style=flat-square)](https://github.com/yicr/aws-secure-flow-log-bucket/releases)

# AWS Secure Flow Log Bucket

Specific AWS VPC FlowLog Bucket

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-flow-log-bucket
# or
yarn add @gammarer/aws-secure-flow-log-bucket
```

### Python

```shell
pip install gammarer.aws-secure-flow-log-bucket
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.SecureFlowLogBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-flow-log-bucket</artifactId>
</dependency>
```

## Example

### TypeScript

```shell
npm install @gammarer/aws-secure-flow-log-bucket
```

```python
import { SecureFlowLogBucket } from '@gammarer/aws-secure-flow-log-bucket';

const bucket = new SecureFlowLogBucket(stack, 'SecureFlowLogBucket', {
  keyPrefixes: [
    'example-prefix-a',
    'example-prefix-b',
  ],
});
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
import gammarer.aws_secure_log_bucket as _gammarer_aws_secure_log_bucket_fdb2c067


class SecureFlowLogBucket(
    _gammarer_aws_secure_log_bucket_fdb2c067.SecureLogBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-secure-flow-log-bucket.SecureFlowLogBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        key_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        change_class_transition: typing.Optional[typing.Union[_gammarer_aws_secure_log_bucket_fdb2c067.StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param key_prefixes: 
        :param bucket_name: 
        :param change_class_transition: 
        :param object_ownership: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f6ef2647db41c3c576cb67c0e64ab491d068015ee7d64db056c567659e823f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecureFlowLogBucketProps(
            key_prefixes=key_prefixes,
            bucket_name=bucket_name,
            change_class_transition=change_class_transition,
            object_ownership=object_ownership,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-secure-flow-log-bucket.SecureFlowLogBucketProps",
    jsii_struct_bases=[_gammarer_aws_secure_log_bucket_fdb2c067.SecureLogBucketProps],
    name_mapping={
        "bucket_name": "bucketName",
        "change_class_transition": "changeClassTransition",
        "object_ownership": "objectOwnership",
        "key_prefixes": "keyPrefixes",
    },
)
class SecureFlowLogBucketProps(
    _gammarer_aws_secure_log_bucket_fdb2c067.SecureLogBucketProps,
):
    def __init__(
        self,
        *,
        bucket_name: typing.Optional[builtins.str] = None,
        change_class_transition: typing.Optional[typing.Union[_gammarer_aws_secure_log_bucket_fdb2c067.StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
        key_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param bucket_name: 
        :param change_class_transition: 
        :param object_ownership: 
        :param key_prefixes: 
        '''
        if isinstance(change_class_transition, dict):
            change_class_transition = _gammarer_aws_secure_log_bucket_fdb2c067.StorageClassTransitionProperty(**change_class_transition)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa6db25dda941d6999f872d3237ace5f14682af0dde6e6bbdfdd0f48bc557d73)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument change_class_transition", value=change_class_transition, expected_type=type_hints["change_class_transition"])
            check_type(argname="argument object_ownership", value=object_ownership, expected_type=type_hints["object_ownership"])
            check_type(argname="argument key_prefixes", value=key_prefixes, expected_type=type_hints["key_prefixes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if change_class_transition is not None:
            self._values["change_class_transition"] = change_class_transition
        if object_ownership is not None:
            self._values["object_ownership"] = object_ownership
        if key_prefixes is not None:
            self._values["key_prefixes"] = key_prefixes

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_class_transition(
        self,
    ) -> typing.Optional[_gammarer_aws_secure_log_bucket_fdb2c067.StorageClassTransitionProperty]:
        result = self._values.get("change_class_transition")
        return typing.cast(typing.Optional[_gammarer_aws_secure_log_bucket_fdb2c067.StorageClassTransitionProperty], result)

    @builtins.property
    def object_ownership(
        self,
    ) -> typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership]:
        result = self._values.get("object_ownership")
        return typing.cast(typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership], result)

    @builtins.property
    def key_prefixes(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("key_prefixes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureFlowLogBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecureFlowLogBucket",
    "SecureFlowLogBucketProps",
]

publication.publish()

def _typecheckingstub__91f6ef2647db41c3c576cb67c0e64ab491d068015ee7d64db056c567659e823f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    key_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    change_class_transition: typing.Optional[typing.Union[_gammarer_aws_secure_log_bucket_fdb2c067.StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa6db25dda941d6999f872d3237ace5f14682af0dde6e6bbdfdd0f48bc557d73(
    *,
    bucket_name: typing.Optional[builtins.str] = None,
    change_class_transition: typing.Optional[typing.Union[_gammarer_aws_secure_log_bucket_fdb2c067.StorageClassTransitionProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    object_ownership: typing.Optional[_gammarer_aws_secure_bucket_909c3804.SecureObjectOwnership] = None,
    key_prefixes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
