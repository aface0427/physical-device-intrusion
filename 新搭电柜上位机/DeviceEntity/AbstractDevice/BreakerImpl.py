from typing import List

from DeviceEntity.AbstractDevice.InstructionInterface import Instruction


# TODO 这里需要实现累积校验，这里我不清楚累积原理，不敢乱写
def crc(segment: bytes) -> bytes:
    check = 0
    cmd = segment[6:7]  # 提取固定包头
    check += int.from_bytes(cmd,'big')
    cmd = segment[7:8]
    check += int.from_bytes(cmd,'big')
    cmd = segment[8:9]
    check += int.from_bytes(cmd,'big')
    cmd = segment[9:10]
    check += int.from_bytes(cmd,'big')
    cmd = segment[10:11]
    check += int.from_bytes(cmd,'big')
    cmd = segment[11:12]
    check += int.from_bytes(cmd,'big')
    cmd = segment[12:13]
    check += int.from_bytes(cmd,'big')
    return check.to_bytes(1,'big')


class BreakerImpl(Instruction):
    __data = b''  # TODO　写寄存器信息（非强制）

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

        segment = cmd[6:8]  # 提取数据段
        segments.append(segment)

        # segment = cmd[7:9]  # 提取数据段
        # segments.append(segment)

        # segment = cmd[8:8]  # 提取功能码
        # segments.append(segment)

        # segment = cmd[9:9]  # 提取数据长度
        # segments.append(segment)

        # segment = cmd[10:10]  # 提取20h
        # segments.append(segment)

        # segment = cmd[8:8 + validLen - 4]  # 提取数据段
        # segments.append(segment)

        # segment = cmd[8 + validLen - 4:8 + validLen - 2]  # TODO 校验段是否是两位
        # segments.append(segment)

        return segments

    def _buildCmd(self, addrCode: bytes, funcCode: bytes, data: bytes, controlCode: bytes) -> bytes:
        segment = b''
        segment += b'\x00\x01\x00\x00\x00\x08\x68'
        # validLen = len(addrCode) + len(funcCode) + len(data)
        # segment += validLen.to_bytes(2, byteorder='big')
        segment += addrCode
        segment += funcCode
        segment += b'\x03\x20'
        segment += addrCode
        segment += controlCode
        segment += data
        segment += crc(segment)
        return segment

    @classmethod
    def getData(cls):
        return cls.__data
