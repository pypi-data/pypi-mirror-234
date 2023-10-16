'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-secure-vpc-bucket?style=flat-square)](https://github.com/yicr/aws-secure-vpc-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-vpc-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-vpc-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-vpc-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-vpc-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureVpcBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.SecureVpcBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-vpc-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-vpc-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-secure-vpc-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-secure-vpc-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-secure-vpc-bucket?sort=semver&style=flat-square)](https://github.com/yicr/aws-secure-vpc-bucket/releases)

# AWS Secure VPC Bucket

Access from specific VPC Endpoint only Bucket

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-vpc-bucket
# or
yarn add @gammarer/aws-secure-vpc-bucket
```

### Python

```shell
pip install gammarer.aws-secure-vpc-bucket
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.SecureVpcBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-vpc-bucket</artifactId>
</dependency>
```

## Example

```python
import { SecureSpecificVpcOnlyBucket } from '@gammarer/aws-secure-vpc-bucket';

new SecureVpcBucket(stack, 'SecureVpcBucket', {
  bucketName: 'example-origin-bucket',
  vpcEndpointId: 'vpce-0xxxxxxxxxxxxxxxx', // allready created vpc endpoint id
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


class SecureVpcBucket(
    _gammarer_aws_secure_bucket_909c3804.SecureBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-secure-vpc-bucket.SecureVpcBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc_endpoint_id: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc_endpoint_id: 
        :param bucket_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d4f305bdf47f4ddeb0857475f6bec26a7e9ebd18335746ad3d7d9049f1b64d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecureVpcBucketProps(
            vpc_endpoint_id=vpc_endpoint_id, bucket_name=bucket_name
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-secure-vpc-bucket.SecureVpcBucketProps",
    jsii_struct_bases=[],
    name_mapping={"vpc_endpoint_id": "vpcEndpointId", "bucket_name": "bucketName"},
)
class SecureVpcBucketProps:
    def __init__(
        self,
        *,
        vpc_endpoint_id: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param vpc_endpoint_id: 
        :param bucket_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7aaccb4f62ecf54aa3dd5a836f8d5edb230f8802c1e75144b03453f3c7f182)
            check_type(argname="argument vpc_endpoint_id", value=vpc_endpoint_id, expected_type=type_hints["vpc_endpoint_id"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc_endpoint_id": vpc_endpoint_id,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name

    @builtins.property
    def vpc_endpoint_id(self) -> builtins.str:
        result = self._values.get("vpc_endpoint_id")
        assert result is not None, "Required property 'vpc_endpoint_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecureVpcBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecureVpcBucket",
    "SecureVpcBucketProps",
]

publication.publish()

def _typecheckingstub__38d4f305bdf47f4ddeb0857475f6bec26a7e9ebd18335746ad3d7d9049f1b64d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc_endpoint_id: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7aaccb4f62ecf54aa3dd5a836f8d5edb230f8802c1e75144b03453f3c7f182(
    *,
    vpc_endpoint_id: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
