'''
# `provider`

Refer to the Terraform Registory for docs: [`proxmox`](https://www.terraform.io/docs/providers/proxmox).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class ProxmoxProvider(
    _cdktf_9a9027ec.TerraformProvider,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.provider.ProxmoxProvider",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/proxmox proxmox}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        endpoint: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/proxmox proxmox} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param endpoint: Proxmox endpoint to connect with. **Ex ``https://10.0.0.2:8006``**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#endpoint ProxmoxProvider#endpoint}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#alias ProxmoxProvider#alias}
        :param api_key: A proxmox api key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#api_key ProxmoxProvider#api_key}
        :param insecure: Skip TLS verification. Defaults to true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#insecure ProxmoxProvider#insecure}
        :param password: Password for specified user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#password ProxmoxProvider#password}
        :param username: The username to use for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#username ProxmoxProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__935349c4134b20b623d82f84dbd0b73c66d30e5de863c8c61fc2f928743e9151)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ProxmoxProviderConfig(
            endpoint=endpoint,
            alias=alias,
            api_key=api_key,
            insecure=insecure,
            password=password,
            username=username,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAlias")
    def reset_alias(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlias", []))

    @jsii.member(jsii_name="resetApiKey")
    def reset_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKey", []))

    @jsii.member(jsii_name="resetInsecure")
    def reset_insecure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInsecure", []))

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetUsername")
    def reset_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUsername", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="aliasInput")
    def alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aliasInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyInput")
    def api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="insecureInput")
    def insecure_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecureInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alias"))

    @alias.setter
    def alias(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b58fbe4ea0f4c7df0c885545037d6a55c03bd79ec2b51082d6d3cc595ffff43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alias", value)

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiKey"))

    @api_key.setter
    def api_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40a53b3738eb9398e965f4f022d581824dc5194b6333be09be8de87a0809120a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKey", value)

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b7ff5f92055d358ed75ad4eb268e436e9e503418a5efb443d1285807fb7d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value)

    @builtins.property
    @jsii.member(jsii_name="insecure")
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "insecure"))

    @insecure.setter
    def insecure(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__327e8259723c2c6760aceb27aa16ae92f8434d4514bd4cb3e6eae81da383131c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "insecure", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "password"))

    @password.setter
    def password(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0b3afb26011b895533fe1ddf2483cb23534fb6c252da1a67bc95005ee7d380)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "username"))

    @username.setter
    def username(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__918dbdb56c33f11db245d3fd6b9a7e42b42b92a3cab3c9835d6d859f52d23624)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.provider.ProxmoxProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint": "endpoint",
        "alias": "alias",
        "api_key": "apiKey",
        "insecure": "insecure",
        "password": "password",
        "username": "username",
    },
)
class ProxmoxProviderConfig:
    def __init__(
        self,
        *,
        endpoint: builtins.str,
        alias: typing.Optional[builtins.str] = None,
        api_key: typing.Optional[builtins.str] = None,
        insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        password: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param endpoint: Proxmox endpoint to connect with. **Ex ``https://10.0.0.2:8006``**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#endpoint ProxmoxProvider#endpoint}
        :param alias: Alias name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#alias ProxmoxProvider#alias}
        :param api_key: A proxmox api key. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#api_key ProxmoxProvider#api_key}
        :param insecure: Skip TLS verification. Defaults to true. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#insecure ProxmoxProvider#insecure}
        :param password: Password for specified user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#password ProxmoxProvider#password}
        :param username: The username to use for authentication. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#username ProxmoxProvider#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d367ba6e73a25ffd6e9b3aa130b6174c5be5c1258936c651d58a1e3a6820038)
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument alias", value=alias, expected_type=type_hints["alias"])
            check_type(argname="argument api_key", value=api_key, expected_type=type_hints["api_key"])
            check_type(argname="argument insecure", value=insecure, expected_type=type_hints["insecure"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint": endpoint,
        }
        if alias is not None:
            self._values["alias"] = alias
        if api_key is not None:
            self._values["api_key"] = api_key
        if insecure is not None:
            self._values["insecure"] = insecure
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def endpoint(self) -> builtins.str:
        '''Proxmox endpoint to connect with. **Ex ``https://10.0.0.2:8006``**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#endpoint ProxmoxProvider#endpoint}
        '''
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias(self) -> typing.Optional[builtins.str]:
        '''Alias name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#alias ProxmoxProvider#alias}
        '''
        result = self._values.get("alias")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_key(self) -> typing.Optional[builtins.str]:
        '''A proxmox api key.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#api_key ProxmoxProvider#api_key}
        '''
        result = self._values.get("api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def insecure(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Skip TLS verification. Defaults to true.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#insecure ProxmoxProvider#insecure}
        '''
        result = self._values.get("insecure")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''Password for specified user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#password ProxmoxProvider#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        '''The username to use for authentication.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox#username ProxmoxProvider#username}
        '''
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProxmoxProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ProxmoxProvider",
    "ProxmoxProviderConfig",
]

publication.publish()

def _typecheckingstub__935349c4134b20b623d82f84dbd0b73c66d30e5de863c8c61fc2f928743e9151(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    endpoint: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b58fbe4ea0f4c7df0c885545037d6a55c03bd79ec2b51082d6d3cc595ffff43(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a53b3738eb9398e965f4f022d581824dc5194b6333be09be8de87a0809120a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b7ff5f92055d358ed75ad4eb268e436e9e503418a5efb443d1285807fb7d08(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__327e8259723c2c6760aceb27aa16ae92f8434d4514bd4cb3e6eae81da383131c(
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0b3afb26011b895533fe1ddf2483cb23534fb6c252da1a67bc95005ee7d380(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__918dbdb56c33f11db245d3fd6b9a7e42b42b92a3cab3c9835d6d859f52d23624(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d367ba6e73a25ffd6e9b3aa130b6174c5be5c1258936c651d58a1e3a6820038(
    *,
    endpoint: builtins.str,
    alias: typing.Optional[builtins.str] = None,
    api_key: typing.Optional[builtins.str] = None,
    insecure: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
