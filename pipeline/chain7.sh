#!/bin/bash
cd /workspace/penn_campus
runr(){ $1; grep -q "BAKE 0" $(dirname $1)/../$(basename $1 .sh | sed s/run_//)/stage.txt || { sleep 30; $1; }; }
pub(){
  st=$(tr "\n" " " < $1/stage.txt); echo "$st" | grep -q "BUILD 0 BAKE 0 FINISH 0 LODCHECK 0" || { echo "STAGEFAIL $1 :: $st" | tee -a _audit/gate.log; echo DONE_$1 | tee -a _audit/gate.log; return; }
  r=$(_audit/lodok.sh $1); ov=$(blender -b $1/work_geo.blend -P _audit/overlap.py 2>/dev/null | grep OVERLAP); echo "$r || $ov" | tee -a _audit/gate.log
  echo "$ov" | grep -q "bad 0 " || r="$r OVERLAPFAIL"
  python3 _audit/sbs.py $1 0,1 | tee -a _audit/gate.log
  if echo "$r" | grep -q PASS && echo "$r" | grep -qE 'flt 0 0 0' && ! echo "$r" | grep -q OVERLAPFAIL; then
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
echo '==== PHASE4b (chain7, stage-guarded) ====' >> _audit/gate.log
runr _pipe/run_PennMuseum.sh
pub PennMuseum NA_PennMuseum_21x15 "Penn Museum" 21x15 "OSM rel 5231601 164.9x114.0 m" "Penn Museum: open portal frame, door clear"
runr _pipe/run_SteinbergDietrich.sh
pub SteinbergDietrich NA_SteinbergDietrich_16x10 "Steinberg-Dietrich Hall" 16x10 "OSM way 51469702 127.4x78.5 m" "Steinberg-Dietrich v3: dark brown brick, nameplate/door spacing"
runr _pipe/run_QuadMemorialTower.sh
pub QuadMemorialTower NA_QuadMemorialTower_3x3 "Quad: MemorialTower" 3x3 "OSM way 320602388 22.1x21.6 m" "QuadMemorialTower: no glass behind door/stone (overlap gate)"
runr _pipe/run_QuadSpeakman.sh
pub QuadSpeakman NA_QuadSpeakman_7x3 "Quad: Speakman" 7x3 "OSM way 320602397 51.2x17.5 m" "QuadSpeakman: no glass behind door/stone (overlap gate)"
runr _pipe/run_QuadMcClelland.sh
pub QuadMcClelland NA_QuadMcClelland_6x3 "Quad: McClelland" 6x3 "OSM way 320602420 45.6x18.8 m" "QuadMcClelland: no glass behind door/stone (overlap gate)"
runr _pipe/run_QuadWard.sh
pub QuadWard NA_QuadWard_4x4 "Quad: Ward" 4x4 "OSM way 320602400 23.6x23.3 m" "QuadWard: no glass behind door/stone (overlap gate)"
runr _pipe/run_QuadMcKean.sh
pub QuadMcKean NA_QuadMcKean_5x4 "Quad: McKean" 5x4 "OSM way 320602389 33.5x22.6 m" "Add Quad: McKean (NA_QuadMcKean_5x4)"
runr _pipe/run_QuadBaldwinW.sh
pub QuadBaldwinW NA_QuadBaldwinW_3x3 "Quad: BaldwinW" 3x3 "OSM way 320602390 16.9x16.9 m" "Add Quad: BaldwinW (NA_QuadBaldwinW_3x3)"
runr _pipe/run_QuadBaldwinE.sh
pub QuadBaldwinE NA_QuadBaldwinE_3x3 "Quad: BaldwinE" 3x3 "OSM way 320602391 14.9x13.5 m" "Add Quad: BaldwinE (NA_QuadBaldwinE_3x3)"
runr _pipe/run_QuadFoerderer.sh
pub QuadFoerderer NA_QuadFoerderer_4x3 "Quad: Foerderer" 4x3 "OSM way 320602392 24.0x12.0 m" "Add Quad: Foerderer (NA_QuadFoerderer_4x3)"
runr _pipe/run_QuadFranklin.sh
pub QuadFranklin NA_QuadFranklin_4x3 "Quad: Franklin" 4x3 "OSM way 320602393 24.6x15.8 m" "Add Quad: Franklin (NA_QuadFranklin_4x3)"
runr _pipe/run_QuadLeidy.sh
pub QuadLeidy NA_QuadLeidy_4x3 "Quad: Leidy" 4x3 "OSM way 320602394 23.4x15.7 m" "Add Quad: Leidy (NA_QuadLeidy_4x3)"
runr _pipe/run_QuadBrooks.sh
pub QuadBrooks NA_QuadBrooks_4x3 "Quad: Brooks" 4x3 "OSM way 320602395 23.1x15.8 m" "Add Quad: Brooks (NA_QuadBrooks_4x3)"
runr _pipe/run_QuadClassOf28.sh
pub QuadClassOf28 NA_QuadClassOf28_3x3 "Quad: ClassOf28" 3x3 "OSM way 320602396 21.4x16.2 m" "Add Quad: ClassOf28 (NA_QuadClassOf28_3x3)"
runr _pipe/run_QuadButcher.sh
pub QuadButcher NA_QuadButcher_5x3 "Quad: Butcher" 5x3 "OSM way 320602398 35.5x14.2 m" "Add Quad: Butcher (NA_QuadButcher_5x3)"
runr _pipe/run_QuadChestnut.sh
pub QuadChestnut NA_QuadChestnut_3x3 "Quad: Chestnut" 3x3 "OSM way 320602399 17.5x16.5 m" "Add Quad: Chestnut (NA_QuadChestnut_3x3)"
runr _pipe/run_QuadNewYorkAlumni.sh
pub QuadNewYorkAlumni NA_QuadNewYorkAlumni_3x3 "Quad: NewYorkAlumni" 3x3 "OSM way 320602401 19.0x13.0 m" "Add Quad: NewYorkAlumni (NA_QuadNewYorkAlumni_3x3)"
runr _pipe/run_QuadCarruth.sh
pub QuadCarruth NA_QuadCarruth_3x3 "Quad: Carruth" 3x3 "OSM way 320602402 14.9x13.3 m" "Add Quad: Carruth (NA_QuadCarruth_3x3)"
runr _pipe/run_QuadCraig.sh
pub QuadCraig NA_QuadCraig_3x3 "Quad: Craig" 3x3 "OSM way 320602403 20.3x17.5 m" "Add Quad: Craig (NA_QuadCraig_3x3)"
runr _pipe/run_QuadBaird.sh
pub QuadBaird NA_QuadBaird_3x3 "Quad: Baird" 3x3 "OSM way 320602404 16.7x16.4 m" "Add Quad: Baird (NA_QuadBaird_3x3)"
runr _pipe/run_QuadHopkinson.sh
pub QuadHopkinson NA_QuadHopkinson_3x3 "Quad: Hopkinson" 3x3 "OSM way 320602406 16.6x16.3 m" "Add Quad: Hopkinson (NA_QuadHopkinson_3x3)"
runr _pipe/run_QuadSmith.sh
pub QuadSmith NA_QuadSmith_3x3 "Quad: Smith" 3x3 "OSM way 320602407 16.6x15.9 m" "Add Quad: Smith (NA_QuadSmith_3x3)"
runr _pipe/run_QuadLippincott.sh
pub QuadLippincott NA_QuadLippincott_3x3 "Quad: Lippincott" 3x3 "OSM way 320602408 17.1x16.1 m" "Add Quad: Lippincott (NA_QuadLippincott_3x3)"
runr _pipe/run_QuadMorgan.sh
pub QuadMorgan NA_QuadMorgan_4x3 "Quad: Morgan" 4x3 "OSM way 320602409 25.0x12.1 m" "Add Quad: Morgan (NA_QuadMorgan_4x3)"
runr _pipe/run_QuadWilson.sh
pub QuadWilson NA_QuadWilson_3x3 "Quad: Wilson" 3x3 "OSM way 320602410 18.6x14.7 m" "Add Quad: Wilson (NA_QuadWilson_3x3)"
runr _pipe/run_QuadEFSmith.sh
pub QuadEFSmith NA_QuadEFSmith_4x3 "Quad: EFSmith" 4x3 "OSM way 320602411 23.7x14.1 m" "Add Quad: EFSmith (NA_QuadEFSmith_4x3)"
runr _pipe/run_QuadCoxe.sh
pub QuadCoxe NA_QuadCoxe_4x3 "Quad: Coxe" 4x3 "OSM way 320602412 24.1x14.3 m" "Add Quad: Coxe (NA_QuadCoxe_4x3)"
runr _pipe/run_QuadRodney.sh
pub QuadRodney NA_QuadRodney_4x3 "Quad: Rodney" 4x3 "OSM way 320602413 24.6x16.3 m" "Add Quad: Rodney (NA_QuadRodney_4x3)"
runr _pipe/run_QuadBishopWhite.sh
pub QuadBishopWhite NA_QuadBishopWhite_4x3 "Quad: BishopWhite" 4x3 "OSM way 320602414 23.7x14.2 m" "Add Quad: BishopWhite (NA_QuadBishopWhite_4x3)"
runr _pipe/run_QuadAshhurst.sh
pub QuadAshhurst NA_QuadAshhurst_3x3 "Quad: Ashhurst" 3x3 "OSM way 320602415 22.3x14.3 m" "Add Quad: Ashhurst (NA_QuadAshhurst_3x3)"
runr _pipe/run_QuadMagee.sh
pub QuadMagee NA_QuadMagee_4x3 "Quad: Magee" 4x3 "OSM way 320602416 27.9x17.4 m" "Add Quad: Magee (NA_QuadMagee_4x3)"
runr _pipe/run_QuadCleemann.sh
pub QuadCleemann NA_QuadCleemann_4x3 "Quad: Cleemann" 4x3 "OSM way 320602417 28.1x10.7 m" "Add Quad: Cleemann (NA_QuadCleemann_4x3)"
runr _pipe/run_QuadMorris.sh
pub QuadMorris NA_QuadMorris_4x4 "Quad: Morris" 4x4 "OSM way 320602418 30.7x19.7 m" "Add Quad: Morris (NA_QuadMorris_4x4)"
runr _pipe/run_QuadBodine.sh
pub QuadBodine NA_QuadBodine_3x3 "Quad: Bodine" 3x3 "OSM way 320602419 22.5x15.7 m" "Add Quad: Bodine (NA_QuadBodine_3x3)"
runr _pipe/run_QuadWarwick.sh
pub QuadWarwick NA_QuadWarwick_4x3 "Quad: Warwick" 4x3 "OSM way 320602421 30.0x14.0 m" "Add Quad: Warwick (NA_QuadWarwick_4x3)"
echo CHAIN7_END >> _audit/gate.log
