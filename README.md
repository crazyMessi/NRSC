# LzdScript

base_val: 放一些通用的变量。

prepare.py: 得到ori、pca的结果。 ori是为了查看flip在gt上的准确率

hoppe.py:得到hoppe的结果。hoppe一般比较慢

run_nrsc.py:得到nrsc分别在ori pca和hoppe上的结果





# NRSC_OP

This is the executable file of orientation propagation module for generating consistent normal orientation on an individual connected region.
How to run this exe program:

1. copy a connected region (point cloud, e.g. SVS1_Root.ply) into the NRSC-OP-EXE fold;
2. run NRSC-OP in the current path with following command: "normal_orienation_propagation_for_NRSC.exe --in SVS1_Root.ply --out SVS1_Root_OP.ply";
3. the output SVS1_Root_OP.ply is the result file.
