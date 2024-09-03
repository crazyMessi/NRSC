'''
输入xyz
对xyz进行法向量估计
将xyz保存为名称唯一的ply文件
调用normal_orienation_propagation_for_NRSC.exe --input_file=name.ply --output_file=name.ply 
读取name.ply文件,返回xyz和normal
'''
import numpy as np
import os
import open3d as o3d
import pymeshlab as ml
import time
from base_val import write_xyznxnynz

output_path = 'temp'
if not os.path.exists(output_path):
    os.makedirs(output_path)

#线程锁
import threading

class UniqueName:
    def __init__(self):
        self.namelist = []
        for i in range(100000):
            self.namelist.append(str(i))
        self.lock = threading.Lock()
    def get_name(self):
        self.lock.acquire()
        name = self.namelist.pop(0)
        self.lock.release()
        return name
    
    def return_name(self,name):
        self.lock.acquire()
        self.namelist.append(name)
        self.lock.release()
name_getter = UniqueName()



def pca_and_nrsc(xyz,conf):
    '''
    xyz: 3xN numpy array
    conf: configuration
    '''
    m = ml.Mesh(xyz)
    ms = ml.MeshSet()
    ms.add_mesh(m)
    ms.compute_normal_for_point_clouds(smoothiter = 0)
    normals = ms.current_mesh().vertex_normal_matrix()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.normals = o3d.utility.Vector3dVector(normals)
    
    name1 = name_getter.get_name()
    name2 = name_getter.get_name()
    ply_path1 = os.path.join(output_path,name1+'.ply')
    ply_path2 = os.path.join(output_path,name2+'.ply')

    write_xyznxnynz(pcd,ply_path1)

    
    cmd = f'cd NRSC-OP-EXE && normal_orientation_propagation_for_NRSC.exe --in ../{ply_path1} --out ../{ply_path2}'
    os.system(cmd)
    pcd = o3d.io.read_point_cloud(ply_path2)
    xyz = np.asarray(pcd.points)
    nrsc_normals = np.asarray(pcd.normals)
    # 将nrsc_normals中的非零部分替换到normals中
    mask = np.sum(nrsc_normals**2,axis=1)>1e-6
    normals[mask] = nrsc_normals[mask]
    if np.sum(mask == False) > 0:
        print("nrsc zero:",np.sum(mask == False))
        # assert False
    
    times = 10
    while times > 0:
        try:
            if os.path.exists(ply_path1):
                os.remove(ply_path1)
            if os.path.exists(ply_path2):
                os.remove(ply_path2)
            break
        except:
            times -= 1
            time.sleep(0.1)
    if times == 0:
        print("remove failed")

    name_getter.return_name(name1)
    name_getter.return_name(name2)
    return xyz,normals
    
def hoppe_and_nrsc(xyz,conf):
    '''
    xyz: 3xN numpy array
    conf: configuration
    '''
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=10))
    pcd.orient_normals_consistent_tangent_plane(10)
    xyz = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    name1 = name_getter.get_name()
    ply_path1 = os.path.join(output_path,name1+'.ply')
    write_xyznxnynz(pcd,ply_path1)
    name2 = name_getter.get_name()

    ply_path2 = os.path.join(output_path,name2+'.ply')
    cmd = f'cd NRSC-OP-EXE && normal_orientation_propagation_for_NRSC.exe --in ../{ply_path1} --out ../{ply_path2}'
    
    os.system(cmd)
    pcd = o3d.io.read_point_cloud(ply_path2)
    xyz = np.asarray(pcd.points)
    nrsc_normals = np.asarray(pcd.normals)
    # 将nrsc_normals中的非零部分替换到normals中
    mask = np.sum(nrsc_normals**2,axis=1)>1e-6
    normals[mask] = nrsc_normals[mask]
    if np.sum(mask == False) > 0:
        print("nrsc zero:",np.sum(mask == False))
        # assert False
    times = 10
    while times > 0:
        try:
            if os.path.exists(ply_path1):
                os.remove(ply_path1)
            if os.path.exists(ply_path2):
                os.remove(ply_path2)
            break
        except:
            times -= 1
            time.sleep(0.1)
    if times == 0:
        print("remove failed")
    name_getter.return_name(name1)
    name_getter.return_name(name2)
    return xyz,normals
