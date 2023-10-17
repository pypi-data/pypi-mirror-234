'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-budgets-notification?style=flat-square)](https://github.com/yicr/aws-budgets-notification/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-budgets-notification?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-budgets-notification)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-budgets-notification?style=flat-square)](https://pypi.org/project/gammarer.aws-budgets-notification/)

<!-- [![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.SecureFrontendWebAppCloudFrontDistribution?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.SecureFrontendWebAppCloudFrontDistribution/)  -->

[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-budgets-notification?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-budgets-notification/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-budgets-notification/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-budgets-notification/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-budgets-notification?sort=semver&style=flat-square)](https://github.com/yicr/aws-budgets-notification/releases)

# AWS Budgets Notification

A construct library for creating AWS Budgets Notification to Slack with the AWS CDK.

## Resources

This construct creating resource list.

* SNS Topic
* ChatBot SlackChannelConfiguration
* Budgets (linked account count or self)

## Install

### TypeScript

```shell
npm install @gammarer/aws-budgets-notification
# or
yarn add @gammarer/aws-budgets-notification
```

### Python

```shell
pip install gammarer.aws-budgets-notification
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-budgets-notification</artifactId>
</dependency>
```

## Example

```python
import { BudgetsNotification } from '@gammarer/aws-budgets-notification';

new BudgetsNotification(stack, 'BudgetsNotification', {
  slackWorkspaceId: 'T0XXXX111', // already AWS account linked your Slack.
  slackChannelId: 'XXXXXXXX', // already created your slack channel.
  budgetLimitAmount: 50,
  // optional linked account list
  linkedAccounts: [
    '111111111111',
    '222222222222',
  ],
});
```

![example notification](./docs/slack-notification-image.png)

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


class BudgetsNotification(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-budgets-notification.BudgetsNotification",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        budget_limit_amount: jsii.Number,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        linked_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param budget_limit_amount: 
        :param slack_channel_id: 
        :param slack_workspace_id: 
        :param linked_accounts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2fcdb5bc02dfda3c46dd137ce1d81357216e090d1d25588359548743044d83)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BudgetsNotificationProps(
            budget_limit_amount=budget_limit_amount,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            linked_accounts=linked_accounts,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-budgets-notification.BudgetsNotificationProps",
    jsii_struct_bases=[],
    name_mapping={
        "budget_limit_amount": "budgetLimitAmount",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "linked_accounts": "linkedAccounts",
    },
)
class BudgetsNotificationProps:
    def __init__(
        self,
        *,
        budget_limit_amount: jsii.Number,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        linked_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param budget_limit_amount: 
        :param slack_channel_id: 
        :param slack_workspace_id: 
        :param linked_accounts: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f91cb26770a89574e656864bff471977d8602082ebd1eebfeb33b043e9b216)
            check_type(argname="argument budget_limit_amount", value=budget_limit_amount, expected_type=type_hints["budget_limit_amount"])
            check_type(argname="argument slack_channel_id", value=slack_channel_id, expected_type=type_hints["slack_channel_id"])
            check_type(argname="argument slack_workspace_id", value=slack_workspace_id, expected_type=type_hints["slack_workspace_id"])
            check_type(argname="argument linked_accounts", value=linked_accounts, expected_type=type_hints["linked_accounts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "budget_limit_amount": budget_limit_amount,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }
        if linked_accounts is not None:
            self._values["linked_accounts"] = linked_accounts

    @builtins.property
    def budget_limit_amount(self) -> jsii.Number:
        result = self._values.get("budget_limit_amount")
        assert result is not None, "Required property 'budget_limit_amount' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def slack_channel_id(self) -> builtins.str:
        result = self._values.get("slack_channel_id")
        assert result is not None, "Required property 'slack_channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_workspace_id(self) -> builtins.str:
        result = self._values.get("slack_workspace_id")
        assert result is not None, "Required property 'slack_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def linked_accounts(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("linked_accounts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BudgetsNotificationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BudgetsNotification",
    "BudgetsNotificationProps",
]

publication.publish()

def _typecheckingstub__fc2fcdb5bc02dfda3c46dd137ce1d81357216e090d1d25588359548743044d83(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    budget_limit_amount: jsii.Number,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    linked_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f91cb26770a89574e656864bff471977d8602082ebd1eebfeb33b043e9b216(
    *,
    budget_limit_amount: jsii.Number,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    linked_accounts: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
