# McClelland 后侧退台修整（离线候选）

只在 Dot 云电脑运行。基于前版完整低砖拱廊资产，把大部分后缘从局部 +9.53m 收到 +5.10m，+X 端保留短折角至 +8.90m。地面中心、48×24m 地块、正面 12 拱窗、石栏和低天窗不变。屋顶投影少约 189.81m²。用 OSM 2017 独立建筑轮廓做近似比较，投影交并比 0.717→0.908，不是测绘。

三档 4324/2624/840 三角，Blender 回读 FBX 相对 GLB 最大顶点误差 1.956μm；已核有效 UV/相对纹理与逐档 12 拱窗和屋面 7 个取点，正面受保护部分 4218/2518/734 三角完全一致，另每档 8 片只在同一平面改变三角划分。ZIP CRC 通过，SHA256 `79561b3f3756c0564ba412d6b40ede3c53bd0f15a7256e3b2fa2dca2e31ef846`。

Morris/Bodine 原始原型按地图锚点放置时，其保守包围框与新屋顶投影仍有约 130/63m² 相交（前约 229/162m²，分别比较，不能相加），不是实际三角面碰撞。只建议独立试放，未做两宿舍组装、高差和 Editor/游戏回读，未推二进制或 pmod。

参考：[Penn Facilities 平面](https://facilities.upenn.edu/sites/default/files/pdfs/QuadrangleHouses.pdf) · [OpenStreetMap 轮廓](https://www.openstreetmap.org/way/320602420)。