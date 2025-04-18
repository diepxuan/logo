#!/usr/bin/env bash
#!/bin/bash

set -e
# set -u

pip install facebook-scraper mysql-connector-python
pip install "lxml[html_clean]"

export TYPE="facebook"
python -u analytic || true

