# 宾大 Quad：Ward 与 Warwick 双段试拼
**可复跑的离线证据，不是新模型、CS2 Editor 实测或 pmod。** 仍用此前交付的两个 ZIP，附件不重复放模型。

| 场景 | 主墙结果 | 地坪结果 |
|---|---|---|
| 把两段模型放到 OSM 轮廓外包框的中心 | 主墙平面交叠 37.75 m²，沿试拼轴穿入约 2.70 m | 同平面重叠 189.51 m² |
| 模型主墙对齐地图共边的中点 | 主墙刚接触，沿接边方向模型主墙共边长 14.00 m | 地坪同高重叠 124.80 m²，重叠带宽 5.20 m |
| 两个地块边紧贴 | 主墙留缝 5.20 m | 地坪无正面积重叠 |

- 校方 [PennAccess 第 3 页](https://facilities.upenn.edu/sites/default/files/pennaccess/PA0490-Quadrangle.pdf) 与 OSM [Ward](https://www.openstreetmap.org/way/320602400)、[Warwick](https://www.openstreetmap.org/way/320602421) 轮廓一同确认邻接。地图共边由节点 3271767129 和 3271767306 组成，投影长约 11.79 m；不是 14 m 的模型矩形边，也不是门洞或实测高程。更正旧包的试放说明：Warwick 另一侧直接接 McIlhenny；Thomas Penn 更靠转角，不是本段接边的邻件。OpenStreetMap contributors，ODbL。
- 共边中点为局部原点。+X 指向 Ward，−Y 大致朝庭院；两个模型不缩放，地坪实在模型坐标 z=0。三档回读确认地坪四角和表面。贴墙时两主屋檐投影重叠 9 m²，但不是屋面相撞的实证。此试验没测真实地形、建筑细部碰撞、入口或路径。
- Editor 先导入 Irvine，再单独导入这两段，最后用一个共用地坪的双段组合试放；用真正的墙檐边和邻接界面查缝，不用两个独立地块强行凑齐。组合尚未制作，现有两个 ZIP 不能算拼装通过。

## 复跑
解压此前 Ward ZIP 到 inputs/ward/、Warwick ZIP 到 inputs/warwick/；各自校验 SHA256SUMS。输入整 ZIP 摘要见 input-sha256.txt。用 Python（NumPy、GDAL/OSGeo）执行 geodesy.py，再用 blender -b -t 2 --python-exit-code 1 -P readback.py。fit.json 是三种偏移与重叠，measured.json 是两段三档回读；Ward-Warwick-Blender-fit.jpg 是三场景对照图。

归档 `宾大-Ward-Warwick-双段试拼与地坪重叠-离线证据.zip`，217,237 字节，SHA-256 `f877ac42163c9c74ff0a0b21ac6161f32d4641f01917cac08d573bf567e569ae`。重新计算三组几何数值并对照归档摘要。仅证据，无新整包、无游戏验收或二进制推送。
