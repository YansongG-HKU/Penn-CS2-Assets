# 宾大 Houston Hall｜北侧校园主门、浅坡和远景双翼坡顶
从 `HoustonHallTrial/` 作为独立候选导入。保留原枢轴、地块 11×5（88×40 米）与建筑范围。模型 +Y 朝 Penn Commons，−Y 朝 Spruce Street；不把 Spruce 侧楼梯认作当前主入口。

- [宾大设施部门](https://facilities.upenn.edu/maps/locations/houston-hall)与 [PennAccess](https://facilities.upenn.edu/sites/default/files/pennaccess/pa0245-houstonhall.pdf)都指向北侧中央木门。三档增设简化木双门和带平段的闭合坡体。模型高差 0.356 米／坡段 4.87 米（约 7.3%），平台高 0.36 米，是模型近似，不是测绘或无障碍合规验证。门片是不透明可见几何，不是通行碰撞。没有套用南侧照片里的栏杆，也没有把早先 552/648 三角的局部草案当成这个整栋包。
- 远景五块原简化体的墙体纹理保持原图集，新增坡屋面以近中档体形为约束：双翼屋脊 16.0→21.4 米，中心屋脊 17.4 米，双烟囱 19.8 米，前山花 17.03 米，建筑全高含尖饰 21.50 米。简化翼端各两窗。三档主体 14,104／9,484／432 三角；近中各另保留 204 窗三角。原两个空玻璃文件不带入。
- 修复近中 **14,400** 个退化 UV（9,498／4,902）；将原来钉在单点的面投到未占用色块，尽量保留原采样色与 PBR，不等同于为旧材质补上真实石纹。未修改原占用图集像素；原有效 UV、近中旧几何保留。新区域用适度简化、支持漫反射/法线/遮罩的同一图集，独立试放没有新增色调配置。
- 重新导入后，三档主体无零面积几何或退化 UV；共 273 坡面、108 门面、63 接近路径采样。远档另 46 屋脊／翼面、18 烟囱、10 中央屋面／山花、72 山墙窗检查。近／中窗格按原档重读；不会把探针通过当游戏导航通过。
- 编辑器可用后先验 Irvine，再轮到本楼时独立测北侧浅坡与人行路连接、访问标记、门槛碰撞、保存重开、三档切换和夜景。不含东南门/室内，南侧原入口未重建。原基线在细部存在接触装饰，本次不是全楼拓扑布尔合并。附图仅 Blender 回读，未游戏验收、未推模型和未发布 pmod。

## Offline evidence (Dot cloud, 2026-11-24 UTC)

- Source: Penn main pinned `3a7097a0ef154f454e0ce67da0b26c37c26bfed4` (19 input files; Git blob SHA checked; any LFS pointer resolved to its exact SHA-256 and size).
- ZIP `宾大-Houston-Hall-北门浅坡与双翼坡顶整栋-未游戏验收.zip`, 20,234,170 bytes, SHA-256 `61a0fa77b59061c4b736e6cf6326db6ad24f9ce931ce29a7251e08da567ec419`. CRC and all 25 extracted SHA-256 entries checked. Blender 4.3.2 readback of all five FBX, ten maps and sharedAssets checked. This replaces no files in main.
- Evidence SHA-256: `placement-qa.json` `934035779033034afefc4e9a463ca282d9d75413411c201282907987ad765c28`; `readback.json` `19f10b09e3123f0e57c8463805ec49b06282bc32427ad47b1704c1c44e48a8cd`; `Houston-Hall-Readback.jpg` `efee1adff2b04139acb1c73a902d50c75ec77b3f9e9eda1a3378ad1c759d889a`.
- No actual CS2 Editor/game session, no navigation validation, no model LFS write or release. No Blender job left running after readback.
