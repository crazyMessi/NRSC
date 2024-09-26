import open3d as o3d
import os

input_path = 'D:\WorkData\ipsr_explore\input\scenenet_v2_taugh_noisy_full/'
output_path = 'D:/WorkData/NRSC/output/scenenet_v2_taugh_noisy_full/'
if not os.path.exists(output_path):
    os.makedirs(output_path)

filenamelist = os.listdir(input_path)
filenamelist = [file for file in filenamelist if file.endswith('.ply')]

filelist = []
for file in filenamelist:
    filelist.append(os.path.join(input_path, file))
# 输出pcd文件为ply,包含点云坐标和法向量
def write_xyznxnynz(pcd,filename):
    xyz = pcd.points
    nxnynz = pcd.normals
    # 输出ply格式文件
    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex %d\n" % len(xyz))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        f.write("property float nx\n")
        f.write("property float ny\n")
        f.write("property float nz\n")
        f.write("end_header\n")
        for i in range(len(xyz)):
            f.write("%f %f %f %f %f %f\n" % (xyz[i][0], xyz[i][1], xyz[i][2], nxnynz[i][0], nxnynz[i][1], nxnynz[i][2]))
    print('Done:', filename)
    
pcaoutpath = output_path+'\\'+'pca'
hoppeoutpath = output_path+'\\'+'hoppe'
if not os.path.exists(output_path):
    os.makedirs(output_path)

ori_nrsc_path = output_path + '/ori_nrsc/'
if not os.path.exists(ori_nrsc_path):
    os.makedirs(ori_nrsc_path)

pca_nrsc_path = output_path + '/pca_nrsc/'
if not os.path.exists(pca_nrsc_path):
    os.makedirs(pca_nrsc_path)
hoppe_nrsc_path = output_path + '/hoppe_nrsc/'
if not os.path.exists(hoppe_nrsc_path):
    os.makedirs(hoppe_nrsc_path)

exe_path = "D:/Documents/zhudoongli/CG/project/NormalEstimation/NRSC/NRSC-OP-EXE/normal_orientation_propagation_for_NRSC.exe"

pcaoutpath = output_path+'\\'+'pca/'
hoppeoutpath = output_path+'\\'+'hoppe/'
orioutpath = output_path+'\\'+'ori/'
if not os.path.exists(orioutpath):
    os.makedirs(orioutpath)
if not os.path.exists(pcaoutpath):
    os.makedirs(pcaoutpath)
if not os.path.exists(hoppeoutpath):
    os.makedirs(hoppeoutpath)
    
