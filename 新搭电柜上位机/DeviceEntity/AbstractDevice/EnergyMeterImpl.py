from enum import Enum
from typing import List

from DeviceEntity.AbstractDevice.InstructionInterface import Instruction


class EnergyMeterType(Enum):
    EPM5500 = "EPM5500"
    PAC4200 = "PAC4200"
    PM800 = "PM800"

    @staticmethod
    def judgeEnergyMeterType(energyMeterType):
        if energyMeterType == EnergyMeterType.PM800.value:
            return PM800Impl
        elif energyMeterType == EnergyMeterType.PAC4200.value:
            return PAC4200Impl
        elif energyMeterType == EnergyMeterType.EPM5500.value:
            return EPM5500Impl
        else:
            return None


class EnergyMeterImpl(Instruction):
    def _parseCmd(self, cmd: bytes) -> List[bytes]:
        # 初始化一个空列表来存储分段后的bytes
        segments = []

        # 循环遍历bytes数据，分段
        segment = cmd[0:2]  # 提取事务符
        segments.append(segment)

        segment = cmd[2:4]  # 提取tcp协议
        segments.append(segment)

        segment = cmd[4:6]  # 提取有效位数
        validLen = int.from_bytes(segment, byteorder='big')
        segments.append(segment)

        segment = cmd[6:7]  # 提取地址吗
        segments.append(segment)

        segment = cmd[7:8]  # 提取功能吗
        segments.append(segment)

        segment = cmd[8:9]  # 提取数据长度
        segments.append(segment)

        segment = cmd[9:len(cmd)]  # 提取数据段
        segments.append(segment)

        return segments

    def _buildCmd(self, addrCode: bytes, funcCode: bytes, data: bytes) -> bytes:
        segment = b''
        segment += b'\x00\x01\x00\x00'
        validLen = len(addrCode) + len(funcCode) + len(data)
        segment += validLen.to_bytes(2, byteorder='big')
        segment += addrCode
        segment += funcCode
        segment += data
        return segment


class EPM5500Impl(EnergyMeterImpl):
    __data1 = b'\x01\x31\x00\x01'
    __data2 = b'\x01\x39\x00\x01'
    __data3 = b'\x01\x3e\x00\x01'  # TODO 静态变量，设置寄存器数据（非强制）

    @classmethod
    def getVoltage(cls):
        return cls.__data1
    @classmethod
    def getCurrent(cls):
        return cls.__data2
    @classmethod
    def getPower(cls):
        return cls.__data3


class PAC4200Impl(EnergyMeterImpl):
    __data1 = b'\x01\x31\x00\x01'
    __data2 = b'\x01\x39\x00\x01'
    __data3 = b'\x01\x3e\x00\x01'  # TODO 静态变量，设置寄存器数据（非强制）

    @classmethod
    def getVoltage(cls):
        return cls.__data1
    @classmethod
    def getCurrent(cls):
        return cls.__data2
    @classmethod
    def getPower(cls):
        return cls.__data3


class PM800Impl(EnergyMeterImpl):
    __data1 = b'\x01\x31\x00\x01'
    __data2 = b'\x01\x39\x00\x01'
    __data3 = b'\x01\x3e\x00\x01'  # TODO 静态变量，设置寄存器数据（非强制）

    @classmethod
    def getVoltage(cls):
        return cls.__data1
    @classmethod
    def getCurrent(cls):
        return cls.__data2
    @classmethod
    def getPower(cls):
        return cls.__data3
