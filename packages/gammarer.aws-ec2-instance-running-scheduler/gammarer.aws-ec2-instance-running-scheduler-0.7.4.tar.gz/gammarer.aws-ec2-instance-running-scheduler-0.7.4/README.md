[![GitHub](https://img.shields.io/github/license/yicr/aws-ec2-instance-running-scheduler?style=flat-square)](https://github.com/yicr/aws-ec2-instance-running-scheduler/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-ec2-instance-running-scheduler?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-ec2-instance-running-scheduler)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-ec2-instance-running-scheduler?style=flat-square)](https://pypi.org/project/gammarer.aws-ec2-instance-running-scheduler/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.Ec2InstanceRunningScheduler?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.Ec2InstanceRunningScheduler/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-ec2-instance-running-scheduler?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-ec2-instance-running-scheduler/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-ec2-instance-running-scheduler/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-ec2-instance-running-scheduler/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-ec2-instance-running-scheduler?sort=semver&style=flat-square)](https://github.com/yicr/aws-ec2-instance-running-scheduler/releases)

# AWS EC2 Instance Running Scheduler

This is an AWS CDK Construct to make EC2 instance running schedule (only running while working hours(start/stop)).

## Fixed

* EC2 Instance

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarer/aws-ec2-instance-running-scheduler
# or
yarn add @gammarer/aws-ec2-instance-running-scheduler
```

### Python

```shell
pip install gammarer.aws-ec2-instance-running-scheduler
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.Ec2InstanceRunningScheduler
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-ec2-instance-running-scheduler</artifactId>
</dependency>
```

## Example

```python
import { Ec2InstanceRunningScheduler } from '@gammarer/aws-ec2-instance-running-scheduler';

new Ec2InstanceRunningScheduler(stack, 'Ec2InstanceRunningScheduler', {
  targets: [
    {
      instances: ['i-0af01c0123456789a', 'i-0af01c0123456789b'],
      startSchedule: {
        timezone: 'Asia/Tokyo',
        minute: '55',
        hour: '8',
        week: 'MON-FRI',
      },
      stopSchedule: {
        timezone: 'Asia/Tokyo',
        minute: '5',
        hour: '19',
        week: 'MON-FRI',
      },
    },
  ],
});
```

## License

This project is licensed under the Apache-2.0 License.
