from base_val import *

ori_idx = 0
pca_idx = 0
hoppe_idx = 0

total_num = len(filelist) * 3

def run_nrsc(input_path, output_path, exe_path):
    if os.path.exists(output_path):
        import open3d as o3d
        try:
            pcd = o3d.io.read_point_cloud(output_path)
            if len(pcd.points) > 0:
                print('Already exists:', output_path)
                return
        except:
            print('Error:', output_path)
            print('Try to remove it')
            os.remove(output_path)
            pass
        print('Already exists:', output_path)
        return
    cmd = exe_path+' --in '+input_path+' --out '+ output_path
    print(cmd)
    os.system(cmd)


while ori_idx < len(filelist) or pca_idx < len(filelist) or hoppe_idx < len(filelist):
    pca_path = pcaoutpath+'\\'+filenamelist[pca_idx]
    hoppe_path = hoppeoutpath+'\\'+filenamelist[hoppe_idx]
    
    if ori_idx < len(filelist):
        ori_path = orioutpath + '\\' + filenamelist[ori_idx]
        if  os.path.exists(ori_path):        
            run_nrsc(ori_path, ori_nrsc_path + filenamelist[ori_idx], exe_path)
            ori_idx += 1

    if pca_idx < len(filelist):
        pca_path = pcaoutpath+'\\'+filenamelist[pca_idx]
        if os.path.exists(pca_path):        
            run_nrsc(pca_path, pca_nrsc_path + filenamelist[pca_idx], exe_path)
            pca_idx += 1
    
    if hoppe_idx < len(filelist):
        hoppe_path = hoppeoutpath+'\\'+filenamelist[hoppe_idx]
        if os.path.exists(hoppe_path):        
            run_nrsc(hoppe_path, hoppe_nrsc_path + filenamelist[hoppe_idx], exe_path)
            hoppe_idx += 1