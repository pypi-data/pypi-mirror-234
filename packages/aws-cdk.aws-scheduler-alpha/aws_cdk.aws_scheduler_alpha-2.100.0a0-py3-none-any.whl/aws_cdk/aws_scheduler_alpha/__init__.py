'''
# Amazon EventBridge Scheduler Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

[Amazon EventBridge Scheduler](https://aws.amazon.com/blogs/compute/introducing-amazon-eventbridge-scheduler/) is a feature from Amazon EventBridge
that allows you to create, run, and manage scheduled tasks at scale. With EventBridge Scheduler, you can schedule one-time or recurrently tens
of millions of tasks across many AWS services without provisioning or managing underlying infrastructure.

1. **Schedule**: A schedule is the main resource you create, configure, and manage using Amazon EventBridge Scheduler. Every schedule has a schedule expression that determines when, and with what frequency, the schedule runs. EventBridge Scheduler supports three types of schedules: rate, cron, and one-time schedules. When you create a schedule, you configure a target for the schedule to invoke.
2. **Targets**: A target is an API operation that EventBridge Scheduler calls on your behalf every time your schedule runs. EventBridge Scheduler
   supports two types of targets: templated targets and universal targets. Templated targets invoke common API operations across a core groups of
   services. For example, EventBridge Scheduler supports templated targets for invoking AWS Lambda Function or starting execution of Step Function state
   machine. For API operations that are not supported by templated targets you can use customizeable universal targets. Universal targets support calling
   more than 6,000 API operations across over 270 AWS services.
3. **Schedule Group**: A schedule group is an Amazon EventBridge Scheduler resource that you use to organize your schedules. Your AWS account comes
   with a default scheduler group. A new schedule will always be added to a scheduling group. If you do not provide a scheduling group to add to, it
   will be added to the default scheduling group. You can create up to 500 schedule groups in your AWS account. Groups can be used to organize the
   schedules logically, access the schedule metrics and manage permissions at group granularity (see details below). Scheduling groups support tagging:
   with EventBridge Scheduler, you apply tags to schedule groups, not to individual schedules to organize your resources.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project. It allows you to define Event Bridge Schedules.

> This module is in active development. Some features may not be implemented yet.

## Defining a schedule

```python
# fn: lambda.Function


target = targets.LambdaInvoke(fn,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    })
)

schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    description="This is a test schedule that invokes lambda function every 10 minutes."
)
```

### Schedule Expressions

You can choose from three schedule types when configuring your schedule: rate-based, cron-based, and one-time schedules.

Both rate-based and cron-based schedules are recurring schedules. You can configure each recurring schedule type using a schedule expression. For
cron-based schedule you can specify a time zone in which EventBridge Scheduler evaluates the expression.

```python
# target: targets.LambdaInvoke


rate_based_schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    description="This is a test rate-based schedule"
)

cron_based_schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.cron(
        minute="0",
        hour="23",
        day="20",
        month="11",
        time_zone=TimeZone.AMERICA_NEW_YORK
    ),
    target=target,
    description="This is a test cron-based schedule that will run at 11:00 PM, on day 20 of the month, only in November in New York timezone"
)
```

A one-time schedule is a schedule that invokes a target only once. You configure a one-time schedule when by specifying the time of the day, date,
and time zone in which EventBridge Scheduler evaluates the schedule.

```python
# target: targets.LambdaInvoke


one_time_schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.at(
        Date(2022, 10, 20, 19, 20, 23), TimeZone.AMERICA_NEW_YORK),
    target=target,
    description="This is a one-time schedule in New York timezone"
)
```

### Grouping Schedules

Your AWS account comes with a default scheduler group. You can access default group in CDK with:

```python
default_group = Group.from_default_group(self, "DefaultGroup")
```

If not specified a schedule is added to the default group. However, you can also add the schedule to a custom scheduling group managed by you:

```python
# target: targets.LambdaInvoke


group = Group(self, "Group",
    group_name="MyGroup"
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    group=group
)
```

### Disabling Schedules

By default, a schedule will be enabled. You can disable a schedule by setting the `enabled` property to false:

```python
# target: targets.LambdaInvoke


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    enabled=False
)
```

## Scheduler Targets

The `@aws-cdk/aws-scheduler-targets-alpha` module includes classes that implement the `IScheduleTarget` interface for
various AWS services. EventBridge Scheduler supports two types of targets: templated targets invoke common API
operations across a core groups of services, and customizeable universal targets that you can use to call more
than 6,000 operations across over 270 services. A list of supported targets can be found at `@aws-cdk/aws-scheduler-targets-alpha`.

### Input

Target can be invoked with a custom input. Class `ScheduleTargetInput` supports free form text input and JSON-formatted object input:

```python
input = ScheduleTargetInput.from_object({
    "QueueName": "MyQueue"
})
```

You can include context attributes in your target payload. EventBridge Scheduler will replace each keyword with
its respective value and deliver it to the target. See
[full list of supported context attributes](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-context-attributes.html):

1. `ContextAttribute.scheduleArn()` – The ARN of the schedule.
2. `ContextAttribute.scheduledTime()` – The time you specified for the schedule to invoke its target, for example, 2022-03-22T18:59:43Z.
3. `ContextAttribute.executionId()` – The unique ID that EventBridge Scheduler assigns for each attempted invocation of a target, for example, d32c5kddcf5bb8c3.
4. `ContextAttribute.attemptNumber()` – A counter that identifies the attempt number for the current invocation, for example, 1.

```python
text = f"Attempt number: {ContextAttribute.attemptNumber}"
input = ScheduleTargetInput.from_text(text)
```

### Specifying Execution Role

An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

The classes for templated schedule targets automatically create an IAM role with all the minimum necessary
permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
will grant minimal required permissions. For example: for invoking Lambda function target `LambdaInvoke` will grant
execution IAM role permission to `lambda:InvokeFunction`.

```python
# fn: lambda.Function


role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com")
)

target = targets.LambdaInvoke(fn,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    }),
    role=role
)
```

### Cross-account and cross-region targets

Executing cross-account and cross-region targets are not supported yet.

### Specifying Encryption key

TODO: Not yet implemented. See section in [L2 Event Bridge Scheduler RFC](https://github.com/aws/aws-cdk-rfcs/blob/master/text/0474-event-bridge-scheduler-l2.md)

## Error-handling

You can configure how your schedule handles failures, when EventBridge Scheduler is unable to deliver an event
successfully to a target, by using two primary mechanisms: a retry policy, and a dead-letter queue (DLQ).

A retry policy determines the number of times EventBridge Scheduler must retry a failed event, and how long
to keep an unprocessed event.

A DLQ is a standard Amazon SQS queue EventBridge Scheduler uses to deliver failed events to, after the retry
policy has been exhausted. You can use a DLQ to troubleshoot issues with your schedule or its downstream target.
If you've configured a retry policy for your schedule, EventBridge Scheduler delivers the dead-letter event after
exhausting the maximum number of retries you set in the retry policy.

```python
# fn: lambda.Function


dlq = sqs.Queue(self, "DLQ",
    queue_name="MyDLQ"
)

target = targets.LambdaInvoke(fn,
    dead_letter_queue=dlq,
    max_event_age=Duration.minutes(1),
    retry_attempts=3
)
```

## Overriding Target Properties

TODO: Not yet implemented. See section in [L2 Event Bridge Scheduler RFC](https://github.com/aws/aws-cdk-rfcs/blob/master/text/0474-event-bridge-scheduler-l2.md)

## Monitoring

You can monitor Amazon EventBridge Scheduler using CloudWatch, which collects raw data
and processes it into readable, near real-time metrics. EventBridge Scheduler emits
a set of metrics for all schedules, and an additional set of metrics for schedules that
have an associated dead-letter queue (DLQ). If you configure a DLQ for your schedule,
EventBridge Scheduler publishes additional metrics when your schedule exhausts its retry policy.

### Metrics for all schedules

TODO: Not yet implemented. See section in [L2 Event Bridge Scheduler RFC](https://github.com/aws/aws-cdk-rfcs/blob/master/text/0474-event-bridge-scheduler-l2.md)

### Metrics for a Group

To view metrics for a specific group you can use methods on class `Group`:

```python
group = Group(self, "Group",
    group_name="MyGroup"
)

cloudwatch.Alarm(self, "MyGroupErrorAlarm",
    metric=group.metric_target_errors(),
    evaluation_periods=1,
    threshold=0
)

# Or use default group
default_group = Group.from_default_group(self, "DefaultGroup")
cloudwatch.Alarm(self, "DefaultGroupErrorAlarm",
    metric=default_group.metric_target_errors(),
    evaluation_periods=1,
    threshold=0
)
```

See full list of metrics and their description at
[Monitoring Using CloudWatch Metrics](https://docs.aws.amazon.com/scheduler/latest/UserGuide/monitoring-cloudwatch.html)
in the *AWS Event Bridge Scheduler User Guide*.
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
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_scheduler as _aws_cdk_aws_scheduler_ceddda9d
import constructs as _constructs_77d1e7e8


class ContextAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.ContextAttribute",
):
    '''(experimental) Represents a field in the event pattern.

    :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-context-attributes.html
    :stability: experimental
    '''

    @jsii.member(jsii_name="fromName")
    @builtins.classmethod
    def from_name(cls, name: builtins.str) -> builtins.str:
        '''(experimental) Escape hatch for other ContextAttribute that might be resolved in future.

        :param name: - name will replace xxx in <aws.scheduler.xxx>.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3298180583c0ddbdf4d5fc4310e8726157d1b4b991a42e01360362e1c7d731)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromName", [name]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Convert the path to the field in the event pattern to JSON.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="attemptNumber")
    def attempt_number(cls) -> builtins.str:
        '''(experimental) A counter that identifies the attempt number for the current invocation, for example, 1.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "attemptNumber"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="executionId")
    def execution_id(cls) -> builtins.str:
        '''(experimental) The unique ID that EventBridge Scheduler assigns for each attempted invocation of a target, for example, d32c5kddcf5bb8c3.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "executionId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(cls) -> builtins.str:
        '''(experimental) The ARN of the schedule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "scheduleArn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="scheduledTime")
    def scheduled_time(cls) -> builtins.str:
        '''(experimental) The time you specified for the schedule to invoke its target, for example, 2022-03-22T18:59:43Z.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "scheduledTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.CronOptionsWithTimezone",
    jsii_struct_bases=[_aws_cdk_aws_events_ceddda9d.CronOptions],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
        "year": "year",
        "time_zone": "timeZone",
    },
)
class CronOptionsWithTimezone(_aws_cdk_aws_events_ceddda9d.CronOptions):
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
    ) -> None:
        '''(experimental) Options to configure a cron expression.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year
        :param time_zone: (experimental) The timezone to run the schedule in. Default: - TimeZone.ETC_UTC

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions
        :stability: experimental
        :exampleMetadata: infused

        Example::

            # target: targets.LambdaInvoke
            
            
            rate_based_schedule = Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(10)),
                target=target,
                description="This is a test rate-based schedule"
            )
            
            cron_based_schedule = Schedule(self, "Schedule",
                schedule=ScheduleExpression.cron(
                    minute="0",
                    hour="23",
                    day="20",
                    month="11",
                    time_zone=TimeZone.AMERICA_NEW_YORK
                ),
                target=target,
                description="This is a test cron-based schedule that will run at 11:00 PM, on day 20 of the month, only in November in New York timezone"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b93c2b718a23f23063cb14b1618a13104c926d0bdf7230ce719160d882d285a)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if week_day is not None:
            self._values["week_day"] = week_day
        if year is not None:
            self._values["year"] = year
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''The day of the month to run this rule at.

        :default: - Every day of the month
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        '''The hour to run this rule at.

        :default: - Every hour
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        '''The minute to run this rule at.

        :default: - Every minute
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        '''The month to run this rule at.

        :default: - Every month
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        '''The day of the week to run this rule at.

        :default: - Any day of the week
        '''
        result = self._values.get("week_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def year(self) -> typing.Optional[builtins.str]:
        '''The year to run this rule at.

        :default: - Every year
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[_aws_cdk_ceddda9d.TimeZone]:
        '''(experimental) The timezone to run the schedule in.

        :default: - TimeZone.ETC_UTC

        :stability: experimental
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.TimeZone], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptionsWithTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.GroupProps",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName", "removal_policy": "removalPolicy"},
)
class GroupProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param group_name: (experimental) The name of the schedule group. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated
        :param removal_policy: (experimental) The removal policy for the group. If the group is removed also all schedules are removed. Default: RemovalPolicy.RETAIN

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # target: targets.LambdaInvoke
            
            
            group = Group(self, "Group",
                group_name="MyGroup"
            )
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(10)),
                target=target,
                group=group
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e70812dffd651250e3c32989b91d882f629f2973738808560a5d95625eae32a)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the schedule group.

        Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed.

        :default: - A unique name will be generated

        :stability: experimental
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(experimental) The removal policy for the group.

        If the group is removed also all schedules are removed.

        :default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-scheduler-alpha.IGroup")
class IGroup(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(experimental) The arn of the schedule group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(experimental) The name of the schedule group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSentToDLQTrunacted")
    def metric_sent_to_dlq_trunacted(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: experimental
        '''
        ...


class _IGroupProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-scheduler-alpha.IGroup"

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(experimental) The arn of the schedule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(experimental) The name of the schedule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c255656ab6f0e3e078e7dc1cbbab1d697e65780cb1fd98622b8baec835090ab)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0687870c381a3baca7f4b904f4ac04af882c393c4e921edbb46354180efea008)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantDeleteSchedules", [identity]))

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4571a0b7363df77ef9266187c2d8848e8e0b8cca1b1f257361cdb5d92b4ee58c)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadSchedules", [identity]))

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc852d9860959f89dec6e107ee923432ec16c8be00fc5dab3b66420d63b4c7b7)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWriteSchedules", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5498dc1be7bc114f9e319e391ca23bdddccb5e44e4c81bce04e4fb998e6c54a)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricAttempts", [props]))

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricDropped", [props]))

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581616256867e412b78ad27c6b1df8ab52f755a908f2e868750a96f4ea7d9db6)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailedToBeSentToDLQ", [error_code, props]))

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQ", [props]))

    @jsii.member(jsii_name="metricSentToDLQTrunacted")
    def metric_sent_to_dlq_trunacted(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQTrunacted", [props]))

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetErrors", [props]))

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetThrottled", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricThrottled", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGroup).__jsii_proxy_class__ = lambda : _IGroupProxy


@jsii.interface(jsii_type="@aws-cdk/aws-scheduler-alpha.ISchedule")
class ISchedule(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Interface representing a created or an imported ``Schedule``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(self) -> builtins.str:
        '''(experimental) The arn of the schedule.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scheduleName")
    def schedule_name(self) -> builtins.str:
        '''(experimental) The name of the schedule.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.Optional[IGroup]:
        '''(experimental) The schedule group associated with this schedule.

        :stability: experimental
        '''
        ...


class _IScheduleProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Interface representing a created or an imported ``Schedule``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-scheduler-alpha.ISchedule"

    @builtins.property
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(self) -> builtins.str:
        '''(experimental) The arn of the schedule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduleName")
    def schedule_name(self) -> builtins.str:
        '''(experimental) The name of the schedule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleName"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.Optional[IGroup]:
        '''(experimental) The schedule group associated with this schedule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IGroup], jsii.get(self, "group"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISchedule).__jsii_proxy_class__ = lambda : _IScheduleProxy


@jsii.interface(jsii_type="@aws-cdk/aws-scheduler-alpha.IScheduleTarget")
class IScheduleTarget(typing_extensions.Protocol):
    '''(experimental) Interface representing a Event Bridge Schedule Target.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, _schedule: ISchedule) -> "ScheduleTargetConfig":
        '''(experimental) Returns the schedule target specification.

        :param _schedule: a schedule the target should be added to.

        :stability: experimental
        '''
        ...


class _IScheduleTargetProxy:
    '''(experimental) Interface representing a Event Bridge Schedule Target.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-scheduler-alpha.IScheduleTarget"

    @jsii.member(jsii_name="bind")
    def bind(self, _schedule: ISchedule) -> "ScheduleTargetConfig":
        '''(experimental) Returns the schedule target specification.

        :param _schedule: a schedule the target should be added to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28f823649c05e2eae45e2c63b5b0684fe861a38416935dbe55bcf0d10451241)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast("ScheduleTargetConfig", jsii.invoke(self, "bind", [_schedule]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScheduleTarget).__jsii_proxy_class__ = lambda : _IScheduleTargetProxy


@jsii.implements(ISchedule)
class Schedule(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.Schedule",
):
    '''(experimental) An EventBridge Schedule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # fn: lambda.Function
        
        
        target = targets.LambdaInvoke(fn,
            input=ScheduleTargetInput.from_object({
                "payload": "useful"
            })
        )
        
        schedule = Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(10)),
            target=target,
            description="This is a test schedule that invokes lambda function every 10 minutes."
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        schedule: "ScheduleExpression",
        target: IScheduleTarget,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        group: typing.Optional[IGroup] = None,
        schedule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param schedule: (experimental) The expression that defines when the schedule runs. Can be either a ``at``, ``rate`` or ``cron`` expression.
        :param target: (experimental) The schedule's target details.
        :param description: (experimental) The description you specify for the schedule. Default: - no value
        :param enabled: (experimental) Indicates whether the schedule is enabled. Default: true
        :param group: (experimental) The schedule's group. Default: - By default a schedule will be associated with the ``default`` group.
        :param schedule_name: (experimental) The name of the schedule. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5630933e51396e7fd66637b557fe7dc9cd565a88ca9ae1d5517435215dbc0220)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduleProps(
            schedule=schedule,
            target=target,
            description=description,
            enabled=enabled,
            group=group,
            schedule_name=schedule_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(self) -> builtins.str:
        '''(experimental) The arn of the schedule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduleName")
    def schedule_name(self) -> builtins.str:
        '''(experimental) The name of the schedule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleName"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.Optional[IGroup]:
        '''(experimental) The schedule group associated with this schedule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IGroup], jsii.get(self, "group"))


class ScheduleExpression(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleExpression",
):
    '''(experimental) ScheduleExpression for EventBridge Schedule.

    You can choose from three schedule types when configuring your schedule: rate-based, cron-based, and one-time schedules.
    Both rate-based and cron-based schedules are recurring schedules.

    :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # fn: lambda.Function
        
        
        target = targets.LambdaInvoke(fn,
            input=ScheduleTargetInput.from_object({
                "payload": "useful"
            })
        )
        
        schedule = Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(10)),
            target=target,
            description="This is a test schedule that invokes lambda function every 10 minutes."
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="at")
    @builtins.classmethod
    def at(
        cls,
        date: datetime.datetime,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
    ) -> "ScheduleExpression":
        '''(experimental) Construct a one-time schedule from a date.

        :param date: The date and time to use. The millisecond part will be ignored.
        :param time_zone: The time zone to use for interpreting the date. Default: - UTC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf0285b6946b1db006663f64ebff2eb43720129f53e712d42b59f3d29620873)
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "at", [date, time_zone]))

    @jsii.member(jsii_name="cron")
    @builtins.classmethod
    def cron(
        cls,
        *,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> "ScheduleExpression":
        '''(experimental) Create a recurring schedule from a set of cron fields and time zone.

        :param time_zone: (experimental) The timezone to run the schedule in. Default: - TimeZone.ETC_UTC
        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year

        :stability: experimental
        '''
        options = CronOptionsWithTimezone(
            time_zone=time_zone,
            day=day,
            hour=hour,
            minute=minute,
            month=month,
            week_day=week_day,
            year=year,
        )

        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "cron", [options]))

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(
        cls,
        expression: builtins.str,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
    ) -> "ScheduleExpression":
        '''(experimental) Construct a schedule from a literal schedule expression.

        :param expression: The expression to use. Must be in a format that EventBridge will recognize
        :param time_zone: The time zone to use for interpreting the expression. Default: - UTC

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0634c4b66b6d96653bcec6e5c37e7587eb5123a94680df0694878cb2276e874)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "expression", [expression, time_zone]))

    @jsii.member(jsii_name="rate")
    @builtins.classmethod
    def rate(cls, duration: _aws_cdk_ceddda9d.Duration) -> "ScheduleExpression":
        '''(experimental) Construct a recurring schedule from an interval and a time unit.

        Rates may be defined with any unit of time, but when converted into minutes, the duration must be a positive whole number of minutes.

        :param duration: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f7ba7d57267bb20d2ff8fd156c360c31850c2fb0387099338165ebc5ba04a4)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "rate", [duration]))

    @builtins.property
    @jsii.member(jsii_name="expressionString")
    @abc.abstractmethod
    def expression_string(self) -> builtins.str:
        '''(experimental) Retrieve the expression for this schedule.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    @abc.abstractmethod
    def time_zone(self) -> typing.Optional[_aws_cdk_ceddda9d.TimeZone]:
        '''(experimental) Retrieve the expression for this schedule.

        :stability: experimental
        '''
        ...


class _ScheduleExpressionProxy(ScheduleExpression):
    @builtins.property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> builtins.str:
        '''(experimental) Retrieve the expression for this schedule.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "expressionString"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> typing.Optional[_aws_cdk_ceddda9d.TimeZone]:
        '''(experimental) Retrieve the expression for this schedule.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.TimeZone], jsii.get(self, "timeZone"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduleExpression).__jsii_proxy_class__ = lambda : _ScheduleExpressionProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "target": "target",
        "description": "description",
        "enabled": "enabled",
        "group": "group",
        "schedule_name": "scheduleName",
    },
)
class ScheduleProps:
    def __init__(
        self,
        *,
        schedule: ScheduleExpression,
        target: IScheduleTarget,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        group: typing.Optional[IGroup] = None,
        schedule_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for ``Schedule``.

        :param schedule: (experimental) The expression that defines when the schedule runs. Can be either a ``at``, ``rate`` or ``cron`` expression.
        :param target: (experimental) The schedule's target details.
        :param description: (experimental) The description you specify for the schedule. Default: - no value
        :param enabled: (experimental) Indicates whether the schedule is enabled. Default: true
        :param group: (experimental) The schedule's group. Default: - By default a schedule will be associated with the ``default`` group.
        :param schedule_name: (experimental) The name of the schedule. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # fn: lambda.Function
            
            
            target = targets.LambdaInvoke(fn,
                input=ScheduleTargetInput.from_object({
                    "payload": "useful"
                })
            )
            
            schedule = Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(10)),
                target=target,
                description="This is a test schedule that invokes lambda function every 10 minutes."
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec894279ff23a2f409c8409807ceac73af12e448ac28d2398385477bf6c2e20)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument schedule_name", value=schedule_name, expected_type=type_hints["schedule_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
            "target": target,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if group is not None:
            self._values["group"] = group
        if schedule_name is not None:
            self._values["schedule_name"] = schedule_name

    @builtins.property
    def schedule(self) -> ScheduleExpression:
        '''(experimental) The expression that defines when the schedule runs.

        Can be either a ``at``, ``rate``
        or ``cron`` expression.

        :stability: experimental
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(ScheduleExpression, result)

    @builtins.property
    def target(self) -> IScheduleTarget:
        '''(experimental) The schedule's target details.

        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(IScheduleTarget, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description you specify for the schedule.

        :default: - no value

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the schedule is enabled.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group(self) -> typing.Optional[IGroup]:
        '''(experimental) The schedule's group.

        :default: - By default a schedule will be associated with the ``default`` group.

        :stability: experimental
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[IGroup], result)

    @builtins.property
    def schedule_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the schedule.

        Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed.

        :default: - A unique name will be generated

        :stability: experimental
        '''
        result = self._values.get("schedule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleTargetConfig",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "role": "role",
        "dead_letter_config": "deadLetterConfig",
        "ecs_parameters": "ecsParameters",
        "event_bridge_parameters": "eventBridgeParameters",
        "input": "input",
        "kinesis_parameters": "kinesisParameters",
        "retry_policy": "retryPolicy",
        "sage_maker_pipeline_parameters": "sageMakerPipelineParameters",
        "sqs_parameters": "sqsParameters",
    },
)
class ScheduleTargetConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        dead_letter_config: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        ecs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        input: typing.Optional["ScheduleTargetInput"] = None,
        kinesis_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Config of a Schedule Target used during initalization of Schedule.

        :param arn: (experimental) The Amazon Resource Name (ARN) of the target.
        :param role: (experimental) Role to use to invoke this event target.
        :param dead_letter_config: (experimental) An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule. If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.\\
        :param ecs_parameters: (experimental) The templated target type for the Amazon ECS RunTask API Operation.
        :param event_bridge_parameters: (experimental) The templated target type for the EventBridge PutEvents API operation.
        :param input: (experimental) What input to pass to the tatget.
        :param kinesis_parameters: (experimental) The templated target type for the Amazon Kinesis PutRecord API operation.
        :param retry_policy: (experimental) A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.
        :param sage_maker_pipeline_parameters: (experimental) The templated target type for the Amazon SageMaker StartPipelineExecution API operation.
        :param sqs_parameters: (experimental) The templated target type for the Amazon SQS SendMessage API Operation.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_scheduler_alpha as scheduler_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            # schedule_target_input: scheduler_alpha.ScheduleTargetInput
            # tags: Any
            
            schedule_target_config = scheduler_alpha.ScheduleTargetConfig(
                arn="arn",
                role=role,
            
                # the properties below are optional
                dead_letter_config=DeadLetterConfigProperty(
                    arn="arn"
                ),
                ecs_parameters=EcsParametersProperty(
                    task_definition_arn="taskDefinitionArn",
            
                    # the properties below are optional
                    capacity_provider_strategy=[CapacityProviderStrategyItemProperty(
                        capacity_provider="capacityProvider",
            
                        # the properties below are optional
                        base=123,
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=NetworkConfigurationProperty(
                        awsvpc_configuration=AwsVpcConfigurationProperty(
                            subnets=["subnets"],
            
                            # the properties below are optional
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"]
                        )
                    ),
                    placement_constraints=[PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=tags,
                    task_count=123
                ),
                event_bridge_parameters=EventBridgeParametersProperty(
                    detail_type="detailType",
                    source="source"
                ),
                input=schedule_target_input,
                kinesis_parameters=KinesisParametersProperty(
                    partition_key="partitionKey"
                ),
                retry_policy=RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                sage_maker_pipeline_parameters=SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                ),
                sqs_parameters=SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            )
        '''
        if isinstance(dead_letter_config, dict):
            dead_letter_config = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty(**dead_letter_config)
        if isinstance(ecs_parameters, dict):
            ecs_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty(**ecs_parameters)
        if isinstance(event_bridge_parameters, dict):
            event_bridge_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty(**event_bridge_parameters)
        if isinstance(kinesis_parameters, dict):
            kinesis_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty(**kinesis_parameters)
        if isinstance(retry_policy, dict):
            retry_policy = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty(**retry_policy)
        if isinstance(sage_maker_pipeline_parameters, dict):
            sage_maker_pipeline_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty(**sage_maker_pipeline_parameters)
        if isinstance(sqs_parameters, dict):
            sqs_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty(**sqs_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b43e95c111929dc4535529e66b018946277654e960b5110e44115e299a6c11)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument ecs_parameters", value=ecs_parameters, expected_type=type_hints["ecs_parameters"])
            check_type(argname="argument event_bridge_parameters", value=event_bridge_parameters, expected_type=type_hints["event_bridge_parameters"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument kinesis_parameters", value=kinesis_parameters, expected_type=type_hints["kinesis_parameters"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument sage_maker_pipeline_parameters", value=sage_maker_pipeline_parameters, expected_type=type_hints["sage_maker_pipeline_parameters"])
            check_type(argname="argument sqs_parameters", value=sqs_parameters, expected_type=type_hints["sqs_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "role": role,
        }
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if ecs_parameters is not None:
            self._values["ecs_parameters"] = ecs_parameters
        if event_bridge_parameters is not None:
            self._values["event_bridge_parameters"] = event_bridge_parameters
        if input is not None:
            self._values["input"] = input
        if kinesis_parameters is not None:
            self._values["kinesis_parameters"] = kinesis_parameters
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if sage_maker_pipeline_parameters is not None:
            self._values["sage_maker_pipeline_parameters"] = sage_maker_pipeline_parameters
        if sqs_parameters is not None:
            self._values["sqs_parameters"] = sqs_parameters

    @builtins.property
    def arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the target.

        :stability: experimental
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) Role to use to invoke this event target.

        :stability: experimental
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, result)

    @builtins.property
    def dead_letter_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty]:
        '''(experimental) An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule.

        If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.\\

        :stability: experimental
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty], result)

    @builtins.property
    def ecs_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty]:
        '''(experimental) The templated target type for the Amazon ECS RunTask API Operation.

        :stability: experimental
        '''
        result = self._values.get("ecs_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty], result)

    @builtins.property
    def event_bridge_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty]:
        '''(experimental) The templated target type for the EventBridge PutEvents API operation.

        :stability: experimental
        '''
        result = self._values.get("event_bridge_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty], result)

    @builtins.property
    def input(self) -> typing.Optional["ScheduleTargetInput"]:
        '''(experimental) What input to pass to the tatget.

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional["ScheduleTargetInput"], result)

    @builtins.property
    def kinesis_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty]:
        '''(experimental) The templated target type for the Amazon Kinesis PutRecord API operation.

        :stability: experimental
        '''
        result = self._values.get("kinesis_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty], result)

    @builtins.property
    def retry_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty]:
        '''(experimental) A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.

        :stability: experimental
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty], result)

    @builtins.property
    def sage_maker_pipeline_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty]:
        '''(experimental) The templated target type for the Amazon SageMaker StartPipelineExecution API operation.

        :stability: experimental
        '''
        result = self._values.get("sage_maker_pipeline_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty], result)

    @builtins.property
    def sqs_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty]:
        '''(experimental) The templated target type for the Amazon SQS SendMessage API Operation.

        :stability: experimental
        '''
        result = self._values.get("sqs_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduleTargetInput(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleTargetInput",
):
    '''(experimental) The text, or well-formed JSON, passed to the target of the schedule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # fn: lambda.Function
        
        
        target = targets.LambdaInvoke(fn,
            input=ScheduleTargetInput.from_object({
                "payload": "useful"
            })
        )
        
        schedule = Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(10)),
            target=target,
            description="This is a test schedule that invokes lambda function every 10 minutes."
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, obj: typing.Any) -> "ScheduleTargetInput":
        '''(experimental) Pass a JSON object to the target, it is possible to embed ``ContextAttributes`` and other cdk references.

        :param obj: object to use to convert to JSON to use as input for the target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8ad466ed6529e9804ae78b120437ef13be3ec57499e1adc15762a5e00bccce)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("ScheduleTargetInput", jsii.sinvoke(cls, "fromObject", [obj]))

    @jsii.member(jsii_name="fromText")
    @builtins.classmethod
    def from_text(cls, text: builtins.str) -> "ScheduleTargetInput":
        '''(experimental) Pass text to the target, it is possible to embed ``ContextAttributes`` that will be resolved to actual values while the CloudFormation is deployed or cdk Tokens that will be resolved when the CloudFormation templates are generated by CDK.

        The target input value will be a single string that you pass.
        For passing complex values like JSON object to a target use method
        ``ScheduleTargetInput.fromObject()`` instead.

        :param text: Text to use as the input for the target.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574fe803ab70d3031262c0aa59859d86504152f998a9cb5954d8eda9a4714e7d)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        return typing.cast("ScheduleTargetInput", jsii.sinvoke(cls, "fromText", [text]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, schedule: ISchedule) -> builtins.str:
        '''(experimental) Return the input properties for this input object.

        :param schedule: -

        :stability: experimental
        '''
        ...


class _ScheduleTargetInputProxy(ScheduleTargetInput):
    @jsii.member(jsii_name="bind")
    def bind(self, schedule: ISchedule) -> builtins.str:
        '''(experimental) Return the input properties for this input object.

        :param schedule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82eb20b61ddff46bbd14d8fd0a9b321cedc42dd29e60faa8e2d03dc8d7e9c9d)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [schedule]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduleTargetInput).__jsii_proxy_class__ = lambda : _ScheduleTargetInputProxy


@jsii.implements(IGroup)
class Group(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.Group",
):
    '''
    :stability: experimental
    :resource: AWS::Scheduler::ScheduleGroup
    :exampleMetadata: infused

    Example::

        # target: targets.LambdaInvoke
        
        
        group = Group(self, "Group",
            group_name="MyGroup"
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(10)),
            target=target,
            group=group
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param group_name: (experimental) The name of the schedule group. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated
        :param removal_policy: (experimental) The removal policy for the group. If the group is removed also all schedules are removed. Default: RemovalPolicy.RETAIN

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03833d1cdfd53d17a515f405994c670d3db76eb8e1b7b0644cc3e79b5f7cdebf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GroupProps(group_name=group_name, removal_policy=removal_policy)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDefaultGroup")
    @builtins.classmethod
    def from_default_group(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> IGroup:
        '''(experimental) Import a default schedule group.

        :param scope: construct scope.
        :param id: construct id.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2398434fe0af2499acd254ee14ed1a1ddf03cdb183b9f4a5eb1acf3100f1dee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromDefaultGroup", [scope, id]))

    @jsii.member(jsii_name="fromGroupArn")
    @builtins.classmethod
    def from_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_arn: builtins.str,
    ) -> IGroup:
        '''(experimental) Import an external group by ARN.

        :param scope: construct scope.
        :param id: construct id.
        :param group_arn: the ARN of the group to import (e.g. ``arn:aws:scheduler:region:account-id:schedule-group/group-name``).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca853fb3786085103e508aab2df418bf2a27504e961904ee0917c8d59159fbc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_arn", value=group_arn, expected_type=type_hints["group_arn"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupArn", [scope, id, group_arn]))

    @jsii.member(jsii_name="fromGroupName")
    @builtins.classmethod
    def from_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_name: builtins.str,
    ) -> IGroup:
        '''(experimental) Import an existing group with a given name.

        :param scope: construct scope.
        :param id: construct id.
        :param group_name: the name of the existing group to import.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3f5c8b704bfb81fab0017945f521fa1f85feb0992a204ad6bf13fcc162a66c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupName", [scope, id, group_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0337793d10fce9f5892ef4024bd3c27eba273469e53a2a4f232c8776713de290)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6279e157b2be9015bedaa73842f155a806c3c23dcda4080b96a88b4760e4d281)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantDeleteSchedules", [identity]))

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9fd27c6fa3b2fe7be510afbf27f59a845a71e1c9e2e83462272d01e99adbd9f)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadSchedules", [identity]))

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670c70dc050cb016f9eb04b7f5b099251cb74c7489f34f6a48991d1ca421271a)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWriteSchedules", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f218efce492e06a45099719a7de7cf0d34b4457ee121c7b854b4ccb99c19405)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricAttempts", [props]))

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricDropped", [props]))

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1252a3e7553c8408b06da1170a1703b3ecb7419c8f88133f82bc0efcda0a0c8)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailedToBeSentToDLQ", [error_code, props]))

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQ", [props]))

    @jsii.member(jsii_name="metricSentToDLQTrunacted")
    def metric_sent_to_dlq_trunacted(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQTrunacted", [props]))

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetErrors", [props]))

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetThrottled", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricThrottled", [props]))

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(experimental) The arn of the schedule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(experimental) The name of the schedule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))


__all__ = [
    "ContextAttribute",
    "CronOptionsWithTimezone",
    "Group",
    "GroupProps",
    "IGroup",
    "ISchedule",
    "IScheduleTarget",
    "Schedule",
    "ScheduleExpression",
    "ScheduleProps",
    "ScheduleTargetConfig",
    "ScheduleTargetInput",
]

publication.publish()

def _typecheckingstub__fa3298180583c0ddbdf4d5fc4310e8726157d1b4b991a42e01360362e1c7d731(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b93c2b718a23f23063cb14b1618a13104c926d0bdf7230ce719160d882d285a(
    *,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    month: typing.Optional[builtins.str] = None,
    week_day: typing.Optional[builtins.str] = None,
    year: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e70812dffd651250e3c32989b91d882f629f2973738808560a5d95625eae32a(
    *,
    group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c255656ab6f0e3e078e7dc1cbbab1d697e65780cb1fd98622b8baec835090ab(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0687870c381a3baca7f4b904f4ac04af882c393c4e921edbb46354180efea008(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4571a0b7363df77ef9266187c2d8848e8e0b8cca1b1f257361cdb5d92b4ee58c(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc852d9860959f89dec6e107ee923432ec16c8be00fc5dab3b66420d63b4c7b7(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5498dc1be7bc114f9e319e391ca23bdddccb5e44e4c81bce04e4fb998e6c54a(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581616256867e412b78ad27c6b1df8ab52f755a908f2e868750a96f4ea7d9db6(
    error_code: typing.Optional[builtins.str] = None,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28f823649c05e2eae45e2c63b5b0684fe861a38416935dbe55bcf0d10451241(
    _schedule: ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5630933e51396e7fd66637b557fe7dc9cd565a88ca9ae1d5517435215dbc0220(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    schedule: ScheduleExpression,
    target: IScheduleTarget,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    group: typing.Optional[IGroup] = None,
    schedule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf0285b6946b1db006663f64ebff2eb43720129f53e712d42b59f3d29620873(
    date: datetime.datetime,
    time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0634c4b66b6d96653bcec6e5c37e7587eb5123a94680df0694878cb2276e874(
    expression: builtins.str,
    time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f7ba7d57267bb20d2ff8fd156c360c31850c2fb0387099338165ebc5ba04a4(
    duration: _aws_cdk_ceddda9d.Duration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec894279ff23a2f409c8409807ceac73af12e448ac28d2398385477bf6c2e20(
    *,
    schedule: ScheduleExpression,
    target: IScheduleTarget,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    group: typing.Optional[IGroup] = None,
    schedule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b43e95c111929dc4535529e66b018946277654e960b5110e44115e299a6c11(
    *,
    arn: builtins.str,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    dead_letter_config: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bridge_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    input: typing.Optional[ScheduleTargetInput] = None,
    kinesis_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_policy: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8ad466ed6529e9804ae78b120437ef13be3ec57499e1adc15762a5e00bccce(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574fe803ab70d3031262c0aa59859d86504152f998a9cb5954d8eda9a4714e7d(
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82eb20b61ddff46bbd14d8fd0a9b321cedc42dd29e60faa8e2d03dc8d7e9c9d(
    schedule: ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03833d1cdfd53d17a515f405994c670d3db76eb8e1b7b0644cc3e79b5f7cdebf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2398434fe0af2499acd254ee14ed1a1ddf03cdb183b9f4a5eb1acf3100f1dee(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca853fb3786085103e508aab2df418bf2a27504e961904ee0917c8d59159fbc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3f5c8b704bfb81fab0017945f521fa1f85feb0992a204ad6bf13fcc162a66c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0337793d10fce9f5892ef4024bd3c27eba273469e53a2a4f232c8776713de290(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6279e157b2be9015bedaa73842f155a806c3c23dcda4080b96a88b4760e4d281(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fd27c6fa3b2fe7be510afbf27f59a845a71e1c9e2e83462272d01e99adbd9f(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670c70dc050cb016f9eb04b7f5b099251cb74c7489f34f6a48991d1ca421271a(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f218efce492e06a45099719a7de7cf0d34b4457ee121c7b854b4ccb99c19405(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1252a3e7553c8408b06da1170a1703b3ecb7419c8f88133f82bc0efcda0a0c8(
    error_code: typing.Optional[builtins.str] = None,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass
