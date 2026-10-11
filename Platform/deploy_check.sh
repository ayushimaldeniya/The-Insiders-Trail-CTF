#!/bin/bash

IP="192.168.56.20"
FAIL=0

check() {
    if eval "$2"; then
        echo "[PASS] $1"
    else
        echo "[FAIL] $1"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== The Insider's Trail: Deployment Check ==="

check "Host-only IP" "ip -4 addr show enp0s8 | grep -q '$IP'"
check "Docker daemon" "docker info >/dev/null 2>&1"

for c in ctfd-ctfd-1 ctfd-db-1 stage4-linux; do
    check "$c running" "docker inspect -f '{{.State.Running}}' '$c' 2>/dev/null | grep -qx true"
done

check "CTFd HTTP" "curl --connect-timeout 3 -s -o /dev/null -w '%{http_code}' http://$IP:8000 | grep -Eq '^(200|301|302|303|307|308)$'"

check "MariaDB internal network" "docker inspect -f '{{range \$n, \$v := .NetworkSettings.Networks}}{{\$n}} {{end}}' ctfd-db-1 2>/dev/null | tr ' ' '\n' | while read n; do docker network inspect -f '{{.Internal}}' \"\$n\" 2>/dev/null; done | grep -qx true"

check "Stage 4 SSH port" "timeout 3 bash -c 'echo > /dev/tcp/$IP/2222' 2>/dev/null"

if [ "$FAIL" -eq 0 ]; then
    echo "RESULT: ALL CHECKS PASSED"
    exit 0
else
    echo "RESULT: $FAIL CHECK(S) FAILED"
    exit 1
fi
