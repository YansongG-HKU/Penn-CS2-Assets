# Penn Quad #61 · McClelland Hall / Junior Balcony 现状复核

**结论：#61 继续保留为远景底面去重试验，但 McClelland 当前三档是代理模型，不能作为 2026 现状模型发布或合并。** 阻塞点是平台、餐厅外墙与邻段定位，不是给模型现有斜屋顶贴一片玻璃。

## 证据与段位

- [Penn Facilities 分段图](https://www.facilities.upenn.edu/sites/default/files/pdfs/QuadrangleHouses.pdf)：实际读图，McClelland 为上下庭院中央横隔向 36th Street 侧伸出的矩形，紧邻但区别于 Morris、Bodine。图上北向约为右，不直接当测绘或地盘高程。
- [2025 PASDA 正射](https://imagery.pasda.psu.edu/arcgis/rest/services/pasda/PhiladelphiaImagery2025/MapServer)：实际取图，EPSG:26918，1250×1000，回传范围 E 483033.404–483353.370 / N 4422170.420–4422426.392，约 0.256 m/输出像素（非传感器 GSD）。未旋转原影像，原点左上：中央连续坡屋顶约在 x=450–510，而 McClelland 对应的邻接平台/工区约 x=513–590、y=505–690，仅为定位窗，不是可直接描绘的天窗或墙边。该图仍可见施工痕迹，不替代完工照片。
- [Penn Today 2026-08-12 图文](https://penntoday.upenn.edu/news/after-multiphase-renovation-project-historic-quad-made-whole-again)：实际查看 Junior Balcony 大图 P-102187-SHS-0043a，确认铺地开放平台、低矮的倾斜玻璃天窗、深色框、浅色石基座与种植边，背后历史宿舍斜屋顶是不同体量。餐厅位于这处平台下方，不是把天窗挂到邻段历史坡顶上。白色活动设施不当永久建筑。单张图不用于确定天窗总数、绝对高程、尺寸或坡向。
- [改建设计单位 Beyer Blinder Belle](https://www.beyerblinderbelle.com/work/view/university-of-pennsylvania-quadrangle-dormitories-renovation/)独立确认 McClelland 已改建封闭外廊立面和上方露台采光。[Penn Residential Services 工期表](https://residential-services.business-services.upenn.edu/continuous-improvement)将 McClelland 关闭期列为 2024-05 到 2025-08。全 Quad 最后阶段到 2026 才完成；不得误认为天窗直到 2026 才安装，应用 2026 图核对完成状态。

## 云端实测的源与候选

| 档位 | 原件 | #61 候选 | 实际观察 |
|---|---:|---:|---|
| LOD0（Base + Win） | 15,504 | 15,504 | 近似对称双坡，多只老虎窗、两烟囱，未表达所需开放平台+低玻璃天窗 |
| LOD1（Base + Win） | 11,796 | 11,796 | 同类斜屋顶形体；近/中档 Gls 对象均为空（0 面），窗类对象仅存在于墙面高度范围 |
| LOD2（Base） | 40 | 38 | 仍是双坡体；此前只处理两张地块内朝下重复遮面三角，没有改屋面 |

Blender 4.3.2 实际重新读取两个 Blend，禁用自动执行。主网格近/中档包围盒 X −24…24、Y −12.1…12.0、Z −0.05…20.85（模型坐标）；远档 Z 上限 17.95。近/中档 Win 高度只在 Z 1.05…12.90，Gls 均为 0 三角；空 Gls **不是单独判定缺天窗的依据**，需结合三档真实模型图和实景比对。以上模型框含地块，不是现状建筑长宽高。
原件 SHA256 `ae54e06a2872d2db85b7eaf3c9c56e1dfae944592fecb4f45d935234b423907e`，#61 离线候选 SHA256 `20ba6778c96010386dc32d76fe78223888a41e4a738af370e8b2051bea8eda89`。旧的 38 三角 FBX 回读记录只证明该局部网格一致，并非版本 2018/游戏验收；本次审查未改 Blend、贴图或 FBX。

## 重建与验收次序

1. 在 Quad 总装中先锁定 Morris、Bodine 与两个院子的实景平面、朝向及高差关系；正式定点不得用 6×3 地块包围盒充当实景边界。
2. 找完工俯视或竣工平/剖，用于确定露台范围、封闭外廊、入口与天窗总数、位置、剖面。先独立做 McClelland，不重画上方邻段宿舍屋顶，不复制照片中的临时设施。
3. 近景保留斜玻璃、石基、平台边和封闭外廊，检查玻璃透视下支撑与背面；远景优先保留台地与两院的轮廓、高差，保持三档共用原点和串联边界。复验分段接缝、遮挡、碰撞、真实 FBX 回读与 CS2 Editor，分开标记结果。
