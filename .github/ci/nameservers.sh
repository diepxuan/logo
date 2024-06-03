#!/bin/bash

# Define the desired nameservers (replace with your preferred servers)
DNS_SERVER1="8.8.8.8"
DNS_SERVER2="1.1.1.1"

# Check if necessary tools are installed (resolvectl for netplan systems)
if ! command -v resolvectl &>/dev/null; then
    sudo apt install resolvconf
    # echo "This script requires 'resolvectl' to be installed. Please install it using 'sudo apt install resolvconf'."
    # exit 1
fi

# Identify the network interface type (eth0 for wired, wlan0 for wireless - adjust if needed)
INTERFACE_NAME=$(ip route show default | awk '{print $5}')

# Check if a valid interface is found
if [ -z "$INTERFACE_NAME" ]; then
    echo "Error: Could not identify the default network interface."
    exit 1
fi

# Check if Netplan is used (systemd-networkd for older systems)
if [[ -f "/etc/netplan/00-installer-config.yaml" ]]; then
    # Netplan is used, configure nameservers in YAML
    echo "Using Netplan for network configuration."
    sudo sed -i "s/dns-nameservers:.*/dns-nameservers: \['$DNS_SERVER1', '$DNS_SERVER2'\]/g" /etc/netplan/00-installer-config.yaml
    sudo netplan apply
else
    # Not using Netplan, configure nameservers for systemd-networkd
    echo "Using systemd-networkd for network configuration."
    sudo bash -c "echo 'nameserver='$DNS_SERVER1'\nnameserver='$DNS_SERVER2'\n' > /etc/resolv.conf"
    sudo chmod 644 /etc/resolv.conf
fi

echo "Nameservers set to: $DNS_SERVER1, $DNS_SERVER2"
