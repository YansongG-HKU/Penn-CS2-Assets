# Claudia Cohen Hall 远档屋顶候选

上一轮宾大候选在 LOD2 用四张水平三角面覆盖实际应为坡屋顶的体量。近、中档中的主屋顶和前伸山墙外壳在模型坐标一致。此次从两档一致的轮廓恢复 12 张屋面三角，再加 4 张檐底三角封住交界。两个檐底沿同一边界相接。图集中使用原远档板岩样本，五张图的改动限定于原平顶腾出的区域。

| 复验项 | 原远档 | 候选远档 |
|---|---:|---:|
| 三角面 | 36 | 48 |
| 模型最高点 | 16.50 m | 23.00 m |
| 完整导入目录 | 18,501,247 B | 18,398,310 B |
| 单件 ZIP | 18,319,401 B | 18,216,591 B |

其余 32 张远档三角的朝向、坐标和角点 UV 以四位小数精度逐项吻合。286 个向下屋面测点均命中，最低 16.61923 m，最高 23.00 m。图集改动区避开原有保留面的 UV，所有位置可从检查记录复算。屋面新切线按新 UV 计算。完整目录的 5 个二进制 7500 FBX 均在 Blender 4.3.2 实际回导。比较图为三组同镜，顶行原远档，底行候选：[轮廓](claudia-roof-same-views.webp) · [实际色图预览](claudia-albedo-same-views.webp)。

此次高度以现有模型坐标约束两档，真实屋顶标高、入口踏步、老虎窗和实际 CS2 切档仍待核。校方照片用于核对坡顶及山墙存在，校方另确认东侧有无障碍入口。[Penn Facilities](https://facilities.upenn.edu/maps/locations/cohen-hall-claudia) · [Penn 官方建筑照片](https://branding.web-resources.upenn.edu/sites/default/files/styles/card_3x2/public/2022-03/penn-claudia-cohen-hall.jpeg?h=75ed424a&itok=rEuId0Vf)

## 重放

1. 使用宾大草稿 `c99184277978e7d3cc36bf46a546472ac4f771a7` 的 ClaudiaCohenHall 试导入包，按该版逐件散列核对。
2. 运行 `python roof_delta.py /path/to/previous/ClaudiaCohenHall /new/ClaudiaCohenHall`，需要 Python 和 zstandard。重放脚本复核 16 个输入及输出，应用 6 份真实二进制差量。
3. 若独立重建，`roof_geometry.py` 在 Blender 4.3.2 中接受原资产目录、新资产目录、报告目录。环境变量 `CS2_CANDIDATE_TOOLS` 指向芝大 [d16f575 同批工具](https://github.com/YansongG-HKU/UChicago-Campus-CS2-Assets/tree/d16f575cd67a2100dc0d07680ea7176784d5f9e2/candidates/20261120-three-campus/tools)。再用 `roof_atlas.py` 写出候选五张图，以 `texture_preview.py` 重新读回。

CS2 Editor 验收仍待完成。
