"""
基于施耐德串口服务器的socket测试
主机作为TCP-client
"""

import socket
import sys
import time

# 选择主机ip和端口
port = 8000
ip = "10.1.1.10"

# 创建socket
try:
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    sys.exit()

# 链接服务器
try:
    server_addr = (ip, port)
    tcp_socket.connect(server_addr)
except Exception as e:
    print(e)
    sys.exit()
print("Socket successfully connected to port " + str(port) + " on ip " + ip)


i = 0
print("正在监听数据……")
buff_size=20 #缓冲区大小
# # 监听数据
# while (True):
#     data = tcp_socket.recv(buff_size)
#     print(str(data.hex()))
#     if (data==""):
#         break

for i in range(30):
    tcp_socket.send(b'\x01\x03\x01\x00\x00\x01\x85\xf6')
    time.sleep(0.1)
    data=tcp_socket.recv((buff_size))
    print(str(data.hex()))
# 4. 关闭套接字
tcp_socket.close()
