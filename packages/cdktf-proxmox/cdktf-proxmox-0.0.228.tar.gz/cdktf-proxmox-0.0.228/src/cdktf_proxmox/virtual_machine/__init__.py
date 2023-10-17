'''
# `proxmox_virtual_machine`

Refer to the Terraform Registory for docs: [`proxmox_virtual_machine`](https://www.terraform.io/docs/providers/proxmox/r/virtual_machine).
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


class VirtualMachine(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachine",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine proxmox_virtual_machine}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        node_attribute: builtins.str,
        agent: typing.Optional[typing.Union[typing.Union["VirtualMachineAgent", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        bios: typing.Optional[builtins.str] = None,
        clone: typing.Optional[typing.Union[typing.Union["VirtualMachineClone", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        cloud_init: typing.Optional[typing.Union[typing.Union["VirtualMachineCloudInit", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        cpu: typing.Optional[typing.Union[typing.Union["VirtualMachineCpu", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[jsii.Number] = None,
        iso: typing.Optional[typing.Union[typing.Union["VirtualMachineIso", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        keyboard_layout: typing.Optional[builtins.str] = None,
        kvm_arguments: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        memory: typing.Optional[typing.Union[typing.Union["VirtualMachineMemory", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pci_devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachinePciDevices", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_pool: typing.Optional[builtins.str] = None,
        start_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_on_node_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union[typing.Union["VirtualMachineTimeouts", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine proxmox_virtual_machine} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param node_attribute: The node to create the virtual machine on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#node VirtualMachine#node}
        :param agent: The agent configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#agent VirtualMachine#agent}
        :param bios: The BIOS type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#bios VirtualMachine#bios}
        :param clone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#clone VirtualMachine#clone}.
        :param cloud_init: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cloud_init VirtualMachine#cloud_init}.
        :param cpu: The CPU configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cpu VirtualMachine#cpu}
        :param description: The virtual machine description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#description VirtualMachine#description}
        :param disks: The terrafrom generated disks attached to the VM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#disks VirtualMachine#disks}
        :param id: The identifier of the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#id VirtualMachine#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iso: The operating system configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#iso VirtualMachine#iso}
        :param keyboard_layout: The keyboard layout. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#keyboard_layout VirtualMachine#keyboard_layout}
        :param kvm_arguments: The arguments to pass to KVM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#kvm_arguments VirtualMachine#kvm_arguments}
        :param machine_type: The machine type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#machine_type VirtualMachine#machine_type}
        :param memory: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#memory VirtualMachine#memory}.
        :param name: The name of the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        :param network_interfaces: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#network_interfaces VirtualMachine#network_interfaces}.
        :param pci_devices: PCI devices passed through to the VM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#pci_devices VirtualMachine#pci_devices}
        :param resource_pool: The resource pool the virtual machine is in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#resource_pool VirtualMachine#resource_pool}
        :param start_on_create: Whether to start the virtual machine on creation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start_on_create VirtualMachine#start_on_create}
        :param start_on_node_boot: Whether to start the virtual machine on node boot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start_on_node_boot VirtualMachine#start_on_node_boot}
        :param tags: The tags of the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#tags VirtualMachine#tags}
        :param timeouts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#timeouts VirtualMachine#timeouts}.
        :param type: The operating system type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#type VirtualMachine#type}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac855b08d6f8e9923a335183bd2d6621b1aa2e6cad0d447023ba8e37d5a4bceb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = VirtualMachineConfig(
            node_attribute=node_attribute,
            agent=agent,
            bios=bios,
            clone=clone,
            cloud_init=cloud_init,
            cpu=cpu,
            description=description,
            disks=disks,
            id=id,
            iso=iso,
            keyboard_layout=keyboard_layout,
            kvm_arguments=kvm_arguments,
            machine_type=machine_type,
            memory=memory,
            name=name,
            network_interfaces=network_interfaces,
            pci_devices=pci_devices,
            resource_pool=resource_pool,
            start_on_create=start_on_create,
            start_on_node_boot=start_on_node_boot,
            tags=tags,
            timeouts=timeouts,
            type=type,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAgent")
    def put_agent(
        self,
        value: typing.Union[typing.Union["VirtualMachineAgent", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83418811f742f8fe7b3f25f83b1f824de55abae3fa54a05c5a57988e1e2d331a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAgent", [value]))

    @jsii.member(jsii_name="putClone")
    def put_clone(
        self,
        value: typing.Union[typing.Union["VirtualMachineClone", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5be555fcbf0ae384a7a0a9fdad33b93362dd226fdc5c88027fceb44f8538e45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClone", [value]))

    @jsii.member(jsii_name="putCloudInit")
    def put_cloud_init(
        self,
        value: typing.Union[typing.Union["VirtualMachineCloudInit", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec17dc969abbc237640ebdb994cdc9dcf89529f9d8b02f6e30f4cef6779d300)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCloudInit", [value]))

    @jsii.member(jsii_name="putCpu")
    def put_cpu(
        self,
        value: typing.Union[typing.Union["VirtualMachineCpu", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f249d667036579028c301877ed4d888e06a7438035eba0a0d8c8c8caf38cfd1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCpu", [value]))

    @jsii.member(jsii_name="putDisks")
    def put_disks(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineDisks", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c240a1a77f4f0e179396d60285e7f22b1459492eeaa0b91e2ea999ddbb705419)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDisks", [value]))

    @jsii.member(jsii_name="putIso")
    def put_iso(
        self,
        value: typing.Union[typing.Union["VirtualMachineIso", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29fbca37452f5499d50f2fd03155649d42967a974cbe99013b60e44e50e32556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIso", [value]))

    @jsii.member(jsii_name="putMemory")
    def put_memory(
        self,
        value: typing.Union[typing.Union["VirtualMachineMemory", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be9cb989446f6faf7555ee370e2a92c8d5d9debac516f9dbed3917865f1543c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMemory", [value]))

    @jsii.member(jsii_name="putNetworkInterfaces")
    def put_network_interfaces(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5c4452a3e1e0f98bacc59a97a216ed7c5dfdc77364a4ec926df86078677b43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkInterfaces", [value]))

    @jsii.member(jsii_name="putPciDevices")
    def put_pci_devices(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachinePciDevices", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd61d2622ca4d0bbb02b8baf6c451445ebed7c6a83df21c7c8c71772e1a9f16a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPciDevices", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        value: typing.Union[typing.Union["VirtualMachineTimeouts", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bcd77991eab5b3ec456c7389616efed9c6bb2a8155d3f3be858acdcb12fca37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAgent")
    def reset_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgent", []))

    @jsii.member(jsii_name="resetBios")
    def reset_bios(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBios", []))

    @jsii.member(jsii_name="resetClone")
    def reset_clone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClone", []))

    @jsii.member(jsii_name="resetCloudInit")
    def reset_cloud_init(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCloudInit", []))

    @jsii.member(jsii_name="resetCpu")
    def reset_cpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpu", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDisks")
    def reset_disks(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisks", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIso")
    def reset_iso(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIso", []))

    @jsii.member(jsii_name="resetKeyboardLayout")
    def reset_keyboard_layout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyboardLayout", []))

    @jsii.member(jsii_name="resetKvmArguments")
    def reset_kvm_arguments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKvmArguments", []))

    @jsii.member(jsii_name="resetMachineType")
    def reset_machine_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMachineType", []))

    @jsii.member(jsii_name="resetMemory")
    def reset_memory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMemory", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetNetworkInterfaces")
    def reset_network_interfaces(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkInterfaces", []))

    @jsii.member(jsii_name="resetPciDevices")
    def reset_pci_devices(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPciDevices", []))

    @jsii.member(jsii_name="resetResourcePool")
    def reset_resource_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourcePool", []))

    @jsii.member(jsii_name="resetStartOnCreate")
    def reset_start_on_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartOnCreate", []))

    @jsii.member(jsii_name="resetStartOnNodeBoot")
    def reset_start_on_node_boot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartOnNodeBoot", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="agent")
    def agent(self) -> "VirtualMachineAgentOutputReference":
        return typing.cast("VirtualMachineAgentOutputReference", jsii.get(self, "agent"))

    @builtins.property
    @jsii.member(jsii_name="clone")
    def clone(self) -> "VirtualMachineCloneOutputReference":
        return typing.cast("VirtualMachineCloneOutputReference", jsii.get(self, "clone"))

    @builtins.property
    @jsii.member(jsii_name="cloudInit")
    def cloud_init(self) -> "VirtualMachineCloudInitOutputReference":
        return typing.cast("VirtualMachineCloudInitOutputReference", jsii.get(self, "cloudInit"))

    @builtins.property
    @jsii.member(jsii_name="computedDisks")
    def computed_disks(self) -> "VirtualMachineComputedDisksList":
        return typing.cast("VirtualMachineComputedDisksList", jsii.get(self, "computedDisks"))

    @builtins.property
    @jsii.member(jsii_name="computedNetworkInterfaces")
    def computed_network_interfaces(
        self,
    ) -> "VirtualMachineComputedNetworkInterfacesList":
        return typing.cast("VirtualMachineComputedNetworkInterfacesList", jsii.get(self, "computedNetworkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="computedPciDevices")
    def computed_pci_devices(self) -> "VirtualMachineComputedPciDevicesList":
        return typing.cast("VirtualMachineComputedPciDevicesList", jsii.get(self, "computedPciDevices"))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> "VirtualMachineCpuOutputReference":
        return typing.cast("VirtualMachineCpuOutputReference", jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="disks")
    def disks(self) -> "VirtualMachineDisksList":
        return typing.cast("VirtualMachineDisksList", jsii.get(self, "disks"))

    @builtins.property
    @jsii.member(jsii_name="iso")
    def iso(self) -> "VirtualMachineIsoOutputReference":
        return typing.cast("VirtualMachineIsoOutputReference", jsii.get(self, "iso"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> "VirtualMachineMemoryOutputReference":
        return typing.cast("VirtualMachineMemoryOutputReference", jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfaces")
    def network_interfaces(self) -> "VirtualMachineNetworkInterfacesList":
        return typing.cast("VirtualMachineNetworkInterfacesList", jsii.get(self, "networkInterfaces"))

    @builtins.property
    @jsii.member(jsii_name="pciDevices")
    def pci_devices(self) -> "VirtualMachinePciDevicesList":
        return typing.cast("VirtualMachinePciDevicesList", jsii.get(self, "pciDevices"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "VirtualMachineTimeoutsOutputReference":
        return typing.cast("VirtualMachineTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="agentInput")
    def agent_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineAgent", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineAgent", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "agentInput"))

    @builtins.property
    @jsii.member(jsii_name="biosInput")
    def bios_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "biosInput"))

    @builtins.property
    @jsii.member(jsii_name="cloneInput")
    def clone_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineClone", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineClone", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloneInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudInitInput")
    def cloud_init_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInit", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInit", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cloudInitInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuInput")
    def cpu_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCpu", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCpu", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "cpuInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="disksInput")
    def disks_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineDisks"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineDisks"]]], jsii.get(self, "disksInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isoInput")
    def iso_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineIso", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineIso", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isoInput"))

    @builtins.property
    @jsii.member(jsii_name="keyboardLayoutInput")
    def keyboard_layout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyboardLayoutInput"))

    @builtins.property
    @jsii.member(jsii_name="kvmArgumentsInput")
    def kvm_arguments_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kvmArgumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="machineTypeInput")
    def machine_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "machineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="memoryInput")
    def memory_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineMemory", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineMemory", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "memoryInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInterfacesInput")
    def network_interfaces_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineNetworkInterfaces"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineNetworkInterfaces"]]], jsii.get(self, "networkInterfacesInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeAttributeInput")
    def node_attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeAttributeInput"))

    @builtins.property
    @jsii.member(jsii_name="pciDevicesInput")
    def pci_devices_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePciDevices"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePciDevices"]]], jsii.get(self, "pciDevicesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcePoolInput")
    def resource_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourcePoolInput"))

    @builtins.property
    @jsii.member(jsii_name="startOnCreateInput")
    def start_on_create_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startOnCreateInput"))

    @builtins.property
    @jsii.member(jsii_name="startOnNodeBootInput")
    def start_on_node_boot_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "startOnNodeBootInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="bios")
    def bios(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bios"))

    @bios.setter
    def bios(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7fdf3234ffc0a45a086b7662782e1efe8ae453ae303dbf71edfd8e730853272)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bios", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2517935fd3510ba0ad5d466ae2904d5e022d7c3f18503653eeb0ed7d515755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "id"))

    @id.setter
    def id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15a025be497fdfaa3b0d842275cc69daebb19e172bced5fbd3aa25b17ae770c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="keyboardLayout")
    def keyboard_layout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyboardLayout"))

    @keyboard_layout.setter
    def keyboard_layout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72ca051627ddd8e472230d692c0b2cf2e8b8502548648f30d9c09a83a108fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyboardLayout", value)

    @builtins.property
    @jsii.member(jsii_name="kvmArguments")
    def kvm_arguments(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kvmArguments"))

    @kvm_arguments.setter
    def kvm_arguments(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abf0326b4f275c1319d9ae7b6554ddf1e19533666215d701169454b80aabd1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kvmArguments", value)

    @builtins.property
    @jsii.member(jsii_name="machineType")
    def machine_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "machineType"))

    @machine_type.setter
    def machine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3c2e4601dc8dfc83905e383b9c71a9dad804e94a09f2e28e420c236946ba332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "machineType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba8f1f0134f6d137c76719f312afbbc7590fb0539eb44e5bc2b92af903eea2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="nodeAttribute")
    def node_attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeAttribute"))

    @node_attribute.setter
    def node_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b210d0ab9c636b9e6d796c66fba050b512d5c51b04b0c8afa4867809bc79ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="resourcePool")
    def resource_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourcePool"))

    @resource_pool.setter
    def resource_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92ab755a041aafc6df63657e9cdf7f1502021197f1b67907764ad139e6bbca0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcePool", value)

    @builtins.property
    @jsii.member(jsii_name="startOnCreate")
    def start_on_create(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startOnCreate"))

    @start_on_create.setter
    def start_on_create(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f46c05ce037c2af727b2d37be37720759782d2bd7084cb647d08c38bb966bec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startOnCreate", value)

    @builtins.property
    @jsii.member(jsii_name="startOnNodeBoot")
    def start_on_node_boot(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "startOnNodeBoot"))

    @start_on_node_boot.setter
    def start_on_node_boot(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5ac732e5479b666ee11ad433b6436782a73f7595688e42021acf4f84b8cee1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startOnNodeBoot", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68f6a6985b9673248602b2dfe49c2c664559a4ad821a6e4c485d2e169ae0bc66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__464c46bfca258bb0efd2a877391319395124fcd52273d2ecc6687c185706e19e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineAgent",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "type": "type", "use_fstrim": "useFstrim"},
)
class VirtualMachineAgent:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
        use_fstrim: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether the agent is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#enabled VirtualMachine#enabled}
        :param type: The guest agent type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#type VirtualMachine#type}
        :param use_fstrim: Whether to use fstrim. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_fstrim VirtualMachine#use_fstrim}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6411bd5f9d10a5f7db06600c8921b8380ef837ae939b4076f6945d87f3990feb)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument use_fstrim", value=use_fstrim, expected_type=type_hints["use_fstrim"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if type is not None:
            self._values["type"] = type
        if use_fstrim is not None:
            self._values["use_fstrim"] = use_fstrim

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the agent is enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#enabled VirtualMachine#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The guest agent type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#type VirtualMachine#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_fstrim(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use fstrim.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_fstrim VirtualMachine#use_fstrim}
        '''
        result = self._values.get("use_fstrim")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineAgent(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineAgentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineAgentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__16db17e5eebd8dda879d2c1f2c0e08902ad2c9b9ca231b1e06829e2d1d3d4e13)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @jsii.member(jsii_name="resetUseFstrim")
    def reset_use_fstrim(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseFstrim", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="useFstrimInput")
    def use_fstrim_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useFstrimInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bdbbc473da0990c22af063f08abb2226fca5e51364cd91ab66b4b3029de4907)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6ddb0e5ac2e478a5e8649768c43d6ede249be7fdbe0c5c65cac741f427a479f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="useFstrim")
    def use_fstrim(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useFstrim"))

    @use_fstrim.setter
    def use_fstrim(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45172b8f896ca5116af29c6f384a48be2564a9be0b889d6b112f48039ce665d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFstrim", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineAgent, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineAgent, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineAgent, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__967859fbf99d9ed36f4a28fb83a16f4b699c025d3b0a601ad584a9dc130545bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineClone",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "full_clone": "fullClone", "storage": "storage"},
)
class VirtualMachineClone:
    def __init__(
        self,
        *,
        source: jsii.Number,
        full_clone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        storage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param source: The identifier of the virtual machine or template to clone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#source VirtualMachine#source}
        :param full_clone: Whether to clone as a full or linked clone. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#full_clone VirtualMachine#full_clone}
        :param storage: The storage to place the clone on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41ca7847e00d8685921476c28bf72b3b40d87ba38ddb6bb5fb35d19f51c1312d)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument full_clone", value=full_clone, expected_type=type_hints["full_clone"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
        }
        if full_clone is not None:
            self._values["full_clone"] = full_clone
        if storage is not None:
            self._values["storage"] = storage

    @builtins.property
    def source(self) -> jsii.Number:
        '''The identifier of the virtual machine or template to clone.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#source VirtualMachine#source}
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def full_clone(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to clone as a full or linked clone.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#full_clone VirtualMachine#full_clone}
        '''
        result = self._values.get("full_clone")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def storage(self) -> typing.Optional[builtins.str]:
        '''The storage to place the clone on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        '''
        result = self._values.get("storage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineClone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineCloneOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloneOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e440bef17916e573c0e2e5a199351daf24de4b94528b792ff19991380edf722)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFullClone")
    def reset_full_clone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFullClone", []))

    @jsii.member(jsii_name="resetStorage")
    def reset_storage(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorage", []))

    @builtins.property
    @jsii.member(jsii_name="fullCloneInput")
    def full_clone_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "fullCloneInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="fullClone")
    def full_clone(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "fullClone"))

    @full_clone.setter
    def full_clone(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__971da7019ac6c242e2999c8aac4dced8bb416891e9ce35657f13c36a51614de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fullClone", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "source"))

    @source.setter
    def source(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07de61649a4cc6af75cb68e9940a696088603cc020fa07484c593eaf91a96656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31d635e3500bfbbf33b2d215c60cc88fe2ee1725525ff7c5cfbc3ae0529d3b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineClone, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineClone, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineClone, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f909b526cd04e9f9d19e027b7653e41eb174a0c98965b10dac60f9c12d186fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInit",
    jsii_struct_bases=[],
    name_mapping={"dns": "dns", "ip": "ip", "user": "user"},
)
class VirtualMachineCloudInit:
    def __init__(
        self,
        *,
        dns: typing.Optional[typing.Union[typing.Union["VirtualMachineCloudInitDns", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineCloudInitIp", typing.Dict[builtins.str, typing.Any]]]]] = None,
        user: typing.Optional[typing.Union[typing.Union["VirtualMachineCloudInitUser", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param dns: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dns VirtualMachine#dns}.
        :param ip: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#ip VirtualMachine#ip}.
        :param user: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#user VirtualMachine#user}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e28b42e970cbc700d2025d6d345202f39f218ba811f2f256d8c0470202a16b)
            check_type(argname="argument dns", value=dns, expected_type=type_hints["dns"])
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns is not None:
            self._values["dns"] = dns
        if ip is not None:
            self._values["ip"] = ip
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def dns(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInitDns", _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dns VirtualMachine#dns}.'''
        result = self._values.get("dns")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInitDns", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineCloudInitIp"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#ip VirtualMachine#ip}.'''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineCloudInitIp"]]], result)

    @builtins.property
    def user(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInitUser", _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#user VirtualMachine#user}.'''
        result = self._values.get("user")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInitUser", _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineCloudInit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitDns",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "nameserver": "nameserver"},
)
class VirtualMachineCloudInitDns:
    def __init__(
        self,
        *,
        domain: typing.Optional[builtins.str] = None,
        nameserver: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: The domain to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#domain VirtualMachine#domain}
        :param nameserver: The nameserver to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#nameserver VirtualMachine#nameserver}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54cd6db34eaadbb9e0b11cbaed0641d2b27a19870a7447fdbf69b1ee7195eb59)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument nameserver", value=nameserver, expected_type=type_hints["nameserver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if nameserver is not None:
            self._values["nameserver"] = nameserver

    @builtins.property
    def domain(self) -> typing.Optional[builtins.str]:
        '''The domain to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#domain VirtualMachine#domain}
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nameserver(self) -> typing.Optional[builtins.str]:
        '''The nameserver to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#nameserver VirtualMachine#nameserver}
        '''
        result = self._values.get("nameserver")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineCloudInitDns(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineCloudInitDnsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitDnsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f225d8e38b4390ce036d4e8cc11c58f600a83710536d1d9949defb3e5de04bb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDomain")
    def reset_domain(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDomain", []))

    @jsii.member(jsii_name="resetNameserver")
    def reset_nameserver(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameserver", []))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="nameserverInput")
    def nameserver_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameserverInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a577b2439d886f2dd7cd691d0ccf0c728d91bf78fa342617d4a6201802f0c32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="nameserver")
    def nameserver(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameserver"))

    @nameserver.setter
    def nameserver(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c28b2c558f7e70daed3179d34309c90bb9b91282e3e2d84e0ec87360a7802c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameserver", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInitDns, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInitDns, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineCloudInitDns, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1cf0b5d280a19b6f9757770225aaede2bc8ec6379c6b80b8e138b05335d5d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitIp",
    jsii_struct_bases=[],
    name_mapping={"position": "position", "v4": "v4", "v6": "v6"},
)
class VirtualMachineCloudInitIp:
    def __init__(
        self,
        *,
        position: jsii.Number,
        v4: typing.Optional[typing.Union[typing.Union["VirtualMachineCloudInitIpV4", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        v6: typing.Optional[typing.Union[typing.Union["VirtualMachineCloudInitIpV6", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param position: The position of the network interface in the VM as an int. Used to determine the interface name (net0, net1, etc). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        :param v4: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#v4 VirtualMachine#v4}.
        :param v6: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#v6 VirtualMachine#v6}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f282493bf9efcdebe536c21965c2ed059db850de04e956b61d695ad4f9b4bc)
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument v4", value=v4, expected_type=type_hints["v4"])
            check_type(argname="argument v6", value=v6, expected_type=type_hints["v6"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "position": position,
        }
        if v4 is not None:
            self._values["v4"] = v4
        if v6 is not None:
            self._values["v6"] = v6

    @builtins.property
    def position(self) -> jsii.Number:
        '''The position of the network interface in the VM as an int.

        Used to determine the interface name (net0, net1, etc).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        '''
        result = self._values.get("position")
        assert result is not None, "Required property 'position' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def v4(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInitIpV4", _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#v4 VirtualMachine#v4}.'''
        result = self._values.get("v4")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInitIpV4", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def v6(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInitIpV6", _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#v6 VirtualMachine#v6}.'''
        result = self._values.get("v6")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInitIpV6", _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineCloudInitIp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineCloudInitIpList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitIpList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27c9ac2d0b241a7a3595446e16230af493795855770d4ee006b70a4dec3dd937)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VirtualMachineCloudInitIpOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1e07af5b8aa46d37b76358a44863e7e2e7b1dcd214dac3d1c0f76457b38938)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineCloudInitIpOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__321c8b72f0c15f105c8509e2c539d0036fcd2fb0ae269c41e518a362fcb60ef0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3460d4129530eb4a0f223c686f69c01f151c3e41ee6a7f255803bfadc0b544da)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e758419348feaf0b082df110c5d3b3c8e39b20d8a3fca34c64958209060cadf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineCloudInitIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineCloudInitIp]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineCloudInitIp]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19dadc0181cecb96bd9eb2a960aac63754f2ffbbbaecbe8c726ccddabec7ea9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachineCloudInitIpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitIpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88fbc89928155632dc799e88c1ae147fa9fee4cbf0d2b84a48c7bc84bdaa79a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putV4")
    def put_v4(
        self,
        value: typing.Union[typing.Union["VirtualMachineCloudInitIpV4", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047b760f656247ce3d06faa600a0f93c8a2d5f52d8e09ef88971c5947b4b01b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putV4", [value]))

    @jsii.member(jsii_name="putV6")
    def put_v6(
        self,
        value: typing.Union[typing.Union["VirtualMachineCloudInitIpV6", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2716f153ee5a0a8480ed87b0277674b6e4198821075baddb08781c7b4e551e66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putV6", [value]))

    @jsii.member(jsii_name="resetV4")
    def reset_v4(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetV4", []))

    @jsii.member(jsii_name="resetV6")
    def reset_v6(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetV6", []))

    @builtins.property
    @jsii.member(jsii_name="v4")
    def v4(self) -> "VirtualMachineCloudInitIpV4OutputReference":
        return typing.cast("VirtualMachineCloudInitIpV4OutputReference", jsii.get(self, "v4"))

    @builtins.property
    @jsii.member(jsii_name="v6")
    def v6(self) -> "VirtualMachineCloudInitIpV6OutputReference":
        return typing.cast("VirtualMachineCloudInitIpV6OutputReference", jsii.get(self, "v6"))

    @builtins.property
    @jsii.member(jsii_name="positionInput")
    def position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "positionInput"))

    @builtins.property
    @jsii.member(jsii_name="v4Input")
    def v4_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInitIpV4", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInitIpV4", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "v4Input"))

    @builtins.property
    @jsii.member(jsii_name="v6Input")
    def v6_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInitIpV6", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInitIpV6", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "v6Input"))

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456c60ab311663c29e8498a96e0268b454bca5114f0a62e36adc620851aec570)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInitIp, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInitIp, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineCloudInitIp, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac7ec251fefa7f7d7ae7c099fe61361eb3bec60aa604655635385ca879aae23f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitIpV4",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "dhcp": "dhcp",
        "gateway": "gateway",
        "netmask": "netmask",
    },
)
class VirtualMachineCloudInitIpV4:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The IP address to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#address VirtualMachine#address}
        :param dhcp: Whether to use DHCP to get the IP address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dhcp VirtualMachine#dhcp}
        :param gateway: The gateway to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#gateway VirtualMachine#gateway}
        :param netmask: The IP address netmask to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#netmask VirtualMachine#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66d24195a92bf1c529b739ac4ca0d0ee0d7aad533affac38e8c13149debdae9)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument dhcp", value=dhcp, expected_type=type_hints["dhcp"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if dhcp is not None:
            self._values["dhcp"] = dhcp
        if gateway is not None:
            self._values["gateway"] = gateway
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The IP address to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#address VirtualMachine#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dhcp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use DHCP to get the IP address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dhcp VirtualMachine#dhcp}
        '''
        result = self._values.get("dhcp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gateway(self) -> typing.Optional[builtins.str]:
        '''The gateway to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#gateway VirtualMachine#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''The IP address netmask to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#netmask VirtualMachine#netmask}
        '''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineCloudInitIpV4(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineCloudInitIpV4OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitIpV4OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6380433b49ff0c2a944fb9df2de254f4c672c7bec827138e0e0f4bd8be51f7e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetDhcp")
    def reset_dhcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcp", []))

    @jsii.member(jsii_name="resetGateway")
    def reset_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateway", []))

    @jsii.member(jsii_name="resetNetmask")
    def reset_netmask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetmask", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpInput")
    def dhcp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dhcpInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__79cedb5611a48b9259c9b4004c166ec73a3e7f6b3f47e6f31b603b1f0b51eeb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="dhcp")
    def dhcp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dhcp"))

    @dhcp.setter
    def dhcp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1b7b15d70b8539e502b57a1a333cddd75e461ab5f760a597abfae4b9c0f9e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dhcp", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4bac085a5fed0ab3b5bb7b694ae138805c914af72e4fc05e5064d0493a4f53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69cde9f6d15851de4a686f23b5723010a9b9e768438cfceb106beae54c7fbbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInitIpV4, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInitIpV4, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineCloudInitIpV4, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815b473b81e20555e84cda13cc3279b6a9762ad22d7508918dded37a36536783)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitIpV6",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "dhcp": "dhcp",
        "gateway": "gateway",
        "netmask": "netmask",
    },
)
class VirtualMachineCloudInitIpV6:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        gateway: typing.Optional[builtins.str] = None,
        netmask: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The IP address to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#address VirtualMachine#address}
        :param dhcp: Whether to use DHCP to get the IP address. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dhcp VirtualMachine#dhcp}
        :param gateway: The gateway to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#gateway VirtualMachine#gateway}
        :param netmask: The IP address netmask to use for the machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#netmask VirtualMachine#netmask}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f16cbf68356c519e317488143acf7d13a008d04be15fe22b2c7fe149ba47d4)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument dhcp", value=dhcp, expected_type=type_hints["dhcp"])
            check_type(argname="argument gateway", value=gateway, expected_type=type_hints["gateway"])
            check_type(argname="argument netmask", value=netmask, expected_type=type_hints["netmask"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if dhcp is not None:
            self._values["dhcp"] = dhcp
        if gateway is not None:
            self._values["gateway"] = gateway
        if netmask is not None:
            self._values["netmask"] = netmask

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The IP address to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#address VirtualMachine#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dhcp(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use DHCP to get the IP address.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dhcp VirtualMachine#dhcp}
        '''
        result = self._values.get("dhcp")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def gateway(self) -> typing.Optional[builtins.str]:
        '''The gateway to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#gateway VirtualMachine#gateway}
        '''
        result = self._values.get("gateway")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def netmask(self) -> typing.Optional[builtins.str]:
        '''The IP address netmask to use for the machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#netmask VirtualMachine#netmask}
        '''
        result = self._values.get("netmask")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineCloudInitIpV6(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineCloudInitIpV6OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitIpV6OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__94597b966ad8298c497f74a7aaae1f787d8efc019539cf6843edc199801ed03f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetDhcp")
    def reset_dhcp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDhcp", []))

    @jsii.member(jsii_name="resetGateway")
    def reset_gateway(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGateway", []))

    @jsii.member(jsii_name="resetNetmask")
    def reset_netmask(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetmask", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="dhcpInput")
    def dhcp_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dhcpInput"))

    @builtins.property
    @jsii.member(jsii_name="gatewayInput")
    def gateway_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gatewayInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__0c4eda9be071d2337d0732e0e5519ba5455fc33d935d0ea8584635da27e46a9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="dhcp")
    def dhcp(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dhcp"))

    @dhcp.setter
    def dhcp(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3139c798680fb08721424b6f43f8d27c05781be28118a937a4c59637119e4aac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dhcp", value)

    @builtins.property
    @jsii.member(jsii_name="gateway")
    def gateway(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gateway"))

    @gateway.setter
    def gateway(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8017b311275aeb4154a034373efb89718ebf2ff04643623da3f083aba65e43b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gateway", value)

    @builtins.property
    @jsii.member(jsii_name="netmask")
    def netmask(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "netmask"))

    @netmask.setter
    def netmask(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6d97d2d138b53c660abc1b50d99c9a6aef84f4de9131904e3155680c70bc5bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "netmask", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInitIpV6, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInitIpV6, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineCloudInitIpV6, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d27f08d22b058d992fa85e0df44803ba79dd54dfe0b4fe69c6a4c46b4f5d1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachineCloudInitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e82d850ece5596b745643fecfebe9acfadfcdb74b8ba3c98d4ae0d523b843aba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDns")
    def put_dns(
        self,
        value: typing.Union[typing.Union[VirtualMachineCloudInitDns, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fbf6c8a6685031386ac6ccfcc198e3f2c7772cd56538c30467048d68bfdf70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDns", [value]))

    @jsii.member(jsii_name="putIp")
    def put_ip(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineCloudInitIp, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ea28088e089353d628145df245927dab52adf13adc4e16f81f5276a626a804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIp", [value]))

    @jsii.member(jsii_name="putUser")
    def put_user(
        self,
        value: typing.Union[typing.Union["VirtualMachineCloudInitUser", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42895dfe13efb2eda5ff69c3d7b8eb5ab11d38b00f651ee4f27d8e4401d4eba8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putUser", [value]))

    @jsii.member(jsii_name="resetDns")
    def reset_dns(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDns", []))

    @jsii.member(jsii_name="resetIp")
    def reset_ip(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIp", []))

    @jsii.member(jsii_name="resetUser")
    def reset_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUser", []))

    @builtins.property
    @jsii.member(jsii_name="dns")
    def dns(self) -> VirtualMachineCloudInitDnsOutputReference:
        return typing.cast(VirtualMachineCloudInitDnsOutputReference, jsii.get(self, "dns"))

    @builtins.property
    @jsii.member(jsii_name="ip")
    def ip(self) -> VirtualMachineCloudInitIpList:
        return typing.cast(VirtualMachineCloudInitIpList, jsii.get(self, "ip"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> "VirtualMachineCloudInitUserOutputReference":
        return typing.cast("VirtualMachineCloudInitUserOutputReference", jsii.get(self, "user"))

    @builtins.property
    @jsii.member(jsii_name="dnsInput")
    def dns_input(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInitDns, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInitDns, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dnsInput"))

    @builtins.property
    @jsii.member(jsii_name="ipInput")
    def ip_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineCloudInitIp]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineCloudInitIp]]], jsii.get(self, "ipInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCloudInitUser", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCloudInitUser", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInit, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInit, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineCloudInit, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b65b1b292e54bd4afb4c3d50e3cbd1ab204a8e320ef66bf7be0126896a0fdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitUser",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "password": "password", "public_keys": "publicKeys"},
)
class VirtualMachineCloudInitUser:
    def __init__(
        self,
        *,
        name: builtins.str,
        password: typing.Optional[builtins.str] = None,
        public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: The name of the user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        :param password: The password of the user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#password VirtualMachine#password}
        :param public_keys: The public ssh keys of the user. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#public_keys VirtualMachine#public_keys}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc7348a691b46c0d8a98262a7c2fa8eaa4de94ed0ac8e730873e05023184ef62)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument public_keys", value=public_keys, expected_type=type_hints["public_keys"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if password is not None:
            self._values["password"] = password
        if public_keys is not None:
            self._values["public_keys"] = public_keys

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> typing.Optional[builtins.str]:
        '''The password of the user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#password VirtualMachine#password}
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_keys(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The public ssh keys of the user.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#public_keys VirtualMachine#public_keys}
        '''
        result = self._values.get("public_keys")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineCloudInitUser(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineCloudInitUserOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCloudInitUserOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__60455c3421370b7d3d829c0df546779b1efa392fbfff42b455ac193e315e8db1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetPassword")
    def reset_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassword", []))

    @jsii.member(jsii_name="resetPublicKeys")
    def reset_public_keys(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicKeys", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="publicKeysInput")
    def public_keys_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "publicKeysInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81a98a256aabd350236168a212e998c3c71ba9f6cee3a6296fcc8ebd84dfa371)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b9b3e253555daf5eb32a0e98811e5d05340a480038ecab78212d01dde658fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="publicKeys")
    def public_keys(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "publicKeys"))

    @public_keys.setter
    def public_keys(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e843c9e8446ee0cb5c68e16f4eb4e359280e062e13182e2aa2fe260e9b81666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeys", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInitUser, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInitUser, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineCloudInitUser, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b36c3a32fb5d91b5e78c6a4e634506e87c380a62c48f6de13862420666c70a74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedDisks",
    jsii_struct_bases=[],
    name_mapping={
        "interface_type": "interfaceType",
        "position": "position",
        "size": "size",
        "storage": "storage",
        "discard": "discard",
        "file_format": "fileFormat",
        "speed_limits": "speedLimits",
        "ssd_emulation": "ssdEmulation",
        "use_iothread": "useIothread",
    },
)
class VirtualMachineComputedDisks:
    def __init__(
        self,
        *,
        interface_type: builtins.str,
        position: jsii.Number,
        size: jsii.Number,
        storage: builtins.str,
        discard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_format: typing.Optional[builtins.str] = None,
        speed_limits: typing.Optional[typing.Union[typing.Union["VirtualMachineComputedDisksSpeedLimits", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ssd_emulation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_iothread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param interface_type: The type of the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#interface_type VirtualMachine#interface_type}
        :param position: The position of the disk. (0, 1, 2, etc.) This is combined with the ``interface_type`` to determine the disk name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        :param size: The size of the disk in GiB. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#size VirtualMachine#size}
        :param storage: The storage the disk is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        :param discard: Whether the disk has discard enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#discard VirtualMachine#discard}
        :param file_format: The file format of the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#file_format VirtualMachine#file_format}
        :param speed_limits: The speed limits of the disk. If not set, no speed limitations are applied. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#speed_limits VirtualMachine#speed_limits}
        :param ssd_emulation: Whether to use SSD emulation. conflicts with virtio disk type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#ssd_emulation VirtualMachine#ssd_emulation}
        :param use_iothread: Whether to use an iothread for the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_iothread VirtualMachine#use_iothread}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6785625476108385ce505f0f23db686be2a224b16e5693c0c0f158eef3c60086)
            check_type(argname="argument interface_type", value=interface_type, expected_type=type_hints["interface_type"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument discard", value=discard, expected_type=type_hints["discard"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument speed_limits", value=speed_limits, expected_type=type_hints["speed_limits"])
            check_type(argname="argument ssd_emulation", value=ssd_emulation, expected_type=type_hints["ssd_emulation"])
            check_type(argname="argument use_iothread", value=use_iothread, expected_type=type_hints["use_iothread"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface_type": interface_type,
            "position": position,
            "size": size,
            "storage": storage,
        }
        if discard is not None:
            self._values["discard"] = discard
        if file_format is not None:
            self._values["file_format"] = file_format
        if speed_limits is not None:
            self._values["speed_limits"] = speed_limits
        if ssd_emulation is not None:
            self._values["ssd_emulation"] = ssd_emulation
        if use_iothread is not None:
            self._values["use_iothread"] = use_iothread

    @builtins.property
    def interface_type(self) -> builtins.str:
        '''The type of the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#interface_type VirtualMachine#interface_type}
        '''
        result = self._values.get("interface_type")
        assert result is not None, "Required property 'interface_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def position(self) -> jsii.Number:
        '''The position of the disk.

        (0, 1, 2, etc.) This is combined with the ``interface_type`` to determine the disk name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        '''
        result = self._values.get("position")
        assert result is not None, "Required property 'position' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''The size of the disk in GiB.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#size VirtualMachine#size}
        '''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage(self) -> builtins.str:
        '''The storage the disk is on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        '''
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def discard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the disk has discard enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#discard VirtualMachine#discard}
        '''
        result = self._values.get("discard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def file_format(self) -> typing.Optional[builtins.str]:
        '''The file format of the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#file_format VirtualMachine#file_format}
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speed_limits(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineComputedDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]]:
        '''The speed limits of the disk. If not set, no speed limitations are applied.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#speed_limits VirtualMachine#speed_limits}
        '''
        result = self._values.get("speed_limits")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineComputedDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssd_emulation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use SSD emulation. conflicts with virtio disk type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#ssd_emulation VirtualMachine#ssd_emulation}
        '''
        result = self._values.get("ssd_emulation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_iothread(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use an iothread for the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_iothread VirtualMachine#use_iothread}
        '''
        result = self._values.get("use_iothread")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineComputedDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineComputedDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedDisksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7bd507be149cc1484086c3f9ac1f6aec839a5c9dbb20c32d7c3302a1d6a3cf4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VirtualMachineComputedDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a41b9e64bf0a69fc661af4649b6335b43d2b8933755dbe6c2e60aa2d8984a09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineComputedDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53777c0e45a35e9d5238ca5ae56ead10b9f2050ed5cc5acd206d0b321b042d61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f306311e47229b84f5592b22cc9e86802726ea54720cd45b8e96c889446993eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__11f747fc8f52385dd5c1e37e0656e433346e1b5760e0a8bfc31b0073f413ba10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedDisks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedDisks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedDisks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bbb70064244356e5fc89b84f232dd172636247c8224376045a77652f68495fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachineComputedDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8f5439e113783b3521f2b3ecddd50323a01a6bd70bf47ea58a53e26f9d5d73a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSpeedLimits")
    def put_speed_limits(
        self,
        value: typing.Union[typing.Union["VirtualMachineComputedDisksSpeedLimits", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81f958e61a00fb22ec5ac21d98b5b3729bc27b4d2cfcd6fe92c25a58faca2c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSpeedLimits", [value]))

    @jsii.member(jsii_name="resetDiscard")
    def reset_discard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscard", []))

    @jsii.member(jsii_name="resetFileFormat")
    def reset_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileFormat", []))

    @jsii.member(jsii_name="resetSpeedLimits")
    def reset_speed_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeedLimits", []))

    @jsii.member(jsii_name="resetSsdEmulation")
    def reset_ssd_emulation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsdEmulation", []))

    @jsii.member(jsii_name="resetUseIothread")
    def reset_use_iothread(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseIothread", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="speedLimits")
    def speed_limits(self) -> "VirtualMachineComputedDisksSpeedLimitsOutputReference":
        return typing.cast("VirtualMachineComputedDisksSpeedLimitsOutputReference", jsii.get(self, "speedLimits"))

    @builtins.property
    @jsii.member(jsii_name="discardInput")
    def discard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "discardInput"))

    @builtins.property
    @jsii.member(jsii_name="fileFormatInput")
    def file_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceTypeInput")
    def interface_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="positionInput")
    def position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "positionInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="speedLimitsInput")
    def speed_limits_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineComputedDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineComputedDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "speedLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="ssdEmulationInput")
    def ssd_emulation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ssdEmulationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="useIothreadInput")
    def use_iothread_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useIothreadInput"))

    @builtins.property
    @jsii.member(jsii_name="discard")
    def discard(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "discard"))

    @discard.setter
    def discard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a825108c12c10e3f93a5cf543cd4d746e444d39b4642f1b63b854461a8b128)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discard", value)

    @builtins.property
    @jsii.member(jsii_name="fileFormat")
    def file_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileFormat"))

    @file_format.setter
    def file_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d815ea4f66a4199967562c634c1cf7609ac7f19c52c70f5830646767d20c43b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileFormat", value)

    @builtins.property
    @jsii.member(jsii_name="interfaceType")
    def interface_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceType"))

    @interface_type.setter
    def interface_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7f0ed3b103c839864fdb4ec3dc89ae1086536b945c6e386b12f3e3043597cdf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceType", value)

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6834fae9c96878886c6f35c065ce1418d7d448cf2effcfb089c2ac5d7234729e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value)

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ca70bd0ad323dfef56b3003a4d721473d6fab03ef3f88c4c7798b4118da775)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value)

    @builtins.property
    @jsii.member(jsii_name="ssdEmulation")
    def ssd_emulation(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ssdEmulation"))

    @ssd_emulation.setter
    def ssd_emulation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591d4f9a21fd44928a2bb9d205218af47a16e10ffec63adb74c285a9f151400a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssdEmulation", value)

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b4e0e6dad388cb1c0fcfd542f2c54dc18497ecb4911397a78c91e6db2946e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value)

    @builtins.property
    @jsii.member(jsii_name="useIothread")
    def use_iothread(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useIothread"))

    @use_iothread.setter
    def use_iothread(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2cdda4c18a48acf67675d4521ad6780c448bff28fac622690fbd132e04f230)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIothread", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VirtualMachineComputedDisks]:
        return typing.cast(typing.Optional[VirtualMachineComputedDisks], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineComputedDisks],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82d930ed85cd10c71d7c6d3e0f0877465798cdcad9e67296bd12ee7a61313249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedDisksSpeedLimits",
    jsii_struct_bases=[],
    name_mapping={
        "read": "read",
        "read_burstable": "readBurstable",
        "write": "write",
        "write_burstable": "writeBurstable",
    },
)
class VirtualMachineComputedDisksSpeedLimits:
    def __init__(
        self,
        *,
        read: typing.Optional[jsii.Number] = None,
        read_burstable: typing.Optional[jsii.Number] = None,
        write: typing.Optional[jsii.Number] = None,
        write_burstable: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param read: The read speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read VirtualMachine#read}
        :param read_burstable: The read burstable speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read_burstable VirtualMachine#read_burstable}
        :param write: The write speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write VirtualMachine#write}
        :param write_burstable: The write burstable speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write_burstable VirtualMachine#write_burstable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3779fb5e2ed08c127cab0434c70364ee8445a588bca109574dd2aec760ff981c)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument read_burstable", value=read_burstable, expected_type=type_hints["read_burstable"])
            check_type(argname="argument write", value=write, expected_type=type_hints["write"])
            check_type(argname="argument write_burstable", value=write_burstable, expected_type=type_hints["write_burstable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read
        if read_burstable is not None:
            self._values["read_burstable"] = read_burstable
        if write is not None:
            self._values["write"] = write
        if write_burstable is not None:
            self._values["write_burstable"] = write_burstable

    @builtins.property
    def read(self) -> typing.Optional[jsii.Number]:
        '''The read speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read VirtualMachine#read}
        '''
        result = self._values.get("read")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_burstable(self) -> typing.Optional[jsii.Number]:
        '''The read burstable speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read_burstable VirtualMachine#read_burstable}
        '''
        result = self._values.get("read_burstable")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write(self) -> typing.Optional[jsii.Number]:
        '''The write speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write VirtualMachine#write}
        '''
        result = self._values.get("write")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_burstable(self) -> typing.Optional[jsii.Number]:
        '''The write burstable speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write_burstable VirtualMachine#write_burstable}
        '''
        result = self._values.get("write_burstable")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineComputedDisksSpeedLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineComputedDisksSpeedLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedDisksSpeedLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e39c56631654e6f7f78544442c83ca17793436d08526aa4667af6d3fcc4868c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetReadBurstable")
    def reset_read_burstable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadBurstable", []))

    @jsii.member(jsii_name="resetWrite")
    def reset_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWrite", []))

    @jsii.member(jsii_name="resetWriteBurstable")
    def reset_write_burstable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteBurstable", []))

    @builtins.property
    @jsii.member(jsii_name="readBurstableInput")
    def read_burstable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readBurstableInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="writeBurstableInput")
    def write_burstable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeBurstableInput"))

    @builtins.property
    @jsii.member(jsii_name="writeInput")
    def write_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "read"))

    @read.setter
    def read(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b43f4bea54276ae0c6643f852dc96d4954d86c9e9459eadd969abbafa1b3ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="readBurstable")
    def read_burstable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readBurstable"))

    @read_burstable.setter
    def read_burstable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__469996e23b8d1c6189b8c7d057560618445177b3d32e5ee7d52de222848e1ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readBurstable", value)

    @builtins.property
    @jsii.member(jsii_name="write")
    def write(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "write"))

    @write.setter
    def write(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ef4eb9726df6efead8faf2e0564084db8f9ab047a53d3020e26c9c83390bb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "write", value)

    @builtins.property
    @jsii.member(jsii_name="writeBurstable")
    def write_burstable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "writeBurstable"))

    @write_burstable.setter
    def write_burstable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98cf5b6611a2da3fe299e9f9c61f167ea18395dc98c078198e3ed07129f9afa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeBurstable", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineComputedDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineComputedDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineComputedDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e9184644c9e74746bcc6f7f1e708765e446603377c5ad020c5ce48bb56fc017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={
        "bridge": "bridge",
        "position": "position",
        "enabled": "enabled",
        "mac_address": "macAddress",
        "model": "model",
        "mtu": "mtu",
        "rate_limit": "rateLimit",
        "use_firewall": "useFirewall",
        "vlan": "vlan",
    },
)
class VirtualMachineComputedNetworkInterfaces:
    def __init__(
        self,
        *,
        bridge: builtins.str,
        position: jsii.Number,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mac_address: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        rate_limit: typing.Optional[jsii.Number] = None,
        use_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vlan: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bridge: The bridge the network interface is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#bridge VirtualMachine#bridge}
        :param position: The position of the network interface in the VM as an int. Used to determine the interface name (net0, net1, etc). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        :param enabled: Whether the network interface is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#enabled VirtualMachine#enabled}
        :param mac_address: The MAC address of the network interface. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mac_address VirtualMachine#mac_address}
        :param model: The model of the network interface. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#model VirtualMachine#model}
        :param mtu: The MTU of the network interface. Only valid for virtio. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mtu VirtualMachine#mtu}
        :param rate_limit: The rate limit of the network interface in megabytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rate_limit VirtualMachine#rate_limit}
        :param use_firewall: Whether the firewall for the network interface is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_firewall VirtualMachine#use_firewall}
        :param vlan: The VLAN tag of the network interface. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#vlan VirtualMachine#vlan}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dc02c5c63992905ad270f0003bcd9556e892f52a9f4480a1e14edbe92350c2a)
            check_type(argname="argument bridge", value=bridge, expected_type=type_hints["bridge"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument mac_address", value=mac_address, expected_type=type_hints["mac_address"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
            check_type(argname="argument use_firewall", value=use_firewall, expected_type=type_hints["use_firewall"])
            check_type(argname="argument vlan", value=vlan, expected_type=type_hints["vlan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bridge": bridge,
            "position": position,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if mac_address is not None:
            self._values["mac_address"] = mac_address
        if model is not None:
            self._values["model"] = model
        if mtu is not None:
            self._values["mtu"] = mtu
        if rate_limit is not None:
            self._values["rate_limit"] = rate_limit
        if use_firewall is not None:
            self._values["use_firewall"] = use_firewall
        if vlan is not None:
            self._values["vlan"] = vlan

    @builtins.property
    def bridge(self) -> builtins.str:
        '''The bridge the network interface is on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#bridge VirtualMachine#bridge}
        '''
        result = self._values.get("bridge")
        assert result is not None, "Required property 'bridge' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def position(self) -> jsii.Number:
        '''The position of the network interface in the VM as an int.

        Used to determine the interface name (net0, net1, etc).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        '''
        result = self._values.get("position")
        assert result is not None, "Required property 'position' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the network interface is enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#enabled VirtualMachine#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mac_address(self) -> typing.Optional[builtins.str]:
        '''The MAC address of the network interface.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mac_address VirtualMachine#mac_address}
        '''
        result = self._values.get("mac_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''The model of the network interface.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#model VirtualMachine#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtu(self) -> typing.Optional[jsii.Number]:
        '''The MTU of the network interface. Only valid for virtio.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mtu VirtualMachine#mtu}
        '''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rate_limit(self) -> typing.Optional[jsii.Number]:
        '''The rate limit of the network interface in megabytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rate_limit VirtualMachine#rate_limit}
        '''
        result = self._values.get("rate_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_firewall(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the firewall for the network interface is enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_firewall VirtualMachine#use_firewall}
        '''
        result = self._values.get("use_firewall")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vlan(self) -> typing.Optional[jsii.Number]:
        '''The VLAN tag of the network interface.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#vlan VirtualMachine#vlan}
        '''
        result = self._values.get("vlan")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineComputedNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineComputedNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee4e225413051eba22f64b871b26203b383d88c56289b1f28c684b7a35d3e9c3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachineComputedNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76e98262b8b8d27da9b39fd2b806b7efd6d124bb47b11a46f1779bf5a03cc582)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineComputedNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593b490f01498a7f9011239bed4a4a1b7d761938f046796eaacd1db03de96a88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b43f27e5ed3c439140cba964a6006e5c16a701cba7598c677027f91fe5278591)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8f30313667499e06a5db1935c42bad7c1ea81fb7af11514272d4d637d07aa92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7432dcb7f675143c69b5b41bbca1bed808d4fc0a577d7e298d69924df6f2b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachineComputedNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a47ce6114bb4902f8658dcad2fe3d1fde71664f48c56531e6305845a2205c94)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMacAddress")
    def reset_mac_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacAddress", []))

    @jsii.member(jsii_name="resetModel")
    def reset_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModel", []))

    @jsii.member(jsii_name="resetMtu")
    def reset_mtu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtu", []))

    @jsii.member(jsii_name="resetRateLimit")
    def reset_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimit", []))

    @jsii.member(jsii_name="resetUseFirewall")
    def reset_use_firewall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseFirewall", []))

    @jsii.member(jsii_name="resetVlan")
    def reset_vlan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVlan", []))

    @builtins.property
    @jsii.member(jsii_name="bridgeInput")
    def bridge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bridgeInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="macAddressInput")
    def mac_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="modelInput")
    def model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="positionInput")
    def position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "positionInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitInput")
    def rate_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="useFirewallInput")
    def use_firewall_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useFirewallInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanInput")
    def vlan_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vlanInput"))

    @builtins.property
    @jsii.member(jsii_name="bridge")
    def bridge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bridge"))

    @bridge.setter
    def bridge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c6707bfe6b48dbdb32f163d3a2679cf65b370fdb9f4da20790bf506f5ee659)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bridge", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a208bb8bfb58fb2e89092b760e486fcc939051d533b2fbe2d9eec338f68f943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="macAddress")
    def mac_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macAddress"))

    @mac_address.setter
    def mac_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a15eac620b655b13a236b3c429d1ebb04f817a778955e14d377c7f328478d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macAddress", value)

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c4ba95191427e171e25c1f13148b02ab81173b751759e7392a27d96efbb253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value)

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b770c1c950551d3dd070cd42bb00aaf106a51ee7f8dba44f072582df217d167f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value)

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db0eb8934c80523b3d8c7d6f9c8bb5a00439aaa67d0629b80c278ac159483a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value)

    @builtins.property
    @jsii.member(jsii_name="rateLimit")
    def rate_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rateLimit"))

    @rate_limit.setter
    def rate_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e377ac2baf54f015f35dcaf42a87780aaaad81b7a803bfca858f1ef98a8b75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="useFirewall")
    def use_firewall(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useFirewall"))

    @use_firewall.setter
    def use_firewall(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a748fb1a1e64cf71c85932895032601c2b69fa9d5feed993a49e65019ec3aa39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFirewall", value)

    @builtins.property
    @jsii.member(jsii_name="vlan")
    def vlan(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlan"))

    @vlan.setter
    def vlan(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f78f6288cc42bb5ff4fe5070266050c5ff5a8a780de924f2914e3250652a4f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlan", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[VirtualMachineComputedNetworkInterfaces]:
        return typing.cast(typing.Optional[VirtualMachineComputedNetworkInterfaces], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineComputedNetworkInterfaces],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb62b1ca21aac0c1a2457d069833d8ebcfe5e4eca177e27c19585ef58aeb4d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedPciDevices",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "name": "name",
        "mdev": "mdev",
        "pcie": "pcie",
        "primary_gpu": "primaryGpu",
        "rombar": "rombar",
        "rom_file": "romFile",
    },
)
class VirtualMachineComputedPciDevices:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        mdev: typing.Optional[builtins.str] = None,
        pcie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        primary_gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rombar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rom_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The device ID of the PCI device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#id VirtualMachine#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The device name of the PCI device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        :param mdev: The mediated device name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mdev VirtualMachine#mdev}
        :param pcie: Whether the PCI device is PCIe. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#pcie VirtualMachine#pcie}
        :param primary_gpu: Whether the PCI device is the primary GPU. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#primary_gpu VirtualMachine#primary_gpu}
        :param rombar: Make the firmware room visible to the VM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rombar VirtualMachine#rombar}
        :param rom_file: The relative path to the ROM for the device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rom_file VirtualMachine#rom_file}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b074cb4cd644c928d0bd6c5e4ace6edd6fd01ee7edfdce03e66886170a8bcc)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mdev", value=mdev, expected_type=type_hints["mdev"])
            check_type(argname="argument pcie", value=pcie, expected_type=type_hints["pcie"])
            check_type(argname="argument primary_gpu", value=primary_gpu, expected_type=type_hints["primary_gpu"])
            check_type(argname="argument rombar", value=rombar, expected_type=type_hints["rombar"])
            check_type(argname="argument rom_file", value=rom_file, expected_type=type_hints["rom_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
        }
        if mdev is not None:
            self._values["mdev"] = mdev
        if pcie is not None:
            self._values["pcie"] = pcie
        if primary_gpu is not None:
            self._values["primary_gpu"] = primary_gpu
        if rombar is not None:
            self._values["rombar"] = rombar
        if rom_file is not None:
            self._values["rom_file"] = rom_file

    @builtins.property
    def id(self) -> builtins.str:
        '''The device ID of the PCI device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#id VirtualMachine#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The device name of the PCI device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mdev(self) -> typing.Optional[builtins.str]:
        '''The mediated device name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mdev VirtualMachine#mdev}
        '''
        result = self._values.get("mdev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pcie(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the PCI device is PCIe.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#pcie VirtualMachine#pcie}
        '''
        result = self._values.get("pcie")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def primary_gpu(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the PCI device is the primary GPU.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#primary_gpu VirtualMachine#primary_gpu}
        '''
        result = self._values.get("primary_gpu")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rombar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Make the firmware room visible to the VM.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rombar VirtualMachine#rombar}
        '''
        result = self._values.get("rombar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rom_file(self) -> typing.Optional[builtins.str]:
        '''The relative path to the ROM for the device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rom_file VirtualMachine#rom_file}
        '''
        result = self._values.get("rom_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineComputedPciDevices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineComputedPciDevicesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedPciDevicesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffbb75afa67e7d6395799b801453cf9f69d7fc91dec07e8703349d094863c8b1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachineComputedPciDevicesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788283e76f4ff2c91fe6e0dc97e29e20db0eecd6a1602fa5c1947b0f798e8fbc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineComputedPciDevicesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08ddc08a3f8202f6796315ca27e28d0f19903e12112c06f3d5d40c5b39b285f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e38a14e438a7ba5386e3c7df14f3d48971bb0090491e84095e5d3a40eccaea1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e979219e4cee7f983d1f89f694a7e6533811a3879daa1e44d38878fdba215f08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedPciDevices]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedPciDevices]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedPciDevices]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14257934fcd76ed64889c64e41c33f235c7dcb0d4a57e2c4b5a8805cb326a637)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachineComputedPciDevicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineComputedPciDevicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8b801bfbe6d45ee5533a8a2cb77f42e4b52ad7d5f7be267ef80aba28fe963df)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMdev")
    def reset_mdev(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMdev", []))

    @jsii.member(jsii_name="resetPcie")
    def reset_pcie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPcie", []))

    @jsii.member(jsii_name="resetPrimaryGpu")
    def reset_primary_gpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryGpu", []))

    @jsii.member(jsii_name="resetRombar")
    def reset_rombar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRombar", []))

    @jsii.member(jsii_name="resetRomFile")
    def reset_rom_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRomFile", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mdevInput")
    def mdev_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mdevInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pcieInput")
    def pcie_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pcieInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryGpuInput")
    def primary_gpu_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryGpuInput"))

    @builtins.property
    @jsii.member(jsii_name="rombarInput")
    def rombar_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rombarInput"))

    @builtins.property
    @jsii.member(jsii_name="romFileInput")
    def rom_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "romFileInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cccc97c1a6d4a54a13e34d6abb50ecea9dc52060eea4d4c9c273d2a994e48b3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mdev")
    def mdev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mdev"))

    @mdev.setter
    def mdev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b82e8516f0b56e3d2fbb96e6d8a2134219888c818e13f6b44768bd1a7f97661c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mdev", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aa00ba7ebda46f28707381995bc0800453f8118c702be0d31da5c972dec8320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pcie")
    def pcie(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pcie"))

    @pcie.setter
    def pcie(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a566e9f74842ef950146551b7ef027355a3ea49c965620f00a90d9580df4dd20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pcie", value)

    @builtins.property
    @jsii.member(jsii_name="primaryGpu")
    def primary_gpu(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryGpu"))

    @primary_gpu.setter
    def primary_gpu(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__874ba96c7ad1486e5b55a2a2c776db48ca909d0f3775706fec1c1678c93dc0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryGpu", value)

    @builtins.property
    @jsii.member(jsii_name="rombar")
    def rombar(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rombar"))

    @rombar.setter
    def rombar(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3744f55caf3b5e414fa0bf8bb67fbd6af95254f4c6b6d79d066b92651138ff48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rombar", value)

    @builtins.property
    @jsii.member(jsii_name="romFile")
    def rom_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "romFile"))

    @rom_file.setter
    def rom_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9abb866e36a1e220cb683bc43adb1d65a63b3a1f031e716d1d9dd577f785d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "romFile", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[VirtualMachineComputedPciDevices]:
        return typing.cast(typing.Optional[VirtualMachineComputedPciDevices], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[VirtualMachineComputedPciDevices],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe4b88b8f53c075a0520fddd6b46c45dae958b86399e0718c0a7a763d10e4db1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "node_attribute": "nodeAttribute",
        "agent": "agent",
        "bios": "bios",
        "clone": "clone",
        "cloud_init": "cloudInit",
        "cpu": "cpu",
        "description": "description",
        "disks": "disks",
        "id": "id",
        "iso": "iso",
        "keyboard_layout": "keyboardLayout",
        "kvm_arguments": "kvmArguments",
        "machine_type": "machineType",
        "memory": "memory",
        "name": "name",
        "network_interfaces": "networkInterfaces",
        "pci_devices": "pciDevices",
        "resource_pool": "resourcePool",
        "start_on_create": "startOnCreate",
        "start_on_node_boot": "startOnNodeBoot",
        "tags": "tags",
        "timeouts": "timeouts",
        "type": "type",
    },
)
class VirtualMachineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        node_attribute: builtins.str,
        agent: typing.Optional[typing.Union[typing.Union[VirtualMachineAgent, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        bios: typing.Optional[builtins.str] = None,
        clone: typing.Optional[typing.Union[typing.Union[VirtualMachineClone, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        cloud_init: typing.Optional[typing.Union[typing.Union[VirtualMachineCloudInit, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        cpu: typing.Optional[typing.Union[typing.Union["VirtualMachineCpu", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineDisks", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[jsii.Number] = None,
        iso: typing.Optional[typing.Union[typing.Union["VirtualMachineIso", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        keyboard_layout: typing.Optional[builtins.str] = None,
        kvm_arguments: typing.Optional[builtins.str] = None,
        machine_type: typing.Optional[builtins.str] = None,
        memory: typing.Optional[typing.Union[typing.Union["VirtualMachineMemory", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachineNetworkInterfaces", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pci_devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["VirtualMachinePciDevices", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_pool: typing.Optional[builtins.str] = None,
        start_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        start_on_node_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        timeouts: typing.Optional[typing.Union[typing.Union["VirtualMachineTimeouts", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param node_attribute: The node to create the virtual machine on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#node VirtualMachine#node}
        :param agent: The agent configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#agent VirtualMachine#agent}
        :param bios: The BIOS type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#bios VirtualMachine#bios}
        :param clone: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#clone VirtualMachine#clone}.
        :param cloud_init: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cloud_init VirtualMachine#cloud_init}.
        :param cpu: The CPU configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cpu VirtualMachine#cpu}
        :param description: The virtual machine description. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#description VirtualMachine#description}
        :param disks: The terrafrom generated disks attached to the VM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#disks VirtualMachine#disks}
        :param id: The identifier of the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#id VirtualMachine#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param iso: The operating system configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#iso VirtualMachine#iso}
        :param keyboard_layout: The keyboard layout. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#keyboard_layout VirtualMachine#keyboard_layout}
        :param kvm_arguments: The arguments to pass to KVM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#kvm_arguments VirtualMachine#kvm_arguments}
        :param machine_type: The machine type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#machine_type VirtualMachine#machine_type}
        :param memory: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#memory VirtualMachine#memory}.
        :param name: The name of the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        :param network_interfaces: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#network_interfaces VirtualMachine#network_interfaces}.
        :param pci_devices: PCI devices passed through to the VM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#pci_devices VirtualMachine#pci_devices}
        :param resource_pool: The resource pool the virtual machine is in. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#resource_pool VirtualMachine#resource_pool}
        :param start_on_create: Whether to start the virtual machine on creation. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start_on_create VirtualMachine#start_on_create}
        :param start_on_node_boot: Whether to start the virtual machine on node boot. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start_on_node_boot VirtualMachine#start_on_node_boot}
        :param tags: The tags of the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#tags VirtualMachine#tags}
        :param timeouts: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#timeouts VirtualMachine#timeouts}.
        :param type: The operating system type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#type VirtualMachine#type}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9990431c355c2efc5f62d35e8044c02343b4170dafff64740c6e60c8147fb768)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument node_attribute", value=node_attribute, expected_type=type_hints["node_attribute"])
            check_type(argname="argument agent", value=agent, expected_type=type_hints["agent"])
            check_type(argname="argument bios", value=bios, expected_type=type_hints["bios"])
            check_type(argname="argument clone", value=clone, expected_type=type_hints["clone"])
            check_type(argname="argument cloud_init", value=cloud_init, expected_type=type_hints["cloud_init"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disks", value=disks, expected_type=type_hints["disks"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument iso", value=iso, expected_type=type_hints["iso"])
            check_type(argname="argument keyboard_layout", value=keyboard_layout, expected_type=type_hints["keyboard_layout"])
            check_type(argname="argument kvm_arguments", value=kvm_arguments, expected_type=type_hints["kvm_arguments"])
            check_type(argname="argument machine_type", value=machine_type, expected_type=type_hints["machine_type"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_interfaces", value=network_interfaces, expected_type=type_hints["network_interfaces"])
            check_type(argname="argument pci_devices", value=pci_devices, expected_type=type_hints["pci_devices"])
            check_type(argname="argument resource_pool", value=resource_pool, expected_type=type_hints["resource_pool"])
            check_type(argname="argument start_on_create", value=start_on_create, expected_type=type_hints["start_on_create"])
            check_type(argname="argument start_on_node_boot", value=start_on_node_boot, expected_type=type_hints["start_on_node_boot"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if agent is not None:
            self._values["agent"] = agent
        if bios is not None:
            self._values["bios"] = bios
        if clone is not None:
            self._values["clone"] = clone
        if cloud_init is not None:
            self._values["cloud_init"] = cloud_init
        if cpu is not None:
            self._values["cpu"] = cpu
        if description is not None:
            self._values["description"] = description
        if disks is not None:
            self._values["disks"] = disks
        if id is not None:
            self._values["id"] = id
        if iso is not None:
            self._values["iso"] = iso
        if keyboard_layout is not None:
            self._values["keyboard_layout"] = keyboard_layout
        if kvm_arguments is not None:
            self._values["kvm_arguments"] = kvm_arguments
        if machine_type is not None:
            self._values["machine_type"] = machine_type
        if memory is not None:
            self._values["memory"] = memory
        if name is not None:
            self._values["name"] = name
        if network_interfaces is not None:
            self._values["network_interfaces"] = network_interfaces
        if pci_devices is not None:
            self._values["pci_devices"] = pci_devices
        if resource_pool is not None:
            self._values["resource_pool"] = resource_pool
        if start_on_create is not None:
            self._values["start_on_create"] = start_on_create
        if start_on_node_boot is not None:
            self._values["start_on_node_boot"] = start_on_node_boot
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if type is not None:
            self._values["type"] = type

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
    def node_attribute(self) -> builtins.str:
        '''The node to create the virtual machine on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#node VirtualMachine#node}
        '''
        result = self._values.get("node_attribute")
        assert result is not None, "Required property 'node_attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineAgent, _cdktf_9a9027ec.IResolvable]]:
        '''The agent configuration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#agent VirtualMachine#agent}
        '''
        result = self._values.get("agent")
        return typing.cast(typing.Optional[typing.Union[VirtualMachineAgent, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def bios(self) -> typing.Optional[builtins.str]:
        '''The BIOS type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#bios VirtualMachine#bios}
        '''
        result = self._values.get("bios")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clone(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineClone, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#clone VirtualMachine#clone}.'''
        result = self._values.get("clone")
        return typing.cast(typing.Optional[typing.Union[VirtualMachineClone, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cloud_init(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCloudInit, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cloud_init VirtualMachine#cloud_init}.'''
        result = self._values.get("cloud_init")
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCloudInit, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cpu(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineCpu", _cdktf_9a9027ec.IResolvable]]:
        '''The CPU configuration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cpu VirtualMachine#cpu}
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineCpu", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The virtual machine description.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#description VirtualMachine#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disks(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineDisks"]]]:
        '''The terrafrom generated disks attached to the VM.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#disks VirtualMachine#disks}
        '''
        result = self._values.get("disks")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineDisks"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[jsii.Number]:
        '''The identifier of the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#id VirtualMachine#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def iso(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineIso", _cdktf_9a9027ec.IResolvable]]:
        '''The operating system configuration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#iso VirtualMachine#iso}
        '''
        result = self._values.get("iso")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineIso", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def keyboard_layout(self) -> typing.Optional[builtins.str]:
        '''The keyboard layout.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#keyboard_layout VirtualMachine#keyboard_layout}
        '''
        result = self._values.get("keyboard_layout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kvm_arguments(self) -> typing.Optional[builtins.str]:
        '''The arguments to pass to KVM.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#kvm_arguments VirtualMachine#kvm_arguments}
        '''
        result = self._values.get("kvm_arguments")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def machine_type(self) -> typing.Optional[builtins.str]:
        '''The machine type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#machine_type VirtualMachine#machine_type}
        '''
        result = self._values.get("machine_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def memory(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineMemory", _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#memory VirtualMachine#memory}.'''
        result = self._values.get("memory")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineMemory", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_interfaces(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineNetworkInterfaces"]]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#network_interfaces VirtualMachine#network_interfaces}.'''
        result = self._values.get("network_interfaces")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachineNetworkInterfaces"]]], result)

    @builtins.property
    def pci_devices(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePciDevices"]]]:
        '''PCI devices passed through to the VM.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#pci_devices VirtualMachine#pci_devices}
        '''
        result = self._values.get("pci_devices")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["VirtualMachinePciDevices"]]], result)

    @builtins.property
    def resource_pool(self) -> typing.Optional[builtins.str]:
        '''The resource pool the virtual machine is in.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#resource_pool VirtualMachine#resource_pool}
        '''
        result = self._values.get("resource_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_on_create(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to start the virtual machine on creation.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start_on_create VirtualMachine#start_on_create}
        '''
        result = self._values.get("start_on_create")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def start_on_node_boot(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to start the virtual machine on node boot.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start_on_node_boot VirtualMachine#start_on_node_boot}
        '''
        result = self._values.get("start_on_node_boot")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The tags of the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#tags VirtualMachine#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineTimeouts", _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#timeouts VirtualMachine#timeouts}.'''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineTimeouts", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The operating system type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#type VirtualMachine#type}
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCpu",
    jsii_struct_bases=[],
    name_mapping={
        "architecture": "architecture",
        "cores": "cores",
        "cpu_units": "cpuUnits",
        "emulated_type": "emulatedType",
        "sockets": "sockets",
    },
)
class VirtualMachineCpu:
    def __init__(
        self,
        *,
        architecture: typing.Optional[builtins.str] = None,
        cores: typing.Optional[jsii.Number] = None,
        cpu_units: typing.Optional[jsii.Number] = None,
        emulated_type: typing.Optional[builtins.str] = None,
        sockets: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param architecture: The CPU architecture. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#architecture VirtualMachine#architecture}
        :param cores: The number of CPU cores. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cores VirtualMachine#cores}
        :param cpu_units: The CPU units. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cpu_units VirtualMachine#cpu_units}
        :param emulated_type: The emulated CPU type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#emulated_type VirtualMachine#emulated_type}
        :param sockets: The number of CPU sockets. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#sockets VirtualMachine#sockets}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f0eea8df55b8cc1b0e1bbfe67406ea841216184849bd1a3249d227a48215f54)
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument cores", value=cores, expected_type=type_hints["cores"])
            check_type(argname="argument cpu_units", value=cpu_units, expected_type=type_hints["cpu_units"])
            check_type(argname="argument emulated_type", value=emulated_type, expected_type=type_hints["emulated_type"])
            check_type(argname="argument sockets", value=sockets, expected_type=type_hints["sockets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if architecture is not None:
            self._values["architecture"] = architecture
        if cores is not None:
            self._values["cores"] = cores
        if cpu_units is not None:
            self._values["cpu_units"] = cpu_units
        if emulated_type is not None:
            self._values["emulated_type"] = emulated_type
        if sockets is not None:
            self._values["sockets"] = sockets

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The CPU architecture.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#architecture VirtualMachine#architecture}
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cores(self) -> typing.Optional[jsii.Number]:
        '''The number of CPU cores.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cores VirtualMachine#cores}
        '''
        result = self._values.get("cores")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_units(self) -> typing.Optional[jsii.Number]:
        '''The CPU units.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#cpu_units VirtualMachine#cpu_units}
        '''
        result = self._values.get("cpu_units")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def emulated_type(self) -> typing.Optional[builtins.str]:
        '''The emulated CPU type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#emulated_type VirtualMachine#emulated_type}
        '''
        result = self._values.get("emulated_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sockets(self) -> typing.Optional[jsii.Number]:
        '''The number of CPU sockets.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#sockets VirtualMachine#sockets}
        '''
        result = self._values.get("sockets")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineCpu(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineCpuOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineCpuOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ae03c501033e794a8af411d4f12ba8516f44453e5673076b2b61c69057bf441c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetArchitecture")
    def reset_architecture(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetArchitecture", []))

    @jsii.member(jsii_name="resetCores")
    def reset_cores(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCores", []))

    @jsii.member(jsii_name="resetCpuUnits")
    def reset_cpu_units(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCpuUnits", []))

    @jsii.member(jsii_name="resetEmulatedType")
    def reset_emulated_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEmulatedType", []))

    @jsii.member(jsii_name="resetSockets")
    def reset_sockets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSockets", []))

    @builtins.property
    @jsii.member(jsii_name="architectureInput")
    def architecture_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architectureInput"))

    @builtins.property
    @jsii.member(jsii_name="coresInput")
    def cores_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "coresInput"))

    @builtins.property
    @jsii.member(jsii_name="cpuUnitsInput")
    def cpu_units_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuUnitsInput"))

    @builtins.property
    @jsii.member(jsii_name="emulatedTypeInput")
    def emulated_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "emulatedTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="socketsInput")
    def sockets_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "socketsInput"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e8f713aacbf0604d35e46ffafc7551f0daff028f95e0f77081e439fbfd2ec64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value)

    @builtins.property
    @jsii.member(jsii_name="cores")
    def cores(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cores"))

    @cores.setter
    def cores(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a92d0a25b5e4725d08c55c37e492ecb30bb8e2ea2099692ffb673e1d428c4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cores", value)

    @builtins.property
    @jsii.member(jsii_name="cpuUnits")
    def cpu_units(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "cpuUnits"))

    @cpu_units.setter
    def cpu_units(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb71acbd172dbd833a324f004547099cb20055009552e8566ee04bbea571a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cpuUnits", value)

    @builtins.property
    @jsii.member(jsii_name="emulatedType")
    def emulated_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "emulatedType"))

    @emulated_type.setter
    def emulated_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5dcbfb4d8c7904d4042685ccf1240808ced51cc6176e8ea3575a3b3e0b4e64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emulatedType", value)

    @builtins.property
    @jsii.member(jsii_name="sockets")
    def sockets(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sockets"))

    @sockets.setter
    def sockets(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040f57604e7b3172f7848bf0bd1acf46c99d7d2e6a3203f5606e8515d8c3362f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sockets", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineCpu, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineCpu, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineCpu, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ba34adb23f4c9b2dbe1ec09215d4e5cab77191ad47ade8ac7af5648484d0ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineDisks",
    jsii_struct_bases=[],
    name_mapping={
        "interface_type": "interfaceType",
        "position": "position",
        "size": "size",
        "storage": "storage",
        "discard": "discard",
        "file_format": "fileFormat",
        "speed_limits": "speedLimits",
        "ssd_emulation": "ssdEmulation",
        "use_iothread": "useIothread",
    },
)
class VirtualMachineDisks:
    def __init__(
        self,
        *,
        interface_type: builtins.str,
        position: jsii.Number,
        size: jsii.Number,
        storage: builtins.str,
        discard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        file_format: typing.Optional[builtins.str] = None,
        speed_limits: typing.Optional[typing.Union[typing.Union["VirtualMachineDisksSpeedLimits", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
        ssd_emulation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_iothread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param interface_type: The type of the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#interface_type VirtualMachine#interface_type}
        :param position: The position of the disk. (0, 1, 2, etc.) This is combined with the ``interface_type`` to determine the disk name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        :param size: The size of the disk in GiB. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#size VirtualMachine#size}
        :param storage: The storage the disk is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        :param discard: Whether the disk has discard enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#discard VirtualMachine#discard}
        :param file_format: The file format of the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#file_format VirtualMachine#file_format}
        :param speed_limits: The speed limits of the disk. If not set, no speed limitations are applied. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#speed_limits VirtualMachine#speed_limits}
        :param ssd_emulation: Whether to use SSD emulation. conflicts with virtio disk type. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#ssd_emulation VirtualMachine#ssd_emulation}
        :param use_iothread: Whether to use an iothread for the disk. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_iothread VirtualMachine#use_iothread}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__724516c81760f160a0baa82bf1df356572b1396b407f8e6aa3bdbefc0164510e)
            check_type(argname="argument interface_type", value=interface_type, expected_type=type_hints["interface_type"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument discard", value=discard, expected_type=type_hints["discard"])
            check_type(argname="argument file_format", value=file_format, expected_type=type_hints["file_format"])
            check_type(argname="argument speed_limits", value=speed_limits, expected_type=type_hints["speed_limits"])
            check_type(argname="argument ssd_emulation", value=ssd_emulation, expected_type=type_hints["ssd_emulation"])
            check_type(argname="argument use_iothread", value=use_iothread, expected_type=type_hints["use_iothread"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "interface_type": interface_type,
            "position": position,
            "size": size,
            "storage": storage,
        }
        if discard is not None:
            self._values["discard"] = discard
        if file_format is not None:
            self._values["file_format"] = file_format
        if speed_limits is not None:
            self._values["speed_limits"] = speed_limits
        if ssd_emulation is not None:
            self._values["ssd_emulation"] = ssd_emulation
        if use_iothread is not None:
            self._values["use_iothread"] = use_iothread

    @builtins.property
    def interface_type(self) -> builtins.str:
        '''The type of the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#interface_type VirtualMachine#interface_type}
        '''
        result = self._values.get("interface_type")
        assert result is not None, "Required property 'interface_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def position(self) -> jsii.Number:
        '''The position of the disk.

        (0, 1, 2, etc.) This is combined with the ``interface_type`` to determine the disk name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        '''
        result = self._values.get("position")
        assert result is not None, "Required property 'position' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def size(self) -> jsii.Number:
        '''The size of the disk in GiB.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#size VirtualMachine#size}
        '''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage(self) -> builtins.str:
        '''The storage the disk is on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        '''
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def discard(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the disk has discard enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#discard VirtualMachine#discard}
        '''
        result = self._values.get("discard")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def file_format(self) -> typing.Optional[builtins.str]:
        '''The file format of the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#file_format VirtualMachine#file_format}
        '''
        result = self._values.get("file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def speed_limits(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]]:
        '''The speed limits of the disk. If not set, no speed limitations are applied.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#speed_limits VirtualMachine#speed_limits}
        '''
        result = self._values.get("speed_limits")
        return typing.cast(typing.Optional[typing.Union["VirtualMachineDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ssd_emulation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use SSD emulation. conflicts with virtio disk type.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#ssd_emulation VirtualMachine#ssd_emulation}
        '''
        result = self._values.get("ssd_emulation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_iothread(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to use an iothread for the disk.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_iothread VirtualMachine#use_iothread}
        '''
        result = self._values.get("use_iothread")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineDisks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineDisksList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineDisksList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4137fcc557d93c6e6c54528f329acd5e490a206a0e43355e87a7f1423042dbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VirtualMachineDisksOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09a3a99e4fd8a2d5f6a200e724a8be26e8832ede3b9d96b737299f0f29ee51b9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineDisksOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472c17240c719bd9e09e66d17985f2b7a2d23cb5b0c9be6a2d85909472cd0404)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6c6c62c26b288418245539b79004b040b0a59e6ff4e666ce183fe182ecfe41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13e55c40d5b9de1fed7d79e353ede56d0857910556e31983983ed68adb9d7cbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineDisks]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineDisks]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineDisks]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26d8556ae50ac5b8093a73ced226d8ecac249084144d7e29061e51fd2111ee1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachineDisksOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineDisksOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dd5a32a75ffe345bf2e3f05c865d141f49587ba6d47dfc361a5567625023dbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putSpeedLimits")
    def put_speed_limits(
        self,
        value: typing.Union[typing.Union["VirtualMachineDisksSpeedLimits", typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8158207d21c5b18d20ebca7155e9bc24d0837a11b329468ad7dc773e830cf056)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSpeedLimits", [value]))

    @jsii.member(jsii_name="resetDiscard")
    def reset_discard(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiscard", []))

    @jsii.member(jsii_name="resetFileFormat")
    def reset_file_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileFormat", []))

    @jsii.member(jsii_name="resetSpeedLimits")
    def reset_speed_limits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeedLimits", []))

    @jsii.member(jsii_name="resetSsdEmulation")
    def reset_ssd_emulation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsdEmulation", []))

    @jsii.member(jsii_name="resetUseIothread")
    def reset_use_iothread(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseIothread", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="speedLimits")
    def speed_limits(self) -> "VirtualMachineDisksSpeedLimitsOutputReference":
        return typing.cast("VirtualMachineDisksSpeedLimitsOutputReference", jsii.get(self, "speedLimits"))

    @builtins.property
    @jsii.member(jsii_name="discardInput")
    def discard_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "discardInput"))

    @builtins.property
    @jsii.member(jsii_name="fileFormatInput")
    def file_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceTypeInput")
    def interface_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="positionInput")
    def position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "positionInput"))

    @builtins.property
    @jsii.member(jsii_name="sizeInput")
    def size_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sizeInput"))

    @builtins.property
    @jsii.member(jsii_name="speedLimitsInput")
    def speed_limits_input(
        self,
    ) -> typing.Optional[typing.Union["VirtualMachineDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["VirtualMachineDisksSpeedLimits", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "speedLimitsInput"))

    @builtins.property
    @jsii.member(jsii_name="ssdEmulationInput")
    def ssd_emulation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ssdEmulationInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="useIothreadInput")
    def use_iothread_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useIothreadInput"))

    @builtins.property
    @jsii.member(jsii_name="discard")
    def discard(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "discard"))

    @discard.setter
    def discard(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190dd236495a455d1402bfdc14ea26b12213cc6e6e95004303146ad4d681f521)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "discard", value)

    @builtins.property
    @jsii.member(jsii_name="fileFormat")
    def file_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileFormat"))

    @file_format.setter
    def file_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9013a43d9aaab7b3f9bc168daaf4b5db01cbde6ca834158f0ed9e4db174b5a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileFormat", value)

    @builtins.property
    @jsii.member(jsii_name="interfaceType")
    def interface_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceType"))

    @interface_type.setter
    def interface_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19febc2b2d2cd0a53fe4d7744e71ef322359bcac79a2b6566deacf242f688c90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceType", value)

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02ec1c8055848e3a6fa8a6a92b1a6498288d13dea82ef678df94d88af732ee9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value)

    @builtins.property
    @jsii.member(jsii_name="size")
    def size(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "size"))

    @size.setter
    def size(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a78aa77220938d303c8dd7d6c52d60934da0fc8ec42fe7c72b3c6c80ca7b0e58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "size", value)

    @builtins.property
    @jsii.member(jsii_name="ssdEmulation")
    def ssd_emulation(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ssdEmulation"))

    @ssd_emulation.setter
    def ssd_emulation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07687ece05f3cdbcdf3c8823f33b9defcd39647e051fb38a688ae4cf26234487)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssdEmulation", value)

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52e1b97909033046728ff40a40bc10be81400020d72fc1516872eb20e2f7c50a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value)

    @builtins.property
    @jsii.member(jsii_name="useIothread")
    def use_iothread(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useIothread"))

    @use_iothread.setter
    def use_iothread(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5e7c4c71e9fe30d23e90a786a267bfbca33baf4925f5a0fc0a5658569360de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useIothread", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineDisks, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineDisks, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineDisks, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83553b29b869338c2fe30547cf52dc266012b7a7ba61230b95109fcda8c9c435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineDisksSpeedLimits",
    jsii_struct_bases=[],
    name_mapping={
        "read": "read",
        "read_burstable": "readBurstable",
        "write": "write",
        "write_burstable": "writeBurstable",
    },
)
class VirtualMachineDisksSpeedLimits:
    def __init__(
        self,
        *,
        read: typing.Optional[jsii.Number] = None,
        read_burstable: typing.Optional[jsii.Number] = None,
        write: typing.Optional[jsii.Number] = None,
        write_burstable: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param read: The read speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read VirtualMachine#read}
        :param read_burstable: The read burstable speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read_burstable VirtualMachine#read_burstable}
        :param write: The write speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write VirtualMachine#write}
        :param write_burstable: The write burstable speed limit in bytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write_burstable VirtualMachine#write_burstable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e64b1544b8f0e9fe1b73225cb7e526b53e2d770504847686dbeacedd93e2cfc5)
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument read_burstable", value=read_burstable, expected_type=type_hints["read_burstable"])
            check_type(argname="argument write", value=write, expected_type=type_hints["write"])
            check_type(argname="argument write_burstable", value=write_burstable, expected_type=type_hints["write_burstable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if read is not None:
            self._values["read"] = read
        if read_burstable is not None:
            self._values["read_burstable"] = read_burstable
        if write is not None:
            self._values["write"] = write
        if write_burstable is not None:
            self._values["write_burstable"] = write_burstable

    @builtins.property
    def read(self) -> typing.Optional[jsii.Number]:
        '''The read speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read VirtualMachine#read}
        '''
        result = self._values.get("read")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def read_burstable(self) -> typing.Optional[jsii.Number]:
        '''The read burstable speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#read_burstable VirtualMachine#read_burstable}
        '''
        result = self._values.get("read_burstable")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write(self) -> typing.Optional[jsii.Number]:
        '''The write speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write VirtualMachine#write}
        '''
        result = self._values.get("write")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def write_burstable(self) -> typing.Optional[jsii.Number]:
        '''The write burstable speed limit in bytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#write_burstable VirtualMachine#write_burstable}
        '''
        result = self._values.get("write_burstable")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineDisksSpeedLimits(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineDisksSpeedLimitsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineDisksSpeedLimitsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__acb6c0c1bbc483013acadf83c2afc7333747ea1f60b0b70e3b83bfdc07dcacdd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetReadBurstable")
    def reset_read_burstable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadBurstable", []))

    @jsii.member(jsii_name="resetWrite")
    def reset_write(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWrite", []))

    @jsii.member(jsii_name="resetWriteBurstable")
    def reset_write_burstable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWriteBurstable", []))

    @builtins.property
    @jsii.member(jsii_name="readBurstableInput")
    def read_burstable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readBurstableInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="writeBurstableInput")
    def write_burstable_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeBurstableInput"))

    @builtins.property
    @jsii.member(jsii_name="writeInput")
    def write_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "writeInput"))

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "read"))

    @read.setter
    def read(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7faa6a04553ed658e498f4d553d547c66a1a93f341ebc0b63bc8b0f1a721654a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="readBurstable")
    def read_burstable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readBurstable"))

    @read_burstable.setter
    def read_burstable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc64fcb1ebd82dbbe08d59e291bad7d54c3165c496aebe1b3ea20c66fee7aaa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readBurstable", value)

    @builtins.property
    @jsii.member(jsii_name="write")
    def write(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "write"))

    @write.setter
    def write(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5abb6ca2d1696740392687835956eb0588d1430ce4410e46739d69cfcd01fd65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "write", value)

    @builtins.property
    @jsii.member(jsii_name="writeBurstable")
    def write_burstable(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "writeBurstable"))

    @write_burstable.setter
    def write_burstable(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f8129f5c21ccc4904fef692bf3163de419fe36d22c1a931f04126ab9cb1b93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "writeBurstable", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c567b5c4be7eac3391e9c02d3f2e8612c44638fa17643e86970abadc0b0a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineIso",
    jsii_struct_bases=[],
    name_mapping={"image": "image", "storage": "storage"},
)
class VirtualMachineIso:
    def __init__(self, *, image: builtins.str, storage: builtins.str) -> None:
        '''
        :param image: The image to use for install media. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#image VirtualMachine#image}
        :param storage: The storage to place install media on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d380de2f8fb0523f0767e791573e4c06f84569a07d9b52bef0c15b92041a1dbd)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
            "storage": storage,
        }

    @builtins.property
    def image(self) -> builtins.str:
        '''The image to use for install media.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#image VirtualMachine#image}
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage(self) -> builtins.str:
        '''The storage to place install media on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#storage VirtualMachine#storage}
        '''
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineIso(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineIsoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineIsoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__78c387aad931cd68402d666f18945aeb29e378f66931ca2b943c48557fec97e9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="imageInput")
    def image_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageInput"))

    @builtins.property
    @jsii.member(jsii_name="storageInput")
    def storage_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageInput"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "image"))

    @image.setter
    def image(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d9a9413b71d687c1bbf794a5e98e42f62ce18f68366be2763bc596686a8df5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "image", value)

    @builtins.property
    @jsii.member(jsii_name="storage")
    def storage(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storage"))

    @storage.setter
    def storage(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b1b1cb81d0cec44a2d0f38196699d5329e1612bbe6189256c11796428d5f258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storage", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineIso, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineIso, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineIso, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4968b44a96abd7ffead827bef3c3e218d134e0f9cdeeb910b1014afb5b152690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineMemory",
    jsii_struct_bases=[],
    name_mapping={
        "dedicated": "dedicated",
        "floating": "floating",
        "shared": "shared",
    },
)
class VirtualMachineMemory:
    def __init__(
        self,
        *,
        dedicated: typing.Optional[jsii.Number] = None,
        floating: typing.Optional[jsii.Number] = None,
        shared: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param dedicated: The size of the memory in MB. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dedicated VirtualMachine#dedicated}
        :param floating: The floating memory in MB. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#floating VirtualMachine#floating}
        :param shared: The shared memory in MB. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#shared VirtualMachine#shared}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0974684686bffa5982faef71322e60afee854e57667f695bbf976fdb7cce61e)
            check_type(argname="argument dedicated", value=dedicated, expected_type=type_hints["dedicated"])
            check_type(argname="argument floating", value=floating, expected_type=type_hints["floating"])
            check_type(argname="argument shared", value=shared, expected_type=type_hints["shared"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dedicated is not None:
            self._values["dedicated"] = dedicated
        if floating is not None:
            self._values["floating"] = floating
        if shared is not None:
            self._values["shared"] = shared

    @builtins.property
    def dedicated(self) -> typing.Optional[jsii.Number]:
        '''The size of the memory in MB.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#dedicated VirtualMachine#dedicated}
        '''
        result = self._values.get("dedicated")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def floating(self) -> typing.Optional[jsii.Number]:
        '''The floating memory in MB.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#floating VirtualMachine#floating}
        '''
        result = self._values.get("floating")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shared(self) -> typing.Optional[jsii.Number]:
        '''The shared memory in MB.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#shared VirtualMachine#shared}
        '''
        result = self._values.get("shared")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineMemory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineMemoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineMemoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b850f8b283b0c0b94ec50ed03f029e6289ae997a8284bb3ad726925c4ef85e55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDedicated")
    def reset_dedicated(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDedicated", []))

    @jsii.member(jsii_name="resetFloating")
    def reset_floating(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFloating", []))

    @jsii.member(jsii_name="resetShared")
    def reset_shared(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShared", []))

    @builtins.property
    @jsii.member(jsii_name="dedicatedInput")
    def dedicated_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dedicatedInput"))

    @builtins.property
    @jsii.member(jsii_name="floatingInput")
    def floating_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "floatingInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedInput")
    def shared_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sharedInput"))

    @builtins.property
    @jsii.member(jsii_name="dedicated")
    def dedicated(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dedicated"))

    @dedicated.setter
    def dedicated(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ee26619b484718c06edb22281785ed4a20579f084261e62b0fd4f0495a7628b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dedicated", value)

    @builtins.property
    @jsii.member(jsii_name="floating")
    def floating(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "floating"))

    @floating.setter
    def floating(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ccc329cd748645a85b6316f6b4b107efe77c15173abbe9e070375da5c649176)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "floating", value)

    @builtins.property
    @jsii.member(jsii_name="shared")
    def shared(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shared"))

    @shared.setter
    def shared(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__431b4a2379d1900eb31fb1d8a9da4cd3e5a958f3bdfc9c8280f4be3d5de71dc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shared", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineMemory, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineMemory, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineMemory, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2264f2d62c16fa75dd9d5aed81aa1c44fea980fd2fadea041420429774c3ab81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineNetworkInterfaces",
    jsii_struct_bases=[],
    name_mapping={
        "bridge": "bridge",
        "position": "position",
        "enabled": "enabled",
        "mac_address": "macAddress",
        "model": "model",
        "mtu": "mtu",
        "rate_limit": "rateLimit",
        "use_firewall": "useFirewall",
        "vlan": "vlan",
    },
)
class VirtualMachineNetworkInterfaces:
    def __init__(
        self,
        *,
        bridge: builtins.str,
        position: jsii.Number,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        mac_address: typing.Optional[builtins.str] = None,
        model: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        rate_limit: typing.Optional[jsii.Number] = None,
        use_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vlan: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bridge: The bridge the network interface is on. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#bridge VirtualMachine#bridge}
        :param position: The position of the network interface in the VM as an int. Used to determine the interface name (net0, net1, etc). Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        :param enabled: Whether the network interface is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#enabled VirtualMachine#enabled}
        :param mac_address: The MAC address of the network interface. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mac_address VirtualMachine#mac_address}
        :param model: The model of the network interface. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#model VirtualMachine#model}
        :param mtu: The MTU of the network interface. Only valid for virtio. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mtu VirtualMachine#mtu}
        :param rate_limit: The rate limit of the network interface in megabytes per second. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rate_limit VirtualMachine#rate_limit}
        :param use_firewall: Whether the firewall for the network interface is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_firewall VirtualMachine#use_firewall}
        :param vlan: The VLAN tag of the network interface. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#vlan VirtualMachine#vlan}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8840af80bb4afb00569be8b14daa1c429616c64477b5a1c7664b182ed951cb63)
            check_type(argname="argument bridge", value=bridge, expected_type=type_hints["bridge"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument mac_address", value=mac_address, expected_type=type_hints["mac_address"])
            check_type(argname="argument model", value=model, expected_type=type_hints["model"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument rate_limit", value=rate_limit, expected_type=type_hints["rate_limit"])
            check_type(argname="argument use_firewall", value=use_firewall, expected_type=type_hints["use_firewall"])
            check_type(argname="argument vlan", value=vlan, expected_type=type_hints["vlan"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bridge": bridge,
            "position": position,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if mac_address is not None:
            self._values["mac_address"] = mac_address
        if model is not None:
            self._values["model"] = model
        if mtu is not None:
            self._values["mtu"] = mtu
        if rate_limit is not None:
            self._values["rate_limit"] = rate_limit
        if use_firewall is not None:
            self._values["use_firewall"] = use_firewall
        if vlan is not None:
            self._values["vlan"] = vlan

    @builtins.property
    def bridge(self) -> builtins.str:
        '''The bridge the network interface is on.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#bridge VirtualMachine#bridge}
        '''
        result = self._values.get("bridge")
        assert result is not None, "Required property 'bridge' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def position(self) -> jsii.Number:
        '''The position of the network interface in the VM as an int.

        Used to determine the interface name (net0, net1, etc).

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#position VirtualMachine#position}
        '''
        result = self._values.get("position")
        assert result is not None, "Required property 'position' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the network interface is enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#enabled VirtualMachine#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def mac_address(self) -> typing.Optional[builtins.str]:
        '''The MAC address of the network interface.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mac_address VirtualMachine#mac_address}
        '''
        result = self._values.get("mac_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model(self) -> typing.Optional[builtins.str]:
        '''The model of the network interface.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#model VirtualMachine#model}
        '''
        result = self._values.get("model")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtu(self) -> typing.Optional[jsii.Number]:
        '''The MTU of the network interface. Only valid for virtio.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mtu VirtualMachine#mtu}
        '''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def rate_limit(self) -> typing.Optional[jsii.Number]:
        '''The rate limit of the network interface in megabytes per second.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rate_limit VirtualMachine#rate_limit}
        '''
        result = self._values.get("rate_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_firewall(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the firewall for the network interface is enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#use_firewall VirtualMachine#use_firewall}
        '''
        result = self._values.get("use_firewall")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vlan(self) -> typing.Optional[jsii.Number]:
        '''The VLAN tag of the network interface.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#vlan VirtualMachine#vlan}
        '''
        result = self._values.get("vlan")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineNetworkInterfaces(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineNetworkInterfacesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineNetworkInterfacesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccfc8e560878f0aae146c0283376ef3c708f1084bde4c80e63fe2f76979e59bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "VirtualMachineNetworkInterfacesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c86c7fda67850ceff00d45ec1793b79a88016b1c61cf7e3a59471dc44f8d7ba)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachineNetworkInterfacesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5bfd81fd69caf460854936e11268d4af0f1ec43b652b69c231cf9d8c650506)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15322702066575a81f3e30a319b5d30b31005435e8809765f1d04ae5526dbeb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a813baeca869b833140dcbfeabeef6fe605ec0922d9a3772fa288ee58e03a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineNetworkInterfaces]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineNetworkInterfaces]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineNetworkInterfaces]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb1abe4ef7b50ef924866dd6b0e9cae743684a8ed8317d73fd8e2ee86072845c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachineNetworkInterfacesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineNetworkInterfacesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb16262d16bc9851ed7d089f06a87326307b0df5da7e64e0a80b2038162fe5ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetMacAddress")
    def reset_mac_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMacAddress", []))

    @jsii.member(jsii_name="resetModel")
    def reset_model(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModel", []))

    @jsii.member(jsii_name="resetMtu")
    def reset_mtu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtu", []))

    @jsii.member(jsii_name="resetRateLimit")
    def reset_rate_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRateLimit", []))

    @jsii.member(jsii_name="resetUseFirewall")
    def reset_use_firewall(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseFirewall", []))

    @jsii.member(jsii_name="resetVlan")
    def reset_vlan(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVlan", []))

    @builtins.property
    @jsii.member(jsii_name="bridgeInput")
    def bridge_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bridgeInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="macAddressInput")
    def mac_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "macAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="modelInput")
    def model_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="positionInput")
    def position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "positionInput"))

    @builtins.property
    @jsii.member(jsii_name="rateLimitInput")
    def rate_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rateLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="useFirewallInput")
    def use_firewall_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useFirewallInput"))

    @builtins.property
    @jsii.member(jsii_name="vlanInput")
    def vlan_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "vlanInput"))

    @builtins.property
    @jsii.member(jsii_name="bridge")
    def bridge(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bridge"))

    @bridge.setter
    def bridge(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea53ca495c9da2855ca7eab9ba2cfbe1c6a7cafeb6736358a77ed1754479c04f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bridge", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35755d02d365905e301b10daf4b1bdc6b827b659adcbc49f68c68cde38c97700)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="macAddress")
    def mac_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "macAddress"))

    @mac_address.setter
    def mac_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__227be3199da7999b75fb29b08d53b119b96ad119b568c3e01c89f6439f058a62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "macAddress", value)

    @builtins.property
    @jsii.member(jsii_name="model")
    def model(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "model"))

    @model.setter
    def model(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7665d3530770434001b68c3b016ee923f785a965668d2ec9fc1415eaf9f3fd09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "model", value)

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f70eba0d3bec125e52bd67ee40f8b30dd67d1df9f7308019adf5b8064e10d4f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value)

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55e0e4b131122e256bb5cb9dadf85221661d8a2afe5be4e950ce26ab6ea792d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value)

    @builtins.property
    @jsii.member(jsii_name="rateLimit")
    def rate_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "rateLimit"))

    @rate_limit.setter
    def rate_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c4fa4c7b2d11a2e5b83044d63ab6c81a01293c907aaae74835ced6594187290)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rateLimit", value)

    @builtins.property
    @jsii.member(jsii_name="useFirewall")
    def use_firewall(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useFirewall"))

    @use_firewall.setter
    def use_firewall(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec13fbaebd1114d4dabe5eb640cb342df8a59086cc377f5cce5f51c652e91b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useFirewall", value)

    @builtins.property
    @jsii.member(jsii_name="vlan")
    def vlan(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "vlan"))

    @vlan.setter
    def vlan(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1641b2adf55c516f72692e98afdd02318f5463118db1a1adba18e733921cc1bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vlan", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineNetworkInterfaces, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineNetworkInterfaces, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineNetworkInterfaces, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb224d17ea6e102a48126ef3960073a1832ab28c8eee385483fced09526b169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachinePciDevices",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "name": "name",
        "mdev": "mdev",
        "pcie": "pcie",
        "primary_gpu": "primaryGpu",
        "rombar": "rombar",
        "rom_file": "romFile",
    },
)
class VirtualMachinePciDevices:
    def __init__(
        self,
        *,
        id: builtins.str,
        name: builtins.str,
        mdev: typing.Optional[builtins.str] = None,
        pcie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        primary_gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rombar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        rom_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: The device ID of the PCI device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#id VirtualMachine#id} Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param name: The device name of the PCI device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        :param mdev: The mediated device name. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mdev VirtualMachine#mdev}
        :param pcie: Whether the PCI device is PCIe. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#pcie VirtualMachine#pcie}
        :param primary_gpu: Whether the PCI device is the primary GPU. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#primary_gpu VirtualMachine#primary_gpu}
        :param rombar: Make the firmware room visible to the VM. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rombar VirtualMachine#rombar}
        :param rom_file: The relative path to the ROM for the device. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rom_file VirtualMachine#rom_file}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9284e3503ea63a540a28b82b8690e58942e424dda6ade374382a574a65fb99c9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mdev", value=mdev, expected_type=type_hints["mdev"])
            check_type(argname="argument pcie", value=pcie, expected_type=type_hints["pcie"])
            check_type(argname="argument primary_gpu", value=primary_gpu, expected_type=type_hints["primary_gpu"])
            check_type(argname="argument rombar", value=rombar, expected_type=type_hints["rombar"])
            check_type(argname="argument rom_file", value=rom_file, expected_type=type_hints["rom_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "name": name,
        }
        if mdev is not None:
            self._values["mdev"] = mdev
        if pcie is not None:
            self._values["pcie"] = pcie
        if primary_gpu is not None:
            self._values["primary_gpu"] = primary_gpu
        if rombar is not None:
            self._values["rombar"] = rombar
        if rom_file is not None:
            self._values["rom_file"] = rom_file

    @builtins.property
    def id(self) -> builtins.str:
        '''The device ID of the PCI device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#id VirtualMachine#id}

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The device name of the PCI device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#name VirtualMachine#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mdev(self) -> typing.Optional[builtins.str]:
        '''The mediated device name.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#mdev VirtualMachine#mdev}
        '''
        result = self._values.get("mdev")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pcie(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the PCI device is PCIe.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#pcie VirtualMachine#pcie}
        '''
        result = self._values.get("pcie")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def primary_gpu(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the PCI device is the primary GPU.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#primary_gpu VirtualMachine#primary_gpu}
        '''
        result = self._values.get("primary_gpu")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rombar(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Make the firmware room visible to the VM.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rombar VirtualMachine#rombar}
        '''
        result = self._values.get("rombar")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def rom_file(self) -> typing.Optional[builtins.str]:
        '''The relative path to the ROM for the device.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#rom_file VirtualMachine#rom_file}
        '''
        result = self._values.get("rom_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachinePciDevices(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachinePciDevicesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachinePciDevicesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a69555719191751ea6b18bca3105e4037a478805722f83388132deda814bd30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "VirtualMachinePciDevicesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41d62edc4c1314417fb0f7079cc3ceee20cc91380a81bcfa8e51821200ffaf5f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("VirtualMachinePciDevicesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607c2860297b5236bf228a29ad87d7351b6a1b629a526c59a66beffbf7ca40a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b7b7795fcfaaeac941c695eb5a607dc6f5f5b96453c89fd5aa99c5050e750d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c41db22f866027195d5454d60f6d2b9bbe9d78391a902db985037de853dfe0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePciDevices]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePciDevices]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePciDevices]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13cebbf2f6f056993297b6f0faf5b7834147de65af17c138eb0786cd9d034d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class VirtualMachinePciDevicesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachinePciDevicesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5faacc8f57febe4cf36fa2477f2346543909ed7d5279587d699ec1c3e3bcbce4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMdev")
    def reset_mdev(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMdev", []))

    @jsii.member(jsii_name="resetPcie")
    def reset_pcie(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPcie", []))

    @jsii.member(jsii_name="resetPrimaryGpu")
    def reset_primary_gpu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrimaryGpu", []))

    @jsii.member(jsii_name="resetRombar")
    def reset_rombar(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRombar", []))

    @jsii.member(jsii_name="resetRomFile")
    def reset_rom_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRomFile", []))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="mdevInput")
    def mdev_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mdevInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pcieInput")
    def pcie_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "pcieInput"))

    @builtins.property
    @jsii.member(jsii_name="primaryGpuInput")
    def primary_gpu_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "primaryGpuInput"))

    @builtins.property
    @jsii.member(jsii_name="rombarInput")
    def rombar_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "rombarInput"))

    @builtins.property
    @jsii.member(jsii_name="romFileInput")
    def rom_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "romFileInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa4622504e05af8612a7f63fad66e9a3e0647e68ec0ea720ed11f04ed4d4525)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mdev")
    def mdev(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mdev"))

    @mdev.setter
    def mdev(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__346c60f37a1d0fed3875cfbfa033ec7b34df9f8a09505d980e4fcc8e645051f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mdev", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adabc82ea4c15e201d96ac958ab89ae9a5cac538c55cbf9d97cbe8b553cc7e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="pcie")
    def pcie(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "pcie"))

    @pcie.setter
    def pcie(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c48f00651e480b7f555411b1cb77b84f8c891983e1a45685c621d135dcc308e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pcie", value)

    @builtins.property
    @jsii.member(jsii_name="primaryGpu")
    def primary_gpu(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "primaryGpu"))

    @primary_gpu.setter
    def primary_gpu(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__661c1dc58fc2cf6a98ffb2327ce370ef197126256ee9745bace80b9b18e87b88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "primaryGpu", value)

    @builtins.property
    @jsii.member(jsii_name="rombar")
    def rombar(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "rombar"))

    @rombar.setter
    def rombar(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a5cd27c9f01dfc0b7028e0e477ad9ba620dafd82fa6d0f7a50dbe5060492317)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rombar", value)

    @builtins.property
    @jsii.member(jsii_name="romFile")
    def rom_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "romFile"))

    @rom_file.setter
    def rom_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aa00dbc2b33c226b5a05ea06c9d28b021801649415df1e16f929cc1af6a8393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "romFile", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachinePciDevices, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachinePciDevices, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachinePciDevices, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da08addfcb345deb484f61e82cafb041332fafe3820378088059705ed8f051b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "clone": "clone",
        "configure": "configure",
        "create": "create",
        "delete": "delete",
        "reboot": "reboot",
        "resize_disk": "resizeDisk",
        "shutdown": "shutdown",
        "start": "start",
        "stop": "stop",
    },
)
class VirtualMachineTimeouts:
    def __init__(
        self,
        *,
        clone: typing.Optional[jsii.Number] = None,
        configure: typing.Optional[jsii.Number] = None,
        create: typing.Optional[jsii.Number] = None,
        delete: typing.Optional[jsii.Number] = None,
        reboot: typing.Optional[jsii.Number] = None,
        resize_disk: typing.Optional[jsii.Number] = None,
        shutdown: typing.Optional[jsii.Number] = None,
        start: typing.Optional[jsii.Number] = None,
        stop: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param clone: The timeout for cloning the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#clone VirtualMachine#clone}
        :param configure: The timeout for configuring the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#configure VirtualMachine#configure}
        :param create: The timeout for creating the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#create VirtualMachine#create}
        :param delete: The timeout for deleting the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#delete VirtualMachine#delete}
        :param reboot: The timeout for rebooting the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#reboot VirtualMachine#reboot}
        :param resize_disk: The timeout for resizing disk the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#resize_disk VirtualMachine#resize_disk}
        :param shutdown: The timeout for shutting down the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#shutdown VirtualMachine#shutdown}
        :param start: The timeout for starting the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start VirtualMachine#start}
        :param stop: The timeout for stopping the virtual machine. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#stop VirtualMachine#stop}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7224ed12626bf3e62c43cc799ce18c16b152d2cb0bb46779585cc4ccde7c1cac)
            check_type(argname="argument clone", value=clone, expected_type=type_hints["clone"])
            check_type(argname="argument configure", value=configure, expected_type=type_hints["configure"])
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument reboot", value=reboot, expected_type=type_hints["reboot"])
            check_type(argname="argument resize_disk", value=resize_disk, expected_type=type_hints["resize_disk"])
            check_type(argname="argument shutdown", value=shutdown, expected_type=type_hints["shutdown"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument stop", value=stop, expected_type=type_hints["stop"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if clone is not None:
            self._values["clone"] = clone
        if configure is not None:
            self._values["configure"] = configure
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if reboot is not None:
            self._values["reboot"] = reboot
        if resize_disk is not None:
            self._values["resize_disk"] = resize_disk
        if shutdown is not None:
            self._values["shutdown"] = shutdown
        if start is not None:
            self._values["start"] = start
        if stop is not None:
            self._values["stop"] = stop

    @builtins.property
    def clone(self) -> typing.Optional[jsii.Number]:
        '''The timeout for cloning the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#clone VirtualMachine#clone}
        '''
        result = self._values.get("clone")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def configure(self) -> typing.Optional[jsii.Number]:
        '''The timeout for configuring the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#configure VirtualMachine#configure}
        '''
        result = self._values.get("configure")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def create(self) -> typing.Optional[jsii.Number]:
        '''The timeout for creating the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#create VirtualMachine#create}
        '''
        result = self._values.get("create")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def delete(self) -> typing.Optional[jsii.Number]:
        '''The timeout for deleting the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#delete VirtualMachine#delete}
        '''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def reboot(self) -> typing.Optional[jsii.Number]:
        '''The timeout for rebooting the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#reboot VirtualMachine#reboot}
        '''
        result = self._values.get("reboot")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resize_disk(self) -> typing.Optional[jsii.Number]:
        '''The timeout for resizing disk the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#resize_disk VirtualMachine#resize_disk}
        '''
        result = self._values.get("resize_disk")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def shutdown(self) -> typing.Optional[jsii.Number]:
        '''The timeout for shutting down the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#shutdown VirtualMachine#shutdown}
        '''
        result = self._values.get("shutdown")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start(self) -> typing.Optional[jsii.Number]:
        '''The timeout for starting the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#start VirtualMachine#start}
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stop(self) -> typing.Optional[jsii.Number]:
        '''The timeout for stopping the virtual machine.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/proxmox/r/virtual_machine#stop VirtualMachine#stop}
        '''
        result = self._values.get("stop")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VirtualMachineTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class VirtualMachineTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@awlsring/cdktf-proxmox.virtualMachine.VirtualMachineTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a884dba693bcf33da8418f86695f9565cacdfc1f01cd96181c0f92fc417dba7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClone")
    def reset_clone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClone", []))

    @jsii.member(jsii_name="resetConfigure")
    def reset_configure(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigure", []))

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetReboot")
    def reset_reboot(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReboot", []))

    @jsii.member(jsii_name="resetResizeDisk")
    def reset_resize_disk(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResizeDisk", []))

    @jsii.member(jsii_name="resetShutdown")
    def reset_shutdown(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetShutdown", []))

    @jsii.member(jsii_name="resetStart")
    def reset_start(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStart", []))

    @jsii.member(jsii_name="resetStop")
    def reset_stop(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStop", []))

    @builtins.property
    @jsii.member(jsii_name="cloneInput")
    def clone_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cloneInput"))

    @builtins.property
    @jsii.member(jsii_name="configureInput")
    def configure_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "configureInput"))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="rebootInput")
    def reboot_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "rebootInput"))

    @builtins.property
    @jsii.member(jsii_name="resizeDiskInput")
    def resize_disk_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "resizeDiskInput"))

    @builtins.property
    @jsii.member(jsii_name="shutdownInput")
    def shutdown_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "shutdownInput"))

    @builtins.property
    @jsii.member(jsii_name="startInput")
    def start_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startInput"))

    @builtins.property
    @jsii.member(jsii_name="stopInput")
    def stop_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "stopInput"))

    @builtins.property
    @jsii.member(jsii_name="clone")
    def clone(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "clone"))

    @clone.setter
    def clone(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2378ebbcf0f44979c1e70a98a7722dc1a2e4a5d864482f275636c16327702b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clone", value)

    @builtins.property
    @jsii.member(jsii_name="configure")
    def configure(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "configure"))

    @configure.setter
    def configure(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d69d6b0addcb34c7d62b4d8668911fe3edfb5028793691b4d8ed420e7e17c681)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configure", value)

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "create"))

    @create.setter
    def create(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796e3a91c5408431969c4f9790596ed312b445eb28f7f9db6a55d95bfc8c4d5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e2e479851cf6eba3d73576058d638f2019a509c641f967d3378448549c0ee6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="reboot")
    def reboot(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "reboot"))

    @reboot.setter
    def reboot(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ceafbafcaac29eb08a0b92b90f6e1cd67d6644f79d5f92db17e5c0ac6bb512b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reboot", value)

    @builtins.property
    @jsii.member(jsii_name="resizeDisk")
    def resize_disk(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "resizeDisk"))

    @resize_disk.setter
    def resize_disk(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4f879d6cc7c7741732e2a3c25db077e097751a7a39d376bbdb6768e8cf0bca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resizeDisk", value)

    @builtins.property
    @jsii.member(jsii_name="shutdown")
    def shutdown(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "shutdown"))

    @shutdown.setter
    def shutdown(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6482bd37eaad1739d2b4c7659be7f1c0a1f9271221c8440223f751af9c5be8b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shutdown", value)

    @builtins.property
    @jsii.member(jsii_name="start")
    def start(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "start"))

    @start.setter
    def start(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9e08c8576da84985f8bb5b5a0beef5a401a57f361256f2f307bbcae1ad3e21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "start", value)

    @builtins.property
    @jsii.member(jsii_name="stop")
    def stop(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "stop"))

    @stop.setter
    def stop(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d61bc078fdd8c759c668ffd41d1472b43076b2ef9be356ab2d42359fa1bac16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stop", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[VirtualMachineTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[VirtualMachineTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[VirtualMachineTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37eb9e18ad401e187dff8ec36c45c6e19efc197b55da75d17723cc73a98929cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "VirtualMachine",
    "VirtualMachineAgent",
    "VirtualMachineAgentOutputReference",
    "VirtualMachineClone",
    "VirtualMachineCloneOutputReference",
    "VirtualMachineCloudInit",
    "VirtualMachineCloudInitDns",
    "VirtualMachineCloudInitDnsOutputReference",
    "VirtualMachineCloudInitIp",
    "VirtualMachineCloudInitIpList",
    "VirtualMachineCloudInitIpOutputReference",
    "VirtualMachineCloudInitIpV4",
    "VirtualMachineCloudInitIpV4OutputReference",
    "VirtualMachineCloudInitIpV6",
    "VirtualMachineCloudInitIpV6OutputReference",
    "VirtualMachineCloudInitOutputReference",
    "VirtualMachineCloudInitUser",
    "VirtualMachineCloudInitUserOutputReference",
    "VirtualMachineComputedDisks",
    "VirtualMachineComputedDisksList",
    "VirtualMachineComputedDisksOutputReference",
    "VirtualMachineComputedDisksSpeedLimits",
    "VirtualMachineComputedDisksSpeedLimitsOutputReference",
    "VirtualMachineComputedNetworkInterfaces",
    "VirtualMachineComputedNetworkInterfacesList",
    "VirtualMachineComputedNetworkInterfacesOutputReference",
    "VirtualMachineComputedPciDevices",
    "VirtualMachineComputedPciDevicesList",
    "VirtualMachineComputedPciDevicesOutputReference",
    "VirtualMachineConfig",
    "VirtualMachineCpu",
    "VirtualMachineCpuOutputReference",
    "VirtualMachineDisks",
    "VirtualMachineDisksList",
    "VirtualMachineDisksOutputReference",
    "VirtualMachineDisksSpeedLimits",
    "VirtualMachineDisksSpeedLimitsOutputReference",
    "VirtualMachineIso",
    "VirtualMachineIsoOutputReference",
    "VirtualMachineMemory",
    "VirtualMachineMemoryOutputReference",
    "VirtualMachineNetworkInterfaces",
    "VirtualMachineNetworkInterfacesList",
    "VirtualMachineNetworkInterfacesOutputReference",
    "VirtualMachinePciDevices",
    "VirtualMachinePciDevicesList",
    "VirtualMachinePciDevicesOutputReference",
    "VirtualMachineTimeouts",
    "VirtualMachineTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__ac855b08d6f8e9923a335183bd2d6621b1aa2e6cad0d447023ba8e37d5a4bceb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    node_attribute: builtins.str,
    agent: typing.Optional[typing.Union[typing.Union[VirtualMachineAgent, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    bios: typing.Optional[builtins.str] = None,
    clone: typing.Optional[typing.Union[typing.Union[VirtualMachineClone, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    cloud_init: typing.Optional[typing.Union[typing.Union[VirtualMachineCloudInit, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    cpu: typing.Optional[typing.Union[typing.Union[VirtualMachineCpu, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[jsii.Number] = None,
    iso: typing.Optional[typing.Union[typing.Union[VirtualMachineIso, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    keyboard_layout: typing.Optional[builtins.str] = None,
    kvm_arguments: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    memory: typing.Optional[typing.Union[typing.Union[VirtualMachineMemory, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pci_devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachinePciDevices, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_pool: typing.Optional[builtins.str] = None,
    start_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_on_node_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[typing.Union[VirtualMachineTimeouts, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__83418811f742f8fe7b3f25f83b1f824de55abae3fa54a05c5a57988e1e2d331a(
    value: typing.Union[typing.Union[VirtualMachineAgent, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5be555fcbf0ae384a7a0a9fdad33b93362dd226fdc5c88027fceb44f8538e45(
    value: typing.Union[typing.Union[VirtualMachineClone, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec17dc969abbc237640ebdb994cdc9dcf89529f9d8b02f6e30f4cef6779d300(
    value: typing.Union[typing.Union[VirtualMachineCloudInit, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f249d667036579028c301877ed4d888e06a7438035eba0a0d8c8c8caf38cfd1a(
    value: typing.Union[typing.Union[VirtualMachineCpu, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c240a1a77f4f0e179396d60285e7f22b1459492eeaa0b91e2ea999ddbb705419(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineDisks, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29fbca37452f5499d50f2fd03155649d42967a974cbe99013b60e44e50e32556(
    value: typing.Union[typing.Union[VirtualMachineIso, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be9cb989446f6faf7555ee370e2a92c8d5d9debac516f9dbed3917865f1543c(
    value: typing.Union[typing.Union[VirtualMachineMemory, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5c4452a3e1e0f98bacc59a97a216ed7c5dfdc77364a4ec926df86078677b43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd61d2622ca4d0bbb02b8baf6c451445ebed7c6a83df21c7c8c71772e1a9f16a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachinePciDevices, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bcd77991eab5b3ec456c7389616efed9c6bb2a8155d3f3be858acdcb12fca37(
    value: typing.Union[typing.Union[VirtualMachineTimeouts, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fdf3234ffc0a45a086b7662782e1efe8ae453ae303dbf71edfd8e730853272(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2517935fd3510ba0ad5d466ae2904d5e022d7c3f18503653eeb0ed7d515755(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15a025be497fdfaa3b0d842275cc69daebb19e172bced5fbd3aa25b17ae770c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72ca051627ddd8e472230d692c0b2cf2e8b8502548648f30d9c09a83a108fcb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abf0326b4f275c1319d9ae7b6554ddf1e19533666215d701169454b80aabd1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3c2e4601dc8dfc83905e383b9c71a9dad804e94a09f2e28e420c236946ba332(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba8f1f0134f6d137c76719f312afbbc7590fb0539eb44e5bc2b92af903eea2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b210d0ab9c636b9e6d796c66fba050b512d5c51b04b0c8afa4867809bc79ccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92ab755a041aafc6df63657e9cdf7f1502021197f1b67907764ad139e6bbca0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f46c05ce037c2af727b2d37be37720759782d2bd7084cb647d08c38bb966bec(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5ac732e5479b666ee11ad433b6436782a73f7595688e42021acf4f84b8cee1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f6a6985b9673248602b2dfe49c2c664559a4ad821a6e4c485d2e169ae0bc66(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__464c46bfca258bb0efd2a877391319395124fcd52273d2ecc6687c185706e19e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6411bd5f9d10a5f7db06600c8921b8380ef837ae939b4076f6945d87f3990feb(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
    use_fstrim: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16db17e5eebd8dda879d2c1f2c0e08902ad2c9b9ca231b1e06829e2d1d3d4e13(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bdbbc473da0990c22af063f08abb2226fca5e51364cd91ab66b4b3029de4907(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6ddb0e5ac2e478a5e8649768c43d6ede249be7fdbe0c5c65cac741f427a479f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45172b8f896ca5116af29c6f384a48be2564a9be0b889d6b112f48039ce665d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__967859fbf99d9ed36f4a28fb83a16f4b699c025d3b0a601ad584a9dc130545bb(
    value: typing.Optional[typing.Union[VirtualMachineAgent, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ca7847e00d8685921476c28bf72b3b40d87ba38ddb6bb5fb35d19f51c1312d(
    *,
    source: jsii.Number,
    full_clone: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    storage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e440bef17916e573c0e2e5a199351daf24de4b94528b792ff19991380edf722(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971da7019ac6c242e2999c8aac4dced8bb416891e9ce35657f13c36a51614de5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07de61649a4cc6af75cb68e9940a696088603cc020fa07484c593eaf91a96656(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31d635e3500bfbbf33b2d215c60cc88fe2ee1725525ff7c5cfbc3ae0529d3b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f909b526cd04e9f9d19e027b7653e41eb174a0c98965b10dac60f9c12d186fd(
    value: typing.Optional[typing.Union[VirtualMachineClone, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e28b42e970cbc700d2025d6d345202f39f218ba811f2f256d8c0470202a16b(
    *,
    dns: typing.Optional[typing.Union[typing.Union[VirtualMachineCloudInitDns, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ip: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineCloudInitIp, typing.Dict[builtins.str, typing.Any]]]]] = None,
    user: typing.Optional[typing.Union[typing.Union[VirtualMachineCloudInitUser, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54cd6db34eaadbb9e0b11cbaed0641d2b27a19870a7447fdbf69b1ee7195eb59(
    *,
    domain: typing.Optional[builtins.str] = None,
    nameserver: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f225d8e38b4390ce036d4e8cc11c58f600a83710536d1d9949defb3e5de04bb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a577b2439d886f2dd7cd691d0ccf0c728d91bf78fa342617d4a6201802f0c32c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c28b2c558f7e70daed3179d34309c90bb9b91282e3e2d84e0ec87360a7802c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1cf0b5d280a19b6f9757770225aaede2bc8ec6379c6b80b8e138b05335d5d17(
    value: typing.Optional[typing.Union[VirtualMachineCloudInitDns, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f282493bf9efcdebe536c21965c2ed059db850de04e956b61d695ad4f9b4bc(
    *,
    position: jsii.Number,
    v4: typing.Optional[typing.Union[typing.Union[VirtualMachineCloudInitIpV4, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    v6: typing.Optional[typing.Union[typing.Union[VirtualMachineCloudInitIpV6, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27c9ac2d0b241a7a3595446e16230af493795855770d4ee006b70a4dec3dd937(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1e07af5b8aa46d37b76358a44863e7e2e7b1dcd214dac3d1c0f76457b38938(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__321c8b72f0c15f105c8509e2c539d0036fcd2fb0ae269c41e518a362fcb60ef0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3460d4129530eb4a0f223c686f69c01f151c3e41ee6a7f255803bfadc0b544da(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e758419348feaf0b082df110c5d3b3c8e39b20d8a3fca34c64958209060cadf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19dadc0181cecb96bd9eb2a960aac63754f2ffbbbaecbe8c726ccddabec7ea9c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineCloudInitIp]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88fbc89928155632dc799e88c1ae147fa9fee4cbf0d2b84a48c7bc84bdaa79a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047b760f656247ce3d06faa600a0f93c8a2d5f52d8e09ef88971c5947b4b01b8(
    value: typing.Union[typing.Union[VirtualMachineCloudInitIpV4, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2716f153ee5a0a8480ed87b0277674b6e4198821075baddb08781c7b4e551e66(
    value: typing.Union[typing.Union[VirtualMachineCloudInitIpV6, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456c60ab311663c29e8498a96e0268b454bca5114f0a62e36adc620851aec570(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac7ec251fefa7f7d7ae7c099fe61361eb3bec60aa604655635385ca879aae23f(
    value: typing.Optional[typing.Union[VirtualMachineCloudInitIp, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66d24195a92bf1c529b739ac4ca0d0ee0d7aad533affac38e8c13149debdae9(
    *,
    address: typing.Optional[builtins.str] = None,
    dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gateway: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6380433b49ff0c2a944fb9df2de254f4c672c7bec827138e0e0f4bd8be51f7e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cedb5611a48b9259c9b4004c166ec73a3e7f6b3f47e6f31b603b1f0b51eeb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1b7b15d70b8539e502b57a1a333cddd75e461ab5f760a597abfae4b9c0f9e9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4bac085a5fed0ab3b5bb7b694ae138805c914af72e4fc05e5064d0493a4f53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69cde9f6d15851de4a686f23b5723010a9b9e768438cfceb106beae54c7fbbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815b473b81e20555e84cda13cc3279b6a9762ad22d7508918dded37a36536783(
    value: typing.Optional[typing.Union[VirtualMachineCloudInitIpV4, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f16cbf68356c519e317488143acf7d13a008d04be15fe22b2c7fe149ba47d4(
    *,
    address: typing.Optional[builtins.str] = None,
    dhcp: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    gateway: typing.Optional[builtins.str] = None,
    netmask: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94597b966ad8298c497f74a7aaae1f787d8efc019539cf6843edc199801ed03f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4eda9be071d2337d0732e0e5519ba5455fc33d935d0ea8584635da27e46a9d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3139c798680fb08721424b6f43f8d27c05781be28118a937a4c59637119e4aac(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8017b311275aeb4154a034373efb89718ebf2ff04643623da3f083aba65e43b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d97d2d138b53c660abc1b50d99c9a6aef84f4de9131904e3155680c70bc5bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d27f08d22b058d992fa85e0df44803ba79dd54dfe0b4fe69c6a4c46b4f5d1b(
    value: typing.Optional[typing.Union[VirtualMachineCloudInitIpV6, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82d850ece5596b745643fecfebe9acfadfcdb74b8ba3c98d4ae0d523b843aba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fbf6c8a6685031386ac6ccfcc198e3f2c7772cd56538c30467048d68bfdf70d(
    value: typing.Union[typing.Union[VirtualMachineCloudInitDns, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ea28088e089353d628145df245927dab52adf13adc4e16f81f5276a626a804(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineCloudInitIp, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42895dfe13efb2eda5ff69c3d7b8eb5ab11d38b00f651ee4f27d8e4401d4eba8(
    value: typing.Union[typing.Union[VirtualMachineCloudInitUser, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b65b1b292e54bd4afb4c3d50e3cbd1ab204a8e320ef66bf7be0126896a0fdf(
    value: typing.Optional[typing.Union[VirtualMachineCloudInit, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7348a691b46c0d8a98262a7c2fa8eaa4de94ed0ac8e730873e05023184ef62(
    *,
    name: builtins.str,
    password: typing.Optional[builtins.str] = None,
    public_keys: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60455c3421370b7d3d829c0df546779b1efa392fbfff42b455ac193e315e8db1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81a98a256aabd350236168a212e998c3c71ba9f6cee3a6296fcc8ebd84dfa371(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b9b3e253555daf5eb32a0e98811e5d05340a480038ecab78212d01dde658fd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e843c9e8446ee0cb5c68e16f4eb4e359280e062e13182e2aa2fe260e9b81666(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b36c3a32fb5d91b5e78c6a4e634506e87c380a62c48f6de13862420666c70a74(
    value: typing.Optional[typing.Union[VirtualMachineCloudInitUser, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6785625476108385ce505f0f23db686be2a224b16e5693c0c0f158eef3c60086(
    *,
    interface_type: builtins.str,
    position: jsii.Number,
    size: jsii.Number,
    storage: builtins.str,
    discard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    file_format: typing.Optional[builtins.str] = None,
    speed_limits: typing.Optional[typing.Union[typing.Union[VirtualMachineComputedDisksSpeedLimits, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ssd_emulation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_iothread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7bd507be149cc1484086c3f9ac1f6aec839a5c9dbb20c32d7c3302a1d6a3cf4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a41b9e64bf0a69fc661af4649b6335b43d2b8933755dbe6c2e60aa2d8984a09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53777c0e45a35e9d5238ca5ae56ead10b9f2050ed5cc5acd206d0b321b042d61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f306311e47229b84f5592b22cc9e86802726ea54720cd45b8e96c889446993eb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f747fc8f52385dd5c1e37e0656e433346e1b5760e0a8bfc31b0073f413ba10(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bbb70064244356e5fc89b84f232dd172636247c8224376045a77652f68495fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedDisks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8f5439e113783b3521f2b3ecddd50323a01a6bd70bf47ea58a53e26f9d5d73a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81f958e61a00fb22ec5ac21d98b5b3729bc27b4d2cfcd6fe92c25a58faca2c9(
    value: typing.Union[typing.Union[VirtualMachineComputedDisksSpeedLimits, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a825108c12c10e3f93a5cf543cd4d746e444d39b4642f1b63b854461a8b128(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d815ea4f66a4199967562c634c1cf7609ac7f19c52c70f5830646767d20c43b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f0ed3b103c839864fdb4ec3dc89ae1086536b945c6e386b12f3e3043597cdf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6834fae9c96878886c6f35c065ce1418d7d448cf2effcfb089c2ac5d7234729e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ca70bd0ad323dfef56b3003a4d721473d6fab03ef3f88c4c7798b4118da775(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591d4f9a21fd44928a2bb9d205218af47a16e10ffec63adb74c285a9f151400a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b4e0e6dad388cb1c0fcfd542f2c54dc18497ecb4911397a78c91e6db2946e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2cdda4c18a48acf67675d4521ad6780c448bff28fac622690fbd132e04f230(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82d930ed85cd10c71d7c6d3e0f0877465798cdcad9e67296bd12ee7a61313249(
    value: typing.Optional[VirtualMachineComputedDisks],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3779fb5e2ed08c127cab0434c70364ee8445a588bca109574dd2aec760ff981c(
    *,
    read: typing.Optional[jsii.Number] = None,
    read_burstable: typing.Optional[jsii.Number] = None,
    write: typing.Optional[jsii.Number] = None,
    write_burstable: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e39c56631654e6f7f78544442c83ca17793436d08526aa4667af6d3fcc4868c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b43f4bea54276ae0c6643f852dc96d4954d86c9e9459eadd969abbafa1b3ffc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__469996e23b8d1c6189b8c7d057560618445177b3d32e5ee7d52de222848e1ccf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ef4eb9726df6efead8faf2e0564084db8f9ab047a53d3020e26c9c83390bb0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98cf5b6611a2da3fe299e9f9c61f167ea18395dc98c078198e3ed07129f9afa7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9184644c9e74746bcc6f7f1e708765e446603377c5ad020c5ce48bb56fc017(
    value: typing.Optional[typing.Union[VirtualMachineComputedDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dc02c5c63992905ad270f0003bcd9556e892f52a9f4480a1e14edbe92350c2a(
    *,
    bridge: builtins.str,
    position: jsii.Number,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mac_address: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    rate_limit: typing.Optional[jsii.Number] = None,
    use_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vlan: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4e225413051eba22f64b871b26203b383d88c56289b1f28c684b7a35d3e9c3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76e98262b8b8d27da9b39fd2b806b7efd6d124bb47b11a46f1779bf5a03cc582(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593b490f01498a7f9011239bed4a4a1b7d761938f046796eaacd1db03de96a88(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b43f27e5ed3c439140cba964a6006e5c16a701cba7598c677027f91fe5278591(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f30313667499e06a5db1935c42bad7c1ea81fb7af11514272d4d637d07aa92(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7432dcb7f675143c69b5b41bbca1bed808d4fc0a577d7e298d69924df6f2b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a47ce6114bb4902f8658dcad2fe3d1fde71664f48c56531e6305845a2205c94(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31c6707bfe6b48dbdb32f163d3a2679cf65b370fdb9f4da20790bf506f5ee659(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a208bb8bfb58fb2e89092b760e486fcc939051d533b2fbe2d9eec338f68f943(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a15eac620b655b13a236b3c429d1ebb04f817a778955e14d377c7f328478d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c4ba95191427e171e25c1f13148b02ab81173b751759e7392a27d96efbb253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b770c1c950551d3dd070cd42bb00aaf106a51ee7f8dba44f072582df217d167f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db0eb8934c80523b3d8c7d6f9c8bb5a00439aaa67d0629b80c278ac159483a4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e377ac2baf54f015f35dcaf42a87780aaaad81b7a803bfca858f1ef98a8b75(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a748fb1a1e64cf71c85932895032601c2b69fa9d5feed993a49e65019ec3aa39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f78f6288cc42bb5ff4fe5070266050c5ff5a8a780de924f2914e3250652a4f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb62b1ca21aac0c1a2457d069833d8ebcfe5e4eca177e27c19585ef58aeb4d4(
    value: typing.Optional[VirtualMachineComputedNetworkInterfaces],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b074cb4cd644c928d0bd6c5e4ace6edd6fd01ee7edfdce03e66886170a8bcc(
    *,
    id: builtins.str,
    name: builtins.str,
    mdev: typing.Optional[builtins.str] = None,
    pcie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    primary_gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rombar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rom_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffbb75afa67e7d6395799b801453cf9f69d7fc91dec07e8703349d094863c8b1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788283e76f4ff2c91fe6e0dc97e29e20db0eecd6a1602fa5c1947b0f798e8fbc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08ddc08a3f8202f6796315ca27e28d0f19903e12112c06f3d5d40c5b39b285f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e38a14e438a7ba5386e3c7df14f3d48971bb0090491e84095e5d3a40eccaea1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e979219e4cee7f983d1f89f694a7e6533811a3879daa1e44d38878fdba215f08(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14257934fcd76ed64889c64e41c33f235c7dcb0d4a57e2c4b5a8805cb326a637(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineComputedPciDevices]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b801bfbe6d45ee5533a8a2cb77f42e4b52ad7d5f7be267ef80aba28fe963df(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccc97c1a6d4a54a13e34d6abb50ecea9dc52060eea4d4c9c273d2a994e48b3a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b82e8516f0b56e3d2fbb96e6d8a2134219888c818e13f6b44768bd1a7f97661c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aa00ba7ebda46f28707381995bc0800453f8118c702be0d31da5c972dec8320(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a566e9f74842ef950146551b7ef027355a3ea49c965620f00a90d9580df4dd20(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874ba96c7ad1486e5b55a2a2c776db48ca909d0f3775706fec1c1678c93dc0fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3744f55caf3b5e414fa0bf8bb67fbd6af95254f4c6b6d79d066b92651138ff48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9abb866e36a1e220cb683bc43adb1d65a63b3a1f031e716d1d9dd577f785d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4b88b8f53c075a0520fddd6b46c45dae958b86399e0718c0a7a763d10e4db1(
    value: typing.Optional[VirtualMachineComputedPciDevices],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9990431c355c2efc5f62d35e8044c02343b4170dafff64740c6e60c8147fb768(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    node_attribute: builtins.str,
    agent: typing.Optional[typing.Union[typing.Union[VirtualMachineAgent, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    bios: typing.Optional[builtins.str] = None,
    clone: typing.Optional[typing.Union[typing.Union[VirtualMachineClone, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    cloud_init: typing.Optional[typing.Union[typing.Union[VirtualMachineCloudInit, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    cpu: typing.Optional[typing.Union[typing.Union[VirtualMachineCpu, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    disks: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineDisks, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[jsii.Number] = None,
    iso: typing.Optional[typing.Union[typing.Union[VirtualMachineIso, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    keyboard_layout: typing.Optional[builtins.str] = None,
    kvm_arguments: typing.Optional[builtins.str] = None,
    machine_type: typing.Optional[builtins.str] = None,
    memory: typing.Optional[typing.Union[typing.Union[VirtualMachineMemory, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    network_interfaces: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachineNetworkInterfaces, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pci_devices: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[VirtualMachinePciDevices, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_pool: typing.Optional[builtins.str] = None,
    start_on_create: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    start_on_node_boot: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[typing.Union[VirtualMachineTimeouts, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f0eea8df55b8cc1b0e1bbfe67406ea841216184849bd1a3249d227a48215f54(
    *,
    architecture: typing.Optional[builtins.str] = None,
    cores: typing.Optional[jsii.Number] = None,
    cpu_units: typing.Optional[jsii.Number] = None,
    emulated_type: typing.Optional[builtins.str] = None,
    sockets: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae03c501033e794a8af411d4f12ba8516f44453e5673076b2b61c69057bf441c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e8f713aacbf0604d35e46ffafc7551f0daff028f95e0f77081e439fbfd2ec64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a92d0a25b5e4725d08c55c37e492ecb30bb8e2ea2099692ffb673e1d428c4a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb71acbd172dbd833a324f004547099cb20055009552e8566ee04bbea571a9e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc5dcbfb4d8c7904d4042685ccf1240808ced51cc6176e8ea3575a3b3e0b4e64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040f57604e7b3172f7848bf0bd1acf46c99d7d2e6a3203f5606e8515d8c3362f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ba34adb23f4c9b2dbe1ec09215d4e5cab77191ad47ade8ac7af5648484d0ae(
    value: typing.Optional[typing.Union[VirtualMachineCpu, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__724516c81760f160a0baa82bf1df356572b1396b407f8e6aa3bdbefc0164510e(
    *,
    interface_type: builtins.str,
    position: jsii.Number,
    size: jsii.Number,
    storage: builtins.str,
    discard: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    file_format: typing.Optional[builtins.str] = None,
    speed_limits: typing.Optional[typing.Union[typing.Union[VirtualMachineDisksSpeedLimits, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable]] = None,
    ssd_emulation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_iothread: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4137fcc557d93c6e6c54528f329acd5e490a206a0e43355e87a7f1423042dbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09a3a99e4fd8a2d5f6a200e724a8be26e8832ede3b9d96b737299f0f29ee51b9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472c17240c719bd9e09e66d17985f2b7a2d23cb5b0c9be6a2d85909472cd0404(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6c6c62c26b288418245539b79004b040b0a59e6ff4e666ce183fe182ecfe41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e55c40d5b9de1fed7d79e353ede56d0857910556e31983983ed68adb9d7cbb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26d8556ae50ac5b8093a73ced226d8ecac249084144d7e29061e51fd2111ee1c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineDisks]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd5a32a75ffe345bf2e3f05c865d141f49587ba6d47dfc361a5567625023dbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8158207d21c5b18d20ebca7155e9bc24d0837a11b329468ad7dc773e830cf056(
    value: typing.Union[typing.Union[VirtualMachineDisksSpeedLimits, typing.Dict[builtins.str, typing.Any]], _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190dd236495a455d1402bfdc14ea26b12213cc6e6e95004303146ad4d681f521(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9013a43d9aaab7b3f9bc168daaf4b5db01cbde6ca834158f0ed9e4db174b5a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19febc2b2d2cd0a53fe4d7744e71ef322359bcac79a2b6566deacf242f688c90(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02ec1c8055848e3a6fa8a6a92b1a6498288d13dea82ef678df94d88af732ee9e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a78aa77220938d303c8dd7d6c52d60934da0fc8ec42fe7c72b3c6c80ca7b0e58(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07687ece05f3cdbcdf3c8823f33b9defcd39647e051fb38a688ae4cf26234487(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52e1b97909033046728ff40a40bc10be81400020d72fc1516872eb20e2f7c50a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5e7c4c71e9fe30d23e90a786a267bfbca33baf4925f5a0fc0a5658569360de(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83553b29b869338c2fe30547cf52dc266012b7a7ba61230b95109fcda8c9c435(
    value: typing.Optional[typing.Union[VirtualMachineDisks, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64b1544b8f0e9fe1b73225cb7e526b53e2d770504847686dbeacedd93e2cfc5(
    *,
    read: typing.Optional[jsii.Number] = None,
    read_burstable: typing.Optional[jsii.Number] = None,
    write: typing.Optional[jsii.Number] = None,
    write_burstable: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acb6c0c1bbc483013acadf83c2afc7333747ea1f60b0b70e3b83bfdc07dcacdd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7faa6a04553ed658e498f4d553d547c66a1a93f341ebc0b63bc8b0f1a721654a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc64fcb1ebd82dbbe08d59e291bad7d54c3165c496aebe1b3ea20c66fee7aaa2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5abb6ca2d1696740392687835956eb0588d1430ce4410e46739d69cfcd01fd65(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f8129f5c21ccc4904fef692bf3163de419fe36d22c1a931f04126ab9cb1b93(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c567b5c4be7eac3391e9c02d3f2e8612c44638fa17643e86970abadc0b0a36(
    value: typing.Optional[typing.Union[VirtualMachineDisksSpeedLimits, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d380de2f8fb0523f0767e791573e4c06f84569a07d9b52bef0c15b92041a1dbd(
    *,
    image: builtins.str,
    storage: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c387aad931cd68402d666f18945aeb29e378f66931ca2b943c48557fec97e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d9a9413b71d687c1bbf794a5e98e42f62ce18f68366be2763bc596686a8df5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b1b1cb81d0cec44a2d0f38196699d5329e1612bbe6189256c11796428d5f258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4968b44a96abd7ffead827bef3c3e218d134e0f9cdeeb910b1014afb5b152690(
    value: typing.Optional[typing.Union[VirtualMachineIso, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0974684686bffa5982faef71322e60afee854e57667f695bbf976fdb7cce61e(
    *,
    dedicated: typing.Optional[jsii.Number] = None,
    floating: typing.Optional[jsii.Number] = None,
    shared: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b850f8b283b0c0b94ec50ed03f029e6289ae997a8284bb3ad726925c4ef85e55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ee26619b484718c06edb22281785ed4a20579f084261e62b0fd4f0495a7628b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ccc329cd748645a85b6316f6b4b107efe77c15173abbe9e070375da5c649176(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__431b4a2379d1900eb31fb1d8a9da4cd3e5a958f3bdfc9c8280f4be3d5de71dc0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2264f2d62c16fa75dd9d5aed81aa1c44fea980fd2fadea041420429774c3ab81(
    value: typing.Optional[typing.Union[VirtualMachineMemory, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8840af80bb4afb00569be8b14daa1c429616c64477b5a1c7664b182ed951cb63(
    *,
    bridge: builtins.str,
    position: jsii.Number,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    mac_address: typing.Optional[builtins.str] = None,
    model: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    rate_limit: typing.Optional[jsii.Number] = None,
    use_firewall: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vlan: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfc8e560878f0aae146c0283376ef3c708f1084bde4c80e63fe2f76979e59bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c86c7fda67850ceff00d45ec1793b79a88016b1c61cf7e3a59471dc44f8d7ba(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5bfd81fd69caf460854936e11268d4af0f1ec43b652b69c231cf9d8c650506(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15322702066575a81f3e30a319b5d30b31005435e8809765f1d04ae5526dbeb5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a813baeca869b833140dcbfeabeef6fe605ec0922d9a3772fa288ee58e03a07(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1abe4ef7b50ef924866dd6b0e9cae743684a8ed8317d73fd8e2ee86072845c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachineNetworkInterfaces]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb16262d16bc9851ed7d089f06a87326307b0df5da7e64e0a80b2038162fe5ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea53ca495c9da2855ca7eab9ba2cfbe1c6a7cafeb6736358a77ed1754479c04f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35755d02d365905e301b10daf4b1bdc6b827b659adcbc49f68c68cde38c97700(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227be3199da7999b75fb29b08d53b119b96ad119b568c3e01c89f6439f058a62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7665d3530770434001b68c3b016ee923f785a965668d2ec9fc1415eaf9f3fd09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f70eba0d3bec125e52bd67ee40f8b30dd67d1df9f7308019adf5b8064e10d4f5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55e0e4b131122e256bb5cb9dadf85221661d8a2afe5be4e950ce26ab6ea792d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c4fa4c7b2d11a2e5b83044d63ab6c81a01293c907aaae74835ced6594187290(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec13fbaebd1114d4dabe5eb640cb342df8a59086cc377f5cce5f51c652e91b6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1641b2adf55c516f72692e98afdd02318f5463118db1a1adba18e733921cc1bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb224d17ea6e102a48126ef3960073a1832ab28c8eee385483fced09526b169(
    value: typing.Optional[typing.Union[VirtualMachineNetworkInterfaces, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9284e3503ea63a540a28b82b8690e58942e424dda6ade374382a574a65fb99c9(
    *,
    id: builtins.str,
    name: builtins.str,
    mdev: typing.Optional[builtins.str] = None,
    pcie: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    primary_gpu: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rombar: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    rom_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a69555719191751ea6b18bca3105e4037a478805722f83388132deda814bd30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41d62edc4c1314417fb0f7079cc3ceee20cc91380a81bcfa8e51821200ffaf5f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607c2860297b5236bf228a29ad87d7351b6a1b629a526c59a66beffbf7ca40a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b7b7795fcfaaeac941c695eb5a607dc6f5f5b96453c89fd5aa99c5050e750d8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c41db22f866027195d5454d60f6d2b9bbe9d78391a902db985037de853dfe0d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13cebbf2f6f056993297b6f0faf5b7834147de65af17c138eb0786cd9d034d8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[VirtualMachinePciDevices]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5faacc8f57febe4cf36fa2477f2346543909ed7d5279587d699ec1c3e3bcbce4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa4622504e05af8612a7f63fad66e9a3e0647e68ec0ea720ed11f04ed4d4525(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__346c60f37a1d0fed3875cfbfa033ec7b34df9f8a09505d980e4fcc8e645051f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adabc82ea4c15e201d96ac958ab89ae9a5cac538c55cbf9d97cbe8b553cc7e06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c48f00651e480b7f555411b1cb77b84f8c891983e1a45685c621d135dcc308e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__661c1dc58fc2cf6a98ffb2327ce370ef197126256ee9745bace80b9b18e87b88(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a5cd27c9f01dfc0b7028e0e477ad9ba620dafd82fa6d0f7a50dbe5060492317(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa00dbc2b33c226b5a05ea06c9d28b021801649415df1e16f929cc1af6a8393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da08addfcb345deb484f61e82cafb041332fafe3820378088059705ed8f051b5(
    value: typing.Optional[typing.Union[VirtualMachinePciDevices, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7224ed12626bf3e62c43cc799ce18c16b152d2cb0bb46779585cc4ccde7c1cac(
    *,
    clone: typing.Optional[jsii.Number] = None,
    configure: typing.Optional[jsii.Number] = None,
    create: typing.Optional[jsii.Number] = None,
    delete: typing.Optional[jsii.Number] = None,
    reboot: typing.Optional[jsii.Number] = None,
    resize_disk: typing.Optional[jsii.Number] = None,
    shutdown: typing.Optional[jsii.Number] = None,
    start: typing.Optional[jsii.Number] = None,
    stop: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a884dba693bcf33da8418f86695f9565cacdfc1f01cd96181c0f92fc417dba7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2378ebbcf0f44979c1e70a98a7722dc1a2e4a5d864482f275636c16327702b6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d69d6b0addcb34c7d62b4d8668911fe3edfb5028793691b4d8ed420e7e17c681(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796e3a91c5408431969c4f9790596ed312b445eb28f7f9db6a55d95bfc8c4d5f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e2e479851cf6eba3d73576058d638f2019a509c641f967d3378448549c0ee6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ceafbafcaac29eb08a0b92b90f6e1cd67d6644f79d5f92db17e5c0ac6bb512b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4f879d6cc7c7741732e2a3c25db077e097751a7a39d376bbdb6768e8cf0bca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6482bd37eaad1739d2b4c7659be7f1c0a1f9271221c8440223f751af9c5be8b9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9e08c8576da84985f8bb5b5a0beef5a401a57f361256f2f307bbcae1ad3e21(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d61bc078fdd8c759c668ffd41d1472b43076b2ef9be356ab2d42359fa1bac16(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37eb9e18ad401e187dff8ec36c45c6e19efc197b55da75d17723cc73a98929cc(
    value: typing.Optional[typing.Union[VirtualMachineTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
