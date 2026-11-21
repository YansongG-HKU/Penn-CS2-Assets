# Fisher Fine Arts Library | west tower roof crown reference
03:30 UTC cloud batch, 21 Nov 2026. Separate upper-tower geometry to guide the high/detail/LOD rebuild. No surrounding facade substitutions, game import, release or UV/PBR signoff.

## Source design and survey controls
The square entrance tower has a battlemented surround, an interior hipped roof visible from above and a narrower raised north crown. The 1892 Bureau history and NPS nomination give 95 ft for the historical square tower; neither marks the exact base or top. Adding 28.956 m to approximate grade 17.10 NAVD88 yields 46.056 m, only a plausibility check near the broad crest. The high return is a separate narrow projection and was **not** placed using 95 ft. Preserve the main entry, north apse and high projection as separate features. 
The measured model uses the previous City-aligned EN frame and local z0 of 17.10 m NAVD88. The four 2022 training source passes (59/60/61/62) determined the distinct bands, the four-sided hip, and 16 discrete high-return stations in the parapet. The stations are simplified, not an exact historic feature count or carving survey. Main ledge elevation 44.825 m; broad crest reference 45.76 m; hip eave 43.522 m and peak 44.945 m; narrow crown reference 50.345 m. A dark opening is visible in the 2025 PASDA overhead image; the provisional opening is 0.84 × 0.84 m in the candidate based on the training-point gap. Its through-cut to the artificial lower model plane is a visualization convention, **not an interior shaft depth**.
Colors distinguish components only. HABS photographs depict the 1964 details and cannot substantiate current material boundaries or dimensions; the 1991 architect documented restored terra-cotta tile/skylights, brick/terra cotta walls, rusticated sandstone base and recreated copper finials. Exact roof finish at the recessed hip and actual 2026 roof replacement conditions remain undetermined. 

## Verification
OBJ and equivalent GLB were reread in clean Blender scenes. 510 unique vertices, 1,020 triangular faces, 1,530 opposite directed edge pairs, zero non-adjacent intersections, aperture ray not obstructed. Solid volume refers only to the cropped proxy, not building volume. GLB materials are simplified inspection swatches only.
Independent 2022 source passes 19/20, no train/hold point mixing:
- Inner roof, 417/417 rays: original survey shell error p50/p90/p95 0.049/0.136/0.171 m; new 0.049/0.117/0.141 m.
- Upper crest height gate, 72/76 matched rays: previous p90/p95 2.307/3.548 m; new 0.384/0.529 m on the same 72 points. Four rays not covered by the isolated model; no imputation.
- Lower perimeter height gate, 181/199 matched rays: old p90 1.603 m, new 0.965 m. Width, ornament silhouette, and facade profile remain provisional.
- Conflicting ways to merge into the previous whole-building survey envelope were tested and **not accepted**. One matched-XY exact Boolean created 48 nonmanifold seam edges. A narrower-cutter variant with clean local outer stitch still worsened the all-height p90 within the tower plan (approx. 5.99→6.67 m) and failed the conservative outside-ray regression. No merged geometry is shipped. The whole-building 03:00 survey model remains intact. A subsequent merge should preserve unchanged roof triangles exactly and resolve overlapping returns at vertical wall/roof boundaries, rather than interpolate a global envelope or use global Boolean cleanup.

## Primary reference locations
- https://npgallery.nps.gov/NRHP/GetAsset/NHLS/72001154_text
- https://www.govinfo.gov/content/pkg/GOVPUB-I16-b946fdaaac52d4f058b1d7e8e96db786/html/GOVPUB-I16-b946fdaaac52d4f058b1d7e8e96db786.htm
- https://tile.loc.gov/storage-services/master/pnp/habshaer/pa/pa0600/pa0675/data/pa0675cap.pdf (HABS entrance/tower -2, cross gable -3, tower double window -4, parapets -5)
- https://venturiscottbrown.org/pdfs/UniversityofPennsylvaniaFisherFineArtsLibrary01.pdf
- https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=7157
- https://www.fisheries.noaa.gov/inport/item/70174 (NOAA 2022, EPT 9848)
