#!/bin/bash
cd /workspace/penn_campus
pub(){
  r=$(_audit/lodok.sh $1); echo "$r" | tee -a _audit/gate.log
  python3 _audit/sbs.py $1 0,1 | tee -a _audit/gate.log
  if echo "$r" | grep -q PASS && echo "$r" | grep -qE 'LOD0 bnd 0' && echo "$r" | grep -qE 'flt 0 0 0'; then
    bash _pipe/pub1.sh $1 $2 $1 "$3" $4 "$5" $4 "$6" | tee -a _audit/gate.log
    cd /workspace/Penn-CS2-Assets && mkdir -p _audit/sbs && cp /workspace/penn_campus/_audit/sbs/${1}_sbs.jpg _audit/sbs/ && cp /workspace/penn_campus/$1/build.py _pipe/${1}_build.py && cp /workspace/penn_campus/SOURCES.md . && git add -A && git commit -qm "$6" && timeout 500 git push -q
    cd /workspace/penn_campus
  else echo "FAIL_STRICT $1 :: $r" | tee -a _audit/gate.log; fi
  echo DONE_$1 | tee -a _audit/gate.log
}
echo '' >> _audit/gate.log
echo '==== PHASE2 ====' >> _audit/gate.log
_pipe/run_HillCollegeHouse.sh
pub HillCollegeHouse NA_HillCollegeHouse_10x6 "Hill College House" 10x6 "OSM rel 5235124 78.9x45.7 m; Saarinen 1960" "Add Hill College House (NA_HillCollegeHouse_10x6)"
_pipe/run_ClaudiaCohenHall.sh
pub ClaudiaCohenHall NA_ClaudiaCohenHall_7x5 "Claudia Cohen Hall" 7x5 "OSM way 51367397 49.5x34.7 m; ex-Logan Hall" "Add Claudia Cohen Hall (NA_ClaudiaCohenHall_7x5)"
_pipe/run_SteinbergDietrich.sh
pub SteinbergDietrich NA_SteinbergDietrich_16x10 "Steinberg-Dietrich Hall" 16x10 "OSM way 51469702 127.4x78.5 m" "Add Steinberg-Dietrich Hall (NA_SteinbergDietrich_16x10)"
_pipe/run_WistarInstitute.sh
pub WistarInstitute NA_WistarInstitute_17x8 "Wistar Institute" 17x8 "OSM way 32120133 130.5x62.0 m" "Add Wistar Institute (NA_WistarInstitute_17x8)"
_pipe/run_PennMuseum.sh
pub PennMuseum NA_PennMuseum_21x15 "Penn Museum" 21x15 "OSM rel 5231601 164.9x114.0 m" "Add Penn Museum (NA_PennMuseum_21x15)"
_pipe/run_FranklinField.sh
pub FranklinField NA_FranklinField_28x19 "Franklin Field" 28x19 "OSM way 665447049 219.7x149.9 m; exterior shell" "Add Franklin Field exterior (NA_FranklinField_28x19)"
echo CHAIN4_END >> _audit/gate.log
