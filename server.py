import socket
import numpy as np
import json
from pathlib import Path


# 设置服务器的IP和端口
HOST = '0.0.0.0'  # 监听所有IP地址
PORT = 10002     # 监听的端口号
REQUEST_BUFFER_SIZE = 1000 # 接收缓冲区大小，单位为字节
max_thread = 50 # 同时处理的最大线程数

import estimator

def pca_nrsc(xyz_data, function_config):
    # 估计法向量
    xyz, normals = estimator.pca_and_nrsc(np.array(xyz_data), function_config)
    return np.concatenate([xyz, normals], axis=1)

def hoppe_nrsc(xyz_data, function_config):
    # 估计法向量
    xyz, normals = estimator.hoppe_and_nrsc(np.array(xyz_data), function_config)
    return np.concatenate([xyz, normals], axis=1)

def handle_client(conn, addr):
    with conn:
        print(f"Connected by {addr}")
        try:
            # 接收数据
            req = conn.recv(REQUEST_BUFFER_SIZE)
            req = json.loads(req.decode())
            print(req)
            data_buffer_size = req['data_size'] * 24
            repo = json.dumps({"status": "OK"})
            conn.sendall(repo.encode())
            data_recv = 0
            data = b''
            while data_recv < data_buffer_size:
                tdata = conn.recv(data_buffer_size - data_recv)
                data_recv += len(tdata)
                if not tdata:
                    break
                print(f"Received {len(tdata)} bytes")
                data += tdata
            if not data:
                return
            print(f"Received {len(data)} bytes in total")
            if len(data) != data_buffer_size:
                print(f"Data size mismatch. Expected {data_buffer_size} bytes, but received {len(data)} bytes.")
                assert False
            # 假设接收到的数据是二进制形式的XYZ浮点数数组
            xyz_data = np.frombuffer(data, dtype=np.float64).reshape(-1, 3)
            
            # 计算法向量
            if req['function_name'] == 'PCA_NRSC':
                result = pca_nrsc(xyz_data, req['function_config'])
            elif req['function_name'] == 'HOPPE_NRSC':
                result = hoppe_nrsc(xyz_data, req['function_config'])
            else:
                assert False, f"Unknown method: {req['function_config']}"
            
            
            # 返回结果
            conn.sendall(result.astype(np.float64).tobytes())
        except Exception as e:
            print(f"Error: {e} 本块被放弃\n")
            conn.sendall(json.dumps({"status": "ERROR"}).encode())
        finally:
            conn.close()
    
    
import threading
import time

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")        
        while True:
            conn, addr = s.accept()
            while threading.active_count() > max_thread:
                time.sleep(1)
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
            print(f"Active threads: {threading.active_count()}")
            
        
if __name__ == "__main__":
    main()
