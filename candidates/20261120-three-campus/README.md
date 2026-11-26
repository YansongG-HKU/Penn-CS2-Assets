# 宾大 12 件建筑和 34 个 Quad 分段的导入包复核

取回并验证 main `3a7097a0ef154f454e0ce67da0b26c37c26bfed4` 的实际 Git LFS 数据。逐件核对 46 份 Blend 和 322 个分拆 FBX，三角数一致。之前私有精修 ZIP 下载返回 HTTP 403，该 ZIP 的内容未纳入这版候选。

## 包体与仍需验收

- 用相同且唯一的路径引用一套贴图，重压 PNG 的 IDAT 数据，原像素、位深和非 IDAT 数据保持一致。作者 Blend、预览图和另一套整组导出仍在仓库基线中。
- 逐个识别、剔除 45 个导入目录里共 90 个确认为零顶点且无独占贴图引用的玻璃占位 FBX。保留余下 FBX 的可见几何与 UV，并统一为可实际回导的 7500 二进制格式。94 个特殊网格解除预览材质绑定。College Hall 的两个非空玻璃 FBX 修复 32 个塌缩 UV 面，通过无重复、无塌缩的回导检查。
- `asset-audit.csv` 逐项记录真实字节，`asset-hashes.json` 列出最终文件散列和引用。最高点差超过 2 米的条目标记为查看切档时轮廓变化，数值用于定位，不判定为游戏硬性阈值。
- Quad McClelland 仍为旧坡屋顶代理，实际露台、天窗、封闭外廊和邻段定位待核。Franklin Field、Wistar 等的现状和三档形体疑点见 [逐栋复核](../../docs/building-by-building-review-20261119.md) 与 [McClelland 专项](../../docs/mcclelland-modern-exterior-verification-20261119.md)。玻璃占位移除不改变这些待处理建筑形态。CS2 Editor 与游戏内仍为 0/46。

[共同的重放工具及技术验收](https://github.com/YansongG-HKU/UChicago-Campus-CS2-Assets/tree/codex/full-source-technical-audit-20261118/candidates/20261120-three-campus)

从校验过的原克隆重放 94 个模型差量，请运行 `python model_delta.py apply /path/to/penn-repo /new/replay-dir fbx-delta`。完整导入目录需要使用体积审计中所列的贴图、设置和其他网格。
