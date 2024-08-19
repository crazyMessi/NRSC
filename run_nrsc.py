from base_val import *

ori_idx = 0
pca_idx = 0
hoppe_idx = 0

total_num = len(filelist) * 3

while ori_idx < len(filelist) or pca_idx < len(filelist) or hoppe_idx < len(filelist):
    pca_path = pcaoutpath+'\\'+filenamelist[pca_idx]
    hoppe_path = hoppeoutpath+'\\'+filenamelist[hoppe_idx]
    
    if ori_idx < len(filelist):
        ori_path = orioutpath + '\\' + filenamelist[ori_idx]
        if  os.path.exists(ori_path):        
            cmd = exe_path+' --in '+ori_path+' --out '+ ori_nrsc_path + filenamelist[ori_idx]
            print(cmd)
            os.system(cmd)
            ori_idx += 1

    if pca_idx < len(filelist):
        pca_path = pcaoutpath+'\\'+filenamelist[pca_idx]
        if os.path.exists(pca_path):        
            cmd = exe_path+' --in '+pca_path+' --out '+ pca_nrsc_path + filenamelist[pca_idx]
            print(cmd)
            os.system(cmd)
            pca_idx += 1
    
    if hoppe_idx < len(filelist):
        hoppe_path = hoppeoutpath+'\\'+filenamelist[hoppe_idx]
        if os.path.exists(hoppe_path):        
            cmd = exe_path+' --in '+hoppe_path+' --out '+ hoppe_nrsc_path + filenamelist[hoppe_idx]
            print(cmd)
            os.system(cmd)
            hoppe_idx += 1
