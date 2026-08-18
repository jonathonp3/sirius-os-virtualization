# Sirius-OS Virtualization Stack

Installs the libvirt/virtnetworkd runtime foundation so virt-manager networking works correctly out of the box (including correct users/groups, permissions, and tmpfiles).

This RPM adds the libvirt networking runtime foundation needed for virt-manager. It installs tmpfiles rules and creates the required virtnetwork / libvirt-qemu groups plus the filesystem layout for libvirt networking state—such as `/var/lib/libvirt/dnsmasq`, `/var/lib/libvirt/network`, and `/var/log/libvirt/qemu`—with correct ownership and write permissions.

With these changes, `virtnetworkd.service` starts cleanly and runs dnsmasq, so libvirt networking behaves as expected and manual bridge creation is no longer necessary.

## Why This Exists

Container-first workflows tend to work well with modern Linux distributions, while traditional VM/virt-manager workflows require additional runtime provisioning. This project bridges that gap by providing a complete, ready-to-use virtualization stack.


What Gets Installed

    libvirt-daemon-config-network - Libvirt network configuration

    libvirt-daemon-kvm - KVM support for libvirt

    qemu-kvm - QEMU with KVM acceleration

    virt-install - Command-line tool for installing VMs

    virt-manager - GUI for managing virtual machines

    virt-viewer - SPICE/VNC viewer for VMs

Network Configuration

The package automatically:

    Creates the libvirt firewalld zone using the system default configuration

    Selects an available subnet (192.168.100-150.0/24) to avoid conflicts

    Configures the default NAT network with DHCP

    Enables the libvirt services: virtqemud, virtnetworkd, virtstoraged, and virtlogd


📦 Installation

On an existing system (Silverblue, Bazzite, Kinoite)

Add the COPR repository, then layer the package:

```bash
sudo curl -Lo /etc/yum.repos.d/_copr_jonathonp3-sirius-os.repo https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/repo/fedora-44/jonathonp3-sirius-os-fedora-44.repo
```

## Install the virtualization stack:
```bash
rpm-ostree install sirius-os-virtualization
```

Reboot to apply changes:
```bash
systemctl reboot
```

## Via BlueBuild / Custom Image

If you're building your own image with BlueBuild, add the COPR repository in your recipe.yml or in your config directory, then add the package(s) you want in the packages section.

Repository URL:
```bash
https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/repo/fedora-44/jonathonp3-sirius-os-fedora-44.repo
```

Add to your recipe:
```bash
- type: rpm-ostree
  install:
    - sirius-os-virtualization
```
    

## Uninstalling

To remove the virtualization stack:
```bash
rpm-ostree remove sirius-os-virtualization
systemctl reboot
```
The uninstall provisioner will clean up all artifacts, including firewall rules, network configurations, and service files.
License

GPLv3

This project is built and hosted via [Fedora COPR](https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/). 
