'''
# `data_proxmox_network_bridges`

Refer to the Terraform Registory for docs: [`data_proxmox_network_bridges`](https://www.terraform.io/docs/providers/proxmox/d/network_bridges).
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


class DataProxmoxNetworkBridges(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridges",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges proxmox_network_bridges}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProxmoxNetworkBridgesFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges proxmox_network_bridges} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#filters DataProxmoxNetworkBridges#filters}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9adee66c130949de6d9568db4dc6540fe886f77ddf6e6c4b0b6c2a2990a608eb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataProxmoxNetworkBridgesConfig(
            filters=filters,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putFilters")
    def put_filters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProxmoxNetworkBridgesFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d7f747c9c8742610b098a9b0c02bbe27bab34f5b5890f17f27b5ce12c437be6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putFilters", [value]))

    @jsii.member(jsii_name="resetFilters")
    def reset_filters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilters", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="filters")
    def filters(self) -> "DataProxmoxNetworkBridgesFiltersList":
        return typing.cast("DataProxmoxNetworkBridgesFiltersList", jsii.get(self, "filters"))

    @builtins.property
    @jsii.member(jsii_name="networkBridges")
    def network_bridges(self) -> "DataProxmoxNetworkBridgesNetworkBridgesList":
        return typing.cast("DataProxmoxNetworkBridgesNetworkBridgesList", jsii.get(self, "networkBridges"))

    @builtins.property
    @jsii.member(jsii_name="filtersInput")
    def filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBridgesFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBridgesFilters"]]], jsii.get(self, "filtersInput"))


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "filters": "filters",
    },
)
class DataProxmoxNetworkBridgesConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProxmoxNetworkBridgesFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#filters DataProxmoxNetworkBridges#filters}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f67a4a55a324fbc37c373a4d7edb0dca6a94e36a88265e04c6d7bdf31626b45f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if filters is not None:
            self._values["filters"] = filters

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
    def filters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBridgesFilters"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#filters DataProxmoxNetworkBridges#filters}.'''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBridgesFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBridgesConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesFilters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class DataProxmoxNetworkBridgesFilters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: The name of the attribute to filter on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#name DataProxmoxNetworkBridges#name}
        :param values: The value(s) to be used in the filter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#values DataProxmoxNetworkBridges#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d45d4a9dcb681b36f3c67c20651a932e77c9718a96dfb503cae4867f2689cc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the attribute to filter on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#name DataProxmoxNetworkBridges#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The value(s) to be used in the filter.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#values DataProxmoxNetworkBridges#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBridgesFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProxmoxNetworkBridgesFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesFiltersList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d376202c640c1217d73e1ba9850f74f2bb7ee97868be1f346ed5f3599ae33e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProxmoxNetworkBridgesFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1463398370b7f2d41bbb3acb845d3f5e2b27b3f8db52dedcd5ff98e0d1d5eb02)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProxmoxNetworkBridgesFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841abd52a20c81108bb736874bfed03ad0a872e60f6d157973f50783fe6b37c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b6d486d66e5812f50a35e13921084e1fa4ba57f5ce1b4e1a797febb280d0c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3b60a5911a59d6059b6a0ec1f8ea0aa425cbccb59e9dcd5d5473566f4403a24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05933ee85ed02ef6c2f0926ba7ab660025a8e2cfbee11d93dcf572755a68cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataProxmoxNetworkBridgesFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesFiltersOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f0baf670c7234eb79f941ddaff9a8d51958d7ab616db8d795c0ce5259ad162)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53263eb8bc64abab80c61e12a2b9a859d1153e071bef48811453c72ef45d3135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f529b25bed8d5be46db303034b8c08f310b04f1d54145203166316b30913b397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataProxmoxNetworkBridgesFilters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataProxmoxNetworkBridgesFilters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataProxmoxNetworkBridgesFilters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e270e633f00dd0f2334580780ff61bc22cac91bff73ed8e43c7c6a2617feeabb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesNetworkBridges",
    jsii_struct_bases=[],
    name_mapping={
        "comments": "comments",
        "ipv4_gateway": "ipv4Gateway",
        "ipv6_gateway": "ipv6Gateway",
    },
)
class DataProxmoxNetworkBridgesNetworkBridges:
    def __init__(
        self,
        *,
        comments: typing.Optional[builtins.str] = None,
        ipv4_gateway: typing.Optional[builtins.str] = None,
        ipv6_gateway: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param comments: Comment in the bond. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#comments DataProxmoxNetworkBridges#comments}
        :param ipv4_gateway: The ipv4 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#ipv4_gateway DataProxmoxNetworkBridges#ipv4_gateway}
        :param ipv6_gateway: The ipv6 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#ipv6_gateway DataProxmoxNetworkBridges#ipv6_gateway}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25e9dfda1f8cde321043c1b3cd3658c69acefe84ecf980f26530c75d683f0729)
            check_type(argname="argument comments", value=comments, expected_type=type_hints["comments"])
            check_type(argname="argument ipv4_gateway", value=ipv4_gateway, expected_type=type_hints["ipv4_gateway"])
            check_type(argname="argument ipv6_gateway", value=ipv6_gateway, expected_type=type_hints["ipv6_gateway"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comments is not None:
            self._values["comments"] = comments
        if ipv4_gateway is not None:
            self._values["ipv4_gateway"] = ipv4_gateway
        if ipv6_gateway is not None:
            self._values["ipv6_gateway"] = ipv6_gateway

    @builtins.property
    def comments(self) -> typing.Optional[builtins.str]:
        '''Comment in the bond.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#comments DataProxmoxNetworkBridges#comments}
        '''
        result = self._values.get("comments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv4 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#ipv4_gateway DataProxmoxNetworkBridges#ipv4_gateway}
        '''
        result = self._values.get("ipv4_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv6 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bridges#ipv6_gateway DataProxmoxNetworkBridges#ipv6_gateway}
        '''
        result = self._values.get("ipv6_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBridgesNetworkBridges(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesNetworkBridgesIpv4",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataProxmoxNetworkBridgesNetworkBridgesIpv4:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBridgesNetworkBridgesIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProxmoxNetworkBridgesNetworkBridgesIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesNetworkBridgesIpv4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb1d0fb437f4b6ac0485002d491e3bc9aa0a6cb2cc3725b0316cd321c1988feb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv4]:
        return typing.cast(typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv4], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv4],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__730047723e56c2b3aee24ebd5c3c99c7a1c1a613fd1ac3bea27376a0a04f53b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesNetworkBridgesIpv6",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataProxmoxNetworkBridgesNetworkBridgesIpv6:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBridgesNetworkBridgesIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProxmoxNetworkBridgesNetworkBridgesIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesNetworkBridgesIpv6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a73c2e0770dc21d655944d04125276f8c911f4777ffcb5ced0e30760c2f9ab0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv6]:
        return typing.cast(typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv6], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv6],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0960a19aded6f597863324e07d04c50a237f47d2d6541f2799992a6eac48a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataProxmoxNetworkBridgesNetworkBridgesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesNetworkBridgesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1924bd2b5dceda0b256facf9a618dfae2aef0bb03e8f5da914fb282acb7bc924)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProxmoxNetworkBridgesNetworkBridgesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d82cbd70b87b4a97c874a86445585b855c7cfa66e736c8f1631b02ef9508462b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProxmoxNetworkBridgesNetworkBridgesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__114422a39f37199ab2b404f4e28fe1edbf64db6c0514a5ddc9527de10a7aef91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28813ba65e5a10594889f707501ad1887bf37ba6c407a18158a8178768f592d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ec47faf8291c24d409211dce99f145618673b39cabb37311a1bc4f241a1953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesNetworkBridges]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesNetworkBridges]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesNetworkBridges]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f604225200f7388d51567ef41c48255ccc865af0cef975ebe43bad1ba60f68b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataProxmoxNetworkBridgesNetworkBridgesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBridges.DataProxmoxNetworkBridgesNetworkBridgesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad2592324bb67308ead2a699c2b6c2a3b090c1d965af77fe8a24e86cf416304)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetComments")
    def reset_comments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComments", []))

    @jsii.member(jsii_name="resetIpv4Gateway")
    def reset_ipv4_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv4Gateway", []))

    @jsii.member(jsii_name="resetIpv6Gateway")
    def reset_ipv6_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpv6Gateway", []))

    @builtins.property
    @jsii.member(jsii_name="active")
    def active(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "active"))

    @builtins.property
    @jsii.member(jsii_name="autostart")
    def autostart(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "autostart"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="interfaces")
    def interfaces(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "interfaces"))

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ipv4"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nodeAttribute")
    def node_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeAttribute"))

    @builtins.property
    @jsii.member(jsii_name="vlanAware")
    def vlan_aware(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "vlanAware"))

    @builtins.property
    @jsii.member(jsii_name="commentsInput")
    def comments_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4GatewayInput")
    def ipv4_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6GatewayInput")
    def ipv6_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="comments")
    def comments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comments"))

    @comments.setter
    def comments(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95930cda6b36ecc6436767dc7434e7a8c7f9007996737c95567c544e9616e20e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comments", value)

    @builtins.property
    @jsii.member(jsii_name="ipv4Gateway")
    def ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Gateway"))

    @ipv4_gateway.setter
    def ipv4_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08b4c6e94aa53c4bc67a51c1f4659ba482e8dded2afdd9b2ced852539659021)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6Gateway")
    def ipv6_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Gateway"))

    @ipv6_gateway.setter
    def ipv6_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963dcf6b345edeb0660d5696aa5649a09e1fadc1aa5e062666e2f5c4b0fc52e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataProxmoxNetworkBridgesNetworkBridges]:
        return typing.cast(typing.Optional[DataProxmoxNetworkBridgesNetworkBridges], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProxmoxNetworkBridgesNetworkBridges],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baacbdd7a6368eb24ddc76f8daadc112fae468de3c4b0a7a805f279cb7277242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataProxmoxNetworkBridges",
    "DataProxmoxNetworkBridgesConfig",
    "DataProxmoxNetworkBridgesFilters",
    "DataProxmoxNetworkBridgesFiltersList",
    "DataProxmoxNetworkBridgesFiltersOutputReference",
    "DataProxmoxNetworkBridgesNetworkBridges",
    "DataProxmoxNetworkBridgesNetworkBridgesIpv4",
    "DataProxmoxNetworkBridgesNetworkBridgesIpv4OutputReference",
    "DataProxmoxNetworkBridgesNetworkBridgesIpv6",
    "DataProxmoxNetworkBridgesNetworkBridgesIpv6OutputReference",
    "DataProxmoxNetworkBridgesNetworkBridgesList",
    "DataProxmoxNetworkBridgesNetworkBridgesOutputReference",
]

publication.publish()

def _typecheckingstub__9adee66c130949de6d9568db4dc6540fe886f77ddf6e6c4b0b6c2a2990a608eb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProxmoxNetworkBridgesFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__4d7f747c9c8742610b098a9b0c02bbe27bab34f5b5890f17f27b5ce12c437be6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProxmoxNetworkBridgesFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f67a4a55a324fbc37c373a4d7edb0dca6a94e36a88265e04c6d7bdf31626b45f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProxmoxNetworkBridgesFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d45d4a9dcb681b36f3c67c20651a932e77c9718a96dfb503cae4867f2689cc(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d376202c640c1217d73e1ba9850f74f2bb7ee97868be1f346ed5f3599ae33e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1463398370b7f2d41bbb3acb845d3f5e2b27b3f8db52dedcd5ff98e0d1d5eb02(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841abd52a20c81108bb736874bfed03ad0a872e60f6d157973f50783fe6b37c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b6d486d66e5812f50a35e13921084e1fa4ba57f5ce1b4e1a797febb280d0c63(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3b60a5911a59d6059b6a0ec1f8ea0aa425cbccb59e9dcd5d5473566f4403a24(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05933ee85ed02ef6c2f0926ba7ab660025a8e2cfbee11d93dcf572755a68cec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f0baf670c7234eb79f941ddaff9a8d51958d7ab616db8d795c0ce5259ad162(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53263eb8bc64abab80c61e12a2b9a859d1153e071bef48811453c72ef45d3135(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f529b25bed8d5be46db303034b8c08f310b04f1d54145203166316b30913b397(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e270e633f00dd0f2334580780ff61bc22cac91bff73ed8e43c7c6a2617feeabb(
    value: typing.Optional[typing.Union[DataProxmoxNetworkBridgesFilters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25e9dfda1f8cde321043c1b3cd3658c69acefe84ecf980f26530c75d683f0729(
    *,
    comments: typing.Optional[builtins.str] = None,
    ipv4_gateway: typing.Optional[builtins.str] = None,
    ipv6_gateway: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1d0fb437f4b6ac0485002d491e3bc9aa0a6cb2cc3725b0316cd321c1988feb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__730047723e56c2b3aee24ebd5c3c99c7a1c1a613fd1ac3bea27376a0a04f53b2(
    value: typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv4],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a73c2e0770dc21d655944d04125276f8c911f4777ffcb5ced0e30760c2f9ab0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0960a19aded6f597863324e07d04c50a237f47d2d6541f2799992a6eac48a5c(
    value: typing.Optional[DataProxmoxNetworkBridgesNetworkBridgesIpv6],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1924bd2b5dceda0b256facf9a618dfae2aef0bb03e8f5da914fb282acb7bc924(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d82cbd70b87b4a97c874a86445585b855c7cfa66e736c8f1631b02ef9508462b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__114422a39f37199ab2b404f4e28fe1edbf64db6c0514a5ddc9527de10a7aef91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28813ba65e5a10594889f707501ad1887bf37ba6c407a18158a8178768f592d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ec47faf8291c24d409211dce99f145618673b39cabb37311a1bc4f241a1953(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f604225200f7388d51567ef41c48255ccc865af0cef975ebe43bad1ba60f68b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBridgesNetworkBridges]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad2592324bb67308ead2a699c2b6c2a3b090c1d965af77fe8a24e86cf416304(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95930cda6b36ecc6436767dc7434e7a8c7f9007996737c95567c544e9616e20e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08b4c6e94aa53c4bc67a51c1f4659ba482e8dded2afdd9b2ced852539659021(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963dcf6b345edeb0660d5696aa5649a09e1fadc1aa5e062666e2f5c4b0fc52e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baacbdd7a6368eb24ddc76f8daadc112fae468de3c4b0a7a805f279cb7277242(
    value: typing.Optional[DataProxmoxNetworkBridgesNetworkBridges],
) -> None:
    """Type checking stubs"""
    pass
