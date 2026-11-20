# Van Pelt 远景：屋顶退台闭合候选

上一版只将同宽的首层与馆体焊接。此版进一步处理局部 z=22 m 的退台：去掉完全遮住的内盖面，保留 368 m² 的露出屋顶环，并按原三角边界裁切 UV；屋顶环与上层两条边需加两个顶点，故从上一候选 44 三角变为 52（原件是 48）。这是拓扑修复，不是削面目标。保留地块为独立闭合件，主体从两个壳连成一个闭合件。

独立 Blender 回导确认 30 顶点、78 条方向一致的双面边、无开边或退化面，边界框与上一版匹配。3 组同视角共 12 张图（底色与基色加法线的固定灯光各一套）：轮廓差全部为 0；底色通道最大差 2/255；带法线固定灯光的俯视仅 1 个像素差超过 12/255（最大 25），正后没有；实际游戏光照和完整 PBR 未测试。新交点切线框架从附近面插值并正交化，未将旧整片屋顶 UV 重新展开。接缝所在几何与真实建筑的部件是否对应仍需现场/档案核验，不能把这次清理当成已通过形体复刻。

`delta` 直接依赖原仓 LFS 的 `VanPeltLibrary/fbx/split/...LOD2.fbx`，已验证输出逐字节相同，与首层版本不叠装。运行 `python candidates/20261120-three-campus/model_delta.py apply <repo> <new-output> candidates/20261120-vanpelt-lod2-attic-weld/delta`。重新计算拓扑时，先按上一个 `20261120-vanpelt-lod2-weld` 候选得到固定的 44 三角输入，然后使用此处 `repair_vanpelt_attic_interface.py`。两件旁保持相同原 PNG，再以 `verify_vanpelt_attic.py` 和 `vanpelt_attic_compare.py` 重新验证。

未覆盖原件、两档近景未改、未发布 pmod。退出 Blender 后可用内存 8795 MiB，无本批 Blender 任务残留。
