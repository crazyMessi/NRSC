from base_val import *

for i in range(len(filelist)):
    print(i, filelist[i])
    pcd = o3d.io.read_point_cloud(filelist[i])
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=10))
    pcd.orient_normals_consistent_tangent_plane(10)
    write_xyznxnynz(pcd, hoppeoutpath+'\\'+filenamelist[i])
    print('Done:', i)