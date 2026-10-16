# Penn CS2 Assets

Cities: Skylines II building assets of the University of Pennsylvania (Philadelphia / University City) campus core,
modelled procedurally in Blender to the same standard as [Columbia-CS2-Assets](https://github.com/YansongG-HKU/Columbia-CS2-Assets):
real dimensions (1 unit = 1 m), detailed facades, full PBR texture set (`_BaseColor`, `_Normal`, `_MaskMap`,
`_ControlMask`, `_Emissive`), LOD0/LOD1/LOD2, Base/Win/Gls sub-meshes, CS2 window UV grid, `settings.json`,
FBX (Forward -Z, Up Y), lots sized in 8 m cells, names `NA_<Name>_<WxD>`.

| Building | Folder | Asset | Lot |
|---|---|---|---|
| College Hall | [CollegeHall](CollegeHall) | NA_CollegeHall_11x7 | 11x7 |
| Fisher Fine Arts Library | [FisherFineArts](FisherFineArts) | NA_FisherFineArts_8x6 | 8x6 |
| Houston Hall | [HoustonHall](HoustonHall) | NA_HoustonHall_11x5 | 11x5 |
| Irvine Auditorium | [IrvineAuditorium](IrvineAuditorium) | NA_IrvineAuditorium_7x7 | 7x7 |
| Van Pelt–Dietrich Library | [VanPeltLibrary](VanPeltLibrary) | NA_VanPeltLibrary_18x6 | 18x6 |

Each folder: `fbx/` (combined LOD FBX + `split/` per sub-mesh), `textures/`, `settings.json`, `<asset>.blend`,
`renders/` (day, aerial, close-up, night, LOD comparisons), `SOURCES.txt`, README with specs and mesh checks.

## Credits
- Footprints/heights: (c) OpenStreetMap contributors (ODbL) where cited; Penn Facilities, Wikipedia, NRHP, SAH Archipedia.
- All geometry and textures are procedurally generated for this project (no third-party meshes unless noted).
- Unofficial fan project; not affiliated with the University of Pennsylvania.
