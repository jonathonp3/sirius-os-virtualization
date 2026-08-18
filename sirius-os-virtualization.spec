# Disable debug packages
%define debug_package %{nil}

Name:           sirius-os-virtualization
Version:        2.0.0
Release:        1%{?dist}
Summary:        User-Enabled Virtualization Stack for Sirius-OS
License:        GPLv3
URL:            https://github.com/jonathonp3/sirius-os-virtualization
BuildArch:      noarch

# --- SOURCES ---
Source0:        sirius-os-virtualization.sysusers
Source1:        sirius-os-virtualization.tmpfiles
Source2:        sirius-os-virtualization-default-net.xml
Source3:        sirius-os-virtualization-container-http.xml
Source4:        sirius-os-virtualization-container-https.xml
Source5:        sirius-os-virtualization-container-https-alt.xml
Source6:        sirius-os-virtualization-quick-share.xml
Source7:        sirius-os-virtualization-libvirt-provisioning.sh
Source8:        sirius-os-virtualization-libvirt-provision.service
Source9:        sirius-os-virtualization-uninstall-provision.sh
Source10:       sirius-os-virtualization-uninstall-provision.service

# --- DEPENDENCIES ---
Requires:       libvirt-daemon-config-network
Requires:       libvirt-daemon-kvm
Requires:       qemu-kvm
Requires:       virt-install
Requires:       virt-manager
Requires:       virt-viewer
Requires:       firewalld
Requires:       systemd

%description
Provides the full libvirt/virtnetworkd runtime foundation for Sirius-OS.
Uses the system default libvirt zone for maximum VPN compatibility.

%setup -c -T

%build
# No build needed

%install
# Create directories
mkdir -p %{buildroot}/usr/lib/sysusers.d
mkdir -p %{buildroot}/usr/lib/tmpfiles.d
mkdir -p %{buildroot}/usr/share/sirius-os
mkdir -p %{buildroot}/usr/libexec
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/usr/lib/systemd/system/multi-user.target.wants

# Install sysusers and tmpfiles
install -p -m 644 %{SOURCE0} %{buildroot}/usr/lib/sysusers.d/sirius-os-virtualization.conf
install -p -m 644 %{SOURCE1} %{buildroot}/usr/lib/tmpfiles.d/sirius-os-virtualization.conf

# Install source templates to /usr/share/sirius-os/
install -p -m 644 %{SOURCE2} %{buildroot}/usr/share/sirius-os/default-net.xml
install -p -m 644 %{SOURCE3} %{buildroot}/usr/share/sirius-os/container-http.xml
install -p -m 644 %{SOURCE4} %{buildroot}/usr/share/sirius-os/container-https.xml
install -p -m 644 %{SOURCE5} %{buildroot}/usr/share/sirius-os/container-https-alt.xml
install -p -m 644 %{SOURCE6} %{buildroot}/usr/share/sirius-os/quick-share.xml

# Install provisioning scripts
install -p -m 755 %{SOURCE7} %{buildroot}/usr/libexec/sirius-os-virtualization-libvirt-provisioning.sh
install -p -m 755 %{SOURCE9} %{buildroot}/usr/libexec/sirius-os-virtualization-uninstall-provision.sh

# Install systemd services
install -p -m 644 %{SOURCE8} %{buildroot}/usr/lib/systemd/system/sirius-os-virtualization-libvirt-provision.service
install -p -m 644 %{SOURCE10} %{buildroot}/usr/lib/systemd/system/sirius-os-virtualization-uninstall-provision.service

# Enable Services via Symlinks
ln -sf ../sirius-os-virtualization-libvirt-provision.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/sirius-os-virtualization-libvirt-provision.service
ln -sf ../sirius-os-virtualization-uninstall-provision.service %{buildroot}/usr/lib/systemd/system/multi-user.target.wants/sirius-os-virtualization-uninstall-provision.service

%post
# Reload systemd to pick up new services
systemctl daemon-reload 2>/dev/null || :

%postun
# Reload systemd after removal
systemctl daemon-reload 2>/dev/null || :

%files
/usr/lib/sysusers.d/sirius-os-virtualization.conf
/usr/lib/tmpfiles.d/sirius-os-virtualization.conf
/usr/share/sirius-os/default-net.xml
/usr/share/sirius-os/container-http.xml
/usr/share/sirius-os/container-https.xml
/usr/share/sirius-os/container-https-alt.xml
/usr/share/sirius-os/quick-share.xml
/usr/libexec/sirius-os-virtualization-libvirt-provisioning.sh
/usr/libexec/sirius-os-virtualization-uninstall-provision.sh
/usr/lib/systemd/system/sirius-os-virtualization-libvirt-provision.service
/usr/lib/systemd/system/sirius-os-virtualization-uninstall-provision.service
/usr/lib/systemd/system/multi-user.target.wants/sirius-os-virtualization-libvirt-provision.service
/usr/lib/systemd/system/multi-user.target.wants/sirius-os-virtualization-uninstall-provision.service

%changelog
* Tue Aug 18 2026 jonathon <jonathon@sirius-os> - 2.0.0-1
- MAJOR RELEASE: Transitioned to an innovative "Atomic-Native" Provisioning Architecture.
- Designed to solve rpm-ostree limitations:
    - Bypasses the lack of traditional %post scripts by using specialized provisioning services.
    - Implemented a "Relay" model to handle precise installation and uninstallation on immutable filesystems.
- Feature: Blueprint Provisioning Model:
    - Unit templates and XML configs are stored in /usr/share/sirius-os and deployed to /etc at runtime.
    - Ensures full user transparency and persistent, auditable control over virtualization services.
    - Includes a "Dormant Uninstaller" that triggers a 100% clean system purge upon RPM removal.
- Optimization: Intelligent Virtual Networking:
    - Implemented "Auto-Pivot" dynamic subnet selection (192.168.100-150.0/24).
    - Automatically detects and avoids conflicts with existing host or VPN routes.
    - Ensures the default virtual network is active and correctly configured on the first boot.
- Automatic Service Enablement:
    - Orchestrates the startup of modular libvirt daemons: virtqemud, virtnetworkd, virtstoraged, and virtlogd.
