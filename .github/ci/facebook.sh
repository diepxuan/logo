#!/usr/bin/env bash
#!/bin/bash

set -e
# set -u

# sudo killall firefox 2>/dev/null || true
# sudo killall google-chrome 2>/dev/null || true
# sudo killall chrome 2>/dev/null || true

curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up --auth-key=${TS_OAUTH_SECRET} --accept-dns=true --accept-routes=true
nslookup ${DB_HOST} || true

pip install facebook-scraper mysql-connector-python
pip install "lxml[html_clean]"

export TYPE="facebook"
python -u analytic || true

# sudo killall firefox 2>/dev/null || true
# sudo killall google-chrome 2>/dev/null || true
# sudo killall chrome 2>/dev/null || true
