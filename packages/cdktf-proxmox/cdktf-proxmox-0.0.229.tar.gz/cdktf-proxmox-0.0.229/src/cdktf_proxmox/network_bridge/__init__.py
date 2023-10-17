'''
# `proxmox_network_bridge`

Refer to the Terraform Registory for docs: [`proxmox_network_bridge`](https://www.terraform.io/docs/providers/proxmox/r/network_bridge).
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


class NetworkBridge(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.networkBridge.NetworkBridge",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge proxmox_network_bridge}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        interfaces: typing.Sequence[builtins.str],
        node_attribute: builtins.str,
        autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        comments: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[typing.Union[typing.Union["NetworkBridgeIpv4", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_gateway: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[typing.Union[typing.Union["NetworkBridgeIpv6", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv6_gateway: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        vlan_aware: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge proxmox_network_bridge} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param interfaces: List of interfaces on the bridge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#interfaces NetworkBridge#interfaces}
        :param node_attribute: The node the bridge is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#node NetworkBridge#node}
        :param autostart: If the bridge is set to autostart. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#autostart NetworkBridge#autostart}
        :param comments: Comment on the bridge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#comments NetworkBridge#comments}
        :param ipv4: Information of the ipv4 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv4 NetworkBridge#ipv4}
        :param ipv4_gateway: The ipv4 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv4_gateway NetworkBridge#ipv4_gateway}
        :param ipv6: Information of the ipv6 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv6 NetworkBridge#ipv6}
        :param ipv6_gateway: The ipv6 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv6_gateway NetworkBridge#ipv6_gateway}
        :param name: The name of the bridge. Follows the scheme ``vmbr<n>``. If not set, the next available name will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#name NetworkBridge#name}
        :param vlan_aware: If the bridge is vlan aware. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#vlan_aware NetworkBridge#vlan_aware}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19c8b4e5d232f41774ee19e4e45b93cb1e6a021b79182dac65feab4e3fb78a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = NetworkBridgeConfig(
            interfaces=interfaces,
            node_attribute=node_attribute,
            autostart=autostart,
            comments=comments,
            ipv4=ipv4,
            ipv4_gateway=ipv4_gateway,
            ipv6=ipv6,
            ipv6_gateway=ipv6_gateway,
            name=name,
            vlan_aware=vlan_aware,
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

    @jsii.member(jsii_name="resetComments")
    def reset_comments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComments", []))

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

    @jsii.member(jsii_name="resetVlanAware")
    def reset_vlan_aware(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVlanAware", []))

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
    @jsii.member(jsii_name="autostartInput")
    def autostart_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autostartInput"))

    @builtins.property
    @jsii.member(jsii_name="commentsInput")
    def comments_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentsInput"))

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
    ) -> typing.Optional[typing.Union["NetworkBridgeIpv4", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["NetworkBridgeIpv4", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv4Input"))

    @builtins.property
    @jsii.member(jsii_name="ipv6GatewayInput")
    def ipv6_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6Input")
    def ipv6_input(
        self,
    ) -> typing.Optional[typing.Union["NetworkBridgeIpv6", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["NetworkBridgeIpv6", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipv6Input"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAttributeInput")
    def node_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanAwareInput")
    def vlan_aware_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vlanAwareInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__1f2aa28c411311ae72359f9cfd270ab6489f67decc324a51960014c0086b1e98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autostart", value)

    @builtins.property
    @jsii.member(jsii_name="comments")
    def comments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comments"))

    @comments.setter
    def comments(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0ebe1d6f95ceb49ea37b05e5c85a4005eb6a0d86763516f0a5de22aff71a44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comments", value)

    @builtins.property
    @jsii.member(jsii_name="interfaces")
    def interfaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "interfaces"))

    @interfaces.setter
    def interfaces(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8149a680a94b425c5c2a3804cf811dba25b2f9d5af6c5e73818178c8dbf3b9b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaces", value)

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> typing.Union["NetworkBridgeIpv4", _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union["NetworkBridgeIpv4", _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv4"))

    @ipv4.setter
    def ipv4(
        self,
        value: typing.Union["NetworkBridgeIpv4", _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a88e041d3a5c87e6e6788de5864757485c54b800a7ca6ea6b6fcc526aa793c7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4", value)

    @builtins.property
    @jsii.member(jsii_name="ipv4Gateway")
    def ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Gateway"))

    @ipv4_gateway.setter
    def ipv4_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52cfbb2e5de41f9d37f61654d29ac3ba21a4931cfe68ed60cc6d998acf9f36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> typing.Union["NetworkBridgeIpv6", _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union["NetworkBridgeIpv6", _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipv6"))

    @ipv6.setter
    def ipv6(
        self,
        value: typing.Union["NetworkBridgeIpv6", _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc7633ec7e4af1ce76c34d86d2095bf9554cecd38094fb775be61556ee9eae9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6Gateway")
    def ipv6_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Gateway"))

    @ipv6_gateway.setter
    def ipv6_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5fa4bd9b463e013ae8eb6fcfd5266508557f0a428c326a86ac06f24ab56b9ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e4a7df6259e3f4236fac41aa03a9e4926ba781264eca9fbb84865e23874fbe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeAttribute")
    def node_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeAttribute"))

    @node_attribute.setter
    def node_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d125252fe5e299d1ef385c6ef1fdf1c8271362a73ecffcd974cc37e5276ffafa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="vlanAware")
    def vlan_aware(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vlanAware"))

    @vlan_aware.setter
    def vlan_aware(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae4c013f7fb1c9499ab18c6203fcc42cc978e7614cced29d623153b6c02b93f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlanAware", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.networkBridge.NetworkBridgeConfig",
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
        "node_attribute": "nodeAttribute",
        "autostart": "autostart",
        "comments": "comments",
        "ipv4": "ipv4",
        "ipv4_gateway": "ipv4Gateway",
        "ipv6": "ipv6",
        "ipv6_gateway": "ipv6Gateway",
        "name": "name",
        "vlan_aware": "vlanAware",
    },
)
class NetworkBridgeConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        node_attribute: builtins.str,
        autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        comments: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[typing.Union[typing.Union["NetworkBridgeIpv4", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv4_gateway: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[typing.Union[typing.Union["NetworkBridgeIpv6", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ipv6_gateway: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        vlan_aware: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param interfaces: List of interfaces on the bridge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#interfaces NetworkBridge#interfaces}
        :param node_attribute: The node the bridge is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#node NetworkBridge#node}
        :param autostart: If the bridge is set to autostart. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#autostart NetworkBridge#autostart}
        :param comments: Comment on the bridge. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#comments NetworkBridge#comments}
        :param ipv4: Information of the ipv4 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv4 NetworkBridge#ipv4}
        :param ipv4_gateway: The ipv4 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv4_gateway NetworkBridge#ipv4_gateway}
        :param ipv6: Information of the ipv6 address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv6 NetworkBridge#ipv6}
        :param ipv6_gateway: The ipv6 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv6_gateway NetworkBridge#ipv6_gateway}
        :param name: The name of the bridge. Follows the scheme ``vmbr<n>``. If not set, the next available name will be used. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#name NetworkBridge#name}
        :param vlan_aware: If the bridge is vlan aware. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#vlan_aware NetworkBridge#vlan_aware}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cd29d4caab82a85b1b2e341176fdd8375d5349593554f0620b578a44203a6b0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument interfaces", value=interfaces, expected_type=type_hints["interfaces"])
            check_type(argname="argument node_attribute", value=node_attribute, expected_type=type_hints["node_attribute"])
            check_type(argname="argument autostart", value=autostart, expected_type=type_hints["autostart"])
            check_type(argname="argument comments", value=comments, expected_type=type_hints["comments"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv4_gateway", value=ipv4_gateway, expected_type=type_hints["ipv4_gateway"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument ipv6_gateway", value=ipv6_gateway, expected_type=type_hints["ipv6_gateway"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vlan_aware", value=vlan_aware, expected_type=type_hints["vlan_aware"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interfaces": interfaces,
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
        if comments is not None:
            self._values["comments"] = comments
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
        if vlan_aware is not None:
            self._values["vlan_aware"] = vlan_aware

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
        '''List of interfaces on the bridge.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#interfaces NetworkBridge#interfaces}
        '''
        result = self._values.get("interfaces")
        assert result is not None, "Required property 'interfaces' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def node_attribute(self) -> builtins.str:
        '''The node the bridge is on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#node NetworkBridge#node}
        '''
        result = self._values.get("node_attribute")
        assert result is not None, "Required property 'node_attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def autostart(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the bridge is set to autostart.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#autostart NetworkBridge#autostart}
        '''
        result = self._values.get("autostart")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def comments(self) -> typing.Optional[builtins.str]:
        '''Comment on the bridge.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#comments NetworkBridge#comments}
        '''
        result = self._values.get("comments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4(
        self,
    ) -> typing.Optional[typing.Union["NetworkBridgeIpv4", _cdktf_9a9027ec.IResolvable]]:
        '''Information of the ipv4 address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv4 NetworkBridge#ipv4}
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[typing.Union["NetworkBridgeIpv4", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv4_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv4 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv4_gateway NetworkBridge#ipv4_gateway}
        '''
        result = self._values.get("ipv4_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6(
        self,
    ) -> typing.Optional[typing.Union["NetworkBridgeIpv6", _cdktf_9a9027ec.IResolvable]]:
        '''Information of the ipv6 address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv6 NetworkBridge#ipv6}
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[typing.Union["NetworkBridgeIpv6", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ipv6_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv6 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#ipv6_gateway NetworkBridge#ipv6_gateway}
        '''
        result = self._values.get("ipv6_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bridge. Follows the scheme ``vmbr<n>``. If not set, the next available name will be used.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#name NetworkBridge#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vlan_aware(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If the bridge is vlan aware.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#vlan_aware NetworkBridge#vlan_aware}
        '''
        result = self._values.get("vlan_aware")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkBridgeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.networkBridge.NetworkBridgeIpv4",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "netmask": "netmask"},
)
class NetworkBridgeIpv4:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#address NetworkBridge#address}.
        :param netmask: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#netmask NetworkBridge#netmask}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10026c3364bbfda5a757b217bbd4135826a38c1d5abe906c797ca5b8ef477352)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#address NetworkBridge#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#netmask NetworkBridge#netmask}.'''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkBridgeIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkBridgeIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.networkBridge.NetworkBridgeIpv4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc768d5585621ba416f00e474d9ca32aeaaf0970835652bf6399dc8cccdc40a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__67033ca08b4c8f9950845cad902b627c1b0f5c4b32c80df057ba306ed2f36bc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8d0d484c68485b94a45d1c6cede07079e9e13d27bd41a3ed406439956a396d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetworkBridgeIpv4, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetworkBridgeIpv4, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetworkBridgeIpv4, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8131ec16a136f6d30b8980be6b69001f8f6ecf7576042c2c500162686ad40956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.networkBridge.NetworkBridgeIpv6",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "netmask": "netmask"},
)
class NetworkBridgeIpv6:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#address NetworkBridge#address}.
        :param netmask: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#netmask NetworkBridge#netmask}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd7bfd7fb2a391c8d55a1b49e74bf2e6f84f5982db4eeb7fc2ae30c94ef86b0)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#address NetworkBridge#address}.'''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/network_bridge#netmask NetworkBridge#netmask}.'''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkBridgeIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkBridgeIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.networkBridge.NetworkBridgeIpv6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02a3cec045712c9f68f596a91360a7488623674e6b3529553a1f85efae4438a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9606575b6af7e29bbf3b1246efc8728b92a8afb8085a953da094b60b51b7a7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd2ed85e487d080ad2b8e7959fbb4fe46ef255c4bd782f8119e6fe571e650918)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetworkBridgeIpv6, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetworkBridgeIpv6, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetworkBridgeIpv6, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98bb4975b10819e6017ab7437c711d8cc0a11867a8594c06f5e5a1deef81a10d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetworkBridge",
    "NetworkBridgeConfig",
    "NetworkBridgeIpv4",
    "NetworkBridgeIpv4OutputReference",
    "NetworkBridgeIpv6",
    "NetworkBridgeIpv6OutputReference",
]

publication.publish()

def _typecheckingstub__a19c8b4e5d232f41774ee19e4e45b93cb1e6a021b79182dac65feab4e3fb78a3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    interfaces: typing.Sequence[builtins.str],
    node_attribute: builtins.str,
    autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    comments: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[typing.Union[typing.Union[NetworkBridgeIpv4, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_gateway: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[typing.Union[typing.Union[NetworkBridgeIpv6, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv6_gateway: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    vlan_aware: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__1f2aa28c411311ae72359f9cfd270ab6489f67decc324a51960014c0086b1e98(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0ebe1d6f95ceb49ea37b05e5c85a4005eb6a0d86763516f0a5de22aff71a44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8149a680a94b425c5c2a3804cf811dba25b2f9d5af6c5e73818178c8dbf3b9b7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a88e041d3a5c87e6e6788de5864757485c54b800a7ca6ea6b6fcc526aa793c7b(
    value: typing.Union[NetworkBridgeIpv4, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52cfbb2e5de41f9d37f61654d29ac3ba21a4931cfe68ed60cc6d998acf9f36c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc7633ec7e4af1ce76c34d86d2095bf9554cecd38094fb775be61556ee9eae9(
    value: typing.Union[NetworkBridgeIpv6, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5fa4bd9b463e013ae8eb6fcfd5266508557f0a428c326a86ac06f24ab56b9ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e4a7df6259e3f4236fac41aa03a9e4926ba781264eca9fbb84865e23874fbe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d125252fe5e299d1ef385c6ef1fdf1c8271362a73ecffcd974cc37e5276ffafa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae4c013f7fb1c9499ab18c6203fcc42cc978e7614cced29d623153b6c02b93f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cd29d4caab82a85b1b2e341176fdd8375d5349593554f0620b578a44203a6b0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    interfaces: typing.Sequence[builtins.str],
    node_attribute: builtins.str,
    autostart: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    comments: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[typing.Union[typing.Union[NetworkBridgeIpv4, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv4_gateway: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[typing.Union[typing.Union[NetworkBridgeIpv6, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ipv6_gateway: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    vlan_aware: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10026c3364bbfda5a757b217bbd4135826a38c1d5abe906c797ca5b8ef477352(
    *,
    address: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc768d5585621ba416f00e474d9ca32aeaaf0970835652bf6399dc8cccdc40a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67033ca08b4c8f9950845cad902b627c1b0f5c4b32c80df057ba306ed2f36bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8d0d484c68485b94a45d1c6cede07079e9e13d27bd41a3ed406439956a396d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8131ec16a136f6d30b8980be6b69001f8f6ecf7576042c2c500162686ad40956(
    value: typing.Optional[typing.Union[NetworkBridgeIpv4, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd7bfd7fb2a391c8d55a1b49e74bf2e6f84f5982db4eeb7fc2ae30c94ef86b0(
    *,
    address: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02a3cec045712c9f68f596a91360a7488623674e6b3529553a1f85efae4438a6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9606575b6af7e29bbf3b1246efc8728b92a8afb8085a953da094b60b51b7a7e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd2ed85e487d080ad2b8e7959fbb4fe46ef255c4bd782f8119e6fe571e650918(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98bb4975b10819e6017ab7437c711d8cc0a11867a8594c06f5e5a1deef81a10d(
    value: typing.Optional[typing.Union[NetworkBridgeIpv6, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
