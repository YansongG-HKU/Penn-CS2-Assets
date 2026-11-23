# Franklin Field: offline 30×20 lot candidate

From the 2026-11-22 three-LOD material intake, moved stadium geometry +13.0815 m on X, Y/Z and rotation unchanged. Local-to-new coordinate for any old props or path markers is (x + 13.0815, y, z). At nominal 8 m grid, 30×20 uses 600 versus 660 cells (33×20), with verified clearances W/E/S/N 5.28/5.28/4.96/6.91 m. Prefer this to a tight 29×19. Do not mix this model with unadjusted marker positions.

Blender 4.3.2 readback: 16,048 / 9,142 / 4,018 triangles, ordered UVs equal, translation residual <3 µm, max world normal-vector delta 0.000141. BaseColor/Normal paths of all three exports resolved within the new asset directory. Textures and settings identical byte for byte. No game navigation, collision, editor grid, dynamic rendering or saved-game testing performed.

Independent ZIP SHA-256 `01ba528b180ee02b87d44c6d8a6ee4a5dc88c82231cedebc52cab58edab7443e`; 1,087,214 bytes; members verified. Select `FranklinField/` as source in an isolated test project. No binaries uploaded to this branch, no merge or publication.
