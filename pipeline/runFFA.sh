#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/FisherFineArts
export BD=$PWD AN=NA_FisherFineArts_8x6 BRICKCOL=0.42,0.16,0.09 ROOFCOL=0.20,0.11,0.08 CARVECOL=0.46,0.20,0.12 LIMECOL=0.52,0.28,0.19 SASHM=Iron IRONCOL=0.20,0.07,0.05 IRONMET=0
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
