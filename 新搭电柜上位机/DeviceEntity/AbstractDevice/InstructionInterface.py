from abc import abstractmethod, ABCMeta

from typing import List


class Instruction(object):
    """
    解析接口，断路器和电表不一样
    """
    __metaclass__ = ABCMeta  # 指定这是一个抽象类

    @abstractmethod  # 抽象方法
    def _parseCmd(self, cmd: bytes) -> List[bytes]:
        """
        不同有不同的解析方式
        :return:
        """
        pass

    @abstractmethod  # 抽象方法
    def _buildCmd(self, addrCode: bytes, funcCode: bytes, data: bytes) -> bytes:
        """
        构建
        """
        pass
