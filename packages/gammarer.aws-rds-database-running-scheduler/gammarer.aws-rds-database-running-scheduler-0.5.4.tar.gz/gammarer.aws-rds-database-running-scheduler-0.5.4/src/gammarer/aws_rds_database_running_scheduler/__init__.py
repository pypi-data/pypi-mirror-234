'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-rds-database-running-scheduler?style=flat-square)](https://github.com/yicr/aws-rds-database-running-scheduler/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-rds-database-running-scheduler?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-rds-database-running-scheduler)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-rds-database-running-scheduler?style=flat-square)](https://pypi.org/project/gammarer.aws-rds-database-running-scheduler/)
[![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.RdsDatabaseRunningScheduler?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.RdsDatabaseRunningScheduler/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-rds-database-running-scheduler?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-rds-database-running-scheduler/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-rds-database-running-scheduler/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-rds-database-running-scheduler/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-rds-database-running-scheduler?sort=semver&style=flat-square)](https://github.com/yicr/aws-rds-database-running-scheduler/releases)

# AWS RDS Database Running Scheduler

This is an AWS CDK Construct to make RDS Database running schedule (only running while working hours(start/stop)).

## Fixed

* RDS Aurora Cluster
* RDS Instance

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarer/aws-rds-database-running-scheduler
# or
yarn add @gammarer/aws-rds-database-running-scheduler
```

### Python

```shell
pip install gammarer.aws-rds-database-running-scheduler
```

### C# / .NET

```shell
dotnet add package Gammarer.CDK.AWS.RdsDatabaseRunningScheduler
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-rds-database-running-scheduler</artifactId>
</dependency>
```

## Example

```python
import { RdsDatabaseRunningScheduler, DatabaseType } from '@gammarer/aws-rds-database-running-scheduler';

new RdsDatabaseRunningScheduler(stack, 'RdsDatabaseRunningScheduler', {
  targets: [
    {
      type: DatabaseType.CLUSTER,
      identifiers: ['db-cluster-1a'],
      startSchedule: {
        timezone: 'UTC',
      },
      stopSchedule: {
        timezone: 'UTC',
      },
    },
    {
      type: DatabaseType.INSTANCE,
      identifiers: ['db-instance-1a'],
      startSchedule: {
        timezone: 'UTC',
      },
      stopSchedule: {
        timezone: 'UTC',
      },
    },
  ],
});)
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


@jsii.enum(jsii_type="@gammarer/aws-rds-database-running-scheduler.DatabaseType")
class DatabaseType(enum.Enum):
    CLUSTER = "CLUSTER"
    INSTANCE = "INSTANCE"


class RdsDatabaseRunningScheduler(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-rds-database-running-scheduler.RdsDatabaseRunningScheduler",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        targets: typing.Sequence[typing.Union["TargetProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param targets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e065e5e7ee6b4aadba8877ea0dd5c01f0fcea1b2eb0644947a875aca253a514d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RdsDatabaseRunningSchedulerProps(targets=targets)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-rds-database-running-scheduler.RdsDatabaseRunningSchedulerProps",
    jsii_struct_bases=[],
    name_mapping={"targets": "targets"},
)
class RdsDatabaseRunningSchedulerProps:
    def __init__(
        self,
        *,
        targets: typing.Sequence[typing.Union["TargetProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param targets: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8b08f2fb5bfde5e26b55305d02bde02398b8d23119497638c431929f6abf77)
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "targets": targets,
        }

    @builtins.property
    def targets(self) -> typing.List["TargetProperty"]:
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.List["TargetProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RdsDatabaseRunningSchedulerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarer/aws-rds-database-running-scheduler.ScheduleProperty",
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
            type_hints = typing.get_type_hints(_typecheckingstub__632d3c2b123620f96e21b95475fdb2088d25269f4aff43f1e8edd9cb7051cb0c)
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
    jsii_type="@gammarer/aws-rds-database-running-scheduler.TargetProperty",
    jsii_struct_bases=[],
    name_mapping={
        "identifiers": "identifiers",
        "start_schedule": "startSchedule",
        "stop_schedule": "stopSchedule",
        "type": "type",
    },
)
class TargetProperty:
    def __init__(
        self,
        *,
        identifiers: typing.Sequence[builtins.str],
        start_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
        stop_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
        type: DatabaseType,
    ) -> None:
        '''
        :param identifiers: 
        :param start_schedule: 
        :param stop_schedule: 
        :param type: 
        '''
        if isinstance(start_schedule, dict):
            start_schedule = ScheduleProperty(**start_schedule)
        if isinstance(stop_schedule, dict):
            stop_schedule = ScheduleProperty(**stop_schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1a3cdc8a1722fd131f4eaa1f12a6dd4761250a5ded09131650344f64cae5be)
            check_type(argname="argument identifiers", value=identifiers, expected_type=type_hints["identifiers"])
            check_type(argname="argument start_schedule", value=start_schedule, expected_type=type_hints["start_schedule"])
            check_type(argname="argument stop_schedule", value=stop_schedule, expected_type=type_hints["stop_schedule"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identifiers": identifiers,
            "start_schedule": start_schedule,
            "stop_schedule": stop_schedule,
            "type": type,
        }

    @builtins.property
    def identifiers(self) -> typing.List[builtins.str]:
        result = self._values.get("identifiers")
        assert result is not None, "Required property 'identifiers' is missing"
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

    @builtins.property
    def type(self) -> DatabaseType:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(DatabaseType, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DatabaseType",
    "RdsDatabaseRunningScheduler",
    "RdsDatabaseRunningSchedulerProps",
    "ScheduleProperty",
    "TargetProperty",
]

publication.publish()

def _typecheckingstub__e065e5e7ee6b4aadba8877ea0dd5c01f0fcea1b2eb0644947a875aca253a514d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    targets: typing.Sequence[typing.Union[TargetProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8b08f2fb5bfde5e26b55305d02bde02398b8d23119497638c431929f6abf77(
    *,
    targets: typing.Sequence[typing.Union[TargetProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632d3c2b123620f96e21b95475fdb2088d25269f4aff43f1e8edd9cb7051cb0c(
    *,
    timezone: builtins.str,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    week: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1a3cdc8a1722fd131f4eaa1f12a6dd4761250a5ded09131650344f64cae5be(
    *,
    identifiers: typing.Sequence[builtins.str],
    start_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
    stop_schedule: typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]],
    type: DatabaseType,
) -> None:
    """Type checking stubs"""
    pass
