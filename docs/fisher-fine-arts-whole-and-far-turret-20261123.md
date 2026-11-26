# Fisher Fine Arts 整栋与远景塔顶试放

只用 Dot 云电脑。基于已验证的 344 面远景双接缝版本（输入 SHA `079e2239ebec87beebd9d9f922d64a3a0c0f13bfa2f65ee13e68127eafad551a`），删 1 个 z35m 顶盖面，加由该面原 UV 仿射映射的露天屋面环与四层索引环拼接的两段小塔，塔址、宽度与高度来自近中档模型而非测绘。199 个既有面位置、UV、法线和材质不动；新面局部采样原砖色，不动十图。每条索引边成反向配对，新塔与原塔屋面共享索引而非叠面。远档 344→376 三角，最高 35→38m，近中仍 38m。复进口五个塔顶与外圈探针分别落在 38/35m ±0.05mm。

试放 8×6，选择 `FisherFineArtsTrial/`，主体 15816/12264/376，2 Win 各 398。省略原本完全空的 2 Gls；10 PNG 解码、5 FBX 隔离回读，CRC 已核。ZIP SHA-256 `df4f549c94632fe80aaf1ca02c9d48da27a8423b92e726d8fb4dde9c651d9af5`（20,801,187 bytes）。近中主体存在 7674/4122 片非零几何、零面积 UV，未改动，不等于确定的可见缺陷；先做可见分布核对。远场还简化塔栏与圆翼尖饰，未验昼夜、入口、落地、实际材质、LOD 或存档重开。无发布、LFS 推送、pmod。实景参考 [Penn Facilities](https://facilities.upenn.edu/maps/discover-penn/fisher-fine-arts-library)。