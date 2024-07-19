from base_val import *

# 并行处理
for i in range(len(filelist)):
    ori_path = orioutpath + '\\' + filenamelist[i]
    o3d_path = o3destoutpath+'\\'+filenamelist[i]
    hoppe_path = hoppeoutpath+'\\'+filenamelist[i]
    
    cmd = exe_path+' --in '+o3d_path+' --out '+ o3d_nrsc_path + filenamelist[i]
    print(cmd)
    os.system(cmd)
    
    cmd = exe_path+' --in '+ori_path+' --out '+ ori_nrsc_path + filenamelist[i]
    print(cmd)
    os.system(cmd)
    
    cmd = exe_path+' --in '+hoppe_path+' --out '+ hoppe_nrsc_path + filenamelist[i]
    print(cmd)
    os.system(cmd)    
    print('Done:', i)