from base_val import *
import os
import open3d as o3d
import numpy as np

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


def cal_res(filename):
    try:
        gt_normal = np.asarray(o3d.io.read_point_cloud(input_path + filename).normals)
        ori_normal = np.asarray(o3d.io.read_point_cloud(orioutpath + filename).normals)
        o3d_normal = np.asarray(o3d.io.read_point_cloud(o3destoutpath + filename).normals)
        hoppe_normal = np.asarray(o3d.io.read_point_cloud(hoppeoutpath + filename).normals)
        ori_nrsc_normal = np.asarray(o3d.io.read_point_cloud(ori_nrsc_path + filename).normals)
        o3d_nrsc_normal = np.asarray(o3d.io.read_point_cloud(o3d_nrsc_path + filename).normals)
        hoppe_nrsc_normal = np.asarray(o3d.io.read_point_cloud(hoppe_nrsc_path + filename).normals)
    except:
        print('Error:', filename)
        return
    
    loss = {}
    loss['ori_loss'] = cal_loss(gt_normal, ori_normal)
    loss['o3d_loss'] = cal_loss(gt_normal, o3d_normal)
    loss['hoppe_loss'] = cal_loss(gt_normal, hoppe_normal)
    loss['ori_nrsc_loss'] = cal_loss(gt_normal, ori_nrsc_normal)
    loss['o3d_nrsc_loss'] = cal_loss(gt_normal, o3d_nrsc_normal)
    loss['hoppe_nrsc_loss'] = cal_loss(gt_normal, hoppe_nrsc_normal)
    
    inc = {}
    inc['ori_inc'] = cal_inc(gt_normal, ori_normal)
    inc['o3d_inc'] = cal_inc(gt_normal, o3d_normal)
    inc['hoppe_inc'] = cal_inc(gt_normal, hoppe_normal)
    inc['ori_nrsc_inc'] = cal_inc(gt_normal, ori_nrsc_normal)
    inc['o3d_nrsc_inc'] = cal_inc(gt_normal, o3d_nrsc_normal)
    inc['hoppe_nrsc_inc'] = cal_inc(gt_normal, hoppe_nrsc_normal)
    
    # 临界区
    lock.acquire()
    final_loss[filename] = loss
    final_inc[filename] = inc
    lock.release()
    print('Done:', filename)
    
threads = []
for i in range(0,15):
    t = threading.Thread(target=cal_res, args=(filenamelist[i],))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

threads = []
for i in range(15,30):
    t = threading.Thread(target=cal_res, args=(filenamelist[i],))
    threads.append(t)
    t.start()
for t in threads:
    t.join()

threads = []
for i in range(30,45):
    t = threading.Thread(target=cal_res, args=(filenamelist[i],))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
    
threads = []
for i in range(45,60):
    t = threading.Thread(target=cal_res, args=(filenamelist[i],))
    threads.append(t)
    t.start()

    
    
    
# save as csv
respath = 'res/ipsr_demo/'
if not os.path.exists(respath):
    os.makedirs(respath)
import pandas as pd
df = pd.DataFrame(final_loss)
df = df.T
df.to_csv(respath+'loss.csv')

df = pd.DataFrame(final_inc)
df = df.T
df.to_csv(respath + 'inc.csv')



    
    
    
    