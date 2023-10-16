'''
# `data_proxmox_network_bonds`

Refer to the Terraform Registory for docs: [`data_proxmox_network_bonds`](https://www.terraform.io/docs/providers/proxmox/d/network_bonds).
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


class DataProxmoxNetworkBonds(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBonds",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds proxmox_network_bonds}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProxmoxNetworkBondsFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds proxmox_network_bonds} Data Source.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#filters DataProxmoxNetworkBonds#filters}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa03f90b249ef85d32b04fd3350f34cf5b678c38746f31b70ac6087d2643fc5f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = DataProxmoxNetworkBondsConfig(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProxmoxNetworkBondsFilters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ea6cbb5065bf0e7cf9ee6b5fef024411fa912c80eb1cf4910dc92183d8df5e)
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
    def filters(self) -> "DataProxmoxNetworkBondsFiltersList":
        return typing.cast("DataProxmoxNetworkBondsFiltersList", jsii.get(self, "filters"))

    @builtins.property
    @jsii.member(jsii_name="networkBonds")
    def network_bonds(self) -> "DataProxmoxNetworkBondsNetworkBondsList":
        return typing.cast("DataProxmoxNetworkBondsNetworkBondsList", jsii.get(self, "networkBonds"))

    @builtins.property
    @jsii.member(jsii_name="filtersInput")
    def filters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBondsFilters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBondsFilters"]]], jsii.get(self, "filtersInput"))


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsConfig",
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
class DataProxmoxNetworkBondsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DataProxmoxNetworkBondsFilters", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param filters: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#filters DataProxmoxNetworkBonds#filters}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f2eac7fea839d6b2c591b36f351a1a2766f9b4b749d30951360c5d1c0e1a4f)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBondsFilters"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#filters DataProxmoxNetworkBonds#filters}.'''
        result = self._values.get("filters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DataProxmoxNetworkBondsFilters"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBondsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsFilters",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "values": "values"},
)
class DataProxmoxNetworkBondsFilters:
    def __init__(
        self,
        *,
        name: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: The name of the attribute to filter on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#name DataProxmoxNetworkBonds#name}
        :param values: The value(s) to be used in the filter. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#values DataProxmoxNetworkBonds#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9950eb3f576890d4f61cf05821c75d49fceaafd4dde7c18eb6cb45f836e9bfb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the attribute to filter on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#name DataProxmoxNetworkBonds#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The value(s) to be used in the filter.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#values DataProxmoxNetworkBonds#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBondsFilters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProxmoxNetworkBondsFiltersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsFiltersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a6de5238058c7efcb710e9ef6b8e91d12837f768757e4af19ce892f8cf4d504)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProxmoxNetworkBondsFiltersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d41584d266ee5a66d21a7d0b79e43a2b05be6b07825c52e81624e1b457d36eb0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProxmoxNetworkBondsFiltersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c295c116d357003abb093aa6482b9f5fa346c3f80012cc16946904b4d6315798)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1761ec6b5d41f997e30503b6cbf59d47b593085309029cf0e932f35c197046a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c414e0035f459d591f937ebf4ca1ee07627b960a0f8b6dd53c08542ddc9cbcd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsFilters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsFilters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsFilters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14f86216addde0778e9a935424920f84776c9ccca810fe9b10275f0335b8218)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataProxmoxNetworkBondsFiltersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsFiltersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__59d02ab44379f28c1533c40091a1e4c2dd750761f7c7f02e5a6c266b3ba92e76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a80ea52bd16245d5eb2341826e34d7c6945d6a1da2d0e54c1c43b38c7cacb769)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcae81b383ef7ce052883a27b4c45272a658cfc9bac4ac66de47a6215f2fbc19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DataProxmoxNetworkBondsFilters, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DataProxmoxNetworkBondsFilters, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DataProxmoxNetworkBondsFilters, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ec3ae35e26b154a964632467c10da546e991b12ce723f4aac166afb74ad16ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsNetworkBonds",
    jsii_struct_bases=[],
    name_mapping={"ipv4_gateway": "ipv4Gateway", "ipv6_gateway": "ipv6Gateway"},
)
class DataProxmoxNetworkBondsNetworkBonds:
    def __init__(
        self,
        *,
        ipv4_gateway: typing.Optional[builtins.str] = None,
        ipv6_gateway: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ipv4_gateway: The ipv4 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#ipv4_gateway DataProxmoxNetworkBonds#ipv4_gateway}
        :param ipv6_gateway: The ipv6 gateway. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#ipv6_gateway DataProxmoxNetworkBonds#ipv6_gateway}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__966ac40140b66a40447b1863b4718169d6080c8d7906bbf96841c6485a677dbf)
            check_type(argname="argument ipv4_gateway", value=ipv4_gateway, expected_type=type_hints["ipv4_gateway"])
            check_type(argname="argument ipv6_gateway", value=ipv6_gateway, expected_type=type_hints["ipv6_gateway"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ipv4_gateway is not None:
            self._values["ipv4_gateway"] = ipv4_gateway
        if ipv6_gateway is not None:
            self._values["ipv6_gateway"] = ipv6_gateway

    @builtins.property
    def ipv4_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv4 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#ipv4_gateway DataProxmoxNetworkBonds#ipv4_gateway}
        '''
        result = self._values.get("ipv4_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6_gateway(self) -> typing.Optional[builtins.str]:
        '''The ipv6 gateway.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/d/network_bonds#ipv6_gateway DataProxmoxNetworkBonds#ipv6_gateway}
        '''
        result = self._values.get("ipv6_gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBondsNetworkBonds(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsNetworkBondsIpv4",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataProxmoxNetworkBondsNetworkBondsIpv4:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBondsNetworkBondsIpv4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProxmoxNetworkBondsNetworkBondsIpv4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsNetworkBondsIpv4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__041ff154fbc78d04f9ccc95dcbfa25a0d60fd19581aae8db5a803c9e2090e4d7)
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
    ) -> typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv4]:
        return typing.cast(typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv4], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv4],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bc930943ef84b5ab69e09c8450a0d2d08c49e2f8275b47b3b19dd6081c5e491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsNetworkBondsIpv6",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataProxmoxNetworkBondsNetworkBondsIpv6:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataProxmoxNetworkBondsNetworkBondsIpv6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataProxmoxNetworkBondsNetworkBondsIpv6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsNetworkBondsIpv6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88437324b6e93ff4edf7cadae30f29a1f0d158e9d11f632e4cc78c71b1de9916)
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
    ) -> typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv6]:
        return typing.cast(typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv6], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv6],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fc7a1eba37129660db3053cc8051611c1f6869d092a135f60bb2592c5cffb91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataProxmoxNetworkBondsNetworkBondsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsNetworkBondsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a39a8ba93a193c038489b5480611937dc957e7fcc27c08b03a1b25be809f23)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataProxmoxNetworkBondsNetworkBondsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94f5e8b4f05e9563c3f2c82211e0c64ab54f154cc0fcca0c2ea5f55f850c872d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataProxmoxNetworkBondsNetworkBondsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d255665ac563b97071e25888a5c933b243e136ce5b4e1d9f92d28497141c4354)
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
            type_hints = typing.get_type_hints(_typecheckingstub__65cb6ae3e9ae0dc33763fdf76be892dc05c29ac5bec395baa6a1ce495d64d695)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52ddef751ed98a086bd564ab06d1ea92efec4a4ded6eaf353267e47393afd42a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsNetworkBonds]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsNetworkBonds]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsNetworkBonds]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e8514b83af0dffb8bfd280434ca2bf8eb77ea8e676bfb006d254d0c8431bde4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DataProxmoxNetworkBondsNetworkBondsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.dataProxmoxNetworkBonds.DataProxmoxNetworkBondsNetworkBondsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a156e34235103cbddbeab4f090608d7d5dd79cb8fb02ece80f0b4a7431d130a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

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
    @jsii.member(jsii_name="bondPrimary")
    def bond_primary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bondPrimary"))

    @builtins.property
    @jsii.member(jsii_name="comments")
    def comments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comments"))

    @builtins.property
    @jsii.member(jsii_name="hashPolicy")
    def hash_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hashPolicy"))

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
    @jsii.member(jsii_name="miiMon")
    def mii_mon(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "miiMon"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nodeAttribute")
    def node_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeAttribute"))

    @builtins.property
    @jsii.member(jsii_name="ipv4GatewayInput")
    def ipv4_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv4GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv6GatewayInput")
    def ipv6_gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipv6GatewayInput"))

    @builtins.property
    @jsii.member(jsii_name="ipv4Gateway")
    def ipv4_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv4Gateway"))

    @ipv4_gateway.setter
    def ipv4_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bac4d90ab849ceba1b559d2556230b862f1216c4082e9dc700b0cbf1b66b055)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv4Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="ipv6Gateway")
    def ipv6_gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipv6Gateway"))

    @ipv6_gateway.setter
    def ipv6_gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccaf7e75acca1ac7d2c2aa480c8bebbdbc0210ef96f1bedbdfc455f4ddae41d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipv6Gateway", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataProxmoxNetworkBondsNetworkBonds]:
        return typing.cast(typing.Optional[DataProxmoxNetworkBondsNetworkBonds], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataProxmoxNetworkBondsNetworkBonds],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aedd7bc1fbedbb0fab99d64541c0d01ae7f2a4341838191424646652ad3d79ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DataProxmoxNetworkBonds",
    "DataProxmoxNetworkBondsConfig",
    "DataProxmoxNetworkBondsFilters",
    "DataProxmoxNetworkBondsFiltersList",
    "DataProxmoxNetworkBondsFiltersOutputReference",
    "DataProxmoxNetworkBondsNetworkBonds",
    "DataProxmoxNetworkBondsNetworkBondsIpv4",
    "DataProxmoxNetworkBondsNetworkBondsIpv4OutputReference",
    "DataProxmoxNetworkBondsNetworkBondsIpv6",
    "DataProxmoxNetworkBondsNetworkBondsIpv6OutputReference",
    "DataProxmoxNetworkBondsNetworkBondsList",
    "DataProxmoxNetworkBondsNetworkBondsOutputReference",
]

publication.publish()

def _typecheckingstub__aa03f90b249ef85d32b04fd3350f34cf5b678c38746f31b70ac6087d2643fc5f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProxmoxNetworkBondsFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__c2ea6cbb5065bf0e7cf9ee6b5fef024411fa912c80eb1cf4910dc92183d8df5e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProxmoxNetworkBondsFilters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f2eac7fea839d6b2c591b36f351a1a2766f9b4b749d30951360c5d1c0e1a4f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    filters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DataProxmoxNetworkBondsFilters, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9950eb3f576890d4f61cf05821c75d49fceaafd4dde7c18eb6cb45f836e9bfb(
    *,
    name: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6de5238058c7efcb710e9ef6b8e91d12837f768757e4af19ce892f8cf4d504(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d41584d266ee5a66d21a7d0b79e43a2b05be6b07825c52e81624e1b457d36eb0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c295c116d357003abb093aa6482b9f5fa346c3f80012cc16946904b4d6315798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1761ec6b5d41f997e30503b6cbf59d47b593085309029cf0e932f35c197046a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c414e0035f459d591f937ebf4ca1ee07627b960a0f8b6dd53c08542ddc9cbcd3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14f86216addde0778e9a935424920f84776c9ccca810fe9b10275f0335b8218(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsFilters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d02ab44379f28c1533c40091a1e4c2dd750761f7c7f02e5a6c266b3ba92e76(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a80ea52bd16245d5eb2341826e34d7c6945d6a1da2d0e54c1c43b38c7cacb769(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcae81b383ef7ce052883a27b4c45272a658cfc9bac4ac66de47a6215f2fbc19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ec3ae35e26b154a964632467c10da546e991b12ce723f4aac166afb74ad16ac(
    value: typing.Optional[typing.Union[DataProxmoxNetworkBondsFilters, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__966ac40140b66a40447b1863b4718169d6080c8d7906bbf96841c6485a677dbf(
    *,
    ipv4_gateway: typing.Optional[builtins.str] = None,
    ipv6_gateway: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__041ff154fbc78d04f9ccc95dcbfa25a0d60fd19581aae8db5a803c9e2090e4d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bc930943ef84b5ab69e09c8450a0d2d08c49e2f8275b47b3b19dd6081c5e491(
    value: typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv4],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88437324b6e93ff4edf7cadae30f29a1f0d158e9d11f632e4cc78c71b1de9916(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fc7a1eba37129660db3053cc8051611c1f6869d092a135f60bb2592c5cffb91(
    value: typing.Optional[DataProxmoxNetworkBondsNetworkBondsIpv6],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a39a8ba93a193c038489b5480611937dc957e7fcc27c08b03a1b25be809f23(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94f5e8b4f05e9563c3f2c82211e0c64ab54f154cc0fcca0c2ea5f55f850c872d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d255665ac563b97071e25888a5c933b243e136ce5b4e1d9f92d28497141c4354(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65cb6ae3e9ae0dc33763fdf76be892dc05c29ac5bec395baa6a1ce495d64d695(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ddef751ed98a086bd564ab06d1ea92efec4a4ded6eaf353267e47393afd42a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e8514b83af0dffb8bfd280434ca2bf8eb77ea8e676bfb006d254d0c8431bde4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DataProxmoxNetworkBondsNetworkBonds]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a156e34235103cbddbeab4f090608d7d5dd79cb8fb02ece80f0b4a7431d130a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bac4d90ab849ceba1b559d2556230b862f1216c4082e9dc700b0cbf1b66b055(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccaf7e75acca1ac7d2c2aa480c8bebbdbc0210ef96f1bedbdfc455f4ddae41d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aedd7bc1fbedbb0fab99d64541c0d01ae7f2a4341838191424646652ad3d79ad(
    value: typing.Optional[DataProxmoxNetworkBondsNetworkBonds],
) -> None:
    """Type checking stubs"""
    pass
