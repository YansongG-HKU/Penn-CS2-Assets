# 宾大博物馆 Harrison Rotunda：外屋面内缘两段接缝

沿原外锥屋面向内拓至 4.00 m。仅补 0°–56.25°、213.75°–270° 两段（0° 向东，逆时针），水平投影约 2.28 m²。两段合计在 r=4.28 m 处与旧网格逐边贴合，约 8.40 m。两边顶点坐标和 UV 精确一致，但对象独立、未焊接。三档总面数为 2256 / 1452 / 964。之前 12 个 Blender 网格对象的顶点、面、UV、角法线、材质槽与变换均未变。

候选延续原定位 EPSG:6347 (E483593.5259128295, N4422145.391199051)，+X东、+Y北、几何 Z0=40m NAVD88。2022 NOAA 9848 为原模型同源数据，按采集编号单独复核；2025 Philadelphia PASDA 7158 为跨期核查，未公布的高程单位、垂直基准不能视作官方确认，使用邻近地面点经验换算 raw Z ×1200/3937 +0.03402591m、未进行 XY 拟合。留存候选范围的全部符合类别、首回波和组号的 199 个点：197 个归入较低一层，两个较高点另列。划分阈值是既有两锥面中点，不按新网格残差删除点。最稀疏的单组覆盖最近邻最远约 0.62 m。

Blender 4.3.2 重读全部三份 FBX；2610 组接缝两侧（各 0.5 mm）射线没有跨边误命中，高度差最大 0.51 mm，接缝顶点无位移；6240 处三档共同命中点高度最大差 2.58 mm。分段、分批次复核的 P95 最大约 0.186 m；最大单点差约 0.321 m，不隐藏离群点。

原始基准文件来自上一版四片屋面包。要复现构建，把上一版唯一的 .blend 复制为 previous.blend，并将试件目录作为 Blender 脚本的 -- 参数。witness.npz 包含本次实际复核摘取点及另列的高层候选；evaluate.py/probe.py 另需两期原始提取数据，远程原始数据没有整份打包。点云不是现状摄影或材料证明。

未补完整环带、垂直连接、墙体或贴图。本件是候选组件，不是完整建筑；未通过 CS2 Editor / 游戏验收、未发布 Paradox Mods、未生成 pmod。

## Evidence receipt

- Candidate ZIP: 541833 bytes; SHA-256 `1795c60724bd40f50b9e3c6afcb837f339faefa4be712b6b47b329f137cb8114`.
- Blender: SHA-256 `f2e5e2abf217af5a4d914d45e0a6baad9f567b0475168b4ae956538a086dafe8`.
- 2022/2025: NOAA EPT 9848 is identified in the earlier baseline; [PASDA 7158](https://www.pasda.psu.edu/uci/DataSummary.aspx?dataset=7158) is separate input. Only this receipt is committed. No production replacement, LFS commit or merge.
