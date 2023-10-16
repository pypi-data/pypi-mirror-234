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
