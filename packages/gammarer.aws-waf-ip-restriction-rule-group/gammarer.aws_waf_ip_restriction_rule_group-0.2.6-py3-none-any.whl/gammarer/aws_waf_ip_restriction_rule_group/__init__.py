'''
[![GitHub](https://img.shields.io/github/license/yicr/aws-waf-ip-restriction-rule-group?style=flat-square)](https://github.com/yicr/aws-waf-ip-restriction-rule-group/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@gammarer/aws-waf-ip-restriction-rule-group?style=flat-square)](https://www.npmjs.com/package/@gammarer/aws-waf-ip-restriction-rule-group)
[![PyPI](https://img.shields.io/pypi/v/gammarer.aws-waf-ip-restriction-rule-group?style=flat-square)](https://pypi.org/project/gammarer.aws-waf-ip-restriction-rule-group/)

<!-- [![Nuget](https://img.shields.io/nuget/v/Gammarer.CDK.AWS.WafIpRestrictionRuleGroup?style=flat-square)](https://www.nuget.org/packages/Gammarer.CDK.AWS.WafIpRestrictionRuleGroup/)  -->

[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.gammarer/aws-waf-ip-restriction-rule-group?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/gammarer/aws-waf-ip-restriction-rule-group/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/yicr/aws-waf-ip-restriction-rule-group/release.yml?branch=main&label=release&style=flat-square)](https://github.com/yicr/aws-waf-ip-restriction-rule-group/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/yicr/aws-waf-ip-restriction-rule-group?sort=semver&style=flat-square)](https://github.com/yicr/aws-waf-ip-restriction-rule-group/releases)

# AWS WAF(V2) IP Restriction Rule Group

This is an AWS CDK Construct for IP Restriction Rule Group on WAF V2

## Resources

This construct creating resource list.

* WAF V2 RuleGroup

## Install

### TypeScript

```shell
npm install @gammarer/aws-waf-ip-restriction-rule-group
# or
yarn add @gammarer/aws-waf-ip-restriction-rule-group
```

### Python

```shell
pip install gammarer.aws-waf-ip-restriction-rule-group
```

### Java

Add the following to pom.xml:

```xml
<dependency>
  <groupId>com.gammarer</groupId>
  <artifactId>aws-waf-ip-restriction-rule-group</artifactId>
</dependency>
```

## Example

```python
import { WafIpRestrictRuleGroup } from '@gammarer/aws-waf-ip-restriction-rule-group';

declare const allowIpSet: waf.CfnIPSet;

new WafIpRestrictRuleGroup(stack, 'WafIpRestrictRuleGroup', {
  scope: Scope.GLOBAL, // GLOBAL(CloudFront) or REIGONAL(Application Load Balancer (ALB), Amazon API Gateway REST API, an AWS AppSync GraphQL API, or an Amazon Cognito user pool)
  allowIpSetArn: allowIpSet.attrArn,
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

import aws_cdk.aws_wafv2 as _aws_cdk_aws_wafv2_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@gammarer/aws-waf-ip-restriction-rule-group.Scope")
class Scope(enum.Enum):
    GLOBAL = "GLOBAL"
    REGIONAL = "REGIONAL"


class WafIpRestrictRuleGroup(
    _aws_cdk_aws_wafv2_ceddda9d.CfnRuleGroup,
    metaclass=jsii.JSIIMeta,
    jsii_type="@gammarer/aws-waf-ip-restriction-rule-group.WafIpRestrictRuleGroup",
):
    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allow_ip_set_arn: builtins.str,
        scope: Scope,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope_: Specifies whether this is for an Amazon CloudFront distribution or for a regional application. A regional application can be an Application Load Balancer (ALB), an Amazon API Gateway REST API, an AWS AppSync GraphQL API, an Amazon Cognito user pool, or an AWS App Runner service. Valid Values are ``CLOUDFRONT`` and ``REGIONAL`` . .. epigraph:: For ``CLOUDFRONT`` , you must create your WAFv2 resources in the US East (N. Virginia) Region, ``us-east-1`` .
        :param id: -
        :param allow_ip_set_arn: 
        :param scope: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4aedf70627727742f817cb5449b6529af143bb3ac85d5b10dd95a2291fcf734)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WafIpRestrictRuleGroupProps(
            allow_ip_set_arn=allow_ip_set_arn, scope=scope, name=name
        )

        jsii.create(self.__class__, self, [scope_, id, props])


@jsii.data_type(
    jsii_type="@gammarer/aws-waf-ip-restriction-rule-group.WafIpRestrictRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "allow_ip_set_arn": "allowIpSetArn",
        "scope": "scope",
        "name": "name",
    },
)
class WafIpRestrictRuleGroupProps:
    def __init__(
        self,
        *,
        allow_ip_set_arn: builtins.str,
        scope: Scope,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow_ip_set_arn: 
        :param scope: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97065e2e59277dc5a965a7e0ea460b80f0de2d5a48e8e1ab1a15a21965411093)
            check_type(argname="argument allow_ip_set_arn", value=allow_ip_set_arn, expected_type=type_hints["allow_ip_set_arn"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "allow_ip_set_arn": allow_ip_set_arn,
            "scope": scope,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def allow_ip_set_arn(self) -> builtins.str:
        result = self._values.get("allow_ip_set_arn")
        assert result is not None, "Required property 'allow_ip_set_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scope(self) -> Scope:
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(Scope, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WafIpRestrictRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Scope",
    "WafIpRestrictRuleGroup",
    "WafIpRestrictRuleGroupProps",
]

publication.publish()

def _typecheckingstub__c4aedf70627727742f817cb5449b6529af143bb3ac85d5b10dd95a2291fcf734(
    scope_: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allow_ip_set_arn: builtins.str,
    scope: Scope,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97065e2e59277dc5a965a7e0ea460b80f0de2d5a48e8e1ab1a15a21965411093(
    *,
    allow_ip_set_arn: builtins.str,
    scope: Scope,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
