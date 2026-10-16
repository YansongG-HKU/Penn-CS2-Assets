#!/bin/bash
export PATH=/workspace/tools:$PATH; P=/workspace/penn_campus/_pipe
cd /workspace/penn_campus/CollegeHall
export BD=$PWD AN=NA_CollegeHall_11x7 BRICKCOL=0.28,0.42,0.30 ROOFCOL=0.18,0.18,0.20 CARVECOL=0.62,0.52,0.38
rm -f render.log
blender -b -P $P/finish.py > finish.log 2>&1; echo FINISH $? > stage.txt
blender -b $AN.blend -P $P/lodcheck.py > lodcheck.log 2>&1; echo LODCHECK $? >> stage.txt
blender -b $AN.blend -P $P/render.py -- 32 > render.log 2>&1; echo ALLDONE >> render.log; echo RENDER >> stage.txt
