#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 19:29
# @File    : fsad.py
# @Description : 主机作为服务器实现蓝牙连接通信

# 模块安装需要执行
# >> sudo apt-get install libbluetooth-dev
# >> sudo pip3 install pybluez

import time
import ctypes
import bluetooth
from bluetooth import *
import uuid


def get_mac_address():
    """
    获得本机MAC地址
    :return: MAC地址
    """
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


class BluetoothConnection:
    '''
    蓝牙连接类，主机作为服务器
    '''

    def __init__(self):
        # 是否找到目标蓝牙设备
        self.find = False
        # 附近蓝牙设备列表
        self.nearby_devices = []
        # 通信连接
        self.server_sock = None
        # 存储数据
        self.data = []
        # 取数据标志
        self.data_flag = 0

    def find_nearby_devices(self):
        """
        查找附近的蓝牙设备
        :return: 找到的蓝牙设备列表
        """
        print("Detecting nearby bluetooth……")
        try:
            devs = discover_devices(lookup_names=True)
            # 重复检测
            i = 0
            i_max = 3  # 重复检测次数
            while len(devs) == 0 and i < i_max:
                devs = discover_devices(lookup_names=True)
                if len(devs) > 0:
                    break
                time.sleep(2)
                i = i + 1
            # 输出蓝牙设备列表
            for (addr, name) in devs:
                if addr not in devs:
                    print("[*]Device name:" + str(name))
                    print("[+]Device MAC address：" + str(addr))
            self.nearby_devices = devs
        except Exception as e:
            print("Can not detect bluetooth！")

    def find_target_device(self, target_name=None, target_address=None):
        """
        根据蓝牙名称或者MAC地址查找蓝牙
        :param target_name:连接目标名称
        :param target_address: 连接目标MAC地址
        :return: true成功 false失败
        """
        self.find_nearby_devices()
        if len(self.nearby_devices) != 0:
            for (addr, name) in self.nearby_devices:
                if target_name == name or target_address == addr:
                    print("Find the device with name: {0}，MAC addreess: {1}\n".format(name, addr))
                    self.find = True
                    return addr
            print("Can not detect the target device, please open its bluetooth!")
        else:
            print("Can not detect the nearby device！")
        return None

    def server_bind(self, port):
        """
        服务器绑定socket通信端口
        :return:
        """
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(('', port))  # 绑定地址和端口
        self.server_sock.listen(1)  # 绑定监听，最大挂起连接数为1






def kill_PID(port):
    """
    杀死指定PID进程
    :param port:
    :return:
    """
    r = os.popen("netstat -ano | findstr " + port)
    text = r.read()
    arr = text.split("\n")
    print("进程个数为：", len(arr) - 1)
    text0 = arr[0]
    arr2 = text0.split(" ")
    if len(arr2) > 1:
        pid = arr2[len(arr2) - 1]
        os.system("taskkill /PID " + pid + " /T /F")
        print(pid)
    r.close()

if __name__ == '__main__':
    target_name = "raspberrypi"
    # target_name = "DESKTOP-6OIPRKI"
    bt = BluetoothConnection()

    bt.server_bind(14)
