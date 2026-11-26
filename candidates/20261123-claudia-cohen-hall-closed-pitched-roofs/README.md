# 宾大 Claudia Cohen Hall｜主坡屋顶、前山墙与闭合远景

解压后独立导入 ClaudiaCohenHallTrial/。沿用 7×5（56×40 米）候选地块和旧枢轴，三档模型顶约 23 米。这是原模型离线改版，不是测绘或真实东侧入口复原。宾大[官方楼宇资料](https://facilities.upenn.edu/maps/locations/cohen-hall-claudia)标明，实际无障碍入口在东侧 Perelman Quadrangle，不能把此包的正面门当成实际无障碍入口。

- 以此前已恢复坡屋顶的完整候选为基线，不回退到 main 的平顶简模（36 三角），也不混装另案的 124 三角模型。重建原坡顶与前山墙的内侧封面、缝边和接触去叠面，再与楼体、前伸体块和底座合为一套闭合远景。最后 96 三角、144 条边正反配对；按原始索引比，56 条开边变为 0。按同位边计，14→0；正面积同面重叠 10→0；非邻接 BVH 交叉筛查 35→0。
- 六方向 21,346 个外表命中，未增减，首交点最大差 0.046 毫米，UV 最大差约 4.54e−7。两张同机位无灯光图总共只有 140 个像素不同，1 个像素通道差超过 20/255。Studio 对照中原墙体圆形光斑消失，原因是远档墙面法线不再跨硬边平滑；实际游戏材质仍待验。
- 三档 14,522 / 9,266 / 96 主体三角，近、中另各 216 个 Win 三角。近、中网格与之前候选一致；没有空 Gls 文件。十张贴图保留原候选字节。本轮未按实物新增老虎窗、改东侧路径或承诺色彩完全真实。
- 进 Editor 优先核主屋顶、前山墙和外廊换档、材料昼夜、无障碍入口和地块冲突。附图仅 Blender 回读，尚无游戏通过、LFS 推送或 pmod。

- Input: prior 48-triangle pitched roof `Penn-Claudia-Cohen-Hall-CS2-Editor-candidate.zip`; older 124-triangle standalone not used. New ZIP: 17,992,915 bytes, SHA-256 `f1bc0586dd797e8918f04a8ce27a9b2ea25cd23bec9556f224b7d44d4902e215`. ZIP CRC and all extracted SHA entries verified. Offline whole count 21 (Columbia 11, Penn 10). Editor, LFS, pmod 0. Text evidence only.
