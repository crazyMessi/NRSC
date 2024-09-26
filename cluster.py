import open3d as o3d
import numpy as np

'''
对点云进行聚类
Disjoint_cluster: 并查集聚类

visualize_clusters: 可视化聚类
'''

'''
并查集聚类
输入: 点云, 聚类距离阈值, KNN搜索邻域大小
输出: 聚类标签, 聚类列表
'''
def Disjoint_cluster(xyz, distance_threshold=0.02, k_search=20, verbose=True):
    xyz = np.array(xyz)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    # 建立搜索树
    tree = o3d.geometry.KDTreeFlann(pcd)
    labels = np.arange(len(pcd.points))
    def find(i):
        if labels[i] != i:
            labels[i] = find(labels[i])
        return labels[i]

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            labels[root_i] = root_j
    knn_time = 0
    tpercent = 0
    # 遍历所有点
    for i in range(len(pcd.points)):
        if find(i) != i:
            continue
        # 查找邻域内的点
        [k, idx, _] = tree.search_radius_vector_3d(pcd.points[i], distance_threshold)
        knn_time += 1
        root_i = find(i)
        for j in idx[0:k_search]:
            union(j,root_i)
        percent = float(i) / len(pcd.points) * 100        
        if verbose and percent - tpercent > 1:
            print('\rProgress: {:.2f}%'.format(percent), end='')
            tpercent = percent
    if verbose:    
        print('\rProgress: 100%')
        print('KNN search times:',knn_time) #176315 179591
    
    # 合并聚类
    clusters = {}
    for i in range(len(pcd.points)):
        root = find(i)
        if root in clusters:
            clusters[root].append(i)
        else:
            clusters[root] = [i]
    rclusters = []
    for cluster in clusters.values():
        rclusters.append(cluster)
    return labels, rclusters

import matplotlib.pyplot as plt


# def spectral_cluster(pcd):
#     adj = graph.pc2graph(np.asarray(pcd.points), k=20, r=0.1)
#     D = np.diag(np.sum(adj, axis=1))
#     L = D - adj
#     eigvals, eigvecs = np.linalg.eig(L)
#     idx = np.argsort(eigvals)
#     k = 3
#     U = eigvecs[:, idx[1:k+1]]
#     U = U / np.linalg.norm(U, axis=1, keepdims=True)
#     kmeans = KMeans(n_clusters=k, random_state=0).fit(U)
#     labels = kmeans.labels_
#     clusters = []
#     for i in range(k):
#         cluster = np.where(labels == i)[0]
#         clusters.append(cluster)
#     return clusters


def visualize_labels(pcd,labels):
    labels = np.array(labels, dtype=int)
    labels_set = set(labels)
    label2color = {label: np.random.rand(3) for label in labels_set}
    colors = np.array([label2color[label] for label in labels])
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([pcd])
    return pcd

# 可视化聚类
def visualize_clusters(pcd,clusters):
    # 随机生成颜色
    colors = np.random.rand(len(clusters), 3)
    # 创建一个空点云
    pcd_cluster = o3d.geometry.PointCloud()
    # 遍历所有聚类
    for i, cluster in enumerate(clusters):
        # 为每个聚类赋予不同的颜色
        color = colors[i, :3]
        for j in cluster:
            pcd_cluster.points.append(pcd.points[j])
            pcd_cluster.colors.append(color) 
            pcd_cluster.normals.append(pcd.normals[j])
    # 可视化
    o3d.visualization.draw_geometries([pcd_cluster])
    return pcd_cluster

# save to path_base1.ply, path_base2.ply, ..., sorted by size
def save_cluster(pad,clusters,path_base):
    clusters = sorted(clusters, key=lambda x: len(x), reverse=True)
    for i, cluster in enumerate(clusters):
        pcd_cluster = o3d.geometry.PointCloud()
        for j in cluster:
            pcd_cluster.points.append(pad.points[j])
        o3d.io.write_point_cloud(path_base+str(i)+'.ply', pcd_cluster)
       