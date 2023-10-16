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
