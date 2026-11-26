# 宾大 Hill College House｜主入口平桥、种植沟与门槛

解压后独立导入 HillCollegeHouseTrial/，10×6（80×48 米），保持原枢轴。按[宾大楼宇资料](https://facilities.upenn.edu/maps/locations/hill-college-house)，从 34th/Walnut 方向走平桥到主要入口，较低西门只作应急出口。此次复现主入口的空间关系，不将模型局部坐标当现场测绘值。

- 三档将原实心高台和盖住浅沟的地面替换为平桥、开口种植沟和闭合地面网格。桥净宽约 5.30 米、跨模型沟口 3.60 米，桥面与两岸同高；沟底低于模型步道 0.62 米。实物桥宽、沟深、植栽和尖桩栏形未经测量，不宣称已复刻。
- 近、中删掉悬在桥上方的旧门框；远档只在对应前立面局部重涂旧门残影。新门与桥面对齐，仍是实色门片，不是可穿过的门洞或游戏寻路点。三档共 120 个竖向探针确认桥、两岸与沟底，九个横向探针命中新门；新增网格三档各自无开边、无零面积 UV。原楼主体顶分别为 23.95／22.95／22.50 米，换档仍要实测。
- 三档主体 36,198 / 23,142 / 304 三角，另有近、中各 540 个窗分件；原玻璃分件无几何，未整理进试放目录。远档保留结构形体，改硬边法线，Blender 墙面不再出现原圆斑。贴图仅改新构件色块、远档旧门区域；其他现存外墙网格与 UV 未动。
- Editor 要单独确认地形不会重新填平种植沟、路面接上桥面、门的入口标记可用，并保存重开后观察市民走完。附图是 Blender 回读，尚未验证实际方向、游戏碰撞/夜景、Git LFS 推送或 pmod。

- Main `3a7097a0ef154f454e0ce67da0b26c37c26bfed4`; prior 62-triangle standalone only read as evidence, not copied into geometry. New ZIP: 7,059,696 bytes, SHA-256 `1b2a1d8db7a98d12a3311191670e2b6ef3b2232bc7d9d0cfa76aba8445107ded`. Archive CRC and all extracted checksums passed. Total 23 offline whole trials (Columbia 12, Penn 11); game acceptances, LFS, pmod 0. Text evidence only.
