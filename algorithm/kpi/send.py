import socket

# 定义UDP套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 目标地址和端口
server_address = ('10.169.26.98', 12345)  # 替换为实际的目标地址和端口

abnormal_kpi = [2, 6, 2, 4, 6]
kpis = [[3, 8, 3, 3, 8], [4, 12, 4, 8, 16], [0, 20, 8, 16, 16]]
# 构建发送数据
abnormal_kpi_str = 'abnormal:' + ' '.join(str(x) for x in abnormal_kpi) + "\n"
sock.sendto(abnormal_kpi_str.encode('utf-8'), server_address)
for i, kpi in enumerate(kpis):
    kpi_str = f"kpi_{i + 1}: " + ' '.join(str(x) for x in kpi)
    sent = sock.sendto(kpi_str.encode('utf-8'), server_address)
# 发送数据

sock.sendto("finished".encode(), server_address)

# 关闭套接字
sock.close()
