#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/HoustonHall
export BD=$PWD AN=NA_HoustonHall_11x5 BRICKCOL=0.32,0.31,0.29 ROOFCOL=0.22,0.23,0.25 CARVECOL=0.42,0.13,0.09 LIMECOL=0.68,0.62,0.50 SASHM=Iron IRONCOL=0.12,0.12,0.12 IRONMET=0 RUSTCOL=0.38,0.37,0.35 GRANCOL=0.42,0.41,0.39
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
