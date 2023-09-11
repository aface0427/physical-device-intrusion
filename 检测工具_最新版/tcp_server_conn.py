#-*- coding:utf-8 -*-

import socket
import threading


class TcpConnection:
    '''
    TCP/IP连接类，主机作为服务器
    '''

    def __init__(self):
        # 通信连接
        self.server_sock = None
        # 存储数据
        self.data = []
        # 取数据标志
        self.data_flag = 0

    def server_bind(self, ADDR):
        """
        服务器绑定socket通信端口
        :return:
        """
        self.server_sock = socket.socket()
        # self.server_sock.settimeout(5.0)  # 设定超时时间后，socket其实内部变成了非阻塞，但有一个超时时间
        self.server_sock.bind(ADDR)  # 绑定地址端口
        self.server_sock.listen(2)  # 开启监听
        # print("build connect when new TCP comes")



# def handle(connected_sock):
#     while True:
#         data = connected_sock.recv(BUFSIZE)     # 接收client传来的数据
#         if len(data) >0:
#             print("receive:")
#             print(data)
#         else:
#             print("close the connected socket and terminate sub thread")
#             connected_sock.close()
#             break


# BUFSIZE = 1024
# HOST = '192.168.50.144'
# PORT = 12356
# ADDR = (HOST, PORT)
# sub_threads = []
#
# listen_sock = socket.socket()
# listen_sock.settimeout(5.0) # 设定超时时间后，socket其实内部变成了非阻塞，但有一个超时时间
# listen_sock.bind(ADDR)  # 绑定地址端口
# listen_sock.listen(2)   # 开启监听
# print("build connect when new TCP comes")

# while True:
#     try:
#         connected_sock, client_addr = listen_sock.accept()  # 阻塞等待连接
#     except socket.timeout:
#         length = len(sub_threads)
#         while length:
#             sub = sub_threads.pop(0)
#             sub_id = sub.ident  # 进程ID
#             sub.join(0.1)   # 等待线程结束，0.1秒
#             if sub.is_alive():
#                 sub_threads.append(sub)
#             else:
#                 print("killed sub thread ")
#                 print(sub_id)
#             length -= 1
#     else:
#         t = threading.Thread(target=handle, name='sub thread', args=(connected_sock,))
#         # 它继承了listen_socket的阻塞/非阻塞特性，因为listen_socket是非阻塞的，所以它也是非阻塞的
#         # 要让他变为阻塞，所以要调用setblocking
#         connected_sock.setblocking(1)
#         t.start()
#         sub_threads.append(t)