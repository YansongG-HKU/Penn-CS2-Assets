# Penn Museum / Harrison Rotunda whole-asset baseline

Cloud Blender 4.3.2 readback against pinned main `3a7097a0ef154f454e0ce67da0b26c37c26bfed4`. Verified each LFS object's SHA-256 and size. Five non-empty FBX files (three body, two window) plus ten unchanged PNG maps and the same LOD1 sharedAssets mapping. The two legacy Gls entries were confirmed empty and excluded from the isolated trial folder, not removed from Git. Trial stem `NA_PennMuseumTrial_21x15`; geometry/normals/UV arrays unchanged, image paths local, 168×120 m lot, max height 31.00 m; body tris 5408/4376/232, zero degenerate triangles read back. CRC and expected paths passed.

Geometric LOD1/LOD2 projection IoU across facade, diagonal and side: 96.0%, 87.4%, 82.7%. The original far tier omits the central front pavilion gable and reduces the rear Rotunda roof to a near straight cone. Prioritize the gable, then the folded Rotunda roof profile; do not overlay separate survey meshes without alignment.

Baseline ZIP `宾大-Penn-Museum-整栋三档对照-未游戏验收.zip`, 9,131,854 bytes, SHA-256 `8aae2ef791d7de0144709c2d6a83160e70cca4b7dd8ac82c14b31689f4932142`. No binary uploads, Editor, game placement, dynamic LOD or pmod release in this draft.
