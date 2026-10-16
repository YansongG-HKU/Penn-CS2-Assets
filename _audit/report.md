# Penn CS2 assets - audit
## College Hall - v2
- Reality (Commons 2010 photos): green serpentine walls, buff/brown sandstone trim, slate mansard roofs with gabled dormers, pointed-arch windows with red sashes, Gothic portico.
- v1 (CollegeHall/v1/): flat-roof attic boxes, neoclassical rectangular windows -> rejected.
- v2: mansard roofs + gabled dormers, tall arched windows on 2nd-3rd and 4th floors, sandstone LIMECOL, muted serpentine green, flush belts (o=0.04). Fixed floating lamp caps.
- LOD gate: LOD0/1/2 boundary 0/0/0, floating 0/0/0, flipped 0, bad winding 0 -> PASS. tris 70766/38246/144.
- Remaining: windows rounded not pointed; red sash colour weak; side pinnacles/spire turrets, polychrome banding, Franklin statue omitted; full 3-pavilion plan approximated from OSM envelope.

## Fisher Fine Arts Library - v1
- Massing: rusticated red-sandstone rotunda drum + brick upper drum + conical roof, gabled reading-room hall, crenellated stair tower (~38 m), stacks wing, gabled arched porch. LOD 0/0/0 bnd, floating 0 -> PASS. tris 13716/10164/336.
- Remaining vs photos: rotunda dormer gables/finials, gargoyles, terracotta detail, darker roof, tower corner turret; extents estimated (OSM node only).

## Irvine Auditorium v2
- Root cause of 19 LOD0/1 boundary edges: 2 orphan open faces (all-boundary) left on Base after Win split (one 15-gon gothic pane duplicate, one rectangular pane). Fixed in `_pipe/bake.py` via DROP_ORPHAN_OPEN. Softened buttress caps (Limestone vs bright LimeDark).
- LOD: 0/0/0 bnd, floating 0 → PASS. Commit b362ce5.

## Houston Hall v2
- RUSTCOL=0.38,0.37,0.35 / GRANCOL darker grey schist; curved/serpentine entrance gable (Flemish-style prism, not triangle). Orphan-open fix also cleared prior FAIL.
- LOD: 0/0/0 bnd, floating 0 → PASS. Commit 7f5c227.

## Van Pelt–Dietrich Library v1 (NEW)
- Mid-century brown brick panels between white concrete fins; recessed glazed ground + attic. Lot 18x6. OSM 140.7×46.7 m.
- LOD PASS. Commit dedc702.

## Annenberg Center v1 (NEW)
- Brown brick hexagonal tower + glass entrance under metal canopy + lower wings. Lot 10x9. OSM 79.8×69.2 m.
- LOD 0/0/0 PASS. Commit d687ca0.
