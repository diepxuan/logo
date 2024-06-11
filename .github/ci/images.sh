#!/usr/bin/env bash
#!/bin/bash

set -e
# set -u

sudo killall firefox 2>/dev/null || true
sudo killall google-chrome 2>/dev/null || true
sudo killall chrome 2>/dev/null || true

export MODE="product"
export TYPE="images"
python -u analytic || true

sudo killall firefox 2>/dev/null || true
sudo killall google-chrome 2>/dev/null || true
sudo killall chrome 2>/dev/null || true
