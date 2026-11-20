# Irvine Auditorium: secondary roof surfaces

Three inset flat roof surfaces and three lower hipped roof surfaces (west, east, south), built in the same physically registered coordinate frame as the detached main roof. These are genuine same-scale surface meshes, with intentional open perimeter cutoffs, not a complete placeable asset. Walls, eave overhang/parapet, roof ties, north wing and its turret, upper spire, UVs/materials and LOD integration remain outside this prototype. The Editor trial ZIP is unchanged.

## Control data, fitting and verification

- Official 2022 [NOAA Pennsylvania EPT 9848](https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9848/ept.json), target bbox EPSG:6347 [483481,4422287,483550,4422356], NAVD88 GEOID18 metres. Bounded 16-cell QGIS extract (each below the 40,000 result cap), 205,337 distinct records across six analysis columns. Twenty-seven small LAZ nodes totalling 6,307,740 bytes, source receipts included. This covers exterior returns unavailable in the earlier narrow crop.
- Nearby flat decks are distinct from the outer hipped roofs, not one flat mass or the central upper eave. XY orientation uses the previously documented ortho roof axes; origin and Z from the LiDAR control. The 2025 oblique/parallax-sensitive orthophoto helps identify types, without using the apparent roof apex to translate the LiDAR or replacing measured heights from it. The deck model is mildly cambered, not a literal horizontal mathematical plane.
- Outer roofs require **five planes apiece**, not three: the side-to-front transition has two real diagonal facets, not mere noisy points. A 3-plane diagnostic fit over its inner sampled area had median ~0.17–0.18 m and p90 ~1.40–1.47 m. The five-plane candidate reduces those errors on the evaluated surfaces; exact footprints differed slightly by fit, so this is not a matched-pixel metric. Inner edge cutoffs are reduced to preserve known support. Seams between the planar regions share vertices.
- All measurements below use numerically intersected exported triangles at real withheld XY, not just equations. Source IDs 19 and 20 were excluded from estimation; the two data partitions were inspected as diagnostics during iteration, not treated as a blind test. There was no elevation gate on first, unclassified withheld returns under the final modeled surfaces. Each entry below gives an observed range across both full held scans and all relevant surfaces, not survey/instrument accuracy.

| Rebuilt section | Withheld first returns | Median absolute Z error range | p90 range |
| --- | ---: | ---: | ---: |
| 3 lower flat roof surfaces | 1,787 | 0.027–0.038 m | 0.072–0.084 m |
| 3 outer hipped roof surfaces | 2,184 | 0.073–0.099 m | 0.189–0.218 m |

Blender separately imported the exact OBJ (6 surfaces, 119 vertices, 137 upward triangles). Each surface has one deliberately open perimeter, no extra open ridge or inverted/internal seam, no degenerates or >2-face edges. These are geometry tests, not a display/material/LOD acceptance test. No asset parts were replaced or published.

## Replay

Use the prior main-roof calibration's `irvine-roof-plane-fit.json` and exact expanded NOAA CSV gzip digest from `secondary-roof-evidence.json`. Source node receipt and query audit let you reconstruct it (record identical observations after normalising CSV gzip metadata if applicable). Run `python3 build_secondary_roof_surfaces.py CSV_GZ ROOF_CALIBRATION_JSON OUTPUT` and then `python3 validate_secondary_roof.py OUTPUT CSV_GZ` (numpy/scipy). Blender diagnostic script `render_secondary.py` imports and validates both OBJ files in the common basis. Import candidates must wait for measured outer roof boundaries, wall/seam levels, texture atlas and LOD validation.
