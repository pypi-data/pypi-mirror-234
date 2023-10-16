import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-proxmox",
    "version": "0.0.227",
    "description": "A package that vends generated constructs from the Proxmox Terraform provider",
    "license": "Apache-2.0",
    "url": "https://github.com/awlsring/cdktf-proxmox.git",
    "long_description_content_type": "text/markdown",
    "author": "awlsring<mattcanemail@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awlsring/cdktf-proxmox.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_proxmox",
        "cdktf_proxmox._jsii",
        "cdktf_proxmox.data_proxmox_lvm_storage_classes",
        "cdktf_proxmox.data_proxmox_lvm_thinpool_storage_classes",
        "cdktf_proxmox.data_proxmox_lvm_thinpools",
        "cdktf_proxmox.data_proxmox_lvms",
        "cdktf_proxmox.data_proxmox_network_bonds",
        "cdktf_proxmox.data_proxmox_network_bridges",
        "cdktf_proxmox.data_proxmox_nfs_storage_classes",
        "cdktf_proxmox.data_proxmox_node_storage_lvm_thinpools",
        "cdktf_proxmox.data_proxmox_node_storage_lvms",
        "cdktf_proxmox.data_proxmox_node_storage_nfs",
        "cdktf_proxmox.data_proxmox_node_storage_zfs",
        "cdktf_proxmox.data_proxmox_nodes",
        "cdktf_proxmox.data_proxmox_resource_pools",
        "cdktf_proxmox.data_proxmox_template",
        "cdktf_proxmox.data_proxmox_templates",
        "cdktf_proxmox.data_proxmox_virtual_machines",
        "cdktf_proxmox.data_proxmox_zfs_pools",
        "cdktf_proxmox.data_proxmox_zfs_storage_classes",
        "cdktf_proxmox.lvm",
        "cdktf_proxmox.lvm_storage_class",
        "cdktf_proxmox.lvm_thinpool",
        "cdktf_proxmox.lvm_thinpool_storage_class",
        "cdktf_proxmox.network_bond",
        "cdktf_proxmox.network_bridge",
        "cdktf_proxmox.nfs_storage_class",
        "cdktf_proxmox.provider",
        "cdktf_proxmox.resource_pool",
        "cdktf_proxmox.virtual_machine",
        "cdktf_proxmox.zfs_pool",
        "cdktf_proxmox.zfs_storage_class"
    ],
    "package_data": {
        "cdktf_proxmox._jsii": [
            "cdktf-proxmox@0.0.227.jsii.tgz"
        ],
        "cdktf_proxmox": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdktf>=0.14.0, <0.15.0",
        "constructs>=10.0.25, <11.0.0",
        "jsii>=1.90.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
