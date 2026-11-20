# McClelland：上下庭院高程基准（非露台标高）

按[校方分段图](https://www.facilities.upenn.edu/sites/default/files/pdfs/QuadrangleHouses.pdf)对照：Upper Quad 是西侧三角庭院，Lower Quad 是东侧有交叉路的院子。McClelland 从 Morris/Bodine 侧的中间隔带伸向 Lower Quad；2025-09-14 [Lower Quad 实景](https://commons.wikimedia.org/wiki/File:University_of_Pennsylvania_Quadrangle_First-Year_Dormitory.jpg)实际查看可见低层明亮拱廊，后方坡顶与它是不同体量。校方 [2026 年完工图文](https://penntoday.upenn.edu/news/after-multiphase-renovation-project-historic-quad-made-whole-again)核对露台地面、采光玻璃和植栽关系。

- **主证据**：[2022 Philadelphia LiDAR 测绘报告](https://www.pasda.psu.edu/download/phillyLiDAR/2022/Metadata_and_Reports/Lidar_Report/65221207_Philadelphia_Mapping_Report.pdf#page=5)标明 NAVD88、US survey feet。同点位子样本 Upper 3 点中位 71.897 ft、Lower 6 点中位 58.551 ft，点集高差约 **4.07 m**。这是庭院场地级高差，不是走廊、门槛、露台、天窗或任何单个连接点的标高。
- **交叉验证**：[2025 PASDA DEM](https://www.pasda.psu.edu/download/phillyLiDAR/2025/DEM/tiles/)在同点子样本得 13.140 个原始栅格高程单位的差；该批发生在施工期，GeoTIFF 没有可用的垂直单位/基准标签，不作为竣工高程。2025 全点样本 Upper 6 点中位 71.775、Lower 11 点中位 58.600，仅列栅格原值。
- 两份 JSON 记录影像范围、像素、坐标变换、原值和数据局限。取样以邻近道路/路迹地面为主，不落在屋顶上，也不拿施工区作竣工平台。若另有竣工剖面，用实际台阶和外廊边核对后再设模型局部 Z 原点。不可把约 4 m 直接套到任何屋面或接口。

本轮未改原代理模型，不把旧坡顶以微调冒充 2026 复刻。仍需露台本体的剖面、平台边/外廊与邻段接口控制点，以及 CS2 实测。
