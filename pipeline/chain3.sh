#!/bin/bash
cd /workspace/penn_campus
pub(){
  r=$(_audit/lodok.sh $1); echo "$r" | tee -a _audit/gate.log
  python3 _audit/sbs.py $1 0,1 | tee -a _audit/gate.log
  # strict: LOD0/1/2 bnd 0, floating 0
  if echo "$r" | grep -q PASS && echo "$r" | grep -qE 'LOD0 bnd 0' && echo "$r" | grep -qE 'flt 0 0 0'; then
    bash _pipe/pub1.sh $1 $2 $1 "$3" $4 "$5" $4 "$6" | tee -a _audit/gate.log
    cd /workspace/Penn-CS2-Assets && mkdir -p _audit/sbs && cp /workspace/penn_campus/_audit/sbs/${1}_sbs.jpg _audit/sbs/ && cp /workspace/penn_campus/$1/build.py _pipe/${1}_build.py && git add -A && git commit -qm "$6" && timeout 400 git push -q
    cd /workspace/penn_campus
  else echo "FAIL_STRICT $1 :: $r" | tee -a _audit/gate.log; fi
  echo DONE_$1 | tee -a _audit/gate.log
}
echo '==== IA ====' >> _audit/gate.log
_pipe/runIA.sh
pub IrvineAuditorium NA_IrvineAuditorium_7x7 "Irvine Auditorium" 7x7 "OSM 50.5x51.5 m; Trumbauer 1926-32" "Irvine v2: orphan open faces dropped, LOD bnd 0/0/0, softer caps"
echo '==== HH ====' >> _audit/gate.log
_pipe/runHH.sh
pub HoustonHall NA_HoustonHall_11x5 "Houston Hall" 11x5 "OSM 84.0x37.3 m; 1894-96" "Houston v2: deep grey schist RUSTCOL, curved entrance gable"
echo '==== VP ====' >> _audit/gate.log
_pipe/runVP.sh
pub VanPeltLibrary NA_VanPeltLibrary_18x6 "Van Pelt–Dietrich Library" 18x6 "OSM 140.7x46.7 m; 1962" "Add Van Pelt–Dietrich Library (NA_VanPeltLibrary_18x6)"
echo '==== AC ====' >> _audit/gate.log
_pipe/runAC.sh
pub AnnenbergCenter NA_AnnenbergCenter_10x9 "Annenberg Center" 10x9 "OSM 79.8x69.2 m; 1971" "Add Annenberg Center (NA_AnnenbergCenter_10x9)"
echo CHAIN3_END >> _audit/gate.log
