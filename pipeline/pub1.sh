#!/bin/bash
# pub1.sh <dir> <AN> <repoFolder> <Name> <lot> <real> <lotshort> <commitmsg>
export PATH=/workspace/tools:$PATH; C=/workspace/penn_campus
cd $C && python3 _pipe/rgbpng.py $C/$1 && python3 _pipe/zipit.py $C/$1 $2 $1 | tail -3
cd $C/_pipe && python3 publish.py $C/$1 $2 $3 "$4" "$5" "$6" || exit 1
cd /workspace/Penn-CS2-Assets
grep -q "| $4 |" README.md || python3 - "$4" "$3" "$2" "$7" <<'P'
import sys; n,f,a,l=sys.argv[1:]; s=open('README.md').read()
rows=[x for x in s.split('\n') if x.startswith('| ') and '](' in x]; last=rows[-1]
s=s.replace(last,last+f'\n| {n} | [{f}]({f}) | {a} | {l} |'); open('README.md','w').write(s)
P
git add -A && git commit -qm "$8" && git push -q 2>&1 | tail -1; git log --oneline | head -1
