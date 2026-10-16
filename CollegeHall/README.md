# College Hall

`NA_CollegeHall_11x7` - Cities: Skylines II asset (1 unit = 1 m, pivot at bottom centre of lot, FBX Forward -Z / Up Y).

| | |
|---|---|
| Lot | 11x7 |
| Model bounds (incl. lot surface) | 88.0 x 56.0 x 36.35 m |
| Real reference | OSM way 51367353 ~84x52 m; 6 floors; Thomas W. Richards 1871-73 |
| LOD0 tris (Base / Win / Gls) | 113156 / 3147 / 112 |
| LOD1 tris (Base / Win / Gls) | 80624 / 3147 / 112 |
| LOD2 tris | 144 |

Textures (`textures/`, 4096 px LOD0/LOD1 shared, 1024 px LOD2): `_BaseColor`, `_Normal` (OpenGL), `_MaskMap` (R metallic, G coat=0, B=0, A gloss), `_ControlMask`, `_Emissive`.
`settings.json` maps LOD1 textures to the shared LOD0 set (`sharedAssets`). Win sub-mesh uses the 5x5 window UV grid.

LOD verification: side-by-side LOD0/LOD1/LOD2 renders in `renders/lod_compare_*.png`; mesh checks (no flipped closed shells, no bad winding, no loose vertices, no floating parts in Base meshes) in table below.

| mesh | tris | boundary edges | non-manifold edges | zero-area faces | bad winding | flipped shells | floating parts |
|---|---|---|---|---|---|---|---|
| NA_CollegeHall_11x7_Base | 113156 | 0 | 22650 | 0 | 0 | 0 | 0 |
| NA_CollegeHall_11x7_Win | 3147 | 3781 | 0 | 0 | 0 | 0 | 317 |
| NA_CollegeHall_11x7_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_CollegeHall_11x7_LOD1_Base | 80624 | 0 | 22114 | 0 | 0 | 0 | 0 |
| NA_CollegeHall_11x7_LOD1_Win | 3147 | 3781 | 0 | 0 | 0 | 0 | 317 |
| NA_CollegeHall_11x7_LOD1_Gls | 112 | 0 | 0 | 0 | 0 | 0 | 2 |
| NA_CollegeHall_11x7_LOD2_Base | 144 | 0 | 0 | 0 | 0 | 0 | 0 |

(Boundary / non-manifold edges come from intentionally open trim pieces and touching/overlapping detail blocks; Win/Gls panes are single-sided planes that sit on the Base mesh, so they count as 'floating' inside their own sub-mesh.)

See `SOURCES.txt` / `ATTRIBUTION.txt` for dimensions sources and credits.

![front](renders/render_01_front34.png)
