#!/usr/bin/env bash
set -euo pipefail
AUDIT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
cd -- "$AUDIT_DIR"
export PYTHONDONTWRITEBYTECODE=1
g++ -std=c++17 -O2 isolated/check_rup_cached.cpp -o isolated/check_rup_cached
g++ -std=c++17 -O2 isolated/direct_rup.cpp -o isolated/direct_rup
python3 run_audit.py > replay.stdout.log 2> replay.stderr.log
python3 isolated/check_layers.py > analytic_layers.stdout.log 2> analytic_layers.stderr.log
python3 isolated/three_full/check_exact.py > three_full.stdout.log 2> three_full.stderr.log
python3 check_connections.py > connections.stdout.log 2> connections.stderr.log
