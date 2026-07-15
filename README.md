# Sirius-OS Virtualization Stack

Installs the libvirt/virtnetworkd runtime foundation for Fedora Atomic desktops so virt-manager networking works correctly out of the box (including users/groups, permissions, and tmpfiles).

This RPM adds the libvirt networking runtime foundation needed for virt-manager on Fedora Atomic-style images (including Bazzite). It installs /usr/lib/tmpfiles.d/ rules and creates the required virtnetwork/libvirt-qemu groups plus the filesystem layout for libvirt networking state—such as /var/lib/libvirt/dnsmasq, /var/lib/libvirt/network, and /var/log/libvirt/qemu—with correct ownership and write permissions at boot.

With these changes, virtnetworkd.service starts cleanly and runs dnsmasq, so libvirt networking behaves as it should. For my use case, manually creating a bridge is no longer necessary.

This project is built and hosted via [Fedora COPR](https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/). 


📦 Installation

1. On an Existing System (Sirius-OS, Silverblue, Bazzite)

If you are using a standard atomic desktop, add the repository manually and then layer the package:
bash

Add the Copr Repository
```bash
sudo curl -Lo /etc/yum.repos.d/_copr_jonathonp3-sirius-os.repo https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/repo/fedora-44/jonathonp3-sirius-os-fedora-44.repo
```
Install the Sirius-OS Virtualization Stack
```bash
rpm-ostree install sirius-os-virtualization
```
Reboot to apply changes
```bash
systemctl reboot
```

Via BlueBuild / Custom Image (Bazzite, Aurora, etc.)

If you are building your own image via BlueBuild, add the repository to your recipe.yml or your config directory:

Repository URL:
```bash
https://copr.fedorainfracloud.org/coprs/jonathonp3/sirius-os/repo/fedora-44/jonathonp3-sirius-os-fedora-44.repo
```
Under the packages section in recipe.yml:
yaml
```bash
  - type: rpm-ostree
    install:
      - sirius-os-virtualization
```


