#!/bin/bash
cd /workspace/penn_campus
pub(){
  r=$(_audit/lodok.sh $1); echo "$r" | tee -a _audit/gate.log
  python3 _audit/sbs.py $1 0,1 | tee -a _audit/gate.log
  if echo "$r" | grep -q PASS && echo "$r" | grep -qE 'flt 0 0 0'; then
    python3 _pipe/zipit.py $PWD/$1 $2 $1 >/dev/null
    if [ $(stat -c%s zips/${1}_B_textures.zip) -gt 24000000 ]; then
      (cd $1 && python3 -c "
from PIL import Image; import glob
for p in glob.glob('$2_*.png'):
    if 'LOD2' in p: continue
    im=Image.open(p)
    if im.size[0]>2048: im.resize((2048,2048),Image.LANCZOS).save(p,optimize=True); print('resized2048',p)
") | tee -a _audit/gate.log
    fi
    bash _pipe/pub1.sh $1 $2 $1 "$3" $4 "$5" $4 "$6" | tee -a _audit/gate.log
    cd /workspace/Penn-CS2-Assets && mkdir -p _audit/sbs && cp /workspace/penn_campus/_audit/sbs/${1}_sbs.jpg _audit/sbs/ && cp /workspace/penn_campus/$1/build.py _pipe/${1}_build.py && cp /workspace/penn_campus/_pipe/quad_lib.py _pipe/ && cp /workspace/penn_campus/SOURCES.md . && git add -A && git commit -qm "$6 (sbs)"; timeout 500 git push -q
    cd /workspace/penn_campus
  else echo "FAIL_STRICT $1 :: $r" | tee -a _audit/gate.log; fi
  echo DONE_$1 | tee -a _audit/gate.log
}
echo '==== PHASE3 ====' >> _audit/gate.log
_pipe/run_SteinbergDietrich.sh
pub SteinbergDietrich NA_SteinbergDietrich_16x10 "Steinberg-Dietrich Hall" 16x10 "OSM way 51469702 127.4x78.5 m" "Steinberg-Dietrich v2: real-photo match (dark brick, chamfered glazed entry bay)"
for spec in "QuadMemorialTower 3x3|Quad: Memorial Tower|OSM way 320602388 22.1x21.6 m" "QuadSpeakman 7x3|Quad: Speakman|OSM way 320602397 51.2x17.5 m" "QuadMcClelland 6x3|Quad: McClelland|OSM way 320602420 45.6x18.8 m" "QuadWard 4x4|Quad: Ward|OSM way 320602400 23.6x23.3 m" "QuadFitler 3x3|Quad: Fitler|OSM way 320602405 16.7x16.2 m"; do
  IFS='|' read a nm real <<< "$spec"; n=${a% *}; l=${a#* }
  _pipe/run_$n.sh
  pub $n NA_${n}_$l "$nm" $l "$real" "Add $nm (NA_${n}_$l)"
done
echo CHAIN5_END >> _audit/gate.log
