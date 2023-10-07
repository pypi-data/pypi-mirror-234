'''
# AWS CDK Discord Notifier Constructs

This is a CDK construct library the vends constructs used to notify via discord about various resources and services.

## Constructs

The following constructs are available:

`MonthlyCostNotifier` - This construct will notify a discord webhook with a formatted embed of the monthly billing for the account.
`TrueNasAlertNotifier` - Creates resources to ingest a TrueNAS SNS alert by sending it to a lambda where it is parsed and sent to a discord webhook.

## Available Packages

This provider is built for the following languages:

* Javascript/Typescript
* Python
* C#

Details on how to find these packages are below and on [ConstructHub](https://constructs.dev/packages/@awlsring/cdk-aws-discord-notifiers)

### NPM

Javascript/Typescript package is available on NPM.

The npm package is viewable at https://www.npmjs.com/package/@awlsring/cdk-aws-discord-notifiers

```bash
npm install @awlsring/cdk-aws-discord-notifiers
```

### PyPi

Python package is available on PyPi.

The pypi package is viewable at https://pypi.org/project/cdk-aws-discord-notifiers/

```bash
pip install cdk-aws-discord-notifiers
```

### Nuget

C# package is available on Nuget.

The nuget package is viewable at https://www.nuget.org/packages/awlsring.CdkAwsDiscordNotifiers/

```bash
dotnet add package awlsring.CdkAwsDiscordNotifiers
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

import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@awlsring/cdk-aws-discord-notifiers.LambdaOptions",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "log_level": "logLevel",
        "name": "name",
        "role_policy": "rolePolicy",
        "runtime": "runtime",
    },
)
class LambdaOptions:
    def __init__(
        self,
        *,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        log_level: typing.Optional["LogLevel"] = None,
        name: typing.Optional[builtins.str] = None,
        role_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Policy] = None,
        runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
    ) -> None:
        '''
        :param architecture: The lambda architecture. Default: ARM_64
        :param log_level: The lambda log level. Default: INFO
        :param name: The lambda name. Default: TrueNasAlertNotifier
        :param role_policy: An additional policy to attach to the lambda. Default: none
        :param runtime: The lambda runtime. Default: NODES_LATEST
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b366848c5e5fb5e6e3574ec24d569b362b47bf136209035e6925d37c71718a49)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_policy", value=role_policy, expected_type=type_hints["role_policy"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if log_level is not None:
            self._values["log_level"] = log_level
        if name is not None:
            self._values["name"] = name
        if role_policy is not None:
            self._values["role_policy"] = role_policy
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''The lambda architecture.

        :default: ARM_64
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def log_level(self) -> typing.Optional["LogLevel"]:
        '''The lambda log level.

        :default: INFO
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional["LogLevel"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The lambda name.

        :default: TrueNasAlertNotifier
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Policy]:
        '''An additional policy to attach to the lambda.

        :default: none
        '''
        result = self._values.get("role_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Policy], result)

    @builtins.property
    def runtime(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime]:
        '''The lambda runtime.

        :default: NODES_LATEST
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@awlsring/cdk-aws-discord-notifiers.LogLevel")
class LogLevel(enum.Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class MonthlyCostNotifier(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdk-aws-discord-notifiers.MonthlyCostNotifier",
):
    '''A construct that creates a lambda function bundled with the 'monthly-notifier-lambda' code This is trigger via eventbridge on a schedule to post to a discord webhook for the monthly costs  WARNING: This lambda uses a pay per request API.

    Each call to cost explorer costs $0.01 USD.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        webhook: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        account_name: typing.Optional[builtins.str] = None,
        lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        rule_schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        webhook_avatar: typing.Optional[builtins.str] = None,
        webhook_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param webhook: The webhook to post to.
        :param account_id: The accountId this is being deployed to.
        :param account_name: The name of the account this is being deployed to.
        :param lambda_options: options to configure the lambda.
        :param rule_name: The eventbridge rule name. Default: MonthlyCostNotifierRule
        :param rule_schedule: The eventbridge rule schedule. Default: - { minute: '0', hour: '15', day: '1', month: '*', year: '*' }
        :param webhook_avatar: The user avatar to use.
        :param webhook_user: User to post to the webhook as.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f750ebf7ff2f6b9cbfa79e41efe824c83dc3479df4530a0de50e14a6967283b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MonthlyCostNotifierProps(
            webhook=webhook,
            account_id=account_id,
            account_name=account_name,
            lambda_options=lambda_options,
            rule_name=rule_name,
            rule_schedule=rule_schedule,
            webhook_avatar=webhook_avatar,
            webhook_user=webhook_user,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@awlsring/cdk-aws-discord-notifiers.MonthlyCostNotifierProps",
    jsii_struct_bases=[],
    name_mapping={
        "webhook": "webhook",
        "account_id": "accountId",
        "account_name": "accountName",
        "lambda_options": "lambdaOptions",
        "rule_name": "ruleName",
        "rule_schedule": "ruleSchedule",
        "webhook_avatar": "webhookAvatar",
        "webhook_user": "webhookUser",
    },
)
class MonthlyCostNotifierProps:
    def __init__(
        self,
        *,
        webhook: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        account_name: typing.Optional[builtins.str] = None,
        lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        rule_schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        webhook_avatar: typing.Optional[builtins.str] = None,
        webhook_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for a MonthlyCostNotifier.

        :param webhook: The webhook to post to.
        :param account_id: The accountId this is being deployed to.
        :param account_name: The name of the account this is being deployed to.
        :param lambda_options: options to configure the lambda.
        :param rule_name: The eventbridge rule name. Default: MonthlyCostNotifierRule
        :param rule_schedule: The eventbridge rule schedule. Default: - { minute: '0', hour: '15', day: '1', month: '*', year: '*' }
        :param webhook_avatar: The user avatar to use.
        :param webhook_user: User to post to the webhook as.
        '''
        if isinstance(lambda_options, dict):
            lambda_options = LambdaOptions(**lambda_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bcc77056382af1b2846479834ff3db4561c9852d8270e6f0b11bee4f0c88845)
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument lambda_options", value=lambda_options, expected_type=type_hints["lambda_options"])
            check_type(argname="argument rule_name", value=rule_name, expected_type=type_hints["rule_name"])
            check_type(argname="argument rule_schedule", value=rule_schedule, expected_type=type_hints["rule_schedule"])
            check_type(argname="argument webhook_avatar", value=webhook_avatar, expected_type=type_hints["webhook_avatar"])
            check_type(argname="argument webhook_user", value=webhook_user, expected_type=type_hints["webhook_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "webhook": webhook,
        }
        if account_id is not None:
            self._values["account_id"] = account_id
        if account_name is not None:
            self._values["account_name"] = account_name
        if lambda_options is not None:
            self._values["lambda_options"] = lambda_options
        if rule_name is not None:
            self._values["rule_name"] = rule_name
        if rule_schedule is not None:
            self._values["rule_schedule"] = rule_schedule
        if webhook_avatar is not None:
            self._values["webhook_avatar"] = webhook_avatar
        if webhook_user is not None:
            self._values["webhook_user"] = webhook_user

    @builtins.property
    def webhook(self) -> builtins.str:
        '''The webhook to post to.'''
        result = self._values.get("webhook")
        assert result is not None, "Required property 'webhook' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The accountId this is being deployed to.'''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def account_name(self) -> typing.Optional[builtins.str]:
        '''The name of the account this is being deployed to.'''
        result = self._values.get("account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_options(self) -> typing.Optional[LambdaOptions]:
        '''options to configure the lambda.'''
        result = self._values.get("lambda_options")
        return typing.cast(typing.Optional[LambdaOptions], result)

    @builtins.property
    def rule_name(self) -> typing.Optional[builtins.str]:
        '''The eventbridge rule name.

        :default: MonthlyCostNotifierRule
        '''
        result = self._values.get("rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''The eventbridge rule schedule.

        :default: - { minute: '0', hour: '15', day: '1', month: '*', year: '*' }
        '''
        result = self._values.get("rule_schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    @builtins.property
    def webhook_avatar(self) -> typing.Optional[builtins.str]:
        '''The user avatar to use.'''
        result = self._values.get("webhook_avatar")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_user(self) -> typing.Optional[builtins.str]:
        '''User to post to the webhook as.'''
        result = self._values.get("webhook_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonthlyCostNotifierProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TrueNasAlertNotifier(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdk-aws-discord-notifiers.TrueNasAlertNotifier",
):
    '''A construct that creates a series of resources that allows TrueNAS SNS alerts to be sent to a discord webhook.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        webhook: builtins.str,
        create_iam_role: typing.Optional[builtins.bool] = None,
        display_current_alerts: typing.Optional[builtins.bool] = None,
        lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        truenas_url: typing.Optional[builtins.str] = None,
        webhook_avatar: typing.Optional[builtins.str] = None,
        webhook_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param webhook: The webhook to post to.
        :param create_iam_role: If an IAM role should be created TrueNAS to post to the SNS topic.
        :param display_current_alerts: If current alerts should be displayed in embed.
        :param lambda_options: options to configure the lambda.
        :param truenas_url: The URL of the truenas instance.
        :param webhook_avatar: The user avatar to use.
        :param webhook_user: User to post to the webhook as.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8e835c417e577039d0631d7346949f144e09d20c4add548998befa43d26dc06)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TrueNasAlertNotifierProps(
            webhook=webhook,
            create_iam_role=create_iam_role,
            display_current_alerts=display_current_alerts,
            lambda_options=lambda_options,
            truenas_url=truenas_url,
            webhook_avatar=webhook_avatar,
            webhook_user=webhook_user,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@awlsring/cdk-aws-discord-notifiers.TrueNasAlertNotifierProps",
    jsii_struct_bases=[],
    name_mapping={
        "webhook": "webhook",
        "create_iam_role": "createIamRole",
        "display_current_alerts": "displayCurrentAlerts",
        "lambda_options": "lambdaOptions",
        "truenas_url": "truenasUrl",
        "webhook_avatar": "webhookAvatar",
        "webhook_user": "webhookUser",
    },
)
class TrueNasAlertNotifierProps:
    def __init__(
        self,
        *,
        webhook: builtins.str,
        create_iam_role: typing.Optional[builtins.bool] = None,
        display_current_alerts: typing.Optional[builtins.bool] = None,
        lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        truenas_url: typing.Optional[builtins.str] = None,
        webhook_avatar: typing.Optional[builtins.str] = None,
        webhook_user: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param webhook: The webhook to post to.
        :param create_iam_role: If an IAM role should be created TrueNAS to post to the SNS topic.
        :param display_current_alerts: If current alerts should be displayed in embed.
        :param lambda_options: options to configure the lambda.
        :param truenas_url: The URL of the truenas instance.
        :param webhook_avatar: The user avatar to use.
        :param webhook_user: User to post to the webhook as.
        '''
        if isinstance(lambda_options, dict):
            lambda_options = LambdaOptions(**lambda_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94cb25ebe5cdcc7ab489c64370aa03950d64302db6aa49cad288b73ca0a922b9)
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
            check_type(argname="argument create_iam_role", value=create_iam_role, expected_type=type_hints["create_iam_role"])
            check_type(argname="argument display_current_alerts", value=display_current_alerts, expected_type=type_hints["display_current_alerts"])
            check_type(argname="argument lambda_options", value=lambda_options, expected_type=type_hints["lambda_options"])
            check_type(argname="argument truenas_url", value=truenas_url, expected_type=type_hints["truenas_url"])
            check_type(argname="argument webhook_avatar", value=webhook_avatar, expected_type=type_hints["webhook_avatar"])
            check_type(argname="argument webhook_user", value=webhook_user, expected_type=type_hints["webhook_user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "webhook": webhook,
        }
        if create_iam_role is not None:
            self._values["create_iam_role"] = create_iam_role
        if display_current_alerts is not None:
            self._values["display_current_alerts"] = display_current_alerts
        if lambda_options is not None:
            self._values["lambda_options"] = lambda_options
        if truenas_url is not None:
            self._values["truenas_url"] = truenas_url
        if webhook_avatar is not None:
            self._values["webhook_avatar"] = webhook_avatar
        if webhook_user is not None:
            self._values["webhook_user"] = webhook_user

    @builtins.property
    def webhook(self) -> builtins.str:
        '''The webhook to post to.'''
        result = self._values.get("webhook")
        assert result is not None, "Required property 'webhook' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def create_iam_role(self) -> typing.Optional[builtins.bool]:
        '''If an IAM role should be created TrueNAS to post to the SNS topic.'''
        result = self._values.get("create_iam_role")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def display_current_alerts(self) -> typing.Optional[builtins.bool]:
        '''If current alerts should be displayed in embed.'''
        result = self._values.get("display_current_alerts")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lambda_options(self) -> typing.Optional[LambdaOptions]:
        '''options to configure the lambda.'''
        result = self._values.get("lambda_options")
        return typing.cast(typing.Optional[LambdaOptions], result)

    @builtins.property
    def truenas_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the truenas instance.'''
        result = self._values.get("truenas_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_avatar(self) -> typing.Optional[builtins.str]:
        '''The user avatar to use.'''
        result = self._values.get("webhook_avatar")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook_user(self) -> typing.Optional[builtins.str]:
        '''User to post to the webhook as.'''
        result = self._values.get("webhook_user")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TrueNasAlertNotifierProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LambdaOptions",
    "LogLevel",
    "MonthlyCostNotifier",
    "MonthlyCostNotifierProps",
    "TrueNasAlertNotifier",
    "TrueNasAlertNotifierProps",
]

publication.publish()

def _typecheckingstub__b366848c5e5fb5e6e3574ec24d569b362b47bf136209035e6925d37c71718a49(
    *,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    log_level: typing.Optional[LogLevel] = None,
    name: typing.Optional[builtins.str] = None,
    role_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.Policy] = None,
    runtime: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Runtime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f750ebf7ff2f6b9cbfa79e41efe824c83dc3479df4530a0de50e14a6967283b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    webhook: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    account_name: typing.Optional[builtins.str] = None,
    lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    rule_schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    webhook_avatar: typing.Optional[builtins.str] = None,
    webhook_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bcc77056382af1b2846479834ff3db4561c9852d8270e6f0b11bee4f0c88845(
    *,
    webhook: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    account_name: typing.Optional[builtins.str] = None,
    lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    rule_schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    webhook_avatar: typing.Optional[builtins.str] = None,
    webhook_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8e835c417e577039d0631d7346949f144e09d20c4add548998befa43d26dc06(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    webhook: builtins.str,
    create_iam_role: typing.Optional[builtins.bool] = None,
    display_current_alerts: typing.Optional[builtins.bool] = None,
    lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    truenas_url: typing.Optional[builtins.str] = None,
    webhook_avatar: typing.Optional[builtins.str] = None,
    webhook_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94cb25ebe5cdcc7ab489c64370aa03950d64302db6aa49cad288b73ca0a922b9(
    *,
    webhook: builtins.str,
    create_iam_role: typing.Optional[builtins.bool] = None,
    display_current_alerts: typing.Optional[builtins.bool] = None,
    lambda_options: typing.Optional[typing.Union[LambdaOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    truenas_url: typing.Optional[builtins.str] = None,
    webhook_avatar: typing.Optional[builtins.str] = None,
    webhook_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
