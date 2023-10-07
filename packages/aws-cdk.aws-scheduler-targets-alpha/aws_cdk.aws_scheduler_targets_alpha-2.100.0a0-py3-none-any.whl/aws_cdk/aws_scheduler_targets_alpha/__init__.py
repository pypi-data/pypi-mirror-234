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

This library contains integration classes for Amazon EventBridge Scheduler to call any
number of supported AWS Services.

The following targets are supported:

1. `targets.LambdaInvoke`: [Invoke an AWS Lambda function](#invoke-a-lambda-function))

## Invoke a Lambda function

Use the `LambdaInvoke` target to invoke a lambda function.

The code snippet below creates an event rule with a Lambda function as a target
called every hour by Event Bridge Scheduler with custom payload. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
import aws_cdk.aws_lambda as lambda_


fn = lambda_.Function(self, "MyFunc",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_inline("exports.handler = handler.toString()")
)

dlq = sqs.Queue(self, "DLQ",
    queue_name="MyDLQ"
)

target = targets.LambdaInvoke(fn,
    dead_letter_queue=dlq,
    max_event_age=Duration.minutes(1),
    retry_attempts=3,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    })
)

schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=target
)
```
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
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_scheduler_alpha as _aws_cdk_aws_scheduler_alpha_61df44e1
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d


class ScheduleTargetBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.ScheduleTargetBase",
):
    '''(experimental) Base class for Schedule Targets.

    :stability: experimental
    '''

    def __init__(
        self,
        base_props: typing.Union["ScheduleTargetBaseProps", typing.Dict[builtins.str, typing.Any]],
        target_arn: builtins.str,
    ) -> None:
        '''
        :param base_props: -
        :param target_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e59e7b340dc335b31c4a0d18b1845659c5a575671ec4c54fa176892cb9bd54)
            check_type(argname="argument base_props", value=base_props, expected_type=type_hints["base_props"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        jsii.create(self.__class__, self, [base_props, target_arn])

    @jsii.member(jsii_name="addTargetActionToRole")
    @abc.abstractmethod
    def _add_target_action_to_role(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> None:
        '''
        :param schedule: -
        :param role: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''(experimental) Create a return a Schedule Target Configuration for the given schedule.

        :param schedule: -

        :stability: experimental
        :returnn: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e82b6bad0ce8e66d78921fb69afc41cc589ff68e7fde7d3a116a558622ba0b)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bind", [schedule]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d8230d421e6fe144b04cf440bae3b93c14a1af6ea5635fc876670037e3a4ee)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def _target_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


class _ScheduleTargetBaseProxy(ScheduleTargetBase):
    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> None:
        '''
        :param schedule: -
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610cc83281b440576390d0e3dbfaa9a65adba95233cb7ffdfba72197abc9da29)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [schedule, role]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduleTargetBase).__jsii_proxy_class__ = lambda : _ScheduleTargetBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.ScheduleTargetBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
    },
)
class ScheduleTargetBaseProps:
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Base properties for a Schedule Target.

        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Universal target automatically create an IAM role if you do not specify your own IAM role. However, in comparison with templated targets, for universal targets you must grant the required IAM permissions yourself. Default: - created by target

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
            type_hints = typing.get_type_hints(_typecheckingstub__3e05948e70de09bca87c06a271bef4e0b3a07893d3e2112141ebdce3856e9e80)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(experimental) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(experimental) Input passed to the target.

        :default: - no input.

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        Universal target automatically create an IAM role if you do not specify your own IAM role.
        However, in comparison with templated targets, for universal targets you must grant the required
        IAM permissions yourself.

        :default: - created by target

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleTargetBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class LambdaInvoke(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.LambdaInvoke",
):
    '''(experimental) Use an AWS Lambda function as a target for AWS EventBridge Scheduler.

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
        func: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param func: -
        :param dead_letter_queue: (experimental) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (experimental) Input passed to the target. Default: - no input.
        :param max_event_age: (experimental) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (experimental) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (experimental) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Universal target automatically create an IAM role if you do not specify your own IAM role. However, in comparison with templated targets, for universal targets you must grant the required IAM permissions yourself. Default: - created by target

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cee0b6faf4f1c2dcade061e69cf02b9c302a868d55e47f591978024f5da0075)
            check_type(argname="argument func", value=func, expected_type=type_hints["func"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [func, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
    ) -> None:
        '''
        :param schedule: -
        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bceedc3f4419f27eac20d417a223b3233c972e163393fd278acd75b7129d89)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [schedule, role]))


__all__ = [
    "LambdaInvoke",
    "ScheduleTargetBase",
    "ScheduleTargetBaseProps",
]

publication.publish()

def _typecheckingstub__10e59e7b340dc335b31c4a0d18b1845659c5a575671ec4c54fa176892cb9bd54(
    base_props: typing.Union[ScheduleTargetBaseProps, typing.Dict[builtins.str, typing.Any]],
    target_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e82b6bad0ce8e66d78921fb69afc41cc589ff68e7fde7d3a116a558622ba0b(
    schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d8230d421e6fe144b04cf440bae3b93c14a1af6ea5635fc876670037e3a4ee(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610cc83281b440576390d0e3dbfaa9a65adba95233cb7ffdfba72197abc9da29(
    schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e05948e70de09bca87c06a271bef4e0b3a07893d3e2112141ebdce3856e9e80(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cee0b6faf4f1c2dcade061e69cf02b9c302a868d55e47f591978024f5da0075(
    func: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bceedc3f4419f27eac20d417a223b3233c972e163393fd278acd75b7129d89(
    schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass
