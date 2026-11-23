# 宾大 Quad Memorial Tower｜贯通拱门、三穹顶整段试放

解压后只从 QuadMemorialTowerTrial/ 导入。3×3（24×24 米），保持原点、朝向和 Quad 模块尺寸。该塔是 Spruce 与 37th 的北入口，通向 Upper Quad；不要把它当成 36th Street Walk 东入口或 Provost Tower。参考：[宾大通行图](https://facilities.upenn.edu/sites/default/files/pennaccess/PA0490-Quadrangle.pdf)、[校方历史照片与建筑图](https://almanac.upenn.edu/uploads/media/No._29_Architecture_Supplement-Quad-2020_.pdf)、[校方拱门档案照片](https://penntoday.upenn.edu/news/photo-gallery-back-beginning-penn-quadrangle)。

- 原近、中、远三档是实心入口，街侧有仿门窗，背后也有挡面。此次在导入 FBX 中做出贯通拱口，模型内净宽 4.20 米、拱尖 5.42 米，实体内拱顶和两侧连续约 21.40 米；铺装在地块范围内随原基准面，保留塔群体量。近/中各去掉院侧挡路的两个整窗片。没有测绘这些尺寸，也没有复刻现实的闸机和无障碍控制设施。
- 远景旧三塔为截平块。按近/中档的轮廓控制点重建三个八边闭合塔冠，消除了顶部截平并对齐中塔 41.34 米、两侧 34.73 米的模型顶高。远景平外墙改为面法线，去掉 Blender 回读中的大块圆状高光。三档主体为 12,692 / 10,364 / 476 三角，近/中各有 104 三角的独立窗层；原空玻璃分件未整理进试放目录。
- Blender 回读：每档 4,108 个正反穿透采样，旧模型均被挡、新模型均通过；三档共 162 个地面、168 个内拱采样。21,383 个改动区外的相交样本最大偏差 0.010 毫米，UV 差约 2.55e−7；该比对不包括顶部设计改动和两片局部拆窗。旧图集新色块之外像素不变，近中共用五图，远景单独五图。
- Editor 验收分开做：先在平地从两头看拱孔和铺装，再把 37th/Spruce 一端接街、另一端接 Upper Quad。检查模板碰撞是否实际存在通孔，另连通人行路径并观察市民通行；随后在正确方向和标高拼接相邻 Quad 段、拉远/拉近和重开存档。附图仅为 Blender 预览，未实测游戏碰撞、通行、夜景、相邻段拼接或发布。不是 pmod。


## 核对与交付

源仓固定 `3a7097a0ef154f454e0ce67da0b26c37c26bfed4`，验证所有 FBX 和 10 PNG 的 Git/LFS 对象。新三档同时开通通道，不套用先前的 1,328 三角独立遮底补丁。现有资产只处理本段，未试其它 Quad 模块。便携 ZIP 8,304,144 bytes，SHA-256 `15a079339d60fe65d4520c8adb1dfa7604825a8d4e7b99537db3357a2beb429c`，ZIP CRC 与 21 份内部 SHA-256 在解压副本上通过。云电脑尚无可运行 CS2 Editor；此提交只有证据，不含模型 LFS 更新、不涉及 main、没有游戏验收或发布。
