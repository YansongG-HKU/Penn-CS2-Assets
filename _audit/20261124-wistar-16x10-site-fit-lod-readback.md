# 宾大 Wistar Institute｜16×10 场地版，三档离线试导

解压后选 `WistarInstituteSiteFitTrial/`。这是单独的新场地候选，不覆盖旧 17×8 ZIP，不拿旧近档与本远档混用。模型以 Spruce Street 临街中心为高程零点，正面朝模型 −Y，主体水平约 115.63 × 70.33 m，16×10 格是暂定试放占地。市政源轮廓约 115.63 × 70.53 m，原 8 格深度不能容纳；当前体量没有强行缩放旧模型。以模型居中算，16×10 单侧大致留 6.18 m 宽、至少 4.74 m 深，不代表游戏道路对接已经通过。

- 按市政外轮廓重新做一个闭合壳体，轮廓差集 7.58 m²，约占源面积 0.16%。根据已核对的屋面高程分区保留东翼双坡与中部高低错台；只有局部高度参考点经过测量，屋面分界和绝大多数细节属于建模近似。模型最高约 40.3 m（相对本地基准）。
- 以 Spruce 街建筑照片保留蓝灰 Fox 幕墙、浅色台基、东侧暖砖及凹入式入口。四面纹理为原创程序图集，不包含参考图片；背面和非标志细节概化。入口为地坪、雨棚与不透明玻璃代理，无真实门洞、通行、透明/室内或实测门槛。
- 近／中／远主体与入口总计 542／434／362 三角。三档共用闭合外壳与枢轴；中档少部分细框，远档保留地坪、雨棚和门图，不再保留小框。5 个通道文件／组，近中共用 2048²、远景 1024²。中性法线、黑色发光图有意保守，未做夜景灯光效果。
- Blender 4.3.2 隔离目录回读 3 个 FBX，位置、UV、三角面数和贴图本地引用正确。主体 28,000 条三档射线中 6,404 个共同命中位置完全一致（其余同为空）；入口侧的 168 次纯几何探针通过。图是 Blender 光照预览，不是游戏截图。
- Dot 云电脑仍没有可用的 CS2 Editor。等能导入，按队列先验 Irvine；Wistar 先对向 Spruce 平地试摆，检查入口基准、路缘、近中远轮廓、阴影、重开和实际碰撞。未发布，无 pmod，无室内验收。

参考：[Philadelphia 市政建筑轮廓](https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/LI_BUILDING_FOOTPRINTS/FeatureServer/0)（OID 494057），[NOAA 点云元数据](https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9848/ept.json)及其既有局部校核，[宾大校方地址与实景](https://facilities.upenn.edu/maps/locations/wistar-institute)、[Ballinger 的设计和入口图](https://www.ballinger.com/design/robert-and-penny-fox-tower/)。


候选包：宾大-Wistar-Institute-16x10新场地三档-未游戏验收.zip；2,479,311 字节；SHA-256 `bc8b345aad1353a7f31697557b92cf7c952cec795e6776c5f898fbe50eb1dc4a`。干净解包后 CRC、内附全部文件 SHA 通过。三档 FBX 依次 `1af9a2fbe55d1cd3e8583784508c4e0c6b91eab4f3369182e3443b6cd6af0aef`、`06bcbd08496de7e590776ea1be2e7212009883f0acf506a3e7eca420f6afc384`、`4a246253127fac4add5703ac71cf68cace8d35ba1babcedf19bdae6dbb09ae76`。总数仍35；替换试放队列中的旧稿，不提交模型或发布。