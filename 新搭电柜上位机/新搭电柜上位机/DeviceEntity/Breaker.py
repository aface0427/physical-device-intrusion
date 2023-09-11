import socket

from Config.SocketLock import socketLock
from DeviceEntity.AbstractDevice.BreakerImpl import BreakerImpl


class Breaker(BreakerImpl):
    def __init__(self, addr: int):
        # 地址码
        self.__branch = None
        self.addr = addr

    # TODO 设置开断,可参考 DeviceEntity/Energymeter.py中的__queryInfoCmd方法
    def open(self, tcp_socket:socket.socket):
        with socketLock:
            print(self.__str__() + "正在占用socket对象")
            # TODO 自己改发送数据，每个类型设备写死就行
            message = self._buildCmd(int.to_bytes(self.addr, byteorder="big", length=1), b'\x02',
                                     Breaker.getData(), b'\x01')
            print(tcp_socket)
            tcp_socket.send(message)
            # 尝试接收数据
            data = tcp_socket.recv(1024)
            if data:
                print("Received:", self._parseCmd(data))

    def close(self, tcp_socket:socket.socket):
        with socketLock:
            print(self.__str__() + "正在占用socket对象")
            # TODO 自己改发送数据，每个类型设备写死就行
            message = self._buildCmd(int.to_bytes(self.addr, byteorder="big", length=1), b'\x02',
                                     Breaker.getData(), b'\x00')
            print(tcp_socket)
            tcp_socket.send(message)
            # 尝试接收数据
            data = tcp_socket.recv(1024)
            if data:
                print("Received:", self._parseCmd(data))

    def bindBranch(self, branch):
        self.__branch = branch
