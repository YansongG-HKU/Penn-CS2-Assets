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
| Annenberg Center | [AnnenbergCenter](AnnenbergCenter) | NA_AnnenbergCenter_10x9 | 10x9 |
| Hill College House | [HillCollegeHouse](HillCollegeHouse) | NA_HillCollegeHouse_10x6 | 10x6 |
| Claudia Cohen Hall | [ClaudiaCohenHall](ClaudiaCohenHall) | NA_ClaudiaCohenHall_7x5 | 7x5 |
| Steinberg-Dietrich Hall | [SteinbergDietrich](SteinbergDietrich) | NA_SteinbergDietrich_16x10 | 16x10 |
| Wistar Institute | [WistarInstitute](WistarInstitute) | NA_WistarInstitute_17x8 | 17x8 |
| Franklin Field | [FranklinField](FranklinField) | NA_FranklinField_28x19 | 28x19 |
| Penn Museum | [PennMuseum](PennMuseum) | NA_PennMuseum_21x15 | 21x15 |
| Quad: Memorial Tower | [QuadMemorialTower](QuadMemorialTower) | NA_QuadMemorialTower_3x3 | 3x3 |
| Quad: Speakman | [QuadSpeakman](QuadSpeakman) | NA_QuadSpeakman_7x3 | 7x3 |
| Quad: McClelland | [QuadMcClelland](QuadMcClelland) | NA_QuadMcClelland_6x3 | 6x3 |
| Quad: Ward | [QuadWard](QuadWard) | NA_QuadWard_4x4 | 4x4 |
| Quad: Fitler | [QuadFitler](QuadFitler) | NA_QuadFitler_3x3 | 3x3 |
| Quad: MemorialTower | [QuadMemorialTower](QuadMemorialTower) | NA_QuadMemorialTower_3x3 | 3x3 |
| Quad: McKean | [QuadMcKean](QuadMcKean) | NA_QuadMcKean_5x4 | 5x4 |
| Quad: BaldwinW | [QuadBaldwinW](QuadBaldwinW) | NA_QuadBaldwinW_3x3 | 3x3 |
| Quad: BaldwinE | [QuadBaldwinE](QuadBaldwinE) | NA_QuadBaldwinE_3x3 | 3x3 |
| Quad: Foerderer | [QuadFoerderer](QuadFoerderer) | NA_QuadFoerderer_4x3 | 4x3 |
| Quad: Franklin | [QuadFranklin](QuadFranklin) | NA_QuadFranklin_4x3 | 4x3 |
| Quad: Leidy | [QuadLeidy](QuadLeidy) | NA_QuadLeidy_4x3 | 4x3 |
| Quad: Brooks | [QuadBrooks](QuadBrooks) | NA_QuadBrooks_4x3 | 4x3 |
| Quad: ClassOf28 | [QuadClassOf28](QuadClassOf28) | NA_QuadClassOf28_3x3 | 3x3 |
| Quad: Butcher | [QuadButcher](QuadButcher) | NA_QuadButcher_5x3 | 5x3 |
| Quad: Chestnut | [QuadChestnut](QuadChestnut) | NA_QuadChestnut_3x3 | 3x3 |
| Quad: NewYorkAlumni | [QuadNewYorkAlumni](QuadNewYorkAlumni) | NA_QuadNewYorkAlumni_3x3 | 3x3 |
| Quad: Carruth | [QuadCarruth](QuadCarruth) | NA_QuadCarruth_3x3 | 3x3 |

Each folder: `fbx/` (combined LOD FBX + `split/` per sub-mesh), `textures/`, `settings.json`, `<asset>.blend`,
`renders/` (day, aerial, close-up, night, LOD comparisons), `SOURCES.txt`, README with specs and mesh checks.

## Credits
- Footprints/heights: (c) OpenStreetMap contributors (ODbL) where cited; Penn Facilities, Wikipedia, NRHP, SAH Archipedia.
- All geometry and textures are procedurally generated for this project (no third-party meshes unless noted).
- Unofficial fan project; not affiliated with the University of Pennsylvania.
