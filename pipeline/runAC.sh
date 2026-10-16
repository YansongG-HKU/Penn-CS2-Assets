#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/AnnenbergCenter
export BD=$PWD AN=NA_AnnenbergCenter_10x9 BRICKCOL=0.38,0.22,0.13 ROOFCOL=0.35,0.35,0.36 CARVECOL=0.42,0.13,0.09 LIMECOL=0.78,0.76,0.72 SASHM=Iron IRONCOL=0.18,0.18,0.19 IRONMET=0
rm -f render.log stage.txt
blender -b -P build.py > build.log 2>&1; echo BUILD $? > stage.txt
blender -b -P $P/bake.py -- 4096 > bake.log 2>&1; echo BAKE $? >> stage.txt
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? >> stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
