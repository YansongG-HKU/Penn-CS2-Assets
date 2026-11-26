# Franklin Field east bowl: April 2025 cross-survey review

Purpose: independently check the 51 delivered 2022-based extension cells, not replace them. No model, texture, collision, physical connection or game state changed.

## Inputs and safeguards
- [City/PASDA public April 2025 LiDAR catalogue](https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=7158), [metadata](https://www.pasda.psu.edu/uci/FullMetadataDisplay.aspx?file=Philadelphia_Lidar_2025.xml), and [source tile](https://www.pasda.psu.edu/download/phillyLiDAR/2025/LAS/26848E233112N.las). Exact file 794,020,979 bytes, SHA‑256 247ab6b6a8d022f260020de28046af0798d998d45649144b8fae567f9e18cdeb. Its EPSG:6565 WKT defines only horizontal coordinates. Do not treat the raw Z as NAVD88 or assign the 2022 geoid to it.
- Streamed crops converted XY to EPSG:6347 and initially left Z unconverted. Franklin E483655–483895 / N4422110–4422350: 2,707,522 records from source IDs 11,12,22,23. Irvine cropped separately (725,391 records), not interpreted or combined with this Franklin fit.
- Retained the previous EPSG:6347 stadium orientation and origin. Five existing non-roof class-2 first-return rectangles estimate an additive adjustment +0.02555 m under the **local US survey foot scale hypothesis**. Five untouched rectangles have signed difference of medians between −1.47 and +0.97 cm under that mapping; the equivalent metre-scale test ranges from −50 to +19 cm. This does not establish 2025 official vertical datum, individual-point precision or position accuracy on steep faces. No horizontal translation was fitted. Three high windows are class-sensitive and not used to estimate the adjustment. Project works occurred 2022–2024 [according to Penn](https://facilities.upenn.edu/maps/locations/franklin-field-team-operations), so don't assume every difference is noise or that any seat actually moved.

## Decision
For each cell compare both groups of 2025 source IDs 11/12 and 22/23. Condition on |dX| <1.15 m relative to the same model profile and a minimum 12 screened points per group. Require P95 absolute vertical-equivalent residual <0.40 m and greatest 3D distance to a |dX| <0.54 m support return <0.94 m over each cell's 11×21 grid. The original near-plane population fraction is shown separately in the data, not used for these screening counts. These are fixed-profile coverage classifications, not fit quality over all raw returns or epoch-change detection.

- **13 / 51** satisfy those screening conditions with classes 1 or 6 alone.
- **16 / 51** satisfy only after adding class 5 returns; classification ambiguity requires manual separation, so don't mark them fully confirmed.
- **22 / 51** are not independently confirmed at the screening thresholds. This can reflect classification mix, coverage, local profile bias, debris, or relevant physical changes. All earlier 2022-backed models are retained without upgrades or deletions.
- North lower seating's high half (seven old bands) has no Class 1/6 confirmation. South lower high half beyond |Y|31 m warrants a separate line refit and independent edge comparison, not a simple extension of the old curve. No joint between the curved and straight stands can be inferred from this check.

For reproducibility, inputs are the already shared 13:30 bowl source archive (SHA‑256 cee70194710bd9d5930a33c1dc4db825eec9fe17aa6b31ae8ecfe79e4b3bd3bc), 03:00 east-bowl extension ZIP (67d4319d1d1466f1db5c336ced09c9b28a665807bc21c58bcf9939f4dc5d96e4), and publicly sourced LAS. Run crop_las.py with --native-z and the Franklin box above, then windows.py, cross_epoch.py (arguments shown by argparse) and support_card.py. Raw full tile and point crops are not redistributed here. This review is not an Editor or game pass.

Report archive SHA-256 `489480e6c2d3fcf6f9dbaa09bbc06dd4d7d51c85921660f44c5d0bd415f1cd66`, 174,907 bytes. No asset binary change.
