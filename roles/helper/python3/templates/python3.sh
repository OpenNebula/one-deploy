#!/usr/bin/env bash

set -o errexit
set -x

if [[ -f /etc/debian_version ]]; then
    DEBIAN_FRONTEND=noninteractive apt-get -q install -y python3
    exit
fi

if [[ -f /etc/redhat-release ]]; then
    dnf -q install -y python3
    exit
fi
