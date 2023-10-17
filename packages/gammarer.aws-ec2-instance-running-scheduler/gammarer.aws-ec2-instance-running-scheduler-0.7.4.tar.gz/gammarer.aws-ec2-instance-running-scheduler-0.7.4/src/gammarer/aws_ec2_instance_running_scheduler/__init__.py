'''
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


class Ec2InstanceRunningScheduler(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-ec2-instance-running-scheduler.Ec2InstanceRunningScheduler",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        targets: typing.Sequence[typing.Union["TargetsProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param targets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb66d0b4bce27e96fde7eda271ea3e2717175cdc5c5eeecf07a7c86eea4d6b4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2InstanceRunningSchedulerProps(targets=targets)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-ec2-instance-running-scheduler.Ec2InstanceRunningSchedulerProps",
    jsii_struct_bases=[],
    name_mapping={"targets": "targets"},
)
class Ec2InstanceRunningSchedulerProps:
    def __init__(
        self,
        *,
        targets: typing.Sequence[typing.Union["TargetsProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param targets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f77dbd553445403b459f4a50a8e201b5b565ef51abd7f780da781e16e24d0b7b)
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "targets": targets,
        }

    @builtins.property
    def targets(self) -> typing.List["TargetsProperty"]:
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.List["TargetsProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2InstanceRunningSchedulerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarer/aws-ec2-instance-running-scheduler.ScheduleProperty",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0c5d28736f0b92e8fb9dec4eea0f4f43525f0063a7a3ebc41ae66a4cb74fbbe)
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


@jsii.data_type(
    jsii_type="@gammarer/aws-ec2-instance-running-scheduler.TargetsProperty",
    jsii_struct_bases=[],
    name_mapping={
        "instances": "instances",
        "start_schedule": "startSchedule",
        "stop_schedule": "stopSchedule",
    },
)
class TargetsProperty:
    def __init__(
        self,
        *,
        instances: typing.Sequence[builtins.str],
        start_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
        stop_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param instances: 
        :param start_schedule: 
        :param stop_schedule: 
        '''
        if isinstance(start_schedule, dict):
            start_schedule = ScheduleProperty(**start_schedule)
        if isinstance(stop_schedule, dict):
            stop_schedule = ScheduleProperty(**stop_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9defd4b3cd11be9abb4b583c61a5216f04fb78f61394bfd5b413fb21ff6194c7)
            check_type(argname="argument instances", value=instances, expected_type=type_hints["instances"])
            check_type(argname="argument start_schedule", value=start_schedule, expected_type=type_hints["start_schedule"])
            check_type(argname="argument stop_schedule", value=stop_schedule, expected_type=type_hints["stop_schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instances": instances,
            "start_schedule": start_schedule,
            "stop_schedule": stop_schedule,
        }

    @builtins.property
    def instances(self) -> typing.List[builtins.str]:
        result = self._values.get("instances")
        assert result is not None, "Required property 'instances' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def start_schedule(self) -> ScheduleProperty:
        result = self._values.get("start_schedule")
        assert result is not None, "Required property 'start_schedule' is missing"
        return typing.cast(ScheduleProperty, result)

    @builtins.property
    def stop_schedule(self) -> ScheduleProperty:
        result = self._values.get("stop_schedule")
        assert result is not None, "Required property 'stop_schedule' is missing"
        return typing.cast(ScheduleProperty, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetsProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Ec2InstanceRunningScheduler",
    "Ec2InstanceRunningSchedulerProps",
    "ScheduleProperty",
    "TargetsProperty",
]

publication.publish()

def _typecheckingstub__bb66d0b4bce27e96fde7eda271ea3e2717175cdc5c5eeecf07a7c86eea4d6b4e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    targets: typing.Sequence[typing.Union[TargetsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f77dbd553445403b459f4a50a8e201b5b565ef51abd7f780da781e16e24d0b7b(
    *,
    targets: typing.Sequence[typing.Union[TargetsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c5d28736f0b92e8fb9dec4eea0f4f43525f0063a7a3ebc41ae66a4cb74fbbe(
    *,
    timezone: builtins.str,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    week: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9defd4b3cd11be9abb4b583c61a5216f04fb78f61394bfd5b413fb21ff6194c7(
    *,
    instances: typing.Sequence[builtins.str],
    start_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
    stop_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass
