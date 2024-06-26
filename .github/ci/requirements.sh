#!/usr/bin/env bash
#!/bin/bash

set -e
# set -u

echo '
Package: *
Pin: release o=LP-PPA-mozillateam
Pin-Priority: 1001

Package: firefox
Pin: version 1:1snap*
Pin-Priority: -1
' | sudo tee /etc/apt/preferences.d/mozilla-firefox
echo 'Unattended-Upgrade::Allowed-Origins:: "LP-PPA-mozillateam:${distro_codename}";' |
    sudo tee /etc/apt/apt.conf.d/51unattended-upgrades-firefox

sudo snap remove firefox ||
    (
        sudo systemctl stop var-snap-firefox-common-host\\x2dhunspell.mount &&
            sudo systemctl disable var-snap-firefox-common-host\\x2dhunspell.mount &&
            sudo snap remove firefox
    )

if ! which firefox >/dev/null 2>&1; then
    sudo apt install -y software-properties-common
    sudo add-apt-repository ppa:mozillateam/ppa -y
    sudo apt install -y firefox
fi

# pip install -r $(dirname $(realpath "$BASH_SOURCE"))/requirements.txt
pip install -r requirements.txt

debInst() {
    dpkg-query -Wf'${db:Status-abbrev}' "$1" 2>/dev/null | grep -q '^i'
}

if debInst "google-chrome-stable"; then
    printf 'WhyThe package %s is already !\n' "$1"
else
    wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo apt install -f ./google-chrome-stable_current_amd64.deb
fi
