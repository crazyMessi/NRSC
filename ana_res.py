from base_val import *
import os
import open3d as o3d
import numpy as np
from cluster import Disjoint_cluster

def cal_loss(gt,x):
    # cal angle loss
    cos = np.sum(gt*x, axis=1)
    cos = np.clip(cos, -1, 1)
    angle = np.arccos(cos)
    angle = np.mean(angle)
    angle = angle * 180 / np.pi
    angle = min(angle, 180 - angle)
    return angle

def cal_inc(gt,x):
    # inc = rate of angle >90
    cos = np.sum(gt*x, axis=1)
    cos = np.clip(cos, -1, 1)
    # 找cos>0的点即可
    inc = np.sum(cos>0) / len(cos)
    inc = min(inc, 1-inc)
    return inc


# final_res = {}
final_loss = {}
final_inc = {}

import threading
lock = threading.Lock()

multi_thread = True

def get_biggest_component_idx(pcd):
    # get biggest component's points idx in pcd
    labels,_ = Disjoint_cluster(pcd.points, 0.1,20,verbose= not multi_thread)
    labelset = set(labels)
    # labelset.remove(-1)
    labelset = list(labelset)
    max_len = 0
    max_idx = 0
    for i in labelset:
        if len(labels[labels==i]) > max_len:
            max_len = len(labels[labels==i])
            max_idx = i
    return labels == max_idx



def cal_res(filename):
    try:
        # pcd = o3d.io.read_point_cloud(input_path + filename)
        # idx = get_biggest_component_idx(pcd)
        gt_normal = np.asarray(o3d.io.read_point_cloud(input_path + filename).normals)
        ori_normal = np.asarray(o3d.io.read_point_cloud(orioutpath + filename).normals)
        pca_normal = np.asarray(o3d.io.read_point_cloud(pcaoutpath + filename).normals)
        hoppe_normal = np.asarray(o3d.io.read_point_cloud(hoppeoutpath + filename).normals)
        ori_nrsc_normal = np.asarray(o3d.io.read_point_cloud(ori_nrsc_path + filename).normals)
        pca_nrsc_normal = np.asarray(o3d.io.read_point_cloud(pca_nrsc_path + filename).normals)
        hoppe_nrsc_normal = np.asarray(o3d.io.read_point_cloud(hoppe_nrsc_path + filename).normals)
    except:
        print('Error:', filename)
        return
    
    # print('len bigget component:', len(idx))
    # # 将最大连通域的点云输出到temp文件夹
    # pcd.points = o3d.utility.Vector3dVector(np.asarray(pcd.points)[idx])
    # pcd.normals = o3d.utility.Vector3dVector(np.asarray(pcd.normals)[idx])
    
    # if not os.path.exists('biggest_component/'):
    #     os.makedirs('biggest_component/')

    # o3d.io.write_point_cloud('biggest_component/'+filename, pcd)
    
    # gt_normal = gt_normal[idx]
    # ori_normal = ori_normal[idx]
    # pca_normal = pca_normal[idx]
    # # hoppe_normal = hoppe_normal[idx]
    # ori_nrsc_normal = ori_nrsc_normal[idx]
    # pca_nrsc_normal = pca_nrsc_normal[idx]
    # # hoppe_nrsc_normal = hoppe_nrsc_normal[idx]
    
    loss = {}
    loss['ori_loss'] = cal_loss(gt_normal, ori_normal)
    loss['pca_loss'] = cal_loss(gt_normal, pca_normal)
    loss['hoppe_loss'] = cal_loss(gt_normal, hoppe_normal)
    loss['ori_nrsc_loss'] = cal_loss(gt_normal, ori_nrsc_normal)
    loss['pca_nrsc_loss'] = cal_loss(gt_normal, pca_nrsc_normal)
    loss['hoppe_nrsc_loss'] = cal_loss(gt_normal, hoppe_nrsc_normal)
    
    inc = {}
    inc['ori_inc'] = cal_inc(gt_normal, ori_normal)
    inc['pca_inc'] = cal_inc(gt_normal, pca_normal)
    inc['hoppe_inc'] = cal_inc(gt_normal, hoppe_normal)
    inc['ori_nrsc_inc'] = cal_inc(gt_normal, ori_nrsc_normal)
    inc['pca_nrsc_inc'] = cal_inc(gt_normal, pca_nrsc_normal)
    inc['hoppe_nrsc_inc'] = cal_inc(gt_normal, hoppe_nrsc_normal)
    
    # 临界区
    lock.acquire()
    final_loss[filename] = loss
    final_inc[filename] = inc
    lock.release()
    print('Done:', filename)

if multi_thread:
    threads = []
    for i in range(0, len(filenamelist)):
        t = threading.Thread(target=cal_res, args=(filenamelist[i],))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
else:
    for i in range(0, len(filenamelist)):
        cal_res(filenamelist[i])
    
    
    
# save as csv
respath = 'res/scnennetv2_noisy/'
if not os.path.exists(respath):
    os.makedirs(respath)
import pandas as pd
df = pd.DataFrame(final_loss)
df = df.T
df.to_csv(respath+'loss.csv')

df = pd.DataFrame(final_inc)
df = df.T
df.to_csv(respath + 'inc.csv')



    
    
    
    