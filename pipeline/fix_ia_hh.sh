#!/bin/bash
set -e
cd /workspace/penn_campus
pub(){ r=$(_audit/lodok.sh $1); echo "$r" | tee -a _audit/gate.log
  python3 _audit/sbs.py $1 0,1 | tee -a _audit/gate.log
  if echo "$r" | grep -q PASS && echo "$r" | grep -qE 'LOD0 bnd 0'; then
    bash _pipe/pub1.sh $1 $2 $1 "$3" $4 "$5" $4 "$6" | tee -a _audit/gate.log
    cd /workspace/Penn-CS2-Assets && mkdir -p _audit/sbs && cp /workspace/penn_campus/_audit/sbs/$1_sbs.jpg _audit/sbs/ && cp /workspace/penn_campus/$1/build.py _pipe/$1_build.py && git add -A && git commit -qm "$1: $6" && timeout 300 git push -q; cd /workspace/penn_campus
  else echo "FAIL_STRICT $1 $r" | tee -a _audit/gate.log; fi
  echo DONE_$1 | tee -a _audit/gate.log; }
_pipe/runIA.sh
pub IrvineAuditorium NA_IrvineAuditorium_7x7 "Irvine Auditorium" 7x7 "OSM 50.5x51.5 m; Trumbauer 1926-32" "Irvine v2: 0 boundary edges, softer buttress caps"
_pipe/runHH.sh
pub HoustonHall NA_HoustonHall_11x5 "Houston Hall" 11x5 "OSM 84.0x37.3 m; 1894-96" "Houston v2: deep grey schist, curved entrance gable"
echo FIX_CHAIN_END >> _audit/gate.log
