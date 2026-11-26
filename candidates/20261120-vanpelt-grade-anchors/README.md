# Van Pelt 两个入口方向的地面控制

对照 2025 年宾州空间数据中心（PASDA）正射、2026 年 11 月 Penn 导览两页和 PennAccess 原文，确认南侧主入口沿台阶上升到 First Floor；更东侧平层门进入 Ground Floor 的 Goldstein 学习中心。两门不在同一个立面坐标，也不能从南侧看起来相近而赋同一高度。未改模型首层或入口。

实际按 HTTP 字节范围读取 NOAA 2022 裸地数据，仅写出 274×260 像元局部裁片；原栅格为 3 ft 网格，横向 EPSG:6565，垂直 EPSG:6360、NAVD88 美制测量英尺。对正射可见铺装各 3×3 栅格取中位数：南主楼梯下方 19.331 m、更南步道 19.291 m，东侧铺装 17.910 m。约 1.42 m 是这两个铺装采样区域的地面差，不是两个门槛差、更不是楼梯升高。东南门方向的近似点 18.150 m 未达可靠铺装控制标准。主阶中部和顶部临建筑边的采样结果不单调，按插值风险排除，不拿台阶像元或八级台阶数量作真实升高。应取有测量的两入口门槛和楼梯剖面后再建精确台阶。

市政完整轮廓按局部轴约 142.04×56.69 m（参数来自 BIN 1386251 图形，含侧翼/附件）；新最高属性 104.92015 ft ≈31.98 m，早期资料 AVG_HGT 76.2 ft、MAX_HGT 101.1 ft。它们是整体统计，不覆盖东翼屋台、露台、设备顶的独立标高。别把远景焊接件中的 z=22 当测绘数据。保留现有焊接件；真实入口和屋面仍待验，未进入游戏。

复现：用 `gdal_translate -projwin 2684610 236340 2685432 235560 /vsicurl/https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/PA_Phil_DEM_2022_9849/Philadelphia_dem_3ft_2022.tif vanpelt-dem-crop.tif`，再 `/usr/bin/python3 vanpelt_grade.py vanpelt-dem-crop.tif vanpelt-grade.json`。原图用 [PASDA 正射服务](https://imagery.pasda.psu.edu/arcgis/rest/services/pasda/PhiladelphiaImagery2025/MapServer/export) bbox 与 imageSR 均 EPSG:26918，bbox=483323,4422400,483554,4422620，size=924,880；SHA-256 `3152d7c4420f9a72fce152119ea42d31486b812574a0513056ff8c370f7156c9`。
来源：[Penn 导览 p.1–2](https://www.library.upenn.edu/sites/default/files/2026-11/Van%20Pelt%20-%20Floor%20Plans.pdf)、[PennAccess](https://facilities.upenn.edu/sites/default/files/pennaccess/PA0110-DietrichLibrary.pdf)、[费城建筑轮廓](https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/LI_BUILDING_FOOTPRINTS/FeatureServer/0)、[NOAA 地面档案](https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/dem/PA_Phil_DEM_2022_9849/index.html)。
