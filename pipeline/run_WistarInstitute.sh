#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/WistarInstitute
export BD=$PWD AN=NA_WistarInstitute_17x8 BRICKCOL=0.55,0.28,0.12 ROOFCOL=0.25,0.24,0.22 CARVECOL=0.55,0.42,0.30 LIMECOL=0.78,0.72,0.60 SASHM=Iron IRONCOL=0.10,0.10,0.10 IRONMET=0
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
