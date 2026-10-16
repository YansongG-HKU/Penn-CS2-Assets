#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/SteinbergDietrich
export BD=$PWD AN=NA_SteinbergDietrich_16x10 BRICKCOL=0.17,0.08,0.055 ROOFCOL=0.45,0.45,0.46 CARVECOL=0.55,0.42,0.30 LIMECOL=0.66,0.62,0.56 SASHM=Iron IRONCOL=0.15,0.15,0.15 IRONMET=0  
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
