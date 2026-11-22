# 宾大 Franklin Field：三档材质与地块离线试导入包

先打开 `Franklin-Field-Materials-OFFLINE.blend` 查看可编辑模型。要试官方 Asset Importer，选择 `FranklinField/` 文件夹作为资产来源，不要拆分其中文件。这是等待游戏端验收的候选，不发布或覆盖现有资产。

- 保留三档几何、UV、法线和枢轴，Blender 全新回读对比三档 16,048 / 9,142 / 4,018 三角面完全一致。近档、中档实际读取主贴图，远档读取远景贴图。
- 加工 10 张同前缀贴图：1024 主套、512 远套，中档用 `settings.json` 共享主套。BaseColor 主图 RGB 与立面上版一致；玻璃是较光滑的非金属，砖墙较粗并带浅法线，仅金属图块（以及部分栅栏、金属屋面）有金属参数。建筑打包约定为 MaskMap R 金属、G 涂层、B 零、A 光滑度。ControlMask 和 Emissive 全黑，防止加出未经确认的涂色和夜景照明。不是物理测量、真透明玻璃或独立照明导入验证。
- 以 8m 为名义网格，按现有不居中的模型枢轴初试 **33×20 格**，南侧入口坡道约有 4.96m 边余量、西侧约 4.2m；29×19 若直接以原点居中会从西侧越出 11.8m。能在 Editor 平移地块中心后，才测试紧凑 29×19 对照。平地首测建议用静态预设，检查南北朝向、屋顶、主材质和远档，保存后重开；下一步才编辑地形、碰撞和路网。无真正导入、通行、地块设置或游戏运行证明。
- 本地含验证日志和合成脚本，重建需上一版立面源和 RGB atlas。开发者流程见 [Paradox 资产导入说明](https://www.paradoxinteractive.com/zh-CN/games/cities-skylines-ii/news/adding-custom-assets)，通道布局可参照 [纹理打包工具的实现说明](https://github.com/Macwelshman/CS2-Combiner)。没有在本轮验证 FBX SDK/Editor 兼容版本，不能仅凭命名视作游戏规范过检。

## Audit

{
  "NA_FranklinField_Trial.fbx": {
    "triangles": 16048,
    "exact_xyz_triangles_uv": true,
    "normal_vector_delta_max": 0.0,
    "paths_resolved": [
      "NA_FranklinField_Trial_BaseColor.png",
      "NA_FranklinField_Trial_Normal.png"
    ]
  },
  "NA_FranklinField_Trial_LOD1.fbx": {
    "triangles": 9142,
    "exact_xyz_triangles_uv": true,
    "normal_vector_delta_max": 0.0,
    "paths_resolved": [
      "NA_FranklinField_Trial_BaseColor.png",
      "NA_FranklinField_Trial_Normal.png"
    ]
  },
  "NA_FranklinField_Trial_LOD2.fbx": {
    "triangles": 4018,
    "exact_xyz_triangles_uv": true,
    "normal_vector_delta_max": 0.0,
    "paths_resolved": [
      "NA_FranklinField_Trial_LOD2_BaseColor.png",
      "NA_FranklinField_Trial_LOD2_Normal.png"
    ]
  }
}
{
  "assumed_cell_m": 8,
  "asset_bounds_m": [
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
  ],
  "cases": [
    {
      "scenario": "small_centered",
      "cells_W_E_by_S_N": [
        29,
        19
      ],
      "center_world_local_m": [
        0,
        0
      ],
      "clearance_W_E_S_N_m": [
        -11.8,
        14.363,
        0.96,
        2.908
      ],
      "all_inside_envelope": false
    },
    {
      "scenario": "first_test_centered",
      "cells_W_E_by_S_N": [
        33,
        20
      ],
      "center_world_local_m": [
        0,
        0
      ],
      "clearance_W_E_S_N_m": [
        4.2,
        30.363,
        4.96,
        6.908
      ],
      "all_inside_envelope": true
    },
    {
      "scenario": "tight_optional_adjustment",
      "cells_W_E_by_S_N": [
        29,
        19
      ],
      "center_world_local_m": [
        -13.081499999999998,
        -0.9740000000000038
      ],
      "clearance_W_E_S_N_m": [
        1.2815,
        1.2815,
        1.934,
        1.934
      ],
      "all_inside_envelope": true
    }
  ],
  "note": "Arithmetic, not an Editor grid or connection test."
}
e355fd938fa43784542ed0346be98a671700195d578945b0c5ff9ca9cdd2646b  FranklinField/NA_FranklinField_Trial.fbx
53af06c4629b137d3b0917252bda4755f7311076ad1443bdaf86fddeaa8fbc8e  FranklinField/NA_FranklinField_Trial_BaseColor.png
f12ddfea20dcca2fa350d75d5ed2ae76a4fffbcdfd2b8f2357558b90072dab9f  FranklinField/NA_FranklinField_Trial_ControlMask.png
87658cfaf8e619d7f15fe7179e5874c38663d3254302928d9c1e7eaacee0a9f4  FranklinField/NA_FranklinField_Trial_Emissive.png
6a57f8a7b513f51679e7150873db6711253e945ca203045a93d5b94ae7dc28cb  FranklinField/NA_FranklinField_Trial_LOD1.fbx
d9be35c74456b1028aa5234315c42846536a71411b4c5885dcd7f167892c2639  FranklinField/NA_FranklinField_Trial_LOD2.fbx
dc7930896ff5526921ffd48835eb19a8b09541553cbc968c2e54b605364dcf11  FranklinField/NA_FranklinField_Trial_LOD2_BaseColor.png
9b04f10d403456a5dc17495d1e558b3c412862e34be805faae06e263a2668920  FranklinField/NA_FranklinField_Trial_LOD2_ControlMask.png
57b5e40e68e97c62837b9d0a5a8f7aac22471c1633897f9bcf4fa62864ecc974  FranklinField/NA_FranklinField_Trial_LOD2_Emissive.png
4e60c03e4a5a995718c9928c81d47cb0c7ffcf4f4217c55b94d4ab04b8d50ab2  FranklinField/NA_FranklinField_Trial_LOD2_MaskMap.png
71d432413a10aab25e5dee0aa377a1ca29dddef8eb2e30584135268d218c9d96  FranklinField/NA_FranklinField_Trial_LOD2_Normal.png
f8cf2415a322758047bab33039949a9accf996b87897e78daca247da71d069c9  FranklinField/NA_FranklinField_Trial_MaskMap.png
83aa941ed3ec17149f20c32b43deb7b2d793955cde5b91d89fad9082494820a2  FranklinField/NA_FranklinField_Trial_Normal.png
b5df8614b0d9f8171ba0e8e313e5c80d63feac38273210184ae4bbc9a9af0263  FranklinField/settings.json
d2ce5bc39d38d0211ce92c2cea51f1ed08f4de10d892c21cb1bd616024686f10  Franklin-Field-Materials-OFFLINE.blend
4e01e7da264b1e61344754c757b01783fc1278df2064140d050615f39ea22468  map-audit.json
5bf33aae93bdc626def09724d2d6d1aa6207a59f611bdf73dcbb453acfbb8b7f  fbx-audit.json
1fb9aa56da4443290b69f662b4b53e5873ceed781ecb2b4aa4abb18fde5d1226  lot-audit.json

ZIP SHA-256 `0060805cce450a1ecd52d7687ac5bb312dbaad28531e7f9d2efd5b085e72b54d` (1,074,027 bytes). Main unchanged; game import, navigation and publish not performed.
