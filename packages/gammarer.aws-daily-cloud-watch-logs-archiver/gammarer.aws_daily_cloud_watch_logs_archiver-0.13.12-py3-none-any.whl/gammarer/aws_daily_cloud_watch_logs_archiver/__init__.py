'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-daily-cloud-watch-logs-archiver?style=flat-square)](https://github.com/yicr/aws-daily-cloud-watch-logs-archiver/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-daily-cloud-watch-logs-archiver?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-daily-cloud-watch-logs-archiver)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-daily-cloud-watch-logs-archiver?style=flat-square)](https://pypi.org/project/gammarer.aws-daily-cloud-watch-logs-archiver/)

<!-- [![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.DailyCloudWatchLogsArchiver?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.DailyCloudWatchLogsArchiver/)  --><!-- [![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-daily-cloud-watch-logs-archiver?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-daily-cloud-watch-logs-archiver/) -->

[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-daily-cloud-watch-logs-archiver/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-daily-cloud-watch-logs-archiver/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-daily-cloud-watch-logs-archiver?sort=semver&style=flat-square)](https://github.com/yicr/aws-daily-cloud-watch-logs-archiver/releases)

# AWS Daily CloudWatch Logs Archiver

AWS CloudWatch Logs daily(13:00Z) archive to s3 bucket.

## Resources

This construct creating resource list.

* S3 Bucket (log-archive-xxxxxxxx from @yicr/aws-secure-log-bucket)
* Lambda function execution role
* Lambda function
* EventBridge Scheduler execution role
* EventBridge Scheduler Group
* EventBridge Scheduler (this construct props specified count)

## Install

### TypeScript

```shell
npm install @gammarer/aws-daily-cloud-watch-logs-archiver
# or
yarn add @gammarer/aws-daily-cloud-watch-logs-archiver
```

### Python

```shell
pip install gammarer.aws-daily-cloud-watch-logs-archiver
```

## Example

```shell
npm install @gammarer/aws-daily-cloud-watch-logs-archiver
```

```python
import { DailyCloudWatchLogsArchiver } from '@gammarer/aws-daily-cloud-watch-logs-archiver';

new DailyCloudWatchLogsArchiver(stack, 'DailyCloudWatchLogsArchiver', {
  schedules: [
    {
      name: 'example-log-archive-1st-rule',
      description: 'example log archive 1st rule.',
      target: {
        logGroupName: 'example-log-1st-group', // always created CloudWatch Log group
        destinationPrefix: 'example-1st-log',
      },
    },
    {
      name: 'example-log-archive-2nd-rule',
      description: 'example log archive 2nd rule.',
      target: {
        logGroupName: 'example-log-2nd-group',
        destinationPrefix: 'example-2nd-log',
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


class DailyCloudWatchLogsArchiver(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-daily-cloud-watch-logs-archiver.DailyCloudWatchLogsArchiver",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        schedules: typing.Sequence[typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param schedules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e72c2c7b24eae3cd643e26390a7256d4cd092a754c618a1f7640c2fb0e27b3b1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DailyCloudWatchLogsArchiverProps(schedules=schedules)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-daily-cloud-watch-logs-archiver.DailyCloudWatchLogsArchiverProps",
    jsii_struct_bases=[],
    name_mapping={"schedules": "schedules"},
)
class DailyCloudWatchLogsArchiverProps:
    def __init__(
        self,
        *,
        schedules: typing.Sequence[typing.Union["ScheduleProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param schedules: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f57aec0f3186cca3b12d63a473fd51ab3ed39b18d5a0bd495a8899be9278bbc5)
            check_type(argname="argument schedules", value=schedules, expected_type=type_hints["schedules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedules": schedules,
        }

    @builtins.property
    def schedules(self) -> typing.List["ScheduleProperty"]:
        result = self._values.get("schedules")
        assert result is not None, "Required property 'schedules' is missing"
        return typing.cast(typing.List["ScheduleProperty"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DailyCloudWatchLogsArchiverProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarer/aws-daily-cloud-watch-logs-archiver.ScheduleProperty",
    jsii_struct_bases=[],
    name_mapping={"description": "description", "name": "name", "target": "target"},
)
class ScheduleProperty:
    def __init__(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        target: typing.Union["ScheduleTargetProperty", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param description: 
        :param name: 
        :param target: 
        '''
        if isinstance(target, dict):
            target = ScheduleTargetProperty(**target)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd1b459c8a92fef592adb89398d411854ffc89b2f3a9fb9d9b637918354a0a3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "name": name,
            "target": target,
        }

    @builtins.property
    def description(self) -> builtins.str:
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> "ScheduleTargetProperty":
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast("ScheduleTargetProperty", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@gammarer/aws-daily-cloud-watch-logs-archiver.ScheduleTargetProperty",
    jsii_struct_bases=[],
    name_mapping={
        "destination_prefix": "destinationPrefix",
        "log_group_name": "logGroupName",
    },
)
class ScheduleTargetProperty:
    def __init__(
        self,
        *,
        destination_prefix: builtins.str,
        log_group_name: builtins.str,
    ) -> None:
        '''
        :param destination_prefix: 
        :param log_group_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d6f49215937a7258060332688c10ed60897726f04288d693931f01e35a827f4)
            check_type(argname="argument destination_prefix", value=destination_prefix, expected_type=type_hints["destination_prefix"])
            check_type(argname="argument log_group_name", value=log_group_name, expected_type=type_hints["log_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_prefix": destination_prefix,
            "log_group_name": log_group_name,
        }

    @builtins.property
    def destination_prefix(self) -> builtins.str:
        result = self._values.get("destination_prefix")
        assert result is not None, "Required property 'destination_prefix' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_name(self) -> builtins.str:
        result = self._values.get("log_group_name")
        assert result is not None, "Required property 'log_group_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleTargetProperty(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "DailyCloudWatchLogsArchiver",
    "DailyCloudWatchLogsArchiverProps",
    "ScheduleProperty",
    "ScheduleTargetProperty",
]

publication.publish()

def _typecheckingstub__e72c2c7b24eae3cd643e26390a7256d4cd092a754c618a1f7640c2fb0e27b3b1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    schedules: typing.Sequence[typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57aec0f3186cca3b12d63a473fd51ab3ed39b18d5a0bd495a8899be9278bbc5(
    *,
    schedules: typing.Sequence[typing.Union[ScheduleProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd1b459c8a92fef592adb89398d411854ffc89b2f3a9fb9d9b637918354a0a3(
    *,
    description: builtins.str,
    name: builtins.str,
    target: typing.Union[ScheduleTargetProperty, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6f49215937a7258060332688c10ed60897726f04288d693931f01e35a827f4(
    *,
    destination_prefix: builtins.str,
    log_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
