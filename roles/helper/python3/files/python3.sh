#!/usr/bin/env bash

: "${PYTHON3:=python3}"
: "${PYTHON3_NO_DOTS:=${PYTHON3//.}}"

set -o errexit
set -x

if [[ -f /etc/debian_version ]]; then
    DEBIAN_FRONTEND=noninteractive apt-get -q install -y "$PYTHON3"
    exit
fi

if [[ -f /etc/redhat-release ]]; then
    dnf -q install -y "$PYTHON3"
    exit
fi

if [[ -f /etc/SUSE-brand ]]; then
    zypper --non-interactive install -y "$PYTHON3_NO_DOTS"
    exit
fi
