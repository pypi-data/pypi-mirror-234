'''
# datadog-monitors-downtimeschedule

> AWS CDK [L1 construct](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html) and data structures for the [AWS CloudFormation Registry](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry.html) type `Datadog::Monitors::DowntimeSchedule` v1.0.0.

## Description

Datadog Downtime Schedule 1.0.0

## Usage

In order to use this library, you will need to activate this AWS CloudFormation Registry type in your account. You can do this via the AWS Management Console or using the [AWS CLI](https://aws.amazon.com/cli/) using the following command:

```sh
aws cloudformation activate-type \
  --type-name Datadog::Monitors::DowntimeSchedule \
  --publisher-id 7171b96e5d207b947eb72ca9ce05247c246de623 \
  --type RESOURCE \
  --execution-role-arn ROLE-ARN
```

Alternatively:

```sh
aws cloudformation activate-type \
  --public-type-arn arn:aws:cloudformation:us-east-1::type/resource/7171b96e5d207b947eb72ca9ce05247c246de623/Datadog-Monitors-DowntimeSchedule \
  --execution-role-arn ROLE-ARN
```

You can find more information about activating this type in the [AWS CloudFormation documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/registry-public.html).

## Feedback

This library is auto-generated and published to all supported programming languages by the [cdklabs/cdk-cloudformation](https://github.com/cdklabs/cdk-cloudformation) project based on the API schema published for `Datadog::Monitors::DowntimeSchedule`.

* Issues related to this generated library should be [reported here](https://github.com/cdklabs/cdk-cloudformation/issues/new?title=Issue+with+%40cdk-cloudformation%2Fdatadog-monitors-downtimeschedule+v1.0.0).
* Issues related to `Datadog::Monitors::DowntimeSchedule` should be reported to the [publisher](undefined).

## License

Distributed under the Apache-2.0 License.
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

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CfnDowntimeSchedule(
    _aws_cdk_ceddda9d.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdk-cloudformation/datadog-monitors-downtimeschedule.CfnDowntimeSchedule",
):
    '''A CloudFormation ``Datadog::Monitors::DowntimeSchedule``.

    :cloudformationResource: Datadog::Monitors::DowntimeSchedule
    :link: http://unknown-url
    '''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        monitor_identifier: typing.Any,
        scope: builtins.str,
        display_timezone: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        mute_first_recovery_notification: typing.Optional[builtins.bool] = None,
        notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        schedule: typing.Any = None,
    ) -> None:
        '''Create a new ``Datadog::Monitors::DowntimeSchedule``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param monitor_identifier: 
        :param scope: The scope to which the downtime applies. Must follow the `common search syntax <https://docs.datadoghq.com/logs/explorer/search_syntax/>`_.
        :param display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. The timezone is not used as an offset for scheduling.
        :param message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same ``@username`` notation as events.
        :param mute_first_recovery_notification: If the first recovery notification during a downtime should be muted.
        :param notify_end_states: States that will trigger a monitor notification when the ``notify_end_types`` action occurs.
        :param notify_end_types: Actions that will trigger a monitor notification if the downtime is in the ``notify_end_types`` state.
        :param schedule: The schedule that defines when the monitor starts, stops, and recurs. There are two types of schedules: one-time and recurring. Recurring schedules may have up to five RRULE-based recurrences. If no schedules are provided, the downtime will begin immediately and never end.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e66d72db62d52d37704ce37191636da6024f10a156a892897e582f1c52f536)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDowntimeScheduleProps(
            monitor_identifier=monitor_identifier,
            scope=scope,
            display_timezone=display_timezone,
            message=message,
            mute_first_recovery_notification=mute_first_recovery_notification,
            notify_end_states=notify_end_states,
            notify_end_types=notify_end_types,
            schedule=schedule,
        )

        jsii.create(self.__class__, self, [scope_, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''Attribute ``Datadog::Monitors::DowntimeSchedule.Id``.

        :link: http://unknown-url
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def props(self) -> "CfnDowntimeScheduleProps":
        '''Resource props.'''
        return typing.cast("CfnDowntimeScheduleProps", jsii.get(self, "props"))


@jsii.data_type(
    jsii_type="@cdk-cloudformation/datadog-monitors-downtimeschedule.CfnDowntimeScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "monitor_identifier": "monitorIdentifier",
        "scope": "scope",
        "display_timezone": "displayTimezone",
        "message": "message",
        "mute_first_recovery_notification": "muteFirstRecoveryNotification",
        "notify_end_states": "notifyEndStates",
        "notify_end_types": "notifyEndTypes",
        "schedule": "schedule",
    },
)
class CfnDowntimeScheduleProps:
    def __init__(
        self,
        *,
        monitor_identifier: typing.Any,
        scope: builtins.str,
        display_timezone: typing.Optional[builtins.str] = None,
        message: typing.Optional[builtins.str] = None,
        mute_first_recovery_notification: typing.Optional[builtins.bool] = None,
        notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
        notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        schedule: typing.Any = None,
    ) -> None:
        '''Datadog Downtime Schedule 1.0.0.

        :param monitor_identifier: 
        :param scope: The scope to which the downtime applies. Must follow the `common search syntax <https://docs.datadoghq.com/logs/explorer/search_syntax/>`_.
        :param display_timezone: The timezone in which to display the downtime's start and end times in Datadog applications. The timezone is not used as an offset for scheduling.
        :param message: A message to include with notifications for this downtime. Email notifications can be sent to specific users by using the same ``@username`` notation as events.
        :param mute_first_recovery_notification: If the first recovery notification during a downtime should be muted.
        :param notify_end_states: States that will trigger a monitor notification when the ``notify_end_types`` action occurs.
        :param notify_end_types: Actions that will trigger a monitor notification if the downtime is in the ``notify_end_types`` state.
        :param schedule: The schedule that defines when the monitor starts, stops, and recurs. There are two types of schedules: one-time and recurring. Recurring schedules may have up to five RRULE-based recurrences. If no schedules are provided, the downtime will begin immediately and never end.

        :schema: CfnDowntimeScheduleProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0341e644d80f73372cc8b4d6697198340fc45fb5e2b598de14ecbc929124473)
            check_type(argname="argument monitor_identifier", value=monitor_identifier, expected_type=type_hints["monitor_identifier"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument display_timezone", value=display_timezone, expected_type=type_hints["display_timezone"])
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument mute_first_recovery_notification", value=mute_first_recovery_notification, expected_type=type_hints["mute_first_recovery_notification"])
            check_type(argname="argument notify_end_states", value=notify_end_states, expected_type=type_hints["notify_end_states"])
            check_type(argname="argument notify_end_types", value=notify_end_types, expected_type=type_hints["notify_end_types"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitor_identifier": monitor_identifier,
            "scope": scope,
        }
        if display_timezone is not None:
            self._values["display_timezone"] = display_timezone
        if message is not None:
            self._values["message"] = message
        if mute_first_recovery_notification is not None:
            self._values["mute_first_recovery_notification"] = mute_first_recovery_notification
        if notify_end_states is not None:
            self._values["notify_end_states"] = notify_end_states
        if notify_end_types is not None:
            self._values["notify_end_types"] = notify_end_types
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def monitor_identifier(self) -> typing.Any:
        '''
        :schema: CfnDowntimeScheduleProps#MonitorIdentifier
        '''
        result = self._values.get("monitor_identifier")
        assert result is not None, "Required property 'monitor_identifier' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def scope(self) -> builtins.str:
        '''The scope to which the downtime applies.

        Must follow the `common search syntax <https://docs.datadoghq.com/logs/explorer/search_syntax/>`_.

        :schema: CfnDowntimeScheduleProps#Scope
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_timezone(self) -> typing.Optional[builtins.str]:
        '''The timezone in which to display the downtime's start and end times in Datadog applications.

        The timezone is not used as an offset for scheduling.

        :schema: CfnDowntimeScheduleProps#DisplayTimezone
        '''
        result = self._values.get("display_timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message(self) -> typing.Optional[builtins.str]:
        '''A message to include with notifications for this downtime.

        Email notifications can be sent to specific users by using the same ``@username`` notation as events.

        :schema: CfnDowntimeScheduleProps#Message
        '''
        result = self._values.get("message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mute_first_recovery_notification(self) -> typing.Optional[builtins.bool]:
        '''If the first recovery notification during a downtime should be muted.

        :schema: CfnDowntimeScheduleProps#MuteFirstRecoveryNotification
        '''
        result = self._values.get("mute_first_recovery_notification")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notify_end_states(self) -> typing.Optional[typing.List[builtins.str]]:
        '''States that will trigger a monitor notification when the ``notify_end_types`` action occurs.

        :schema: CfnDowntimeScheduleProps#NotifyEndStates
        '''
        result = self._values.get("notify_end_states")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def notify_end_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Actions that will trigger a monitor notification if the downtime is in the ``notify_end_types`` state.

        :schema: CfnDowntimeScheduleProps#NotifyEndTypes
        '''
        result = self._values.get("notify_end_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def schedule(self) -> typing.Any:
        '''The schedule that defines when the monitor starts, stops, and recurs.

        There are two types of schedules: one-time and recurring. Recurring schedules may have up to five RRULE-based recurrences. If no schedules are provided, the downtime will begin immediately and never end.

        :schema: CfnDowntimeScheduleProps#Schedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDowntimeScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnDowntimeSchedule",
    "CfnDowntimeScheduleProps",
]

publication.publish()

def _typecheckingstub__56e66d72db62d52d37704ce37191636da6024f10a156a892897e582f1c52f536(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    monitor_identifier: typing.Any,
    scope: builtins.str,
    display_timezone: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    mute_first_recovery_notification: typing.Optional[builtins.bool] = None,
    notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    schedule: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0341e644d80f73372cc8b4d6697198340fc45fb5e2b598de14ecbc929124473(
    *,
    monitor_identifier: typing.Any,
    scope: builtins.str,
    display_timezone: typing.Optional[builtins.str] = None,
    message: typing.Optional[builtins.str] = None,
    mute_first_recovery_notification: typing.Optional[builtins.bool] = None,
    notify_end_states: typing.Optional[typing.Sequence[builtins.str]] = None,
    notify_end_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    schedule: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass
