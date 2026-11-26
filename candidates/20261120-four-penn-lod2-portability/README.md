# Hill College House、Irvine Auditorium、Steinberg–Dietrich、Wistar Institute 的远景候选

这批按原始 Git LFS 哈希固定 4 个远景 FBX 和 20 张原贴图，修复每个 FBX 6 处旧机器绝对路径，改为同目录名称。重序列后，全部类型化内容仅这 24 处预定路径编辑发生变化。回导从第二份干净目录执行，禁用自动找图；各有 3 张随 FBX 绑定的图成功载入，另 2 张 ControlMask/MaskMap 作为配套 PNG 独立载入。有向网格、UV、材质和四栋原（三角数 72 / 108 / 72 / 36）完全保留，无零面积几何三角。所有 20 张贴图实际解码为 1024×1024。独立解码不等于游戏按正确 shader 解释。

四栋均未找到 Van Pelt 那种足迹完全一致且方向相反的四角水平接口，因此未套用焊接或删面。筛查范围不是证明其他接缝不存在。原模型、近中档、真实入口和地坪、建筑间对接、游戏渲染均未放行。尤其不能把本轮可移植性修复当成 Wistar 现代连廊或 Steinberg 西入口的造型修复。

复验：使用拉取 LFS 的仓库作为 reference。运行 `blender -b -t 2 --disable-autoexec --python-exit-code 1 --python portable_penn_lod2.py -- --reference <repo> --output <new-output> --clean <new-readback> --pins texture-pins.json`。输出清单 24 个条目，报告和脚本留在本草稿，不替换主分支资产。
