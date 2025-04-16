#!/usr/bin/env bash
#!/bin/bash

set -e
# set -u

# sudo killall firefox 2>/dev/null || true
# sudo killall google-chrome 2>/dev/null || true
# sudo killall chrome 2>/dev/null || true

curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --auth-key=${TS_OAUTH_SECRET} --accept-dns=true --accept-routes=true
tailscale status
ip a
ip r

nslookup ${DB_HOST} 10.10.1.253 || true
nslookup ${DB_HOST} 100.100.100.100 || true
# dig mysql.diepxuan.corp || true
# dig @10.10.1.253 mysql.diepxuan.corp || true
# dig @100.100.100.100 mysql.diepxuan.corp || true
# resolvectl status || cat /etc/resolv.conf

pip install facebook-scraper mysql-connector-python
pip install "lxml[html_clean]"

export TYPE="facebook"
python -u analytic || true

sudo tailscale logout

# sudo killall firefox 2>/dev/null || true
# sudo killall google-chrome 2>/dev/null || true
# sudo killall chrome 2>/dev/null || true
