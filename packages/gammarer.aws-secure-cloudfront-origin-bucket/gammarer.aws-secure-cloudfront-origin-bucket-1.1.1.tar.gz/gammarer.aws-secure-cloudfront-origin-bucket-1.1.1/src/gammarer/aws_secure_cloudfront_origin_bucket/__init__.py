'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-secure-cloudfront-origin-bucket?style=flat-square)](https://github.com/yicr/aws-secure-cloudfront-origin-bucket/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-secure-cloudfront-origin-bucket?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-secure-cloudfront-origin-bucket)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-secure-cloudfront-origin-bucket?style=flat-square)](https://pypi.org/project/gammarer.aws-secure-cloudfront-origin-bucket/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureCloudFrontOriginBucket?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.ScureCloudFrontOriginBucket/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-secure-cloudfront-origin-bucket?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-secure-cloudfront-origin-bucket/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-secure-cloudfront-origin-bucket/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-secure-cloudfront-origin-bucket/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-secure-cloudfront-origin-bucket?sort=semver&style=flat-square)](https://github.com/yicr/aws-secure-cloudfront-origin-bucket/releases)

# AWS Secure CloudFront Origin Bucket (for CDK v2)

An AWS CDK construct library to create secure S3 buckets for CloudFront origin.

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-cloudfront-origin-bucket
# or
yarn add @gammarer/aws-secure-cloudfront-origin-bucket
```

### Python

```shell
pip install gammarer.aws-secure-cloudfront-origin-bucket
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.SecureCloudFrontOriginBucket
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-secure-cloudfront-origin-bucket</artifactId>
</dependency>
```

## Example

```python
import { SecureCloudFrontOriginBucket } from '@gammarer/aws-secure-cloudfront-origin-bucket';

const oai = new cloudfront.OriginAccessIdentity(stack, 'OriginAccessIdentity');

new SecureCloudFrontOriginBucket(stack, 'SecureCloudFrontOriginBucket', {
  bucketName: 'example-origin-bucket',
  cloudFrontOriginAccessIdentityS3CanonicalUserId: oai.cloudFrontOriginAccessIdentityS3CanonicalUserId,
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


class SecureCloudFrontOriginBucket(
    _gammarer_aws_secure_bucket_909c3804.SecureBucket,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-secure-cloudfront-origin-bucket.SecureCloudFrontOriginBucket",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_front_origin_access_identity_s3_canonical_user_id: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_front_origin_access_identity_s3_canonical_user_id: 
        :param bucket_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c004eda6f2e178cfac2a2d0f96c77d7f739a5eb764d44067c2b96280e19cb8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecureCloudFrontOriginBucketProps(
            cloud_front_origin_access_identity_s3_canonical_user_id=cloud_front_origin_access_identity_s3_canonical_user_id,
            bucket_name=bucket_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-secure-cloudfront-origin-bucket.SecureCloudFrontOriginBucketProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_front_origin_access_identity_s3_canonical_user_id": "cloudFrontOriginAccessIdentityS3CanonicalUserId",
        "bucket_name": "bucketName",
    },
)
class SecureCloudFrontOriginBucketProps:
    def __init__(
        self,
        *,
        cloud_front_origin_access_identity_s3_canonical_user_id: builtins.str,
        bucket_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param cloud_front_origin_access_identity_s3_canonical_user_id: 
        :param bucket_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42658b2930f93c5cba303b10d30e2d90cda1f089c1e042218cbfbee418d0fe07)
            check_type(argname="argument cloud_front_origin_access_identity_s3_canonical_user_id", value=cloud_front_origin_access_identity_s3_canonical_user_id, expected_type=type_hints["cloud_front_origin_access_identity_s3_canonical_user_id"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_front_origin_access_identity_s3_canonical_user_id": cloud_front_origin_access_identity_s3_canonical_user_id,
        }
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name

    @builtins.property
    def cloud_front_origin_access_identity_s3_canonical_user_id(self) -> builtins.str:
        result = self._values.get("cloud_front_origin_access_identity_s3_canonical_user_id")
        assert result is not None, "Required property 'cloud_front_origin_access_identity_s3_canonical_user_id' is missing"
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
        return "SecureCloudFrontOriginBucketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SecureCloudFrontOriginBucket",
    "SecureCloudFrontOriginBucketProps",
]

publication.publish()

def _typecheckingstub__5c004eda6f2e178cfac2a2d0f96c77d7f739a5eb764d44067c2b96280e19cb8f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_front_origin_access_identity_s3_canonical_user_id: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42658b2930f93c5cba303b10d30e2d90cda1f089c1e042218cbfbee418d0fe07(
    *,
    cloud_front_origin_access_identity_s3_canonical_user_id: builtins.str,
    bucket_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
