# Penn 第三轮增量精修

仅包含13个目标模型；请保留前轮包，按目录使用增量候选。原仓库和前轮penn-refined未改。

|模型|LOD1前|LOD1后|LOD1/LOD0|
|---|---:|---:|---:|
|AnnenbergCenter|18322|13366|46.6%|
|ClaudiaCohenHall|9482|6890|46.7%|
|CollegeHall|83883|78931|67.8%|
|FisherFineArts|12662|10374|64.0%|
|FranklinField|11106|9450|56.8%|
|HillCollegeHouse|23558|17078|46.6%|
|HoustonHall|9492|7008|49.7%|
|IrvineAuditorium|16606|15346|77.8%|
|PennMuseum|4552|3784|67.8%|
|SteinbergDietrich|14354|10502|43.1%|
|VanPeltLibrary|64492|47164|47.5%|
|WistarInstitute|22904|16568|45.7%|
|QuadMemorialTower|9628|4780|40.1%|

LOD1累计减少59800个三角；8个目标低于50%建议：AnnenbergCenter, ClaudiaCohenHall, HillCollegeHouse, HoustonHall, SteinbergDietrich, VanPeltLibrary, WistarInstitute, QuadMemorialTower。

方法：删除小尺寸独立装饰组件，保留屋顶与主要体量；共面消融限定UV、材质、锐边和缝边，不使用盲目整体压面。13组三列几何图已逐行检查，主轮廓保持；Memorial顶部小垛口减少。当前预览为单角度Workbench，不等同材质/动态LOD切换验收。

LOD2：CollegeHall 1690→1600，同时补回162三角高位尖饰并删除252三角低价值带条；HoustonHall600→552；Memorial1336不变，进一步减面存在圆顶轮廓风险。本轮没有把这三栋降至500，仍列为待优化，不宣称预算通过。

39个新FBX已全部重新导入成功，13个源文件重开无使用纹理缺失。FBX仍为7400，不是官方2018版本验收；无CS2 Editor及游戏实测。保留原UV贴图不等于完成烘焙质量验证。

## 可选FBX7500结构格式候选
39个7400导出均完整解析并重新序列化为7500，位于各模型fbx7500目录，未覆盖refined_exports中的7400版本。每个转换均验证除版本字段外的解码树摘要不变，并在Blender分别真实导入原版和新版，39对网格数、三角数、世界坐标边界全部一致。此处仅证明文件结构转换和Blender回读一致，不代表Autodesk FBX2018工具链认证或CS2游戏兼容验收。明细见fbx7500_verification.json。
