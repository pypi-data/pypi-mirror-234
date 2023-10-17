'''
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


@jsii.data_type(
    jsii_type="@gammarer/aws-ec2-auto-scaling-instance-running-scheduler.AutoScalingGroupsProperty",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "running_desired_capacity": "runningDesiredCapacity",
        "start_schedule": "startSchedule",
        "stop_schedule": "stopSchedule",
    },
)
class AutoScalingGroupsProperty:
    def __init__(
        self,
        *,
        group_name: builtins.str,
        running_desired_capacity: jsii.Number,
        start_schedule: typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]],
        stop_schedule: typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param group_name: 
        :param running_desired_capacity: 
        :param start_schedule: 
        :param stop_schedule: 
        '''
        if isinstance(start_schedule, dict):
            start_schedule = ScheduleProperty(**start_schedule)
        if isinstance(stop_schedule, dict):
            stop_schedule = ScheduleProperty(**stop_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ab2cae4970846ce19ad5d88ab7b40cf528ce7dba1d2cde3a9a204d05fd95b2)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument running_desired_capacity", value=running_desired_capacity, expected_type=type_hints["running_desired_capacity"])
            check_type(argname="argument start_schedule", value=start_schedule, expected_type=type_hints["start_schedule"])
            check_type(argname="argument stop_schedule", value=stop_schedule, expected_type=type_hints["stop_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
            "running_desired_capacity": running_desired_capacity,
            "start_schedule": start_schedule,
            "stop_schedule": stop_schedule,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def running_desired_capacity(self) -> jsii.Number:
        result = self._values.get("running_desired_capacity")
        assert result is not None, "Required property 'running_desired_capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_schedule(self) -> "ScheduleProperty":
        result = self._values.get("start_schedule")
        assert result is not None, "Required property 'start_schedule' is missing"
        return typing.cast("ScheduleProperty", result)

    @builtins.property
    def stop_schedule(self) -> "ScheduleProperty":
        result = self._values.get("stop_schedule")
        assert result is not None, "Required property 'stop_schedule' is missing"
        return typing.cast("ScheduleProperty", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalingGroupsProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Ec2AutoScalingInstanceRunningScheduler(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-ec2-auto-scaling-instance-running-scheduler.Ec2AutoScalingInstanceRunningScheduler",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        targets: typing.Sequence[typing.Union[AutoScalingGroupsProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param targets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8f83333aa75ffedd5ef7badeb34823cd6473c296d29f352717f600b7dd9c44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2AutoScalingInstanceRunningSchedulerProps(targets=targets)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-ec2-auto-scaling-instance-running-scheduler.Ec2AutoScalingInstanceRunningSchedulerProps",
    jsii_struct_bases=[],
    name_mapping={"targets": "targets"},
)
class Ec2AutoScalingInstanceRunningSchedulerProps:
    def __init__(
        self,
        *,
        targets: typing.Sequence[typing.Union[AutoScalingGroupsProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param targets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2458fb90dd1688deb8563e54c4b8f268a528aa543b23595b7cfc55bcc4a12e55)
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "targets": targets,
        }

    @builtins.property
    def targets(self) -> typing.List[AutoScalingGroupsProperty]:
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.List[AutoScalingGroupsProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2AutoScalingInstanceRunningSchedulerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarer/aws-ec2-auto-scaling-instance-running-scheduler.ScheduleProperty",
    jsii_struct_bases=[],
    name_mapping={
        "timezone": "timezone",
        "hour": "hour",
        "minute": "minute",
        "week": "week",
    },
)
class ScheduleProperty:
    def __init__(
        self,
        *,
        timezone: builtins.str,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        week: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param timezone: 
        :param hour: 
        :param minute: 
        :param week: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d94bb6c0d5bf625835b08d3c057e1eb3135db41f2f6c327905c8d0dfafe044)
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument week", value=week, expected_type=type_hints["week"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "timezone": timezone,
        }
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if week is not None:
            self._values["week"] = week

    @builtins.property
    def timezone(self) -> builtins.str:
        result = self._values.get("timezone")
        assert result is not None, "Required property 'timezone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week(self) -> typing.Optional[builtins.str]:
        result = self._values.get("week")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AutoScalingGroupsProperty",
    "Ec2AutoScalingInstanceRunningScheduler",
    "Ec2AutoScalingInstanceRunningSchedulerProps",
    "ScheduleProperty",
]

publication.publish()

def _typecheckingstub__c4ab2cae4970846ce19ad5d88ab7b40cf528ce7dba1d2cde3a9a204d05fd95b2(
    *,
    group_name: builtins.str,
    running_desired_capacity: jsii.Number,
    start_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
    stop_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8f83333aa75ffedd5ef7badeb34823cd6473c296d29f352717f600b7dd9c44(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    targets: typing.Sequence[typing.Union[AutoScalingGroupsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2458fb90dd1688deb8563e54c4b8f268a528aa543b23595b7cfc55bcc4a12e55(
    *,
    targets: typing.Sequence[typing.Union[AutoScalingGroupsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d94bb6c0d5bf625835b08d3c057e1eb3135db41f2f6c327905c8d0dfafe044(
    *,
    timezone: builtins.str,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    week: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
