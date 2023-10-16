'''
# Terrafrom CDK Proxmox Provider

This is a repo that builds default CDKTF bindings for the awlsring/proxmox provider. It is semi auto-generated from the providers schema using methods pulled from the HashiCorp [cdktf-provider-project](https://github.com/cdktf/cdktf-provider-project)

This repo and the provider are still in development and should not be used in production.

As this matures, additional custom constructs will be added to this to speed up the creation of VMs and other resources.

## Links

* Provider Repo: https://github.com/awlsring/terraform-provider-proxmox
* Provider Registry: https://registry.terraform.io/providers/awlsring/proxmox/latest
* ConstructHub: https://constructs.dev/packages/@awlsring/cdktf-proxmox

## Available Packages

This provider is built for the following languages:

* Javascript/Typescript
* Python
* C#

Details on how to find these packages are below and on [ConstructHub](https://constructs.dev/packages/@awlsring/cdktf-proxmox)

### NPM

Javascript/Typescript package is available on NPM.

The npm package is viewable at https://www.npmjs.com/package/@awlsring/cdktf-proxmox

```bash
npm install @awlsring/cdktf-proxmox
```

### PyPi

Python package is available on PyPi.

The pypi package is viewable at https://pypi.org/project/cdktf-proxmox/

```bash
pip install cdktf-proxmox
```

### Nuget

C# package is available on Nuget.

The nuget package is viewable at https://www.nuget.org/packages/awlsring.CdktfProxmox/

```bash
dotnet add package awlsring.CdktfProxmox
```
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


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.AgentType")
class AgentType(enum.Enum):
    VIRTIO = "VIRTIO"
    ISA = "ISA"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.Architecture")
class Architecture(enum.Enum):
    X86_64 = "X86_64"
    AARCH64 = "AARCH64"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.Bios")
class Bios(enum.Enum):
    SEABIOS = "SEABIOS"
    OVMF = "OVMF"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.DiskInterface")
class DiskInterface(enum.Enum):
    SCSI = "SCSI"
    SATA = "SATA"
    VIRTIO = "VIRTIO"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.EmulatedType")
class EmulatedType(enum.Enum):
    _486 = "_486"
    BROADWELL = "BROADWELL"
    BROADWELL_IBRS = "BROADWELL_IBRS"
    BROADWELL_NO_TSX = "BROADWELL_NO_TSX"
    BROADWELL_NO_TSX_IBRS = "BROADWELL_NO_TSX_IBRS"
    CASCADELAKE_SERVER = "CASCADELAKE_SERVER"
    CONROE = "CONROE"
    EPYC = "EPYC"
    EPYC_IBPB = "EPYC_IBPB"
    EPYC_ROME = "EPYC_ROME"
    EPYC_MILAN = "EPYC_MILAN"
    HASWELL = "HASWELL"
    HASWELL_IBRS = "HASWELL_IBRS"
    HASWELL_NO_TSX = "HASWELL_NO_TSX"
    HASWELL_NO_TSX_IBRS = "HASWELL_NO_TSX_IBRS"
    HOST = "HOST"
    IVY_BRIDGE = "IVY_BRIDGE"
    IVY_BRIDGE_IBRS = "IVY_BRIDGE_IBRS"
    KNIGHTS_MILL = "KNIGHTS_MILL"
    NEHALEM = "NEHALEM"
    NEHALEM_IBRS = "NEHALEM_IBRS"
    OPTERON_G1 = "OPTERON_G1"
    OPTERON_G2 = "OPTERON_G2"
    OPTERON_G3 = "OPTERON_G3"
    OPTERON_G4 = "OPTERON_G4"
    OPTERON_G5 = "OPTERON_G5"
    PENRYN = "PENRYN"
    SKYLAKE_CLIENT = "SKYLAKE_CLIENT"
    SKYLAKE_CLIENT_IBRS = "SKYLAKE_CLIENT_IBRS"
    SKYLAKE_SERVER = "SKYLAKE_SERVER"
    SKYLAKE_SERVER_IBRS = "SKYLAKE_SERVER_IBRS"
    SANDY_BRIDGE = "SANDY_BRIDGE"
    SANDY_BRIDGE_IBRS = "SANDY_BRIDGE_IBRS"
    WESTMERE = "WESTMERE"
    WESTMERE_IBRS = "WESTMERE_IBRS"
    ATHLON = "ATHLON"
    CORE2DUO = "CORE2DUO"
    COREDUO = "COREDUO"
    KVM32 = "KVM32"
    KVM64 = "KVM64"
    MAX = "MAX"
    PENTIUM = "PENTIUM"
    PENTIUM2 = "PENTIUM2"
    PENTIUM3 = "PENTIUM3"
    PHENOM = "PHENOM"
    QEMU32 = "QEMU32"
    QEMU64 = "QEMU64"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.FileFormat")
class FileFormat(enum.Enum):
    RAW = "RAW"
    VMDK = "VMDK"
    QCOW2 = "QCOW2"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.KeyboardLayout")
class KeyboardLayout(enum.Enum):
    DA = "DA"
    DE = "DE"
    DE_CH = "DE_CH"
    EN_GB = "EN_GB"
    EN_US = "EN_US"
    ES = "ES"
    FI = "FI"
    FR = "FR"
    FR_BE = "FR_BE"
    FR_CA = "FR_CA"
    FR_CH = "FR_CH"
    HU = "HU"
    IS = "IS"
    IT = "IT"
    JA = "JA"
    LT = "LT"
    NL = "NL"
    NO = "NO"
    PL = "PL"
    PT = "PT"
    PT_BR = "PT_BR"
    SL = "SL"
    SV = "SV"
    TR = "TR"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.MachineType")
class MachineType(enum.Enum):
    I440FX = "I440FX"
    Q35 = "Q35"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.NetworkHashPolicy")
class NetworkHashPolicy(enum.Enum):
    LAYER_2 = "LAYER_2"
    LAYER_2_3 = "LAYER_2_3"
    LAYER_3 = "LAYER_3"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.NetworkInterfaceModel")
class NetworkInterfaceModel(enum.Enum):
    VIRTIO = "VIRTIO"
    E1000 = "E1000"
    RTL8139 = "RTL8139"
    VMXNET3 = "VMXNET3"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.NetworkMode")
class NetworkMode(enum.Enum):
    BALANCE_RR = "BALANCE_RR"
    ACTIVE_BACKUP = "ACTIVE_BACKUP"
    BALANCE_XOR = "BALANCE_XOR"
    BALANCE_TLB = "BALANCE_TLB"
    BALANCE_ALB = "BALANCE_ALB"
    BALANCE_SLB = "BALANCE_SLB"
    BROADCAST = "BROADCAST"
    LCAP_802_3AD = "LCAP_802_3AD"
    LCAP_BALANCE_SLB = "LCAP_BALANCE_SLB"
    LCAP_BALANCE_TCP = "LCAP_BALANCE_TCP"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.OsType")
class OsType(enum.Enum):
    L24 = "L24"
    L26 = "L26"
    OTHER = "OTHER"
    WINDOWS_XP = "WINDOWS_XP"
    WINDOWS_2000 = "WINDOWS_2000"
    WINDOWS_2003 = "WINDOWS_2003"
    WINDOWS_2008 = "WINDOWS_2008"
    WINDOWS_VISTA = "WINDOWS_VISTA"
    WINDOWS_7 = "WINDOWS_7"
    WINDOWS_8 = "WINDOWS_8"
    WINDOWS_10 = "WINDOWS_10"
    WINDOWS_11 = "WINDOWS_11"
    SOLARIS = "SOLARIS"


@jsii.enum(jsii_type="@awlsring/cdktf-proxmox.ZFSRaidLevel")
class ZFSRaidLevel(enum.Enum):
    SINGLE = "SINGLE"
    MIRROR = "MIRROR"
    RAIDZ = "RAIDZ"
    RAIDZ2 = "RAIDZ2"
    RAIDZ3 = "RAIDZ3"


__all__ = [
    "AgentType",
    "Architecture",
    "Bios",
    "DiskInterface",
    "EmulatedType",
    "FileFormat",
    "KeyboardLayout",
    "MachineType",
    "NetworkHashPolicy",
    "NetworkInterfaceModel",
    "NetworkMode",
    "OsType",
    "ZFSRaidLevel",
    "data_proxmox_lvm_storage_classes",
    "data_proxmox_lvm_thinpool_storage_classes",
    "data_proxmox_lvm_thinpools",
    "data_proxmox_lvms",
    "data_proxmox_network_bonds",
    "data_proxmox_network_bridges",
    "data_proxmox_nfs_storage_classes",
    "data_proxmox_node_storage_lvm_thinpools",
    "data_proxmox_node_storage_lvms",
    "data_proxmox_node_storage_nfs",
    "data_proxmox_node_storage_zfs",
    "data_proxmox_nodes",
    "data_proxmox_resource_pools",
    "data_proxmox_template",
    "data_proxmox_templates",
    "data_proxmox_virtual_machines",
    "data_proxmox_zfs_pools",
    "data_proxmox_zfs_storage_classes",
    "lvm",
    "lvm_storage_class",
    "lvm_thinpool",
    "lvm_thinpool_storage_class",
    "network_bond",
    "network_bridge",
    "nfs_storage_class",
    "provider",
    "resource_pool",
    "virtual_machine",
    "zfs_pool",
    "zfs_storage_class",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import data_proxmox_lvm_storage_classes
from . import data_proxmox_lvm_thinpool_storage_classes
from . import data_proxmox_lvm_thinpools
from . import data_proxmox_lvms
from . import data_proxmox_network_bonds
from . import data_proxmox_network_bridges
from . import data_proxmox_nfs_storage_classes
from . import data_proxmox_node_storage_lvm_thinpools
from . import data_proxmox_node_storage_lvms
from . import data_proxmox_node_storage_nfs
from . import data_proxmox_node_storage_zfs
from . import data_proxmox_nodes
from . import data_proxmox_resource_pools
from . import data_proxmox_template
from . import data_proxmox_templates
from . import data_proxmox_virtual_machines
from . import data_proxmox_zfs_pools
from . import data_proxmox_zfs_storage_classes
from . import lvm
from . import lvm_storage_class
from . import lvm_thinpool
from . import lvm_thinpool_storage_class
from . import network_bond
from . import network_bridge
from . import nfs_storage_class
from . import provider
from . import resource_pool
from . import virtual_machine
from . import zfs_pool
from . import zfs_storage_class
