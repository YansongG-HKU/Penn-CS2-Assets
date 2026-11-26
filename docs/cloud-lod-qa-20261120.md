# 云端 LOD 复核：单批次、低内存

在云电脑上只跑一栋（或一个小批次）。先做统计，需要画面时再单独渲染。用最新、已经校验的模型文件；这里的统计脚本不代替 CS2 Editor 测试。

```sh
export BD=/absolute/writable-output-dir AN=NA_asset_name
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2
python pipeline/cloud_blender_guard.py --timeout 180 --min-free-mib 2048 -- \
  blender -b -t 2 /absolute/path/model.blend --python-exit-code 1 \
  --python pipeline/lodcheck.py -- --stats-only
```

- `--stats-only` 要求近、中、远三个主体网格均有几何，只写 `lodcheck/mesh_checks.json`，不渲染。请为每次复验用新输出目录，不要把旧图或旧报告当作本轮证据。
- 要生成三张同取景 LOD 对照图，去掉最后的 `-- --stats-only`。默认两线程，每块临时图像数据使用后移除；仅在 Blender 实际报告构建不支持 OpenImageDenoise 时回退到不降噪，其他错误仍中止。
- Linux 护栏启动前及运行中检查 `MemAvailable`，低于阈值或超时只终止本次启动的 Blender；任务结束输出采样峰值和前后可用内存。不要并发跑多个重任务。它不是系统内存的硬配额、不会释放其他任务的内存，也不能保证防住瞬间内存尖峰。

## 本轮复验

在 Blender 4.3.2 独立回读仓库 LFS 的 Claudia Cohen Hall 主体 FBX 三档：14,522 / 9,266 / 36 个三角，各档均无零面积面；采样峰值 239 MiB，退出后可用 9,349 MiB。近中档的各 224 条多面共边仍须分类，未一键删除。这里是仓库原始主体（不含 Win/Gls FBX），不是已另行交付的远档 48 三角屋顶修复候选，二者并不矛盾。未改成品、未新增游戏内验收。

McClelland 的低拱廊、露台及天窗已获照片支持，但没有露台、天窗及两翼接缝的同基准标高；不以庭院高差代替。

[实际源 FBX 哈希与三档统计](cloud-lod-qa-readback-20261120.json)。另用最小测试模型确认渲染模式即使缺少降噪组件也正常生成三张 1920×400 图，终止测试未留下 Blender 进程。
