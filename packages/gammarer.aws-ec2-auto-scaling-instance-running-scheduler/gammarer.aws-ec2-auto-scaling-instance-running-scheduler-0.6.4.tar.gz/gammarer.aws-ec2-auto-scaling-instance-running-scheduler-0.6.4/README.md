[![GitHub](https://img.shields.io/github/license/yicr/aws-ec2-auto-scaling-instance-running-scheduler?style=flat-square)](https://github.com/yicr/aws-ec2-auto-scaling-instance-running-scheduler/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-ec2-auto-scaling-instance-running-scheduler?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-ec2-auto-scaling-instance-running-scheduler)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-ec2-auto-scaling-instance-running-scheduler?style=flat-square)](https://pypi.org/project/gammarer.aws-ec2-auto-scaling-instance-running-scheduler/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.Ec2AutoScalingInstanceRunningScheduler?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.Ec2AutoScalingInstanceRunningScheduler/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-ec2-auto-scaling-instance-running-scheduler?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-ec2-auto-scaling-instance-running-scheduler/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-ec2-auto-scaling-instance-running-scheduler/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-ec2-auto-scaling-instance-running-scheduler/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-ec2-auto-scaling-instance-running-scheduler?sort=semver&style=flat-square)](https://github.com/yicr/aws-ec2-auto-scaling-instance-running-scheduler/releases)

# AWS EC2 AutoScaling Instance Running Scheduler

This is an AWS CDK Construct to make EC2 AutoScaling instance running schedule (only running while working hours(start/stop)).
But only capacity min value is 0 for the AutoScalingGroup.

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarer/aws-ec2-auto-scaling-instance-running-scheduler
# or
yarn add @gammarer/aws-ec2-auto-scaling-instance-running-scheduler
```

### Python

```shell
pip install gammarer.aws-ec2-auto-scaling-instance-running-scheduler
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.Ec2AutoScalingInstanceRunningScheduler
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-ec2-auto-scaling-instance-running-scheduler</artifactId>
</dependency>
```

## Example

```python
import { Ec2AutoScalingInstanceRunningScheduler } from '@gammarer/aws-ec2-auto-scaling-instance-running-scheduler';

new Ec2AutoScalingInstanceRunningScheduler(stack, 'Ec2AutoScalingInstanceRunningScheduler', {
  targets: [
    {
      groupName: 'example-scaling-group',
      runningDesiredCapacity: 2,
      startSchedule: {
        timezone: 'UTC',
      },
      stopSchedule: {
        timezone: 'UTC',
      },
    },
  ],
});
```

## License

This project is licensed under the Apache-2.0 License.
