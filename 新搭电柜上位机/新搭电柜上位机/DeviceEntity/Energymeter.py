from socket import socket
from enum import Enum
import tkinter as tk

from Config.SocketLock import socketLock
from DeviceEntity.AbstractDevice.EnergyMeterImpl import EnergyMeterType, EnergyMeterImpl
from Utils.TimerUtil import TimerUtil


class EnergyMeterState(Enum):
    Off = 0
    On = 1


class EnergyMeter(EnergyMeterImpl):
    def __init__(self, _type: EnergyMeterType, addr: int):
        # 名称
        self._branch = None
        self.type = _type
        # 地址码
        self.addr = addr
        # 所在支路

        # 数据
        # 控件变量
        self.stateValueStringVar = tk.StringVar(value="开")
        self.measureVoltValStringVar = tk.DoubleVar(value=0)  # 量测电压
        self.measureElecValStringVar = tk.DoubleVar(value=0)  # 量测电流
        self.measureActivePowerValStringVar = tk.DoubleVar(value=0)  # 有功功率

        self.EnergyMeterType = EnergyMeterType.judgeEnergyMeterType(self.type)

    def queryInfo(self, interval, tcp_socket: socket):
        """
        查询电表信息,*args, **kwargs输入函数元组
        :return:
        """
        t = TimerUtil(interval, self.__queryInfoCmd, (tcp_socket,))
        t.timer_start()

    def __queryInfoCmd(self, tcp_socket: socket):
        """
        查询数据 赋给measureVoltVal、measureElecVal、activePowerVal
        :return:
        """
        # 加锁的有效性待验证
        with socketLock:
            print(self.__str__() + "正在占用socket对象")
            # TODO 自己改发送数据，每个类型设备写死就行
            message = self._buildCmd(int.to_bytes(self.addr, byteorder="big", length=1), b'\x03',
                                     self.EnergyMeterType.getVoltage())
            print(tcp_socket)
            tcp_socket.send(message)
            # 尝试接收数据
            data = tcp_socket.recv(1024)
            if data:
                print("Received:", self._parseCmd(data))
                voltage = b''.join(self._parseCmd(data)[6:7])
                voltage = int.from_bytes(voltage,'big')
                
            message = self._buildCmd(int.to_bytes(self.addr, byteorder="big", length=1), b'\x03',
                                     self.EnergyMeterType.getCurrent())
            print(tcp_socket)
            tcp_socket.send(message)
            # 尝试接收数据
            data = tcp_socket.recv(1024)
            if data:
                print("Received:", self._parseCmd(data))
                current = b''.join(self._parseCmd(data)[6:7])
                current = int.from_bytes(current,'big')

            message = self._buildCmd(int.to_bytes(self.addr, byteorder="big", length=1), b'\x03',
                                     self.EnergyMeterType.getCurrent())
            print(tcp_socket)
            tcp_socket.send(message)
            # 尝试接收数据
            data = tcp_socket.recv(1024)
            if data:
                print("Received:", self._parseCmd(data))
                Power = b''.join(self._parseCmd(data)[6:7])
                Power = int.from_bytes(Power,'big')

            # 更新显示
            self.measureVoltValStringVar.set(voltage/10)
            self.measureElecValStringVar.set(current)
            self.measureActivePowerValStringVar.set(Power)

        self._branch.ruleDetectAndBehave()

    def bindBranch(self, branch):
        self._branch = branch

    def __str__(self):
        return "EnergyMeter " + self.type.__str__() + " " + str(self.addr)
