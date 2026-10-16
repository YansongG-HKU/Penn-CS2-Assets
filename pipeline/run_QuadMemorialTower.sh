#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/QuadMemorialTower
export BD=$PWD AN=NA_QuadMemorialTower_3x3 BRICKCOL=0.36,0.14,0.09 ROOFCOL=0.24,0.25,0.28 CARVECOL=0.55,0.42,0.30 LIMECOL=0.80,0.76,0.66 SASHM=Iron IRONCOL=0.10,0.10,0.10 IRONMET=0
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
