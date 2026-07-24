#!/usr/bin/env bash
# managed by one-deploy

set -o errexit; shopt -s nullglob

/var/lib/one/remotes/hooks/raft/vip.sh "$@"

for SCRIPT in /var/lib/one/remotes/hooks/raft/failover.d/[0-9][0-9]-*; do
    if ! [[ -x "$SCRIPT" ]]; then continue; fi
    $SCRIPT "$@"
done
