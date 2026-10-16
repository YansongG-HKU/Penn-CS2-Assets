#!/bin/bash
cd /workspace/penn_campus
pub(){ # dir AN title lot real msg
  r=$(_audit/lodok.sh $1); echo "$r" >> _audit/gate.log
  python3 _audit/sbs.py $1 0,1 >> _audit/gate.log 2>&1
  if echo "$r" | grep -q PASS; then bash _pipe/pub1.sh $1 $2 $1 "$3" $4 "$5" $4 "$6" >> _audit/gate.log 2>&1
    cd /workspace/Penn-CS2-Assets && mkdir -p _audit/sbs && cp /workspace/penn_campus/_audit/sbs/$1_sbs.jpg _audit/sbs/ && cp /workspace/penn_campus/$1/build.py _pipe/$1_build.py && git add -A && git commit -qm "$1: build script + SBS" && timeout 300 git push -q; cd /workspace/penn_campus
  fi; echo "DONE $1" >> _audit/gate.log; }
while pgrep -f runFFA.sh >/dev/null || pgrep -f runCH.sh >/dev/null; do sleep 20; done
pub CollegeHall NA_CollegeHall_11x7 "College Hall" 11x7 "OSM way 51367353 ~84x52 m; 6 floors; Thomas W. Richards 1871-73" "College Hall v3: pointed Gothic windows, maroon frames, turrets/spires, colored banding"
pub FisherFineArts NA_FisherFineArts_8x6 "Fisher Fine Arts Library" 8x6 "NRHP 72001154: plan ~42.7x24.4 m, apse r 11.8 m; Frank Furness 1888-91" "Fisher v2: darker terracotta roof, rotunda gables/finials, terracotta bands"
_pipe/runHH.sh; pub HoustonHall NA_HoustonHall_11x5 "Houston Hall" 11x5 "OSM way 51469194 84.0x37.3 m; 4 floors; 1894-96" "Add Houston Hall (NA_HoustonHall_11x5)"
_pipe/runIA.sh; pub IrvineAuditorium NA_IrvineAuditorium_7x7 "Irvine Auditorium" 7x7 "OSM way 51469206 50.5x51.5 m; Trumbauer 1926-32" "Add Irvine Auditorium (NA_IrvineAuditorium_7x7)"
echo CHAIN_END >> _audit/gate.log
