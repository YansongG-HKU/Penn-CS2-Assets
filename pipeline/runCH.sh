#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/CollegeHall
export BD=$PWD AN=NA_CollegeHall_11x7 BRICKCOL=0.33,0.40,0.27 ROOFCOL=0.24,0.25,0.28 CARVECOL=0.42,0.13,0.09 LIMECOL=0.66,0.55,0.40 SASHM=Iron IRONCOL=0.32,0.06,0.05 IRONMET=0
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
