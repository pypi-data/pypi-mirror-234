'''
# `proxmox_network_bond`

Refer to the Terraform Registory for docs: [`proxmox_network_bond`](https://www.terraform.io/docs/providers/proxmox/r/network_bond).
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


class NetworkBond(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.networkBond.NetworkBond",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond proxmox_network_bond}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        interfaces: typing.Sequence[builtins.str],
        mode: builtins.str,
        node_attribute: builtins.str,
        autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bond_primary: typing.Optional[builtins.str] = None,
        comments: typing.Optional[builtins.str] = None,
        hash_policy: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[typing.Union[typing.Union["NetworkBondIpv4", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_gateway: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[typing.Union[typing.Union["NetworkBondIpv6", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv6_gateway: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond proxmox_network_bond} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param interfaces: List of interfaces on the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#interfaces NetworkBond#interfaces}
        :param mode: Mode of the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#mode NetworkBond#mode}
        :param node_attribute: The node the bond is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#node NetworkBond#node}
        :param autostart: If the bond is set to autostart. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#autostart NetworkBond#autostart}
        :param bond_primary: Primary interface on the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#bond_primary NetworkBond#bond_primary}
        :param comments: Comment in the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#comments NetworkBond#comments}
        :param hash_policy: Hash policy used on the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#hash_policy NetworkBond#hash_policy}
        :param ipv4: Information of the ipv4 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv4 NetworkBond#ipv4}
        :param ipv4_gateway: The ipv4 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv4_gateway NetworkBond#ipv4_gateway}
        :param ipv6: Information of the ipv6 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv6 NetworkBond#ipv6}
        :param ipv6_gateway: The ipv6 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv6_gateway NetworkBond#ipv6_gateway}
        :param name: The name of the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#name NetworkBond#name}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8466746a459dae9eb8155a2b8f67cbb15b5d2fa049fef2735a684e57c7415c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = NetworkBondConfig(
            interfaces=interfaces,
            mode=mode,
            node_attribute=node_attribute,
            autostart=autostart,
            bond_primary=bond_primary,
            comments=comments,
            hash_policy=hash_policy,
            ipv4=ipv4,
            ipv4_gateway=ipv4_gateway,
            ipv6=ipv6,
            ipv6_gateway=ipv6_gateway,
            name=name,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetAutostart")
    def reset_autostart(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutostart", []))

    @jsii.member(jsii_name="resetBondPrimary")
    def reset_bond_primary(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBondPrimary", []))

    @jsii.member(jsii_name="resetComments")
    def reset_comments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComments", []))

    @jsii.member(jsii_name="resetHashPolicy")
    def reset_hash_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHashPolicy", []))

    @jsii.member(jsii_name="resetIpv4")
    def reset_ipv4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4", []))

    @jsii.member(jsii_name="resetIpv4Gateway")
    def reset_ipv4_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Gateway", []))

    @jsii.member(jsii_name="resetIpv6")
    def reset_ipv6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6", []))

    @jsii.member(jsii_name="resetIpv6Gateway")
    def reset_ipv6_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Gateway", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "active"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="miiMon")
    def mii_mon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "miiMon"))

    @builtins.property
    @jsii.member(jsii_name="autostartInput")
    def autostart_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autostartInput"))

    @builtins.property
    @jsii.member(jsii_name="bondPrimaryInput")
    def bond_primary_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bondPrimaryInput"))

    @builtins.property
    @jsii.member(jsii_name="commentsInput")
    def comments_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentsInput"))

    @builtins.property
    @jsii.member(jsii_name="hashPolicyInput")
    def hash_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hashPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="interfacesInput")
    def interfaces_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "interfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4GatewayInput")
    def ipv4_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Input")
    def ipv4_input(
        self,
    ) -> typing.Optional[typing.Union["NetworkBondIpv4", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["NetworkBondIpv4", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6GatewayInput")
    def ipv6_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(
        self,
    ) -> typing.Optional[typing.Union["NetworkBondIpv6", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["NetworkBondIpv6", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAttributeInput")
    def node_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="autostart")
    def autostart(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autostart"))

    @autostart.setter
    def autostart(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d897f91555ab7c965af0275eee1fa379ce604c07454c343d2abf957cd017f551)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autostart", value)

    @builtins.property
    @jsii.member(jsii_name="bondPrimary")
    def bond_primary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bondPrimary"))

    @bond_primary.setter
    def bond_primary(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8786199ccd54667db25b33a55238478407116045027ed7de605199c2f6605518)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bondPrimary", value)

    @builtins.property
    @jsii.member(jsii_name="comments")
    def comments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comments"))

    @comments.setter
    def comments(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95e7674947523d918ebd943907abc8be98044390dcfe58f9a6f88938ab63f634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comments", value)

    @builtins.property
    @jsii.member(jsii_name="hashPolicy")
    def hash_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashPolicy"))

    @hash_policy.setter
    def hash_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c90649ecdc1b59b1f4d91283106925b431b23d5efe3b6f194c3103358c17e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hashPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="interfaces")
    def interfaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "interfaces"))

    @interfaces.setter
    def interfaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__116c4a206da1e5d5d1b08c43edac164e58f7c1e56fb785fd5ff8c0f4cd922507)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaces", value)

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> typing.Union["NetworkBondIpv4", _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union["NetworkBondIpv4", _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv4"))

    @ipv4.setter
    def ipv4(
        self,
        value: typing.Union["NetworkBondIpv4", _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79233783b076ffea8ca16baaebb0aa208c85cd242e92ff137ae86b5db6c0df3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4", value)

    @builtins.property
    @jsii.member(jsii_name="ipv4Gateway")
    def ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Gateway"))

    @ipv4_gateway.setter
    def ipv4_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ad8b734e882d22f7e75defd5b4955034efc3661f802fbf6a3328825a170a47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> typing.Union["NetworkBondIpv6", _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union["NetworkBondIpv6", _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv6"))

    @ipv6.setter
    def ipv6(
        self,
        value: typing.Union["NetworkBondIpv6", _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4990775a8ff089a046f8ddb2ea48966d540cbe4c3921f5c1cf3a877c07e446e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6Gateway")
    def ipv6_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Gateway"))

    @ipv6_gateway.setter
    def ipv6_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e9a222993e29ba1590bdd3dfa73a1661c254c629285ff8cd4d7b19ac3f473f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4de6ea3dcfdebe88bf5ee8b3c7831d34bb2ce73500d91c9f44326634a467b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bed141f59370ed245b4fcecc8947842a3a8a747b467d11d3e3dc8114f37eb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeAttribute")
    def node_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeAttribute"))

    @node_attribute.setter
    def node_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc94df96431110542ef14e60c60d2c35f66231c5f78b2eb94c858766c969d1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeAttribute", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.networkBond.NetworkBondConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "interfaces": "interfaces",
        "mode": "mode",
        "node_attribute": "nodeAttribute",
        "autostart": "autostart",
        "bond_primary": "bondPrimary",
        "comments": "comments",
        "hash_policy": "hashPolicy",
        "ipv4": "ipv4",
        "ipv4_gateway": "ipv4Gateway",
        "ipv6": "ipv6",
        "ipv6_gateway": "ipv6Gateway",
        "name": "name",
    },
)
class NetworkBondConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        interfaces: typing.Sequence[builtins.str],
        mode: builtins.str,
        node_attribute: builtins.str,
        autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        bond_primary: typing.Optional[builtins.str] = None,
        comments: typing.Optional[builtins.str] = None,
        hash_policy: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[typing.Union[typing.Union["NetworkBondIpv4", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_gateway: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[typing.Union[typing.Union["NetworkBondIpv6", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv6_gateway: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param interfaces: List of interfaces on the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#interfaces NetworkBond#interfaces}
        :param mode: Mode of the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#mode NetworkBond#mode}
        :param node_attribute: The node the bond is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#node NetworkBond#node}
        :param autostart: If the bond is set to autostart. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#autostart NetworkBond#autostart}
        :param bond_primary: Primary interface on the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#bond_primary NetworkBond#bond_primary}
        :param comments: Comment in the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#comments NetworkBond#comments}
        :param hash_policy: Hash policy used on the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#hash_policy NetworkBond#hash_policy}
        :param ipv4: Information of the ipv4 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv4 NetworkBond#ipv4}
        :param ipv4_gateway: The ipv4 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv4_gateway NetworkBond#ipv4_gateway}
        :param ipv6: Information of the ipv6 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv6 NetworkBond#ipv6}
        :param ipv6_gateway: The ipv6 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv6_gateway NetworkBond#ipv6_gateway}
        :param name: The name of the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#name NetworkBond#name}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922043a450a081b713a22466ddc11526a75080d57e8b2ffe045b22956f9add25)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument interfaces", value=interfaces, expected_type=type_hints["interfaces"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument node_attribute", value=node_attribute, expected_type=type_hints["node_attribute"])
            check_type(argname="argument autostart", value=autostart, expected_type=type_hints["autostart"])
            check_type(argname="argument bond_primary", value=bond_primary, expected_type=type_hints["bond_primary"])
            check_type(argname="argument comments", value=comments, expected_type=type_hints["comments"])
            check_type(argname="argument hash_policy", value=hash_policy, expected_type=type_hints["hash_policy"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv4_gateway", value=ipv4_gateway, expected_type=type_hints["ipv4_gateway"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument ipv6_gateway", value=ipv6_gateway, expected_type=type_hints["ipv6_gateway"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interfaces": interfaces,
            "mode": mode,
            "node_attribute": node_attribute,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if autostart is not None:
            self._values["autostart"] = autostart
        if bond_primary is not None:
            self._values["bond_primary"] = bond_primary
        if comments is not None:
            self._values["comments"] = comments
        if hash_policy is not None:
            self._values["hash_policy"] = hash_policy
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv4_gateway is not None:
            self._values["ipv4_gateway"] = ipv4_gateway
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if ipv6_gateway is not None:
            self._values["ipv6_gateway"] = ipv6_gateway
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def interfaces(self) -> typing.List[builtins.str]:
        '''List of interfaces on the bond.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#interfaces NetworkBond#interfaces}
        '''
        result = self._values.get("interfaces")
        assert result is not None, "Required property 'interfaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''Mode of the bond.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#mode NetworkBond#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_attribute(self) -> builtins.str:
        '''The node the bond is on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#node NetworkBond#node}
        '''
        result = self._values.get("node_attribute")
        assert result is not None, "Required property 'node_attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autostart(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the bond is set to autostart.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#autostart NetworkBond#autostart}
        '''
        result = self._values.get("autostart")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bond_primary(self) -> typing.Optional[builtins.str]:
        '''Primary interface on the bond.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#bond_primary NetworkBond#bond_primary}
        '''
        result = self._values.get("bond_primary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def comments(self) -> typing.Optional[builtins.str]:
        '''Comment in the bond.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#comments NetworkBond#comments}
        '''
        result = self._values.get("comments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hash_policy(self) -> typing.Optional[builtins.str]:
        '''Hash policy used on the bond.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#hash_policy NetworkBond#hash_policy}
        '''
        result = self._values.get("hash_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4(
        self,
    ) -> typing.Optional[typing.Union["NetworkBondIpv4", _cdktf_9a9027ec.IResolvable]]:
        '''Information of the ipv4 address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv4 NetworkBond#ipv4}
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[typing.Union["NetworkBondIpv4", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv4_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv4 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv4_gateway NetworkBond#ipv4_gateway}
        '''
        result = self._values.get("ipv4_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6(
        self,
    ) -> typing.Optional[typing.Union["NetworkBondIpv6", _cdktf_9a9027ec.IResolvable]]:
        '''Information of the ipv6 address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv6 NetworkBond#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[typing.Union["NetworkBondIpv6", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv6_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv6 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#ipv6_gateway NetworkBond#ipv6_gateway}
        '''
        result = self._values.get("ipv6_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bond.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#name NetworkBond#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkBondConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.networkBond.NetworkBondIpv4",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "netmask": "netmask"},
)
class NetworkBondIpv4:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#address NetworkBond#address}.
        :param netmask: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#netmask NetworkBond#netmask}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5c16b7cc9bec5e75e61e9048b0f235252a70f21c84aa29e3ad322e38db39384)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#address NetworkBond#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#netmask NetworkBond#netmask}.'''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkBondIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkBondIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.networkBond.NetworkBondIpv4OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ec541e9247d2f3af1df8f82655b3e5b7d99d9d7503b5332faad451baf7842c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetNetmask")
    def reset_netmask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetmask", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="netmaskInput")
    def netmask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netmaskInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b35ed636e2ca12ee175dd720fc67ccf4c510f529115795e476ea1140b4c9fc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fee25af61123956c6b40fff897803e844db491e79c2c55642f3be4b40fe64fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetworkBondIpv4, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetworkBondIpv4, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetworkBondIpv4, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad6e5183ba822baefcd24565dd322aa24d594318e38e29b3bd06c65331d0fa3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.networkBond.NetworkBondIpv6",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "netmask": "netmask"},
)
class NetworkBondIpv6:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#address NetworkBond#address}.
        :param netmask: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#netmask NetworkBond#netmask}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17371e75ecba0bd33e67c68712c9fba718a92130a494bd58c35641d427e2044)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#address NetworkBond#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bond#netmask NetworkBond#netmask}.'''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkBondIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkBondIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.networkBond.NetworkBondIpv6OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b78a5c405be2d7924bce16ad718f102a95fd45bce093efca8ae5478d446e8a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetNetmask")
    def reset_netmask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetmask", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="netmaskInput")
    def netmask_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "netmaskInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a128c022d7956688d7911207ee728cf46b60324aee064dc3b62b207fe9d7561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a4e559a1995e17c3343ab7a9101992d4968f89e25c4254bf7b5ef62adf1200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetworkBondIpv6, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetworkBondIpv6, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetworkBondIpv6, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59839747a88ccbd868cdd14418d7d0a3798c8508d53919fec83fea0842607483)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetworkBond",
    "NetworkBondConfig",
    "NetworkBondIpv4",
    "NetworkBondIpv4OutputReference",
    "NetworkBondIpv6",
    "NetworkBondIpv6OutputReference",
]

publication.publish()

def _typecheckingstub__3d8466746a459dae9eb8155a2b8f67cbb15b5d2fa049fef2735a684e57c7415c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    interfaces: typing.Sequence[builtins.str],
    mode: builtins.str,
    node_attribute: builtins.str,
    autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bond_primary: typing.Optional[builtins.str] = None,
    comments: typing.Optional[builtins.str] = None,
    hash_policy: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[typing.Union[typing.Union[NetworkBondIpv4, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_gateway: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[typing.Union[typing.Union[NetworkBondIpv6, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv6_gateway: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d897f91555ab7c965af0275eee1fa379ce604c07454c343d2abf957cd017f551(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8786199ccd54667db25b33a55238478407116045027ed7de605199c2f6605518(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95e7674947523d918ebd943907abc8be98044390dcfe58f9a6f88938ab63f634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c90649ecdc1b59b1f4d91283106925b431b23d5efe3b6f194c3103358c17e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__116c4a206da1e5d5d1b08c43edac164e58f7c1e56fb785fd5ff8c0f4cd922507(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79233783b076ffea8ca16baaebb0aa208c85cd242e92ff137ae86b5db6c0df3e(
    value: typing.Union[NetworkBondIpv4, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ad8b734e882d22f7e75defd5b4955034efc3661f802fbf6a3328825a170a47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4990775a8ff089a046f8ddb2ea48966d540cbe4c3921f5c1cf3a877c07e446e(
    value: typing.Union[NetworkBondIpv6, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e9a222993e29ba1590bdd3dfa73a1661c254c629285ff8cd4d7b19ac3f473f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4de6ea3dcfdebe88bf5ee8b3c7831d34bb2ce73500d91c9f44326634a467b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bed141f59370ed245b4fcecc8947842a3a8a747b467d11d3e3dc8114f37eb71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc94df96431110542ef14e60c60d2c35f66231c5f78b2eb94c858766c969d1d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922043a450a081b713a22466ddc11526a75080d57e8b2ffe045b22956f9add25(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interfaces: typing.Sequence[builtins.str],
    mode: builtins.str,
    node_attribute: builtins.str,
    autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    bond_primary: typing.Optional[builtins.str] = None,
    comments: typing.Optional[builtins.str] = None,
    hash_policy: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[typing.Union[typing.Union[NetworkBondIpv4, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_gateway: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[typing.Union[typing.Union[NetworkBondIpv6, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv6_gateway: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5c16b7cc9bec5e75e61e9048b0f235252a70f21c84aa29e3ad322e38db39384(
    *,
    address: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ec541e9247d2f3af1df8f82655b3e5b7d99d9d7503b5332faad451baf7842c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b35ed636e2ca12ee175dd720fc67ccf4c510f529115795e476ea1140b4c9fc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fee25af61123956c6b40fff897803e844db491e79c2c55642f3be4b40fe64fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad6e5183ba822baefcd24565dd322aa24d594318e38e29b3bd06c65331d0fa3(
    value: typing.Optional[typing.Union[NetworkBondIpv4, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17371e75ecba0bd33e67c68712c9fba718a92130a494bd58c35641d427e2044(
    *,
    address: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b78a5c405be2d7924bce16ad718f102a95fd45bce093efca8ae5478d446e8a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a128c022d7956688d7911207ee728cf46b60324aee064dc3b62b207fe9d7561(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a4e559a1995e17c3343ab7a9101992d4968f89e25c4254bf7b5ef62adf1200(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59839747a88ccbd868cdd14418d7d0a3798c8508d53919fec83fea0842607483(
    value: typing.Optional[typing.Union[NetworkBondIpv6, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
