# Penn Museum: Front pavilion gable at far LOD

Same isolated 21×15 trial as [the whole original baseline](penn-museum-whole-baseline-20261123.md). Restored a closed 24.5m gable/roof over the front pavilion, based on the existing medium profile; used padded in-face regions from the existing far brick and roof atlas, without rebaking. Fourteen added triangles, 232→246; retained all 232 original triangles and 696 original corner normals; 369 edge pairs and no degenerate triangles. Blender 4.3.2 reread confirmed the same 168×120m envelope and overall 31.00m height, relative images still resolve, and all other files were byte-identical (near/mid, windows, ten PNGs, settings).

Medium/far projection IoU in identical views: facade 96.0→96.0%, diagonal 87.4→96.8%, side 82.7→94.7%. Rotunda roof profile and stair detail were not touched. Next focus: recover layered Rotunda profile without altering lot or front gable. Validate gable material and seams in Editor before treating as finished. No game or publish claim.

ZIP `宾大-Penn-Museum-整栋及远景山墙-未游戏验收.zip`, 9,140,180 bytes, SHA-256 `bfbd722fdabc9be057112547cdfab7b34cdbf0f5ee7ed31087c28965628a85f2`. CRC passed. Audit text only; no LFS binary upload.
