#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 19:49
# @File    : modbus_comm.py
# @Description : 封装串口发送modbus协议
import datetime
import threading
import time

import crcmod
import serial
import serial.tools.list_ports
import tkinter as tk




def Ascii2Hex(ascii):
    """
    字符串转换为16进制字节数组
    :param ascii:输入的ascii码值，可以为字符串
    :return: 返回转换成的十六进制数组
    """
    if isinstance(ascii, tuple) | isinstance(ascii, list):
        ascii = ''.join([str(i) for i in ascii])
    # ascii字符串去空格
    ascii = ascii.replace(" ", "")
    # 字符串长度
    ascii_len = len(ascii)
    hex_list = []
    check_code = 0
    for i in range(int(ascii_len / 2)):
        # 将字符串每两个数组组成一个16进制数
        ascii_actual = int(ascii[2 * i], 16) * 16 + int(ascii[2 * i + 1], 16)
        hex_list.append(ascii_actual)

    hex1 = bytes(hex_list)
    return hex1


def Crc16Add(data):
    """
    生成信号校验码，并连同原信号一同输出字节类型
    :param data: 输入的RS485指令字符串，不包括校验码
    :return: 返回包括校验码的RS485通信信号，bytes类型
    """
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = str(data.replace(" ", ""))
    datacrcout = hex(crc16(Ascii2Hex(data)))
    datacrc_list = list(datacrcout)

    # 不足补0
    if len(datacrc_list) < 6:
        datacrc_list.insert(2, '0' * (6 - len(datacrc_list)))
    datacrc_str = "".join(str(i) for i in datacrc_list)
    data_all = data + datacrc_str[4:6] + datacrc_str[2:4]
    return Ascii2Hex(data_all)

def splitCommand(command):
    """
    输入字节字符串或者字符串，返回分割后的（地址码，功能码，数据段）
    :param command:
    :return:
    """
    if isinstance(command,bytes):
        command=str(command.hex())
    # return (command[0:2],command[2:4],command[4:12]) #不带校验码
    return (command[0:2],command[2:4],command[4:len(command)-4]) #不带校验码

# return (command[0:2],command[2:4],command[4:12],command[12:16]) #带校验码



###### 以下可能用不到
def scan_serial():
    """
    扫描端口
    :return: 端口列表
    """
    ListPorts = list(serial.tools.list_ports.comports())
    return ListPorts


def FindAddress(num):
    """
    查找设备num的地址，产生信号，自带校验码
    :return: 寻址指令字符串
    """
    findaddress_str = b''
    findaddress_data = Crc16Add(hex(num)[2:].zfill(2) + "0301000001")
    findaddress_str = findaddress_str + findaddress_data
    return findaddress_str


def sendAddress(*args):
    """
    发送单个寻址指令，寻址范围0-255
    :param args: 第一个参数是串口号，后面的参数
    :return: 从机地址列表
    """
    # 获取串口号
    SerialPort = args[0]
    # 获取需要更新的发送信息窗
    Information_Window = args[1]
    # 获取需要更新的接收信息窗
    Receive_Window = args[2]
    # 获取需要更新的从机设备列表
    address_list = args[3]

    ListAddress = []
    for i in range(1, 256):  # 1-255地址轮询
        data1 = FindAddress(i)
        Information_Window.insert("end", 'The command sent is: ' + str(data1.hex()) + '\n')
        Information_Window.see("end")
        SerialPort.write(data1)
        time1 = time.perf_counter()
        while True:
            if ((time.perf_counter() - time1) * 1000) > 50:
                break
        len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
        if len_return_data:
            return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
            # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
            str_return_data = str(return_data.hex())
            ListAddress += [str_return_data[0:2]]
            Receive_Window.insert("end", str_return_data + '\n')
            Receive_Window.see("end")
        # 更新设备列表框
        address_list['values'] = ListAddress
        address_list.current(0)


def cyclesendAddress(*args):
    # 获取串口号
    SerialPort = args[0]
    # 获取需要更新的发送信息窗
    Information_Window = args[1]
    # 获取需要更新的接收信息窗
    Receive_Window = args[2]
    flag = 0  # 发送次数计数
    t_max = 1  # 最大发送次数

    while flag < t_max:
        for i in range(1, 256):  # 1-255地址轮询
            data1 = FindAddress(i)
            if flag < t_max:
                Information_Window.insert("end", 'The command sent is: ' + str(data1.hex()) + '\n')
                Information_Window.see("end")
                SerialPort.write(data1)
                time1 = time.perf_counter()
                while True:
                    if ((time.perf_counter() - time1) * 1000) > 50:
                        break
                len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
                if len_return_data:
                    return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
                    # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
                    str_return_data = str(return_data.hex())
                    Receive_Window.insert("end", str_return_data + '\n')
                    Receive_Window.see("end")


def openLight(SerialPort, moduleAddress, Information_Window, Receive_Window):
    """
    :param SerialPort: 需要开启继电器的端口号
    :param moduleAddress: 需要开启继电器的设备地址
    :param Information_Window: 获取需要更新的发送信息窗
    :param Receive_Window: 获取需要更新的接收信息窗
    :return:
    """
    if SerialPort.isOpen():
        send_data = b''
        send_data = send_data + Crc16Add(moduleAddress + "050000ff00")
        SerialPort.write(send_data)
        Information_Window.insert("end", 'The command sent is: ' + str(send_data.hex()) + '\n')
        Information_Window.see("end")
        time.sleep(0.1)
        len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
        if len_return_data:
            return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
            # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
            str_return_data = str(return_data.hex())
            Receive_Window.insert("end", str_return_data + '\n')
            Receive_Window.see("end")


def closeLight(SerialPort, moduleAddress, Information_Window, Receive_Window):
    """
    :param SerialPort: 需要开启继电器的端口号
    :param moduleAddress: 需要开启继电器的设备地址
    :param Information_Window: 获取需要更新的发送信息窗
    :param Receive_Window: 获取需要更新的接收信息窗
    :return:
    """
    send_data = b''
    send_data = send_data + Crc16Add(moduleAddress + "0500000000")
    SerialPort.write(send_data)
    Information_Window.insert("end", 'The command sent is: ' + str(send_data.hex()) + '\n')
    Information_Window.see("end")
    time.sleep(0.1)
    len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
    if len_return_data:
        return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
        # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
        str_return_data = str(return_data.hex())
        Receive_Window.insert("end", str_return_data + '\n')
        Receive_Window.see("end")





class RelayButton():
    def __init__(self, x_loc,img1_width,address, Figure, Device_display,SerialPort,language,Information_Window,Receive_Window):
        """
        初始化继电器图片类
        :param x_loc: 图片相对于Figure的横坐标
        :param address: 继电器对应从机地址
        :param Figure: 继电器对应tk figure
        :param Device_display: 继电器放在的画布中
        :param img1_width: 图片宽度
        :param SerialPort: 端口号
        :param language:语言
        :param Information_Window:获取输出的发送信息窗
        :param Receive_Window:获取输出的接收信息窗
        """
        self.relay_state_flag = False
        diameter = 50  # ⚪的直径
        y_loc = 70
        self.Figure = Figure
        self.Device_display=Device_display
        # 对应灯
        self.oval = self.Figure.create_oval(x_loc - diameter / 2, y_loc - diameter / 2, x_loc + diameter / 2,
                                            y_loc + diameter / 2,
                                            fill='red', width=2.5, outline='black')  # 矩形左上右下坐标来确定内切圆
        # 对应按钮
        self.button = tk.Button(Device_display, text="开启", command=lambda:self.relay_state_change(SerialPort,language,Information_Window,Receive_Window))
        self.Figure.create_window(x_loc - img1_width / 3, 160, anchor=tk.NW, window=self.button)
        # 对应从机地址
        self.address = address
        self.Figure.create_text(x_loc, y_loc, text=str(address))

    def relay_state_change(self, SerialPort,language,Information_Window,Receive_Window):
        """
        点击按钮改变继电器状态
        :param SerialPort: 端口号
        :param language:语言
        :param Information_Window:获取输出的发送信息窗
        :param Receive_Window:获取输出的接收信息窗
        :return:
        """
        self.relay_state_flag = not self.relay_state_flag
        if self.relay_state_flag:
            # 发送控制指令
            openLight(SerialPort, self.address, Information_Window, Receive_Window)
            # 改变灯的颜色
            self.Figure.itemconfig(self.oval, fill='green')
            # 改变文字
            if language == '中文':
                self.button['text'] = '关闭'
            elif language == 'English':
                self.button['text'] = 'Close'
            # 显示操作信息
            time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            Information_Window.insert("end", time_str + ": " + "Connect Relay " + self.address + '\n')
            Information_Window.see("end")
        else:
            # 发送控制指令
            closeLight(SerialPort, self.address, Information_Window, Receive_Window)
            # 改变灯的颜色
            self.Figure.itemconfig(self.oval, fill='red')
            # 改变文字
            if language == '中文':
                self.button['text'] = '开启'
            elif language == 'English':
                self.button['text'] = 'Open'
            # 显示操作信息
            time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
            Information_Window.insert("end", time_str + ": " + "Disconnect Relay " + self.address + '\n')
            Information_Window.see("end")
        self.Device_display.update()

