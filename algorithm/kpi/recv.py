import socket
import os

# 定义UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定地址和端口
server_address = ('10.169.26.98', 12345)  # 替换为实际的地址和端口
sock.bind(server_address)

filename = "received_data.txt"
f = open(filename, "w")
while True:
    # 接收数据
    data, address = sock.recvfrom(8096)
    data = data.decode('utf-8')
    f.write(data)

# # 解析数据
# lines = data.splitlines()
# abnormal_kpi = [int(x) for x in lines[0].split()[1:]]
# kpis = []
# for line in lines[1:]:
#     kpi = [int(x) for x in line.split()[1:]]
#     kpis.append(kpi)
#
# # 将数据写入文件
# filename = "received_data.txt"
# with open(filename, "w") as f:
#     f.write(f"abnormal: {abnormal_kpi}\n")
#     for i, kpi in enumerate(kpis):
#         f.write(f"kpi_{i+1}: {kpi}\n")
#
# # 打印接收到的数据
# print(f"Received from {address}:")
# print(f"abnormal: {abnormal_kpi}")
# for i, kpi in enumerate(kpis):
#     print(f"kpi_{i+1}: {kpi}")

# 关闭套接字
sock.close()
