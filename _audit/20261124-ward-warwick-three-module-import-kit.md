# Ward–Warwick / Editor 分件试导包
**三个 FBX 模块已通过 Blender 回读，尚未在 Cities: Skylines II 的 Editor 内导入、保存或重载验证。不是 pmod。** 解压 A、B 到同一个父目录，从各模块目录取同名前缀 FBX、贴图和 settings.json。两套原独立资产没有改变。这一包使用原建筑完整分辨率贴图，不是上轮 .blend 的缩小贴图。
 
| 模块 | 局部中心 X／Y／Z（米） | LOD0／LOD1／LOD2 主体三角 |
|---|---:|---:|
| WardNoPaving | +13.4 / 0 / 0 | 14,592 / 10,668 / 286，另近中各 214 窗三角 |
| WarwickNoPaving | −13.4 / 0 / 0 | 13,874 / 10,166 / 436，另近中各 202 窗三角 |
| SharedPaving | 0 / 0 / 0 | 36 / 36 / 36 |
 
这三组数是 **Blender 模型坐标**，不是承诺可照抄的游戏坐标。模型前朝 −Y，导入后先校验朝向和正负轴；共同地坪顶面 z=0，两栋设计主墙接线 x=+1.6 米。新地坪 58.8×32 米，面积 1,667.2 m²，原 124.8 m² 同平面重复地坪没有带进新包。跨檐和主墙接触面的内部关系未重新建模。共用地坪贴图是程序生成的中性石面，不当实景测绘。
 
## Editor 最小试验
1. 先单独用 Irvine 验证当前 Editor 的 FBX、贴图和 LOD 正常。通过再从 Asset Importer 分别导入三个目录：共享地坪用静态对象原型，两个无底板楼体先在空白地图核纹理和窗层，再做组合。不要同时放入有独立地坪的旧试件。
2. 在同一轴向检验地坪和两栋的中点、高程和转向。建议先试 8×4 格组合范围，不当作普通分区建筑规格。可对照 [Colossal Order 编辑器文档](https://colossalorder.fi/news/development-diary-custom-assets/) 的独立静态对象、调整子件和地块工具；绑定为同一资产的步骤需实机试验，不假定此 ZIP 会自动组成 prefab。
3. 验证三段距离的窗层、屋檐衔接、明暗及地坪无闪烁，保存重载后再查碰撞、入口标记与行人通路。不要把 Blender 或空场静态画面当作游戏通过。
 
B 内含 FBX-Readback.png、readback.json 和复查脚本；A 与 B 解压到同一父目录后可运行 blender -b -t 2 --python-exit-code 1 -P readback.py -- <解压后目录>。Blender 4.3.2 回读全三档；剩余遮挡、接缝与 Editor 兼容性均不是该脚本的结论。

A 18,552,044 字节，SHA-256 `a96d517da4f3e63e3a3b77ebc9e813f56f025d2747cdfb723f4a5b60df5b06c4`；B 8,884,544 字节，SHA-256 `e48368e4d6f7b9ed21737f4e0b7cf5b917bc92d5a598965935c3d842bc5a1507`。两包解到空目录逐文件核验，三档 FBX 再导入记录一致。仅证据，无二进制推送、不合并。
