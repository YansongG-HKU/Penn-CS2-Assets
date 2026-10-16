# Penn Campus CS2 Assets — Sources & Dimensions

Cities: Skylines II building assets for University of Pennsylvania (University City / Locust Walk core).
Standards match Columbia Morningside project: 1 unit = 1 m, pivot bottom-centre of lot, 8 m cells,
`NA_<Name>_<WxD>`, Base/Win/Gls, PBR textures, LOD0/1/2.

## Core priority buildings

| Priority | Building | Planned lot (cells) | Planned asset | Footprint estimate (m) | Notes |
|---|---|---|---|---|---|
| 1 | College Hall | **11×7** | NA_CollegeHall_11x7 | ~84×52 envelope / ~2319 m² | Victorian Gothic, green serpentine; flagship |
| 2 | Fisher Fine Arts Library (Furness) | **8×6** | NA_FisherFineArts_8x6 | NRHP ~42.7×24.4 original; complex larger | Venetian Gothic; tower + stacks |
| 3 | Houston Hall | **11×5** | NA_HoustonHall_11x5 | OSM PCA **84.0×37.3**, ~2305 m² | Collegiate Gothic student union |
| 4 | Irvine Auditorium | **7×7** | NA_IrvineAuditorium_7x7 | OSM PCA **50.5×51.5**, ~1855 m² | Octagonal brick, Trumbauer |
| 5 | Van Pelt–Dietrich Library | **18×6** | NA_VanPeltLibrary_18x6 | OSM PCA **140.7×46.7**, ~5062 m² | Large mid-century block |
| 6 | Annenberg Center | **10×9** | NA_AnnenbergCenter_10x9 | OSM PCA **79.8×69.2**, ~3073 m² | Perelman Quad area |
| later | (see Phase 2) | — | — | — | After core |

Cell rule: ceil(dim/8) per axis, lot must contain building + flat lawn/paving (no 3D vegetation).

---

## College Hall (flagship)

- **Address:** 1 College Hall / 3450 Woodland Walk, University City, Philadelphia
- **Built:** 1871–1873 (opened 1872); architect Thomas Webb Richards
- **Style:** Victorian Gothic / Second Empire massing with Gothic fenestration; green **serpentine** with polychrome sandstone, mica schist base, granite
- **Floors:** 6 (Penn Facilities); GSF **110,266 ft² (10,244 m²)**; grounds listed **0.5 acre** (NRHP)
- **OSM:** way **51367353** — oriented PCA bbox **≈84.1 × 51.6 m**, polygon area **≈2319 m²** (© OSM contributors, ODbL)
- **Model lot:** 11×7 cells = **88 × 56 m**; asset `NA_CollegeHall_11x7`
- **Model massing:** tripartite pavilions (arts E / admin centre / sciences W) + recessed connectors; height ≈30 m to roof ridge (end towers historically removed — not rebuilt)
- **Sources:**
  - Wikipedia: College Hall (University of Pennsylvania) — GSF, floors, style, NRHP 78002444
  - Penn Facilities: https://facilities.upenn.edu/maps/locations/college-hall
  - SAH Archipedia PA-02-PH147.2 — serpentine / pavilion program
  - Nominatim/OSM way 51367353 footprint
  - Photos: Wikimedia Commons “College Hall University of Pennsylvania”

## Fisher Fine Arts Library (Furness Building)

- **Address:** 220 South 34th Street
- **Built:** 1888–1891; Frank Furness / Furness, Evans & Co.; restored 1986–1991 (VSBA)
- **Style:** Venetian Gothic; red sandstone, brick, terracotta; tower + reading room + expandable stacks
- **NRHP NHL:** original plan **≈140 × 80 ft (42.7 × 24.4 m)**; tower stair **≈95 ft (29 m)** high (NRHP nomination text)
- **Listed size:** ~65,026–116,000 ft² depending on source (building vs complex)
- **OSM:** amenity node only at time of research; footprint from NRHP + campus map
- **Planned lot:** 8×6 (64×48 m); asset `NA_FisherFineArts_8x6`
- **Sources:** Wikipedia Furness Library; NRHP 72001154 PDF; VSBA restoration sheet

## Houston Hall

- **Address:** 3417 Spruce Street; America’s first college union (1894–96)
- **GSF:** 99,882 ft²; 4 floors (Penn Facilities)
- **OSM way 51469194:** PCA **84.0 × 37.3 m**, area ≈2305 m²
- **Lot:** 11×5; Collegiate Gothic

## Irvine Auditorium

- **Address:** 3401 Spruce Street; Horace Trumbauer, 1926–32
- **GSF:** 116,624 ft²; 5 floors; Main Hall ~1,260 seats; interior tower ~120 ft (VSBA)
- **OSM way 51469206:** PCA **50.5 × 51.5 m**, area ≈1855 m²
- **Lot:** 7×7

## Van Pelt–Dietrich Library Center

- **Address:** 3420 Walnut Street
- **GSF:** 383,484 ft²; 10 floors (Penn Facilities)
- **OSM way 32120084:** PCA **140.7 × 46.7 m**, area ≈5062 m²
- **Lot:** 18×6

## Annenberg Center

- **OSM way 32120984:** PCA **79.8 × 69.2 m**, area ≈3073 m²
- **Lot:** 10×9

## Pipeline

Copied/adapted from `/workspace/columbia_campus/_pipe/` into `/workspace/penn_campus/_pipe/`.
Repo: https://github.com/YansongG-HKU/Penn-CS2-Assets (public). Do **not** put Penn assets in Columbia-CS2-Assets.


## Phase 2 — residential / medical / academic

| Priority | Building | Planned lot | Asset | Footprint (OSM) | Notes |
|---|---|---|---|---|---|
| 7 | Hill College House | **10×6** | NA_HillCollegeHouse_10x6 | PCA **78.9×45.7**, ~3457 m² (rel 5235124) | Eero Saarinen 1960; 6 floors; fortress brick + moat |
| 8 | Claudia Cohen Hall | **7×5** | NA_ClaudiaCohenHall_7x5 | PCA **49.5×34.7**, ~1432 m² (way 51367397) | Collegiate Gothic (ex-Logan Hall); Perelman Quad |
| 9 | Steinberg-Dietrich Hall | **16×10** | NA_SteinbergDietrich_16x10 | PCA **127.4×78.5**, ~4980 m² (way 51469702) | Wharton; Locust Walk / Perelman area |
| 10 | Wistar Institute | **17×8** | NA_WistarInstitute_17x8 | PCA **130.5×62.0**, ~4288 m² (way 32120133) | Lab / historic + modern wings |
| 11 | Penn Museum | **21×15** | NA_PennMuseum_21x15 | PCA **164.9×114.0**, ~10128 m² (rel 5231601) | Rotunda + wings; simplified massing |
| 12 | Franklin Field (exterior) | **28×19** | NA_FranklinField_28x19 | PCA **219.7×149.9**, ~27635 m² (way 665447049) | Stadium bowl shell only; no field veg |
| — | The Quad (full) | — | — | (no single OSM polygon via Nominatim) | Too complex as one asset; defer to distinct houses |

