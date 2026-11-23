# 宾大 Steinberg–Dietrich Hall｜Mack Pavilion 西入口整栋试放

解压后用 SteinbergDietrichTrial/ 独立导入，保持 16×10（128×80 米）、原枢轴和 Locust Walk 大体朝向。在模型 −X 一侧补建 Mack Pavilion，对应真正从 37th Street/Walk 进入的西门，而不是把原 Locust Walk 主门改名。来源：[宾大楼宇资料](https://facilities.upenn.edu/maps/locations/steinberg-hall-dietrich-hall)、[Wharton 2013 完工说明与西塔照片](https://operations.wharton.upenn.edu/shdh/shdh-west-tower-addition-2/)、[PennAccess 三处入口说明](https://facilities.upenn.edu/sites/default/files/pennaccess/pa0535-steinbergdietrich.pdf)。原资产是简化 E 形底模，不作整栋测绘或精确现场配准。

- 新增一个闭合的浅石框塔，内凹幕墙按 6 列分隔，近、中保留窗梃，远景在贴图上保留相同分隔。两侧加低玻璃廊、绿顶和转折砖翼；西门有门罩、独立门面和前方平铺区。塔顶模型高度三档均 20.70 米，最高主体仍 22.00 米，恢复远景原先省略的上部体量。原近中主体与窗除新增几何以外均保留，近/中旧塌缩 UV 为 17,834/7,850 个三角，本轮未改。
- 三档主体三角数 24,820 / 14,812 / 316；近中窗各另 326 个三角。新幕墙是着色的不透明表面，未做真实透明、玻璃内部或可通行入口；不发布空玻璃分件。近中共用五张图，远景五张图，图集只改原三档未使用区。远档旧平面按面更新法线，消除预览的大块高光。
- FBX 回读三档各检 42 个幕墙、18 个玻璃廊、18 个砖翼、12 个门面、20 个铺地和 7 个屋顶点；另外 19,529 个改动范围外的俯视探针没有变。高塔单壳各档 42 边，均两面相接。
- Editor 需独立确认 37th Street 路缘与西门的连续路径、模板碰撞、日夜材质、三档切换和存档重载。现实西门有沿西南翼下降到地层的坡道，Locust Walk 另有一条独立坡道；此次未重建两条真实坡道或 3 个出入口的现场高差。附图为 Blender 对照，未做游戏验收，也不是 pmod。


源仓固定 `3a7097a0ef154f454e0ce67da0b26c37c26bfed4`，验证全部源 FBX 和 10 PNG 的 Git/LFS 对象。本轮基于 72 三角原远档，不混接旧 62 三角的独立遮底测试；原物与现状配准仍待查。便携 ZIP 18,903,025 bytes，SHA-256 `b06d3ba9e95fb65a0febfd6805bb62edcfe698940966b5908b3e416b13c55264`，CRC 与 21 份解压内容 SHA-256 通过。只把证据写入此草稿，未改 main、未推模型 LFS、未游戏验收或发布。
