# 宾大 Quad Ward｜连续坡屋顶、四座老虎窗与角塔整段
从 `QuadWardTrial/` 独立试放。4×4（32×32 米）地块、中心枢轴与主墙底框保持原候选；主楼实体矩形约 23.6×23.2 米（不含角塔、屋檐和地坪）。以 [PennAccess Quad 图](https://facilities.upenn.edu/sites/default/files/pennaccess/PA0490-Quadrangle.pdf)识别 Ward 段；[宾大建筑档案目录](https://www.design.upenn.edu/sites/default/files/017_Cope%20and%20Stewardson%20finding%20aid.pdf#page=5)的 Job 388 将 Ward、Warwick、Chesnut 同列，目录不是已读施工图。本次用近景模型校准远景，不称实测，不合并邻段。

- **远景屋脊**：用连续坡顶替代两段背对背封死的屋顶；删去屋脊内壁，消除原同位置相反法线的 210.54 平方米重合。接外墙的 4 条檐下边复用原墙顶顶点索引，移除原墙顶内盖；不声称整块地坪和角塔已经布尔并网。平面用面法线，远景屋面不再使用原有高光斑、烘焙假窗区域。
- **远景轮廓**：恢复前后各两座老虎窗、中央烟囱和八角塔尖。主脊高 23.0 米；烟囱 25.9 米（原远景整栋最高 23.0 米）；角塔原远景顶 19.5 米，恢复为近中 21.7 米。屋身颜色、窗框及边饰为简化，近中窗叠层不变。
- **回读**：主体 14,604／10,680／298 三角，近中另各 214 窗三角，两个空玻璃占位未带入。从原采样点提取相同颜色和 PBR 值，在近中图集未占用区给 7,766／3,866 个退化 UV 重新展开；原有效 UV、原已占用的图集像素以及近中几何均保持，回读三档无退化 UV／零面积几何。99 屋面、100 老虎窗坡面、36 窗框、25 烟囱、5 角塔和 4 地坪角探针通过。
- **仍待 Editor**：先 Irvine；轮到 Ward 再与 Chesnut、Warwick 分段试摆，复核模型前面（−Y）朝向、接口高差和相邻地块重叠，实测 LOD、碰撞与夜间效果。未验证真实段间拼接、地形、行人、pmod；不假定先前仅底面修补的 316 面版本被合并。附图仅 Blender 回读。

## Offline evidence (Dot cloud, 2026-11-24 UTC)

- Input pinned Penn main `3a7097a0ef154f454e0ce67da0b26c37c26bfed4` (19 exact Git blob/SHA or LFS bytes checked against pinned pointer and size).
- ZIP `宾大-Quad-Ward-连续坡顶与八角尖塔整段-未游戏验收.zip`, 18,736,417 bytes, SHA-256 `1999b0c98a1f5de0646d6b2f96dd427ed0e2c5a13def3e3a15e50a316bd1b97a`; CRC plus all 25 extracted hashes passed. Five FBX, ten PBR PNGs and sharedAssets. No binary pushed to Git.
- `placement-qa.json` `945ce784b91d799b82be79e887351226526fab0b538a9f49a2899f6cd823e3bf`, `readback.json` `8051b7a40408d60845d6a49b1b04d2e08353a6eb601c7b8d9489578f02d15d2c`, `Quad-Ward-Readback.jpg` `944c6900af4dff9dd54db7893eb300f35449f448cc5fea53a7ba5c8629c33571`.
- Replaced three source far components and one internal wall cap (46 triangles), then reused exact wall-top vertex indices for main roof. Original near/mid geometry, valid UV and window overlays unchanged. No claimed grade, neighbor registration, collision, actual game pass, pmod or publishing. No Blender job left running.
