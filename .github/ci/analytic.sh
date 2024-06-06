#!/usr/bin/env bash
#!/bin/bash

set -e
# set -u

sudo killall firefox 2>/dev/null || true

export MODE="product"
python -u analytic || true

sudo killall firefox 2>/dev/null || true