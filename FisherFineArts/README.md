# Fisher Fine Arts Library

`NA_FisherFineArts_8x6` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 8x6 |
| Model bounds (incl. lot surface) | 64.0 x 48.0 x 38.05 m |
| Real reference | NRHP 72001154: plan ~42.7x24.4 m, apse r 11.8 m; Frank Furness 1888-91 |
| LOD0 tris (Base / Win / Gls) | 15816 / 398 / 0 |
| LOD1 tris (Base / Win / Gls) | 12264 / 398 / 0 |
| LOD2 tris | 336 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_FisherFineArts_8x6_Base | 15816 | 0 | 1230 | 0 | 0 | 0 | 0 |
| NA_FisherFineArts_8x6_Win | 398 | 578 | 0 | 0 | 0 | 0 | 90 |
| NA_FisherFineArts_8x6_LOD1_Base | 12264 | 0 | 1230 | 0 | 0 | 0 | 0 |
| NA_FisherFineArts_8x6_LOD1_Win | 398 | 578 | 0 | 0 | 0 | 0 | 90 |
| NA_FisherFineArts_8x6_LOD2_Base | 336 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
