# Fisher Fine Arts Library | Penn survey-based geometry reference
Cloud batch 2026-11-21, 03:00 UTC. A separate pre-restoration survey envelope, neutral diagnostic model, not a final CS2 asset or drop-in LOD.

## Why the old LOD2 was not scaled or stretched
Its 336 triangles represent a nominal 64 × 48 m platform, a box tower, and three full circular components. The official footprint (Philadelphia BIN 1443619, object ID 331525) has a northern reading-room apse, western entrance and tower, and southern/eastern wings. In the common building-aligned axes, the 50-vertex outline is **68.077 × 46.423 m**, 2301.913 m². An axis-aligned 8×6 placement is too short. **9×6 = 72×48 m** is only the geometric minimum on the current axis convention; entrance alignment, assets touching its edge, and game placement have not been tested. Origin/axes are in `frame.json`. The rotated old model in the render is centered for diagnosis with its apse facing north; it is not game registration.

## What was actually changed
Made a closed, standalone footprint-constrained 0.52 m roof reconstruction from 2022 NOAA Philadelphia LiDAR, rather than transferring old UVs to unmatching topology. Sampled 286,658 distinct records in a small crop, used only first class-1 returns in the footprint between 21.6 and 53 m NAVD88 for the roof (56,596 training; passes 19/20 entirely held back). The thin high crest inside the western tower has high support from multiple training passes and matches a small feature in the 2025 orthophoto. Refined 21 local vertices by using that upper return only under a bounded 0.34 m and two-pass support rule. No assumption about the unfitted center, ornamental crenellation count, turret wall thickness, or 2026 restoration state.

Geometry reference shows the 2022 shape, not an as-built drawing. UV/PBR, roof subcomponents and vertical wall transitions, exact entrances/sill/landscape, facade materials and any visible interiors must be authored separately. `17.10 m NAVD88` is nearby grade used as a convenient z0, not a measured threshold. The model's base and side closure are synthetic; compute volumes for mesh sanity only. The 2025 aerial image confirms layout, not post-restoration finishes or datum. Penn's facilities page describes roof/window repairs in the 2025–26 restoration.

## Checks
- FBX and OBJ independently reread: 9,510 vertices, 19,016 triangles, 28,524 shared edges with opposite winding, no non-adjacent face intersection pairs; max FBX roundtrip coordinate displacement under 0.000007 m. This is a high-detail shape reference, not a budgeted LOD.
- 25,605 independent roof samples: absolute error p50/p90/p95 = 0.070/0.959/3.479 m. Holds include multiple roof levels; the wide tail at seams/roof edges is unresolved, so the median does not mean the whole roof is within 7 cm.
- Of those, 86 interior high returns at or above 48 m NAVD88: the upper detail change improves median from 0.536 m to 0.104 m and p90 from 4.435 m to 2.466 m. Worst junctions remain. The alternate 1.0 m coarse mesh lost the top reference (p90 above 10 m at that band); not included.
- On 12,743 of the same samples where the diagnostic old LOD2 had an above-platform hit, legacy height errors p50/p90/p95 were 2.580/13.595/16.778 m; new 0.072/1.140/3.524 m. This is a shape check under the stated pose alignment, not a game footprint certification.
- Existing FBX/texture baseline files were only read. Five original 1024 px files matched their pinned Git LFS checksums and decoded; they do not fit this new geometry. No LFS upload, Editor import or publish.

## Primary references
- https://facilities.upenn.edu/maps/locations/fisher-fine-arts-library-anne-and-jerome (west main steps, separate south Duhring accessible route, restoration)
- https://www.library.upenn.edu/floor-plans/fine-arts (west entrance orientation and documented floor layouts)
- https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/LI_BUILDING_FOOTPRINTS/FeatureServer/0
- https://www.fisheries.noaa.gov/inport/item/70174 (2022 source metadata; point EPT ID 9848)
- https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=7157 (2025 orthophoto)
