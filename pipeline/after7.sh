#!/bin/bash
cd /workspace/penn_campus
while ! grep -q CHAIN7_END _audit/gate.log; do sleep 30; done
eval "$(sed -n '/^runr()/,/^}/p' _pipe/chain7.sh)"
echo '==== MUSEUM v3 (portal coplanar fix) ====' >> _audit/gate.log
runr _pipe/run_PennMuseum.sh
pub PennMuseum NA_PennMuseum_21x15 "Penn Museum" 21x15 "OSM rel 5231601 164.9x114.0 m" "Penn Museum: portal piers below head (no coplanar black patch), door clear"
echo AFTER7_END >> _audit/gate.log
