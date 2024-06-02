#!/usr/bin/env bash
#!/bin/bash

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

sudo apt install -y software-properties-common
sudo add-apt-repository ppa:mozillateam/ppa -y
sudo apt install -y firefox
