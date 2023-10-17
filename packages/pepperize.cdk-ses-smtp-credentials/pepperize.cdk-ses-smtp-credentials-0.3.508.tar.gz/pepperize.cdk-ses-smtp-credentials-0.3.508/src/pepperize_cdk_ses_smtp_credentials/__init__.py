'''
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://makeapullrequest.com)
[![GitHub](https://img.shields.io/github/license/pepperize/cdk-ses-smtp-credentials?style=flat-square)](https://github.com/pepperize/cdk-ses-smtp-credentials/blob/main/LICENSE)
[![npm (scoped)](https://img.shields.io/npm/v/@pepperize/cdk-ses-smtp-credentials?style=flat-square)](https://www.npmjs.com/package/@pepperize/cdk-ses-smtp-credentials)
[![PyPI](https://img.shields.io/pypi/v/pepperize.cdk-ses-smtp-credentials?style=flat-square)](https://pypi.org/project/pepperize.cdk-ses-smtp-credentials/)
[![Nuget](https://img.shields.io/nuget/v/Pepperize.CDK.SesSmtpCredentials?style=flat-square)](https://www.nuget.org/packages/Pepperize.CDK.SesSmtpCredentials/)
[![Sonatype Nexus (Releases)](https://img.shields.io/nexus/r/com.pepperize/cdk-ses-smtp-credentials?server=https%3A%2F%2Fs01.oss.sonatype.org%2F&style=flat-square)](https://s01.oss.sonatype.org/content/repositories/releases/com/pepperize/cdk-ses-smtp-credentials/)
[![GitHub Workflow Status (branch)](https://img.shields.io/github/actions/workflow/status/pepperize/cdk-ses-smtp-credentials/release.yml?branch=main&label=release&style=flat-square)](https://github.com/pepperize/cdk-ses-smtp-credentials/actions/workflows/release.yml)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/pepperize/cdk-ses-smtp-credentials?sort=semver&style=flat-square)](https://github.com/pepperize/cdk-ses-smtp-credentials/releases)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod&style=flat-square)](https://gitpod.io/#https://github.com/pepperize/cdk-ses-smtp-credentials)

# AWS CDK Ses Smtp Credentials

Generate SES smtp credentials for a user and store the credentials in a SecretsManager Secret.

[![View on Construct Hub](https://constructs.dev/badge?package=%40pepperize%2Fcdk-ses-smtp-credentials)](https://constructs.dev/packages/@pepperize/cdk-ses-smtp-credentials)

## Install

### TypeScript

```shell
npm install @pepperize/cdk-ses-smtp-credentials
```

or

```shell
yarn add @pepperize/cdk-ses-smtp-credentials
```

### Python

```shell
pip install pepperize.cdk-ses-smtp-credentials
```

### C# / .Net

```
dotnet add package Pepperize.CDK.SesSmtpCredentials
```

### Java

```xml
<dependency>
  <groupId>com.pepperize</groupId>
  <artifactId>cdk-ses-smtp-credentials</artifactId>
  <version>${cdkSesSmtpCredentials.version}</version>
</dependency>
```

## Usage

```shell
npm install @pepperize/cdk-ses-smtp-credentials
```

See [API.md](https://github.com/pepperize/cdk-ses-smtp-credentials/blob/main/API.md).

### Create AWS SES Smtp Credentials for a given user

> Attaches an inline policy to the user allowing to send emails

```python
import { User } from "@aws-cdk/aws-iam";
import { SesSmtpCredentials } from "@pepperize/cdk-ses-smtp-credentials";

const user = new User(stack, "SesUser", {
  userName: "ses-user",
});
const smtpCredentials = new SesSmtpCredentials(this, "SmtpCredentials", {
  user: user,
});

// smtpCredentials.secret contains json value {username: "<the generated access key id>", password: "<the calculated ses smtp password>"}
```

See [API Reference - SesSmtpCredentials](https://github.com/pepperize/cdk-ses-smtp-credentials/blob/main/API.md#sessmtpcredentials-)

### Create AWS SES Smtp Credentials and create a new user

> Attaches an inline policy to the user allowing to send emails

```python
import { User } from "@aws-cdk/aws-iam";
import { SesSmtpCredentials } from "@pepperize/cdk-ses-smtp-credentials";

const smtpCredentials = new SesSmtpCredentials(this, "SmtpCredentials", {
  userName: "ses-user",
});

// smtpCredentials.secret contains json value {username: "<the generated access key id>", password: "<the calculated ses smtp password>"}
```

See [API Reference - SesSmtpCredentials](https://github.com/pepperize/cdk-ses-smtp-credentials/blob/main/API.md#sessmtpcredentials-)

### Calculate the AWS SES Smtp password on your own

```python
import * as AWS from "aws-sdk";
import { calculateSesSmtpPassword } from "@pepperize/cdk-ses-smtp-credentials";

const iam = new AWS.IAM();
const accessKey = await iam
  .createAccessKey({
    UserName: username,
  })
  .promise();
const accessKeyId = accessKey.AccessKey.AccessKeyId;
const secretAccessKey = accessKey.AccessKey.SecretAccessKey;

const password = calculateSesSmtpPassword(secretAccessKey, "us-east-1");

console.log({
  username: accessKeyId,
  password: password,
});
```

See [Obtaining Amazon SES SMTP credentials by converting existing AWS credentials](https://docs.aws.amazon.com/ses/latest/dg/smtp-credentials.html#smtp-credentials-convert)
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@pepperize/cdk-ses-smtp-credentials.Credentials")
class Credentials(enum.Enum):
    USERNAME = "USERNAME"
    '''The key of the username stored in the secretsmanager key/value json.'''
    PASSWORD = "PASSWORD"
    '''The key of the password stored in the secretsmanager key/value json.'''


class SesSmtpCredentials(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@pepperize/cdk-ses-smtp-credentials.SesSmtpCredentials",
):
    '''This construct creates an access key for the given user and stores the generated SMTP credentials inside a secret.

    Attaches an inline policy to the user allowing to send emails Example::

       const user = User.fromUserName("ses-user-example");
       const credentials = new SesSmtpCredentials(this, 'SmtpCredentials', {
            user: user,
       });
       // smtpCredentials.secret contains json value {username: "<the generated access key id>", password: "<the calculated ses smtp password>"}
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        user: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IUser] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param secret: Optional, an SecretsManager secret to write the AWS SES Smtp credentials to.
        :param user: The user for which to create an AWS Access Key and to generate the smtp password. If omitted a user will be created.
        :param user_name: Optional, a username to create a new user if no existing user is given.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88139012bdf8dfca1a9503eed2c739958e2a41e5e43343b37d2d5a91b58f8f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SesSmtpCredentialsProps(secret=secret, user=user, user_name=user_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The secret that contains the calculated AWS SES Smtp Credentials.

        Example::

           import { aws_ecs } from "aws-cdk-lib";

           const containerDefinitionOptions: aws_ecs.ContainerDefinitionOptions = {
                // ...
                secrets: {
                    MAIL_USERNAME: aws_ecs.Secret.fromSecretsManager(smtpCredentials.secret, "username"),
                    MAIL_PASSWORD: aws_ecs.Secret.fromSecretsManager(smtpCredentials.secret, "password"),
                }
           }
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "secret"))


@jsii.data_type(
    jsii_type="@pepperize/cdk-ses-smtp-credentials.SesSmtpCredentialsProps",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "user": "user", "user_name": "userName"},
)
class SesSmtpCredentialsProps:
    def __init__(
        self,
        *,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        user: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IUser] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param secret: Optional, an SecretsManager secret to write the AWS SES Smtp credentials to.
        :param user: The user for which to create an AWS Access Key and to generate the smtp password. If omitted a user will be created.
        :param user_name: Optional, a username to create a new user if no existing user is given.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8b7861fea08667d22dd102307f69c34104ff37d237ea1ef79e79294fd79cc04)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if secret is not None:
            self._values["secret"] = secret
        if user is not None:
            self._values["user"] = user
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''Optional, an SecretsManager secret to write the AWS SES Smtp credentials to.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    @builtins.property
    def user(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IUser]:
        '''The user for which to create an AWS Access Key and to generate the smtp password.

        If omitted a user will be created.
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IUser], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''Optional, a username to create a new user if no existing user is given.'''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SesSmtpCredentialsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Credentials",
    "SesSmtpCredentials",
    "SesSmtpCredentialsProps",
]

publication.publish()

def _typecheckingstub__b88139012bdf8dfca1a9503eed2c739958e2a41e5e43343b37d2d5a91b58f8f7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    user: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IUser] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8b7861fea08667d22dd102307f69c34104ff37d237ea1ef79e79294fd79cc04(
    *,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    user: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IUser] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
