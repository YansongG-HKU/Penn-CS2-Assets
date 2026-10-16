#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/IrvineAuditorium
export BD=$PWD AN=NA_IrvineAuditorium_7x7 BRICKCOL=0.36,0.14,0.09 ROOFCOL=0.20,0.21,0.23 CARVECOL=0.42,0.13,0.09 LIMECOL=0.72,0.68,0.58 SASHM=Iron IRONCOL=0.10,0.10,0.10 IRONMET=0
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
