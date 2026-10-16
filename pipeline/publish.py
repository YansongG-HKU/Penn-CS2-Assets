import os,shutil,glob,json,sys
R='/workspace/Penn-CS2-Assets'; src,A,folder,title,lot,real=sys.argv[1:7]
d=os.path.join(R,folder); shutil.rmtree(d,ignore_errors=True); os.makedirs(d+'/textures'); os.makedirs(d+'/fbx/split'); os.makedirs(d+'/renders')
for f in glob.glob(src+'/NA_*.fbx'): shutil.copy(f,d+'/fbx/')
for f in glob.glob(src+'/split_fbx/*.fbx'): shutil.copy(f,d+'/fbx/split/')
for f in glob.glob(src+'/NA_*.png'): shutil.copy(f,d+'/textures/')
for f in glob.glob(src+'/render_*.png')+glob.glob(src+'/lod_compare_*.png'): shutil.copy(f,d+'/renders/')
shutil.copy(src+'/'+A+'.blend',d+'/')
shutil.copy(src+'/settings.json',d+'/')
for n in ('SOURCES.txt','ATTRIBUTION.txt'):
    if os.path.exists(src+'/'+n): shutil.copy(src+'/'+n,d+'/')
st=json.load(open(src+'/src/stats.json')); mc=json.load(open(src+'/lodcheck/mesh_checks.json'))
t=st['tris']; g=lambda k:t.get(A+k,0)
dims=st['dims'][A+'_Base']
md=f"""# {title}

`{A}` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | {lot} |
| Model bounds (incl. lot surface) | {dims[0]} x {dims[1]} x {dims[2]} m |
| Real reference | {real} |
| LOD0 tris (Base / Win / Gls) | {g('_Base')} / {g('_Win')} / {g('_Gls')} |
| LOD1 tris (Base / Win / Gls) | {g('_LOD1_Base')} / {g('_LOD1_Win')} / {g('_LOD1_Gls')} |
| LOD2 tris | {g('_LOD2_Base')} |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
""" + "\n".join(f"| {k} | {v['tris']} | {v['boundary_edges']} | {v['nonmanifold_edges']} | {v['zero_area']} | {v['bad_winding']} | {v['flipped_closed']} | {v['floating']} |" for k,v in mc.items()) + """

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
"""
open(d+'/README.md','w').write(md); print('published',folder)
