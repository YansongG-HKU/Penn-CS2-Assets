# Steinberg-Dietrich Hall

`NA_SteinbergDietrich_16x10` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 16x10 |
| Model bounds (incl. lot surface) | 128.0 x 80.0 x 22.05 m |
| Real reference | OSM way 51469702 127.4x78.5 m |
| LOD0 tris (Base / Win / Gls) | 25644 / 384 / 0 |
| LOD1 tris (Base / Win / Gls) | 16356 / 384 / 0 |
| LOD2 tris | 60 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_SteinbergDietrich_16x10_Base | 25644 | 0 | 389 | 0 | 0 | 0 | 0 |
| NA_SteinbergDietrich_16x10_Win | 384 | 768 | 0 | 0 | 0 | 0 | 176 |
| NA_SteinbergDietrich_16x10_LOD1_Base | 16356 | 0 | 389 | 0 | 0 | 0 | 0 |
| NA_SteinbergDietrich_16x10_LOD1_Win | 384 | 768 | 0 | 0 | 0 | 0 | 176 |
| NA_SteinbergDietrich_16x10_LOD2_Base | 60 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
