# Claudia Cohen Hall：云端无旧包重建复验

以宾大草稿 `dd50bef` 的 LFS 原件和芝大 `d16f575` 固定工具为输入。只取 Claudia Cohen Hall 的分拆 FBX、PNG 与设置；核对 LFS 指针的大小与 SHA-256 后读取实际内容。没有使用之前不可下载的私有候选 ZIP。

1. 从单件克隆原件构造 staging 清单，走共享 `portable_readback.py`、`png_storage.py`、`finalize_import.py`（无几何修补记录）、`special_mesh_materials.py` 的顺序。空玻璃占位不进入成品；窗口材质绑定按共享规则处理。
2. 固定 `roof_delta.py` 对重建出的 16 项前序文件逐件校验，再应用 1 个远档 FBX 加 5 张配套图，共 6 个差量。16 件输出均与候选清单 SHA-256 相符。
3. 另起 Blender 4.3.2 两线程批次对最终 5 个 FBX 独立回导、关闭自动搜索；贴图从同目录解码，近中网格和原候选一致，远档 48 三角、最高点 23.00 m，最终 FBX 未检出零面积三角。退出 Blender 后生成并复验 ZIP CRC 与解包 16 项 SHA-256。此次 ZIP 17,914,832 B（SHA-256 `66fc3c7ef2d9f9fdfa7932072a96217ad72d73969e0461b498b2ea9abdd0ad7b`）；压缩方式与早先包不同，解包内容按清单一致。

这是完整的 **CS2 Editor 试导入候选**，不是已通过 CS2 的资产，也未写入仓库 canonical 模型路径或发布 pmod。当前云电脑未找到已安装并可用的 CS2 Editor/游戏，实测待办。
