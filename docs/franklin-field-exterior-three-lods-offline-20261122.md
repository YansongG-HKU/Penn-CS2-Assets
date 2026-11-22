# 宾大 Franklin Field：整场三档外立面修整（离线）

打开 `trial/Franklin-Field-whole-OFFLINE.blend` 可直接查看整场和三档。独立 FBX 可从同包的 `.fbm` 相对目录读取原创新贴图，勿拆散。保留双层马蹄形看台、跑道及球场，用三档共同的街侧节奏替换原实心红砖平墙。

- 北面 Weiss 门廊保留三座明显的玻璃拱和相邻一扇较小的门，近档有接入墙体的约 28 cm 浅退口，中远档用同朝向贴图保留读法。三座拱只代表照片可见的一组，不当作整段立面总数，也不把 PennAccess 的四处入口等同于四座玻璃拱。
- 南街东端近转弯处预留门与坡道形态。西端 Weightman 的两座抬高主入口用阶梯表现，近中档另有北侧平进售票口和西南平进门的视觉位置。南东坡度、入口位置用游戏近似，不认证门洞实测、坡道规范、寻路或碰撞。
- 屋顶轮廓加入砖垛；当代东面门洞未经充分核实，保留砖墙简化。三个 FBX 读回 16,048 / 9,142 / 4,018 个有效三角面，统一约 229.44 × 148.13 × 26.65 m（含外置坡道和新增砖垛；原主体站位未移）。生成网格检查上层主体、所加砖垛和外部阶梯/坡道，每个分别是两面共边且面朝向一致的闭合壳，并不说明不同壳相交问题全清。看台内部沿用原离线几何，开放平面保留。
- 共享 1024 BaseColor，其余 PBR、照明、场地地块、碰撞和游戏内 LOD 切换未验。属于游戏资产候选，不可当作已发布、已能寻路或已通过 CS2 Editor。参考与局限见 `evidence.md`。
- 用 Blender 4.3.2 运行 `python guard.py verify.py -- "$PWD"` 可从 FBX 回读复核。离线预览脚本需 Python NumPy、Pillow 和 Matplotlib。

## Sources and geometry checks

# Franklin Field exterior, offline assembly controls

The North-facing Penn completed-project photo shows three major glazed lower arches within the pictured Weiss bank, a narrower upper arcade, and a smaller pale inset entry to the photographed left (not a fourth matching glazed bay). North upper opening glazing is not assumed. Use a simplified pale spring line, slim dark grid and center sign band. Do not count the four separate accessible entry roles as arches. Exact bank location, bay axes, depths and opening counts outside the photograph are not claimed.

- Penn photo: https://facilities.upenn.edu/sites/default/files/styles/carousel_4_3/public/images/weiss_pavilion_large_1.jpg?itok=z11DrBIY
- Weiss access: https://facilities.upenn.edu/sites/default/files/pennaccess/PA0165-FranklinField-Weiss.pdf
- Stadium access: https://facilities.upenn.edu/sites/default/files/pennaccess/PA0165-FranklinField.pdf
- Weightman access: https://facilities.upenn.edu/sites/default/files/pennaccess/PA0605-Weightman.pdf
- Stadium record and battlement/stone band evidence: https://facilities.upenn.edu/maps/locations/franklin-field
- Modern east: https://www.ewingcole.com/project/coulson-family-training-complex/

SL/SM is on the South Street frontage, near its east end, not on the due-east façade. A separate north ticket entrance and southwest Sports Medicine entry are at grade; the NW and SW main Weightman entrances are separately stair-raised. Ramp grades, exact entry points and navigability are not supplied or verified. Do not mirror the Weiss glass to the whole stadium. East reuse only a conservative brick wall/bay when current photo evidence cannot support a specific opening.

## Integration

The generated four authored 1024 atlas tiles are staged, unassigned to geometry. They do not copy source photo pixels. Use the photographed north bank only for exterior glazing placement and neutral arch-voids elsewhere; preserve pixel identity of original track/field/brick tiles. Reuse a side-coordinate-banded wall, not the currently unused duplicate exterior() full wall. Every medium/far wall tile must map with an explicit face orientation and keep its arch upright. Prefer geometrically recessed near portals only where needed and do not put coplanar face cards on the existing wall. For the parapet use separate thin capped merlons centered just inside the rear rail above the roofline, with rear overhang and side widths explicitly constrained. Preview at street eye height and compare the three levels. Materials/collision/import/navigability remain offline-only until tested.
{
  "NA_FranklinField_Trial": {
    "triangles": 16048,
    "closed_consistent_shells": 132,
    "bounds": [
      [
        -127.8,
        101.637
      ],
      [
        -75.04,
        73.092
      ],
      [
        -0.53,
        26.12
      ]
    ]
  },
  "NA_FranklinField_Trial_LOD1": {
    "triangles": 9142,
    "closed_consistent_shells": 132,
    "bounds": [
      [
        -127.8,
        101.637
      ],
      [
        -75.04,
        73.092
      ],
      [
        -0.53,
        26.12
      ]
    ]
  },
  "NA_FranklinField_Trial_LOD2": {
    "triangles": 4018,
    "closed_consistent_shells": 109,
    "bounds": [
      [
        -127.8,
        101.637
      ],
      [
        -75.04,
        73.092
      ],
      [
        -0.53,
        26.12
      ]
    ]
  }
}
{
  "NA_FranklinField_Trial.fbx": {
    "triangles": 16048,
    "size": [
      229.43700408935547,
      148.13201141357422,
      26.65002417564392
    ],
    "edge_incidence": {
      "2": 22534,
      "1": 3076
    },
    "texture_relative": "NA_FranklinField_Trial.fbm/Franklin-field-atlas.png",
    "min_area": 0.01039998047053814
  },
  "NA_FranklinField_Trial_LOD1.fbx": {
    "triangles": 9142,
    "size": [
      229.43700408935547,
      148.13201141357422,
      26.65002417564392
    ],
    "edge_incidence": {
      "2": 12559,
      "1": 2308
    },
    "texture_relative": "NA_FranklinField_Trial_LOD1.fbm/Franklin-field-atlas.png",
    "min_area": 0.01039998047053814
  },
  "NA_FranklinField_Trial_LOD2.fbx": {
    "triangles": 4018,
    "size": [
      229.43700408935547,
      148.13201141357422,
      26.65002417564392
    ],
    "edge_incidence": {
      "2": 5633,
      "1": 788
    },
    "texture_relative": "NA_FranklinField_Trial_LOD2.fbm/Franklin-field-atlas.png",
    "min_area": 0.05700491741299629
  }
}
4ed4f109a98847a2dee33b2d0cbe8dd7041d4e211658433d4d1e41754f6b7c73  trial/NA_FranklinField_Trial.fbx
e9496f9cdecfb791558e3f3c5f3401b2b2b97a51af7cf388a865e9721890a95b  trial/NA_FranklinField_Trial_LOD1.fbx
256544c82d8e46235ddf28033a75c9e29607f533bc463fe97b7c9f60e26d6668  trial/NA_FranklinField_Trial_LOD2.fbx
6191ce6e3ad69ad72a1094460fc23df6935431c78dda92500cd8b4ae2a5636ae  trial/Franklin-Field-whole-OFFLINE.blend
b728e54db08bd2cbe197b9184285c6f9c0774b6680184285e63194f61f5d4fb9  trial/NA_FranklinField_Trial.fbm/Franklin-field-atlas.png
b728e54db08bd2cbe197b9184285c6f9c0774b6680184285e63194f61f5d4fb9  trial/NA_FranklinField_Trial_LOD1.fbm/Franklin-field-atlas.png
b728e54db08bd2cbe197b9184285c6f9c0774b6680184285e63194f61f5d4fb9  trial/NA_FranklinField_Trial_LOD2.fbm/Franklin-field-atlas.png
7002c8fecbacf066a48622a0ce4ec745be008ef5b5e2f0dd80ecd5b2b8a97ded  readback.json
9dc36270e4b4919263d761d65bb3a5d0fde2f4bf5d9678ae134eb4106effebe9  build-audit.json

ZIP SHA-256 `fa0281bf20350c02985e8449b30e6ea7384ad8e118a11649791b9d2ecf4166df` (1,110,223 bytes). Documentation only: no binary, publishing, collision or game-acceptance claim.
