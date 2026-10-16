import zipfile,glob,os,sys
bd,A,short=sys.argv[1:4]; os.chdir(bd); Z='/workspace/penn_campus/zips/'
def z(out,files):
  with zipfile.ZipFile(Z+out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
    for p in files: f.write(p,A+'/'+p)
  print(out,round(os.path.getsize(Z+out)/2**20,2),'MB',len(files))
z(short+'_A_models.zip',sorted(glob.glob('NA_*.fbx'))+sorted(glob.glob('split_fbx/*.fbx'))+['settings.json','SOURCES.txt'])
z(short+'_B_textures.zip',sorted(glob.glob('NA_*.png')))
z(short+'_C_blend.zip',[A+'.blend','SOURCES.txt'])
