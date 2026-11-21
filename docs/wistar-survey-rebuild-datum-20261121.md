# Wistar Institute：屋面与临街地形基准
这是供 Blender 重建用的实测参考，不是可导入 CS2 的成品，也不替换已修复的 Wistar LOD2 FBX。OBJ 为 Z-up / 米制；在 Blender 以 Forward = -Y、Up = Z 导入。12 张局部面、3 条线均为参考层；不要给参考层赋游戏材质或添加碰撞。

## 已确定
- 费城市政 LI_BUILDING_FOOTPRINTS，OID 494057、BIN 1422414。以 Spruce 临街长边方向对齐，外部投影约 115.63 × 70.53 米；旋转矩形能够达到的最小宽度约 68.71 米，任何方向的 8 格（64 米）都放不下完整外轮廓。若使用 8 米格、按这个临街方向对齐，15 × 9 只是几何下限，前后居中每侧只余约 0.74 米。未加入道路退界或编辑器留量，也不代表每个屋檐都落在地面建筑边线上。
- 中部 Spruce 人行道实测区中心为 19.01 米 NAVD88。相对这个基准，Fox 主屋面局部约 +37.54 米、局部高带约 +40.32 米、南侧低带约 +33.65 米；西区低屋面约 +21.17 米、高平台约 +28.51 米。东翼两坡走势独立可见，实测约 6.8 米的屋脊局部标高约 +22.63 米（不是整条屋脊长度）。Spruce 西侧样窗比东侧约高 1.40 米，北侧开敞样窗比中部临街样窗约高 3.32 米。
- 64 个局部查询 1,007,002 条，精确去重后 1,006,962 条。地面用 class 2，屋面只用 class 1 首回波且按高程模式分离；复核各独立 PointSourceId 和空间交错分块。东翼屋脊在 10 个互不重叠的窗口用 373 条未参与两坡拟合的回波检查，最差窗口 P95 绝对残差 0.125 米。带状屋面可能包含女儿墙或设施，不等于建筑最高点或整片同高。局部残差不代表跨数据源绝对配准误差，图表保留两位仅供相对定位。
- Blender 4.3.2 新会话复读：12 张向上的参考四边面、3 条独立参考线。游戏编辑器尚未验证。门槛、玻璃构造、地面外墙线、跨 LOD 烘焙、摆放枢轴仍需单独验证。没有把旧 136 × 64 米 LOD2 强行缩放。

## 复核文件
正射影像的底图用于对读，地理范围 E483165–483351, N4422304–4422420（市政 EPSG:26918）。市政轮廓和影像转换到 NOAA EPSG:6347 时，当前环境无专用 NAD83→NAD83(2011) 网格、PROJ 标记 ballpark。不可把外墙轮廓与点云当作已做厘米级绝对匹配。Z 为 EPSG:5703 NAVD88（GEOID18）。OBJ 原点是临街坐标系内外投影包围盒中心，Z=0 是人行道样窗；不是游戏枢轴或门槛。
- [Philadelphia 建筑轮廓图层](https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/LI_BUILDING_FOOTPRINTS/FeatureServer/0)；依据 FeatureServer query 返回明确声明 EPSG:26918 的 city.json，而非返回 Web Mercator 坐标的单要素 REST 结果。
- [NOAA EPT 源元数据](https://noaa-nos-coastal-lidar-pds.s3.amazonaws.com/entwine/geoid18/9848/ept.json)；附件附节点收据与已提取压缩 CSV 而不是完整大范围点云。
- 使用系统 Python：依次运行 analysis.py、fit.py、ridge.py、deliver.py。analysis.py 创建本地去重缓存并打印试窗统计；fit.py 生成更新后的正式样窗；ridge.py 校核屋脊；deliver.py 生成参考 OBJ 与图表。extract.py 为从原始 EPT 复现提取的 QGIS 脚本，节点哈希见 ept-receipts.json。check_obj.py 在新 Blender 会话验证几何。

内部交付包 SHA-256: `96d0de760c1f2ef94fef7fb270c1ff83785193174438040b378161f38d0f4171`（10,051,974 字节）。本提交只记录离线重建基准，不改变 FBX 或主分支。
