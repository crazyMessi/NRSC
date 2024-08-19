from base_val import *
import pymeshlab as ml

for i in range(len(filelist)):
    print(i, filelist[i])
    pcd = o3d.io.read_point_cloud(filelist[i])
    ms = ml.MeshSet()
    ms.load_new_mesh(filelist[i])
    ms.compute_normal_for_point_clouds(smoothiter = 0)
    normals = ms.current_mesh().vertex_normal_matrix() 
    # 如果没有法向量，先计算法向量
    if not pcd.has_normals():
        pcd.normals = o3d.utility.Vector3dVector(normals)
    write_xyznxnynz(pcd, orioutpath+'\\'+filenamelist[i])
    pcd.normals = o3d.utility.Vector3dVector(normals)
    write_xyznxnynz(pcd, pcaoutpath+'\\'+filenamelist[i])
    # pcd.orient_normals_consistent_tangent_plane(10)
    # write_xyznxnynz(pcd, hoppeoutpath+'\\'+filenamelist[i])
    print('Done:', i)
print('All Done')