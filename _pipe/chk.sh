cd /workspace/columbia_campus/$1; echo "== $1 $(grep -c ALLDONE render.log 2>/dev/null)"; grep -h "Traceback\|Error" build.log finish.log 2>/dev/null | head -3
grep CHECKS lodcheck.log | python3 -c "
import sys,json; d=json.loads(sys.stdin.read().split('CHECKS ',1)[1])
for k,v in d.items(): print(k.split('_',2)[-1],v['tris'],'bnd',v['boundary_edges'],'flt',v['floating'],'za',v['zero_area'],'lv',v['loose_verts'])"
