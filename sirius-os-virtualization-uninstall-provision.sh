#!/bin/bash
# Sirius-OS Virtualization Uninstall Provisioning
set -euo pipefail

SERVICE_FILE="/etc/systemd/system/sirius-os-virtualization-uninstall.service"
TASK_FILE="/etc/sirius-os-virtualization-uninstall/sirius-os-virtualization-uninstaller.sh"

if [ -e "$SERVICE_FILE" ] || [ -e "$TASK_FILE" ]; then
  echo "ℹ️  Uninstall provision already exists; skipping."
  exit 0
fi

CLEANUP_DIR="/etc/sirius-os-virtualization-uninstall"
UNINSTALL_DIR="$CLEANUP_DIR"

echo "⚙️  Provisioning dormant cleanup infrastructure..."

mkdir -p "$UNINSTALL_DIR"

cat <<'EOF' > "$TASK_FILE"
#!/bin/bash
set -euo pipefail

echo "🧹 Removing Sirius-OS Virtualization..."

# Remove firewalld services
rm -f /etc/firewalld/services/container-http.xml
rm -f /etc/firewalld/services/container-https.xml
rm -f /etc/firewalld/services/container-https-alt.xml
rm -f /etc/firewalld/services/quick-share.xml

# Remove firewalld zone
rm -f /etc/firewalld/zones/libvirt.xml

# Remove libvirt network configs
rm -f /etc/libvirt/qemu/networks/default.xml
rm -f /etc/libvirt/qemu/networks/autostart/default.xml

# Reload firewalld
firewall-cmd --reload 2>/dev/null || :

# Clean up empty directories
rmdir /etc/firewalld/services 2>/dev/null || :
rmdir /etc/firewalld/zones 2>/dev/null || :
rmdir /etc/libvirt/qemu/networks/autostart 2>/dev/null || :
rmdir /etc/libvirt/qemu/networks 2>/dev/null || :

# Remove provisioning marker
rm -f /etc/sirius-os/libvirt-provisioned

# Remove self
rm -f /etc/sirius-os-virtualization-uninstall/sirius-os-virtualization-uninstaller.sh
rmdir /etc/sirius-os-virtualization-uninstall 2>/dev/null || :

# Remove the service file and its symlink
rm -f /etc/systemd/system/multi-user.target.wants/sirius-os-virtualization-uninstall.service
rm -f /etc/systemd/system/sirius-os-virtualization-uninstall.service

echo "✨ Sirius-OS Virtualization has been removed."
EOF

chmod +x "$TASK_FILE"

# Create uninstall service
cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Sirius-OS Virtualization Uninstall
ConditionPathExists=!/usr/libexec/sirius-os-virtualization-libvirt-provisioning.sh
DefaultDependencies=no
After=local-fs.target
Before=multi-user.target

[Service]
Type=oneshot
User=root
ExecStart=/usr/bin/bash $TASK_FILE

[Install]
WantedBy=multi-user.target
EOF

# Enable the uninstall service
mkdir -p /etc/systemd/system/multi-user.target.wants
ln -sf "$SERVICE_FILE" /etc/systemd/system/multi-user.target.wants/sirius-os-virtualization-uninstall.service

echo "✅ Uninstall task installed"
