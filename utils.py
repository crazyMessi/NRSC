import numpy as np

def calculate_angle(a, b):
    return np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


class PointNormalMetric:
    def __init__(self, op, gt, permit_nd = True):
        self.total_count = len(op)
        self.angle15_count = 0
        self.angle30_count = 0
        self.angle45_count = 0
        self.angle60_count = 0
        self.angle90_count = 0
        self.avg_loss = 0
        self.avg_nd_loss = 0
        
        gt = np.array(gt)
        op = np.array(op)
        gt_normals = gt[:, 1]
        op_normals = op[:, 1]
        gt_points = gt[:, 0]
        op_points = op[:, 0]
        
        dist = np.sum(op_points - gt_points)
        inner_product = np.sum(gt_normals * op_normals, axis=1)
        inner_product = np.clip(inner_product, -1, 1)
        angle = np.arccos(inner_product) * 180 / np.pi
        
        self.total_count = len(op)
        self.avg_loss = np.mean(angle)
        self.avg_nd_loss = min(self.avg_loss, 180 - self.avg_loss) 
        self.angle90_rate = float(np.sum(angle > 90))/self.total_count
        
        if dist > 0.15:
            print("Warning: distance is too large")
    
    
    def print(self):
        print(f"total_count: {self.total_count}")
        print(f"avg_loss: {self.avg_loss}")
        print(f"avg_nd_loss: {self.avg_nd_loss}")
        print(f"angle90_rate: {self.angle90_rate}")