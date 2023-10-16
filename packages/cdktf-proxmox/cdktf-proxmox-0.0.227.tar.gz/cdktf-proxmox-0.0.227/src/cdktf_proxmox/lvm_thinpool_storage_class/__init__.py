'''
# `proxmox_lvm_thinpool_storage_class`

Refer to the Terraform Registory for docs: [`proxmox_lvm_thinpool_storage_class`](https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class).
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


class LvmThinpoolStorageClass(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.lvmThinpoolStorageClass.LvmThinpoolStorageClass",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class proxmox_lvm_thinpool_storage_class}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        id: builtins.str,
        thinpool: builtins.str,
        volume_group: builtins.str,
        content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class proxmox_lvm_thinpool_storage_class} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param id: The identifier of the storage class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#id LvmThinpoolStorageClass#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param thinpool: The LVM thinpool that should be implemented by each node. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#thinpool LvmThinpoolStorageClass#thinpool}
        :param volume_group: The associated volume group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#volume_group LvmThinpoolStorageClass#volume_group}
        :param content_types: The content types that can be stored on this storage class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#content_types LvmThinpoolStorageClass#content_types}
        :param nodes: Nodes that implement this storage class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#nodes LvmThinpoolStorageClass#nodes}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f28eb29ecc7cdd9803e2ecd9257f256b04fb79c647ad469ba3c91b56505b1b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LvmThinpoolStorageClassConfig(
            id=id,
            thinpool=thinpool,
            volume_group=volume_group,
            content_types=content_types,
            nodes=nodes,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetContentTypes")
    def reset_content_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentTypes", []))

    @jsii.member(jsii_name="resetNodes")
    def reset_nodes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodes", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="contentTypesInput")
    def content_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "contentTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nodesInput")
    def nodes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "nodesInput"))

    @builtins.property
    @jsii.member(jsii_name="thinpoolInput")
    def thinpool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thinpoolInput"))

    @builtins.property
    @jsii.member(jsii_name="volumeGroupInput")
    def volume_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "volumeGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="contentTypes")
    def content_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "contentTypes"))

    @content_types.setter
    def content_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c953d33019774a29f4a5b7d4762860fe09ec48d440f90c5f15ec31c0db706e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentTypes", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6511a09b82e8a6bfc852a397ca1280b689a8a957d8ed35a28c7b396ec16be004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="nodes")
    def nodes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "nodes"))

    @nodes.setter
    def nodes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4056bb5de1453df06104fe67d77ed485510a9bdb69b6b2c6c0e94c624ffd168f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodes", value)

    @builtins.property
    @jsii.member(jsii_name="thinpool")
    def thinpool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thinpool"))

    @thinpool.setter
    def thinpool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e46fce61c428c30baec72e87f219effa50f768b66a757028a92db753f1d96b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thinpool", value)

    @builtins.property
    @jsii.member(jsii_name="volumeGroup")
    def volume_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "volumeGroup"))

    @volume_group.setter
    def volume_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3160d0cdb815cbe79aa99ba0ac11ae788bd4e8d8af5b1c8d06f1d1432b09e8f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "volumeGroup", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.lvmThinpoolStorageClass.LvmThinpoolStorageClassConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "id": "id",
        "thinpool": "thinpool",
        "volume_group": "volumeGroup",
        "content_types": "contentTypes",
        "nodes": "nodes",
    },
)
class LvmThinpoolStorageClassConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        id: builtins.str,
        thinpool: builtins.str,
        volume_group: builtins.str,
        content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param id: The identifier of the storage class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#id LvmThinpoolStorageClass#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param thinpool: The LVM thinpool that should be implemented by each node. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#thinpool LvmThinpoolStorageClass#thinpool}
        :param volume_group: The associated volume group. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#volume_group LvmThinpoolStorageClass#volume_group}
        :param content_types: The content types that can be stored on this storage class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#content_types LvmThinpoolStorageClass#content_types}
        :param nodes: Nodes that implement this storage class. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#nodes LvmThinpoolStorageClass#nodes}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2777f32a1d50e338241e4244a4b4b344cf69f12df081a4f77a96dba3008e39f0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument thinpool", value=thinpool, expected_type=type_hints["thinpool"])
            check_type(argname="argument volume_group", value=volume_group, expected_type=type_hints["volume_group"])
            check_type(argname="argument content_types", value=content_types, expected_type=type_hints["content_types"])
            check_type(argname="argument nodes", value=nodes, expected_type=type_hints["nodes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "thinpool": thinpool,
            "volume_group": volume_group,
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
        if content_types is not None:
            self._values["content_types"] = content_types
        if nodes is not None:
            self._values["nodes"] = nodes

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
    def id(self) -> builtins.str:
        '''The identifier of the storage class.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#id LvmThinpoolStorageClass#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def thinpool(self) -> builtins.str:
        '''The LVM thinpool that should be implemented by each node.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#thinpool LvmThinpoolStorageClass#thinpool}
        '''
        result = self._values.get("thinpool")
        assert result is not None, "Required property 'thinpool' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def volume_group(self) -> builtins.str:
        '''The associated volume group.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#volume_group LvmThinpoolStorageClass#volume_group}
        '''
        result = self._values.get("volume_group")
        assert result is not None, "Required property 'volume_group' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The content types that can be stored on this storage class.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#content_types LvmThinpoolStorageClass#content_types}
        '''
        result = self._values.get("content_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def nodes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Nodes that implement this storage class.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/lvm_thinpool_storage_class#nodes LvmThinpoolStorageClass#nodes}
        '''
        result = self._values.get("nodes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LvmThinpoolStorageClassConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LvmThinpoolStorageClass",
    "LvmThinpoolStorageClassConfig",
]

publication.publish()

def _typecheckingstub__0f28eb29ecc7cdd9803e2ecd9257f256b04fb79c647ad469ba3c91b56505b1b4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    id: builtins.str,
    thinpool: builtins.str,
    volume_group: builtins.str,
    content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__c953d33019774a29f4a5b7d4762860fe09ec48d440f90c5f15ec31c0db706e11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6511a09b82e8a6bfc852a397ca1280b689a8a957d8ed35a28c7b396ec16be004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4056bb5de1453df06104fe67d77ed485510a9bdb69b6b2c6c0e94c624ffd168f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e46fce61c428c30baec72e87f219effa50f768b66a757028a92db753f1d96b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3160d0cdb815cbe79aa99ba0ac11ae788bd4e8d8af5b1c8d06f1d1432b09e8f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2777f32a1d50e338241e4244a4b4b344cf69f12df081a4f77a96dba3008e39f0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: builtins.str,
    thinpool: builtins.str,
    volume_group: builtins.str,
    content_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    nodes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
