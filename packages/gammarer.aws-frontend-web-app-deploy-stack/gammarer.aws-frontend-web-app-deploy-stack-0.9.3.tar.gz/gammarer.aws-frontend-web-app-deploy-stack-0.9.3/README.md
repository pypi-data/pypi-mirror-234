[![GitHub](https://img.shields.io/github/license/yicr/aws-frontend-web-app-deploy-stack?style=flat-square)](https://github.com/yicr/aws-frontend-web-app-deploy-stack/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-frontend-web-app-deploy-stack?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-frontend-web-app-deploy-stack)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-frontend-web-app-deploy-stack?style=flat-square)](https://pypi.org/project/gammarer.aws-frontend-web-app-deploy-stack/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.FrontendWebAppDeployStack?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.FrontendWebAppDeployStack/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-frontend-web-app-deploy-stack?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-frontend-web-app-deploy-stack/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-frontend-web-app-deploy-stack/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-frontend-web-app-deploy-stack/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-frontend-web-app-deploy-stack?sort=semver&style=flat-square)](https://github.com/yicr/aws-frontend-web-app-deploy-stack/releases)

# AWS Frontend Web App Deploy Stack

This is an AWS CDK Construct to make deploying a Frontend Web App (SPA) deploy to S3 behind CloudFront.

## Install

### TypeScript

```shell
npm install @gammarer/aws-frontend-web-app-deploy-stack
# or
yarn add @gammarer/aws-frontend-web-app-deploy-stack
```

### Python

```shell
pip install gammarer.aws-frontend-web-app-deploy-stack
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.FrontendWebAppDeployStack
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-frontend-web-app-deploy-stack</artifactId>
</dependency>
```

## Example

```python
import { FrontendWebAppDeployStack } from '@gammarer/aws-frontend-web-app-deploy-stack';

new FrontendWebAppDeployStack(app, 'FrontendWebAppDeployStack', {
  env: { account: '012345678901', region: 'us-east-1' },
  domainName: 'example.com',
  hostedZoneId: 'Z0000000000000000000Q',
  originBucketName: 'frontend-web-app-example-origin-bucket', // new create in this stack
  deploySourceAssetPath: 'website/',
  logBucketArn: 'arn:aws:s3:::frontend-web-app-example-access-log-bucket', // already created
});
```

## License

This project is licensed under the Apache-2.0 License.
