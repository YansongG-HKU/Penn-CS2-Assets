# 宾大 College Hall｜中央山墙三档整栋试放

解压后独立导入 CollegeHallTrial/，11×7（88×56 米），保留旧枢轴，不覆盖原资产。参考[宾大校园正立面照片](https://facilities.upenn.edu/maps/discover-penn/college-hall)，现代正立面中央是三角山墙，不复用旧模型山墙上的夸张尖锥。此次只做中央轮廓局部匹配，不是全立面或屋顶测绘。

- 近、中仅删除原本把中央抬到 36.30 m 的一个独立闭合尖锥，每档 6 个三角；原中央山墙和两翼、入口保留。近、中全栋最高点现在为 32.40 m（为原有两侧的小尖饰，而非中央；这些尖饰没有重新测绘）。
- 远景复制近、中已有的中央山墙闭合几何，形体没有重新估尺度。新增 8 个三角、12 条边均成对闭合；中央最高点恢复至 30.20 m。三档在同一中央坐标上回读射线均为 30.175 m，五条正立面射线也一致。全栋主体三档 113,150 / 80,618 / 152 三角。
- 近、中五张共用贴图原样保留。新版远景贴图仅在原 UV 未使用的两个色块写入山墙颜色；Win、Gls 网格与原仓基线一致。JPG 是 Blender 离线回读，非游戏截图。
- 仍有原近、中常量 UV、两翼细节及远景高光待修；本包不合并此前独立的 GIS 重建试件。Editor 先看三档中央屋顶换档，再看玻璃、夜景和地块，尚未游戏验收、推 LFS 或导出 pmod。

- Original main SHA `3a7097a0ef154f454e0ce67da0b26c37c26bfed4`. Package: 13,466,362 bytes, SHA-256 `14b9d6c593c0e34897d103095c59107dac8b2d95feb38af66984aa3971fd44f0`. ZIP and extracted item SHA-256 verified. This textual audit does not publish LFS binaries. Two-campus offline whole total now 18 (Columbia 9, Penn 9).
