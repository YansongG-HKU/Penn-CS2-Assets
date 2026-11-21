# Fisher Fine Arts Library | South raised roof strip and measured crest stitch
04:00 UTC cloud batch, 21 Nov 2026. This updates a narrow window in the previous geographic survey reference, not the production/game asset. The separately reviewed west tower piece is not fused here.

## Change
The 2025 rectified aerial establishes the raised longitudinal element on the south roof. The 2022 independent point sources establish four distinct planes for the center of the long element: south slope, near-flat crest, north slope, and lower north shoulder. The 28-triangle standalone OBJ covers 26.22 × 3.17 m in building E/N coordinates, and closes below on a synthetic datum of 31.95 m NAVD88. The crest is near 34.1 m NAVD88, not the roof’s total height. Current cladding and roof structure under the visible surface were not inferred.
The full-envelope candidate replaces only a 27.04 × 1.04 m grid window at the crest. It keeps the low south and north transition in the old shape, rather than extending a high plane into conflicting returns. There are 108 exactly matched perimeter seam edges, an intermediate collar with 106 vertices sampled on the previous triangulation, and one conservative 90/10 measured/old blend inside the local crest. Broader plane/strip attempts were kept as rejected working trials. The conservative candidate is an offline surface correction, not proof of current roof condition, internal seams, or a game LOD budget.

## What passed and what did not
- Own Blender FBX roundtrip: 9,575 vertices, 19,146 triangles, 28,719 opposite two-face edges. No disjoint triangle intersections; original dimensions retained. **18,808 exterior triangles stayed bit-for-bit identical**, as did the resulting height at each of 25,248 independent points outside the window.
- On 100 measured crest returns from 2022 held passes 19/20 (fit from different source strips), p50/p90/p95 0.092/0.205/0.305 m → 0.055/0.097/0.117 m. Whole 616 conditioned strip returns p50/p90/p95 0.087/0.209/0.277 → 0.076/0.195/0.254 m (same points). The independent low-poly version is a separate reference for the entire visible element, not a drop-in replacement.
- The all-height patch return mix is still heterogeneous: 357 held returns, p50/p90/p95 0.117/4.292/5.005 → 0.094/4.357/5.082 m. No proof that the deep-return tail indicates exact current visible surfaces. For all 25,605 building test points, p50/p90/p95 0.070/0.959/3.479 → 0.070/0.957/3.479 m. Report both gates; do not claim the whole roof is within centimetres. The various roof strip designs were evaluated on the fixed held-flight set during model selection, not an untouched blind test of all development choices.
- The geometry reference has no new UV, PBR atlas, façade reconstruction or game import. Outline/grade not changed; no pmod or Editor release. Keep source meshes, textures, and higher west tower study separate.

### Sources
- https://facilities.upenn.edu/maps/locations/fisher-fine-arts-library-anne-and-jerome
- https://www.fisheries.noaa.gov/inport/item/70174 (2022 point source EPT 9848)
- https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=7157 (2025 orthophoto)
