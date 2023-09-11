import socket


class GateWay:
    def __init__(self, ip: str, port: int, tcp_socket: socket.socket = None):
        # 单个连接包括ip,端口和socket
        self.ip = ip  # 本机ip
        self.port = port

        # self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 不允许修改
        self.socket_ = tcp_socket

    def disConnect(self):
        print("socket对象已清除")
        if self.socket_:
            self.socket_.shutdown(2)
            self.socket_.close()
            del self.socket_
            self.socket_ = None
            return True
        return False

    def getSocket(self) -> socket.socket:
        return self.socket_

    def __str__(self):
        return "GateWay " + self.ip + " " + str(self.port)
