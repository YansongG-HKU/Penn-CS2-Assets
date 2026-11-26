# 宾大 College Hall｜三档整栋试放：中央山墙、远景立面和近中 UV

此包替代旧的“仅中央山墙”试放包，不要混用。解压后把 CollegeHallTrial/ 整个目录导入，11×7（88×56 米），旧枢轴。三档保留上轮中央三角山墙，模型未重新测绘。

- 远档从原来 432 个偏离本面超过 5° 的角点法线修到 0；重建相应切线、副切线。顶点、索引、UV、152 个三角和五张远景贴图不变。旧立面局部亮斑来自跨硬边平滑法线；两组无灯光同机位像素完全相同，带 Blender Studio 灯光可见圆斑消失。未验证 CS2 材质。
- 近、中合计修正 92,204 处折叠到同一点的 UV（三角近档 51,550、中档 40,654）。保留原三角、尺寸、法线、其余 UV；五张共用贴图只改四块未用区域，用旧色值取样。纯主体正、背面各两组，RGB 单通道最大变化 3/255。仍余 15,848 / 7,272 处零面积 UV，本次不宣称完全修复。
- 中央山墙前轮几何修复保留；三档主体 113,150 / 80,618 / 152 三角，Win/Gls 几何与前包一致。实景参考：[宾大正立面照片](https://facilities.upenn.edu/maps/discover-penn/college-hall)。本包未合并 GIS 另案。后续优先检查实际 Editor 的远景日夜光、窗和阶地、保存重开；未推送 LFS 或导出 pmod。

- Supersedes central gable package (SHA-256 `14b9d6c593c0e34897d103095c59107dac8b2d95feb38af66984aa3971fd44f0`), does not change site or increase campus count. This ZIP: 15,985,442 bytes and SHA-256 `8503af9021ec4d195c8708f6c5c5d921ce47c9222c42a556b4bb9ff057498d85`. Each extracted SHA and ZIP CRC passed. No binary assets published to GitHub. Total 18 whole offline trials, 0 Editor passes.
