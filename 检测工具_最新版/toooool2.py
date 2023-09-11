#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/30 22:29
# @File    : toooool.py
# @Description : 优化结构
import csv
import datetime
import socket
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import Frame, Tk, LEFT, BOTH, END, BOTTOM, X, Y, HORIZONTAL, RIGHT, TOP, W, CENTER, scrolledtext
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename

import pandas as pd
import serial.tools.list_ports

import serial
from PIL import Image, ImageTk
from pandas import DataFrame

import bluetooth_server_conn
from common import ThreadFunc, ExporTreeview, create_ToolTip
from modbus_comm import Crc16Add, splitCommand

# 全局重要变量
language = '中文'
SerialPort = serial.Serial() #串口对象
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP 连接对象
timer_time = 3  # 曲线图显示数据时间间隔

# 检测视角曲线有关变量
figureHeight = 320  # 实时检测特征曲线图高
figureWidth = 850  # 实时检测特征曲线图宽
axisDistance = 30  # 坐标轴距离画布边距
bluetoothPort = 14  # 蓝牙端口号
showPoints = 10  # 每页最多十条数据


class Application(Frame):
    """
    总容器，包括菜单栏、图标、选项卡
    """

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # self.config(bg='red',height=100,width=100)
        self.pack(side='top', fill='both', expand=True)  # 继承

        self.tool={}

        self.createMenu()  # 创建菜单栏
        self.createToolbar() #创建工具栏
        self.createWidget()  # 创建子组件

        # 大西交logo
        self.xjtuLogo = ImageTk.PhotoImage(Image.open("resource/xjtu.jpg"))
        xjtuLogo_label = tk.Label(self, image=self.xjtuLogo)
        xjtuLogo_label.place(relx=0.90, rely=0)

    ### ----------组件区----------

    def createMenu(self):
        ## 菜单栏
        menus = ['文件', '设置', '帮助']
        items = [['保存……','全部保存……','-','删除选中数据……','全部删除……'],
                 ['选择语言'],
                 ['使用说明']]
        callbacks = [[self.export, self.exportAll,'-',self.delete,self.deleteAll],
                     [self.changeLanguage],
                     [self.help]]

        menubar = tk.Menu(self.master)
        # 一级菜单
        for i, x in enumerate(menus):
            # 二级菜单
            m = tk.Menu(menubar, tearoff=0)
            for item, callback in zip(items[i], callbacks[i]):
                # 三级菜单（这里用不上，之后扩展可能用上）
                if isinstance(item, list):
                    sm = tk.Menu(menubar, tearoff=0)
                    for subitem, subcallback in zip(item[1:], callback):
                        if subitem == '-':
                            sm.add_separator()
                        else:
                            sm.add_command(label=subitem, command=subcallback, compound='left')
                    m.add_cascade(label=item[0], menu=sm)
                elif item == '-':
                    m.add_separator()
                else:
                    m.add_command(label=item, command=callback, compound='left')
            menubar.add_cascade(label=x, menu=m)
        self.master.config(menu=menubar)

    # 生成工具条
    def createToolbar(self):
        toolframe = tk.Frame(self, height=20, bg='#F7EED6')  # , relief=tk.RAISED)
        toolframe.pack(side=TOP,fill=X)
        imgSize = 20
        toolName = ['save', 'saveAll', 'delete','deleteAll']  # 图片文件名
        toolFunc = [self.export, self.exportAll, self.delete, self.deleteAll]  # 图片绑定事件名
        toolButtonTip = ['保存', '全部保存', '删除', '全部删除']  # 图片绑定按钮提示
        toolButton = []  # 图片绑定按钮
        for i in range(len(toolName)):
            self.tool[i] = ImageTk.PhotoImage(Image.open("resource/" + toolName[i] + ".png").resize((imgSize, imgSize)))
            toolButton.append(ttk.Button(toolframe, width=20, image=self.tool[i], command=toolFunc[i]))
            toolButton[i].pack(side=LEFT)
            create_ToolTip(toolButton[i], toolButtonTip[i])



    def createWidget(self):
        """
        创建子组件
        :return:
        """

        ## 切换不同视角
        # 标签卡
        self.viewNotebook = tk.ttk.Notebook(self)
        self.viewNotebook.pack(side=TOP,fill=BOTH, expand=True)



        viewAngle = ['控制中心', '检测设备', '攻击者']
        # 控制中心视角容器
        self.controlViewFrame = controlViewFrame(self.viewNotebook)
        self.controlViewFrame.pack(fill=BOTH, expand=True)
        # 检测设备视角
        self.detectViewFrame = detectViewFrame(self.viewNotebook)
        self.detectViewFrame.pack(fill=BOTH, expand=True)
        # 攻击者视角
        self.attackViewFrame = attackViewFrame(self.viewNotebook, bg='green')
        self.attackViewFrame.pack(fill=BOTH, expand=True)

        # 关联标签卡选项与视角容器
        self.viewNotebook.add(self.controlViewFrame, text=viewAngle[0])
        self.viewNotebook.add(self.detectViewFrame, text=viewAngle[1])
        self.viewNotebook.add(self.attackViewFrame, text=viewAngle[2])

    ### ----------方法区----------
    def export(self):
        """
        导出单个excel表
        :return:
        """

        # 获取选择窗口
        sn=self.viewNotebook.select().split('.')[-1]
        selectViewTreeView=self.viewNotebook.children[sn].treeview
        sheet_name = self.viewNotebook.tab(self.viewNotebook.select(),option='text')

        selectViewTreeView.export(sheet_name)


    def exportAll(self):
        """
        导出所有excel表
        :return:
        """
        # 打开选择文件夹
        # 打开选择文件夹
        excel_name = asksaveasfilename(initialfile="all", defaultextension='.xlsx',
                                       filetypes=[('XLSX files', '.xlsx'), ('all files', '.*')])
        # 获取选择窗口
        try:
            if (excel_name != ""):
                with pd.ExcelWriter(excel_name) as writer:
                    for (k,v) in self.viewNotebook.children.items():
                        # print(k,v)
                        selectViewTreeView=v.treeview
                        sheet_name=self.viewNotebook.tab(v,option='text')
                        ExporTreeview(writer,selectViewTreeView,sheet_name=sheet_name)
                    res = messagebox.showinfo(title='成功提示', message='Excel已保存')

        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)

    def delete(self):
        # 获取选择窗口
        sn = self.viewNotebook.select().split('.')[-1]
        selectViewTreeView = self.viewNotebook.children[sn].treeview

        selectViewTreeView.clear()

    def deleteAll(self):
        # 获取选择窗口
        sn = self.viewNotebook.select().split('.')[-1]
        selectViewTreeView = self.viewNotebook.children[sn].treeview

        selectViewTreeView.clearAll()

    # TODO
    def changeLanguage(self):
        """
        修改语言
        :return: 弹出修改语言对话框
        """
        global language
        pass

    # TODO
    def help(self):
        """
        帮助
        :return: 瞎写几条帮助
        """
        webbrowser.open("http://c.biancheng.net/tkinter/", new=0)
        pass


class controlViewFrame(Frame):
    """
    控制中心视角框架
    """

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw)
        self.master = master

        # 初始化变量
        self.selectDeviceAddress = None  # 选中设备地址
        self.cycleFindDeviceFlag = tk.IntVar(value=0)  # 循环发送标志位
        self.deviceList = tk.StringVar()  # 可用从机设备列表

        # 初始化组件
        self.createWidget()  # 创建子组件

        # 监听端口状态
        ThreadFunc(self.listenSerialState)

        self.scanSerial()  # 扫描端口



    ### ----------组件区----------

    def createWidget(self):

        # 配置区
        self.setFrame = tk.ttk.LabelFrame(self)
        self.setFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.setFrame_Init()
        # 数据显示区
        self.dataFrame = tk.ttk.LabelFrame(self)
        self.dataFrame.grid(row=0, column=1, padx=5, sticky=tk.NSEW)
        self.dataFrame_Init()

        # 设备列表区
        self.deviceFrame = tk.ttk.LabelFrame(self)
        self.deviceFrame.grid(row=1, column=0, sticky=tk.NSEW)
        self.deviceFrame_Init()
        # 数据发送区
        self.sendFrame = tk.ttk.LabelFrame(self)
        self.sendFrame.grid(row=1, column=1, padx=5, sticky=tk.NSEW)
        self.sendFrame_Init()
        # print(self.dataFrame.winfo_screenwidth())

    def deviceFrame_Init(self):
        """
        设备列表区初始化
        :return:
        """
        padx = 5
        pady = 5
        ## 设备列表
        deviceLable = ttk.Label(self.deviceFrame, text="设备列表")
        deviceLable.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)

        # 寻找设备按钮
        finddeviceButton = ttk.Button(self.deviceFrame, text="寻找设备", command=self.findDeviceThread)
        finddeviceButton.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        self.cycleFindDeviceButton = ttk.Checkbutton(self.deviceFrame, text="循环发送", variable=self.cycleFindDeviceFlag)
        self.cycleFindDeviceButton.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)

        # 设置设备列表窗口
        # self.deviceList.set((11, 22, 33, 44, 354, 534, 534, 534, 53, 45, 34, 534, 5, 34, 5, 34, 5, 34, 5, 3453))  # 为变量设置值
        # 创建Listbox
        self.deviceListBox = tk.Listbox(self.deviceFrame, height=16, listvariable=self.deviceList, selectmode='browse')
        self.deviceListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        self.deviceListBox.bind('<Double-Button-1>', self.changeSelectDevice)

    def sendFrame_Init(self):
        """
        发送区初始化
        :return:
        """
        padx = 5
        pady = 5
        # 选中设备地址文本
        self.selectDeviceAddressLable = ttk.Label(self.sendFrame, text="当前设备地址：")
        self.selectDeviceAddressLable.pack(side=TOP, anchor=W, padx=padx, pady=pady)

        # 选中设备操作选项卡
        selectDeviceOperationNotebook = tk.ttk.Notebook(self.sendFrame)
        selectDeviceOperationNotebook.pack(fill='both', expand=True, padx=padx, pady=pady)
        selectDeviceOperation = ['快捷指令', '读取寄存器', '修改寄存器']  # 选项卡名称
        selectDeviceOperation_Quick = Frame(self.sendFrame)
        selectDeviceOperation_Quick.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Quick, text=selectDeviceOperation[0])
        selectDeviceOperation_Read = Frame(self.sendFrame)
        selectDeviceOperation_Read.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Read, text=selectDeviceOperation[1])
        selectDeviceOperation_Write = Frame(self.sendFrame)
        selectDeviceOperation_Write.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Write, text=selectDeviceOperation[2])

        # 快捷指令界面
        # 寻址指令
        sendFrame_findAddress = tk.Frame(selectDeviceOperation_Quick)
        sendFrame_findAddress.pack(side=TOP, fill=X, padx=padx, pady=pady)
        findAddressLabel = tk.Label(sendFrame_findAddress, text="寻址指令")
        findAddressLabel.pack(side=LEFT, padx=padx, pady=pady)
        ##！！！ 这里没有判断deviceListBox元素是否为0，得改
        findAddressButton = tk.Button(sendFrame_findAddress, text="发送",
                                      command=lambda: self.sendReadDeviceAddressCommand(self.selectDeviceAddress))
        findAddressButton.pack(side=LEFT, padx=padx, pady=pady)
        # 开关继电器指令
        sendFrame_operateRelay = tk.Frame(selectDeviceOperation_Quick)
        sendFrame_operateRelay.pack(side=TOP, fill=X, padx=padx, pady=pady)
        operateRelayLable = tk.Label(sendFrame_operateRelay, text="操作继电器")
        operateRelayLable.pack(side=LEFT, padx=padx, pady=pady)
        connectRelayButton = tk.Button(sendFrame_operateRelay, text='吸合',
                                       command=lambda: self.connectRelay(self.selectDeviceAddress))
        connectRelayButton.pack(side=LEFT, padx=padx, pady=pady)
        disconnectRelayButton = tk.Button(sendFrame_operateRelay, text='断开',
                                          command=lambda: self.disconnectRelay(self.selectDeviceAddress))
        disconnectRelayButton.pack(side=LEFT, padx=padx, pady=pady)

    def setFrame_Init(self):
        """
            配置区 初始化
            :return:
        """
        # ************创建下拉列表**************
        padx = 5
        pady = 5
        width = 30
        ## 串口号
        serialportLable = ttk.Label(self.setFrame, width=width, text="串口号:")
        serialportLable.grid(row=0, column=0, sticky=W, padx=padx, pady=pady)  # 添加串口号标签
        self.serialport = tk.StringVar()  # 端口号字符串
        self.serialportCombobox = ttk.Combobox(self.setFrame, width=width, textvariable=self.serialport,
                                               state='readonly')
        self.serialportCombobox.grid(row=0, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        ##波特率
        BaudrateLable = ttk.Label(self.setFrame, width=width, text="波特率:")
        BaudrateLable.grid(row=1, column=0, sticky=W, padx=padx, pady=pady)  # 添加波特率标签
        self.baudrate = tk.StringVar()  # 波特率绑定字符串
        self.baudrateCombobox = ttk.Combobox(self.setFrame, width=width, textvariable=self.baudrate, state='readonly')
        self.baudrateCombobox['values'] = (1200, 2400, 4800, 9600, 14400, 19200, 38400, 43000, 57600, 76800, 115200)
        self.baudrateCombobox.current(3)
        self.baudrateCombobox.grid(row=1, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        ##数据位
        bytesizeLabel = ttk.Label(self.setFrame, width=width, text="数据位:")
        bytesizeLabel.grid(row=2, column=0, sticky=W, padx=padx, pady=pady)
        self.bytesize = tk.IntVar()  # 波特率绑定字符串
        self.bytesizeCombobox = ttk.Combobox(self.setFrame, width=width, textvariable=self.bytesize, state='readonly')
        self.bytesizeCombobox['values'] = (5, 6, 7, 8)
        self.bytesizeCombobox.current(3)
        self.bytesizeCombobox.grid(row=2, column=1, padx=padx, pady=pady)

        ## 校验位
        parityLabel = ttk.Label(self.setFrame, width=width, text="校验位:")
        parityLabel.grid(row=3, column=0, sticky=W, padx=padx, pady=pady)
        self.parity = tk.StringVar()
        self.parityCombobox = ttk.Combobox(self.setFrame, width=width, textvariable=self.parity, state='readonly')
        self.parityCombobox['values'] = ('N', 'E', 'O', 'M', 'S')
        self.parityCombobox.current(0)
        self.parityCombobox.grid(row=3, column=1, padx=padx, pady=pady)

        ## 停止位
        stopbitsLabel = ttk.Label(self.setFrame, width=width, text="停止位:")
        stopbitsLabel.grid(row=4, column=0, sticky=W, padx=padx, pady=pady)
        self.stopbits = tk.DoubleVar()
        self.stopbitsCombobox = ttk.Combobox(self.setFrame, width=width, textvariable=self.stopbits, state='readonly')
        self.stopbitsCombobox['values'] = (1, 1.5, 2)
        self.stopbitsCombobox.current(0)
        self.stopbitsCombobox.grid(row=4, column=1, padx=padx, pady=pady)

        # 开启关闭串口按钮
        serialOpenButton = tk.ttk.Button(self.setFrame, text="打开串口", command=self.openSerial)
        serialOpenButton.grid(row=5, column=0, padx=padx, pady=pady)
        serialCloseButton = tk.ttk.Button(self.setFrame, text="关闭串口", command=self.closeSerial)
        serialCloseButton.grid(row=5, column=1, padx=padx, pady=pady)

        # 扫描可用串口按钮
        serialScanButton = tk.ttk.Button(self.setFrame, text="扫描可用串口", command=self.scanSerial)
        serialScanButton.grid(row=6, column=0, columnspan=2, padx=padx, pady=pady)

        # 监听串口状态
        # 端口状态
        self.serialPortStateLabel = tk.Label(self.setFrame)
        self.serialPortStateLabel.grid(row=7, column=0, columnspan=2, padx=padx, pady=pady)

        # 放个串口灯

    def dataFrame_Init(self):
        """
        数据显示区 初始化
        :return:
        """
        ## 新建excel 组件，记录发送或接收的解析后的指令
        columns = ("序号", "时间", "地址码", "功能码", "数据", "类型")

        self.treeview = MyTreeview(master=self.dataFrame, setcolumn=columns, columns=columns, height=15,
                                   show="headings")  # 表格
        self.treeview.pack(side=TOP, fill=BOTH)

    # ----------函数区----------
    def scanSerial(self):
        """
        扫描端口
        :return: 端口列表
        """
        ListPorts = list(serial.tools.list_ports.comports())
        if ListPorts:
            self.serialportCombobox['values'] = [i[0] for i in ListPorts]
            self.serialportCombobox.current(0)
        else:
            self.serialportCombobox['values'] = [""]
            self.serialportCombobox.current(0)

    def openSerial(self):
        """
        开启端口，并将设置好的参数传给端口
        :return:
        """
        global SerialPort
        try:
            # 当开启时关闭重新配置端口
            if SerialPort.isOpen():
                SerialPort.close()
            SerialPort.port = self.serialportCombobox.get()
            SerialPort.baudrate = int(self.baudrateCombobox.get())
            SerialPort.bytesize = int(self.bytesizeCombobox.get())
            SerialPort.parity = self.parityCombobox.get()
            SerialPort.stopbits = float(self.stopbitsCombobox.get())
            SerialPort.timeout = 0.1
            SerialPort.writeTimeout =0.1
            SerialPort.open()

        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def closeSerial(self):
        """
        关闭端口
        :return:
        """
        global SerialPort
        try:
            if SerialPort.isOpen():
                SerialPort.close()
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def changeSelectDevice(self, event):
        """
        :param event: 鼠标双击设备列表，改变当前选中设备
        :return:
        """
        try:
            activeDeviceIndex = self.deviceListBox.curselection()[0]
            self.selectDeviceAddress = self.deviceListBox.get(activeDeviceIndex, activeDeviceIndex)[0]
            self.selectDeviceAddressLable.config(text="当前设备地址：0x" + str(self.selectDeviceAddress))
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def generateReadDeviceAddressCommand(self, num: int):
        """
        生成读设备地址的指令
        :return: 寻址指令字符串
        """
        try:
            findaddress_str = b''
            findaddress_data = Crc16Add(hex(num)[2:].zfill(2) + "0301000001")
            findaddress_str = findaddress_str + findaddress_data
            return findaddress_str
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def sendReadDeviceAddressCommand(self, num: str):
        try:
            data1 = self.generateReadDeviceAddressCommand(int(num))
            SerialPort.write(data1)
            self.treeview.insert('', index=END,
                                 values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(str(data1.hex())) + (
                                 "发送",))
            self.treeview.treeviewNum += 1
            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break
            len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
            if len_return_data:
                return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
                # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
                str_return_data = str(return_data.hex())
                # 更新excel表
                self.treeview.insert('', index=END,
                                     values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                         str_return_data) + ("接收",))
                self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def findDevice(self):
        """
        发送单个寻址指令，寻址范围0-255
        :param args: 第一个参数是串口号，后面的参数
        :return: 从机地址列表
        """
        try:
            cycle = 0
            cycle_max = 1
            while (cycle < cycle_max):
                if self.cycleFindDeviceFlag.get() == 0:
                    cycle += 1
                ListAddress = []
                for i in range(1, 256):  # 1-255地址轮询
                    data1 = self.generateReadDeviceAddressCommand(i)
                    self.treeview.insert('', index=END,
                                         values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                             str(data1.hex())) + ("发送",))
                    self.treeview.treeviewNum += 1
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
                        # 更新excel表
                        self.treeview.insert('', index=END,
                                             values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                                 str_return_data) + ("接收",))
                        self.treeview.treeviewNum += 1
                        # 更新设备列表框
                        ListAddress += [str_return_data[0:2]]
                        self.deviceList.set(tuple(ListAddress))
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def findDeviceThread(self):
        t = threading.Thread(target=self.findDevice)
        print(self.cycleFindDeviceFlag.get())
        t.setDaemon(True)
        t.start()

    def connectRelay(self, num):
        try:
            send_data = b''
            send_data = send_data + Crc16Add(str(num) + "050000ff00")
            SerialPort.write(send_data)
            self.treeview.insert('', index=END,
                                 values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                     str(send_data.hex())) + ("发送",))
            self.treeview.treeviewNum += 1
            time.sleep(0.1)
            len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
            if len_return_data:
                return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
                # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
                str_return_data = str(return_data.hex())
                # 更新excel表
                self.treeview.insert('', index=END,
                                     values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                         str(str_return_data)) + ("接收",))
                self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def disconnectRelay(self, num):
        try:
            send_data = b''
            send_data = send_data + Crc16Add(str(num) + "0500000000")
            SerialPort.write(send_data)
            self.treeview.insert('', index=END,
                                 values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                     str(send_data.hex())) + ("发送",))
            self.treeview.treeviewNum += 1
            time.sleep(0.1)
            len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
            if len_return_data:
                return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
                # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
                str_return_data = str(return_data.hex())
                # 更新excel表
                self.treeview.insert('', index=END,
                                     values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                         str_return_data) + ("接收",))
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)


    def listenSerialState(self):
        try:
            if SerialPort.isOpen():
                self.serialPortStateLabel.config(text="串口状态：已开启")
            else:
                self.serialPortStateLabel.config(text="串口状态：已关闭")
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)







class detectViewFrame(Frame):
    """
    检测者视角框架
    """

    def __init__(self, master=None, cnf={}, **kw):
        global timer_time
        super().__init__(master, cnf={}, **kw)
        self.master = master
        self.IntrusionTreeviewNum = 0  # 入侵统计表格条数
        self.FeaturePlotList = []  # 待显示数据列表
        self.thresholdLine = None  # 阈值曲线对象
        self.new_data = []  # 蓝牙传输单个数据
        self.intrusionFlag = 0  # 入侵标志位
        self.detectCount = 0  # 总检测次数
        self.intrusionBeginTime = None  # 开始入侵时间

        self.createWidget()  # 创建子组件
        self.t_timer = threading.Timer(timer_time, self.timer_handler)
        self.t_timer.start()  # 开启定时器，定时显示数据到曲线图
        t_bluetooth_listen = threading.Thread(target=self.thread_server_listen)
        t_bluetooth_listen.start()  # 开启蓝牙数据监听

    ### ----------组件区----------
    def createWidget(self):
        ## 检测信息窗口
        global figureHeight, figureWidth
        padx = 15
        pady = 15
        detectInformationFrame = tk.Frame(self)
        detectInformationFrame.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        detectInformationLabel = tk.Label(detectInformationFrame, text="检测信息",)
        detectInformationLabel.pack(side=TOP, anchor=W, fill=X)
        self.detectInformationScrolledText = scrolledtext.ScrolledText(detectInformationFrame, wrap=tk.WORD)
        self.detectInformationScrolledText.pack(side=TOP, fill=X)

        ## 特征曲线图窗口
        featureCurveFrame = tk.Frame(self)
        featureCurveFrame.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
        featureCurveLabel = tk.Label(featureCurveFrame, text="实时检测特征曲线")
        featureCurveLabel.pack(side=TOP, anchor=W, fill=X)

        # 静态窗口
        Plot = tk.Canvas(featureCurveFrame, bg="#DCDCDC", height=figureHeight, width=figureWidth)
        Plot.pack(side=TOP, fill=X)
        Plot.create_line(axisDistance - 2, 0, axisDistance - 2, figureHeight, fill='black', width=4)  # 纵轴
        Plot.create_line(0, figureHeight - axisDistance + 2, figureWidth,
                         figureHeight - axisDistance + 2, fill='black', width=4)  # 横轴

        # 设置滚动检测窗口
        plot2_height = figureHeight
        plot2_width = figureWidth - axisDistance
        self.Plot2 = tk.Canvas(Plot, bg="#D3D3D3", height=(plot2_height), width=(plot2_width))
        self.Plot2.place(x=axisDistance, y=0)
        self.Plot2.create_line(0, (figureHeight - axisDistance + 2), (figureWidth - axisDistance),
                               (figureHeight - axisDistance + 2), fill='black',
                               width=4)  # 横轴

        # 统计入侵信息表格
        # (入侵序号，入侵开始时间，入侵结束时间，持续时间，检测次数）
        ## 新建excel 组件，记录发送或接收的解析后的指令
        self.columns = ("序号", "入侵开始时间", "入侵结束时间", "特征值","入侵持续时间/秒")
        countIntrusionFrame = Frame(self)
        countIntrusionFrame.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW, padx=padx, pady=pady)

        self.treeview = MyTreeview(master=countIntrusionFrame, setcolumn=self.columns, columns=self.columns, height=15,
                                   show="headings")  # 表格
        self.treeview.pack(side=TOP, fill=BOTH)

        # while (self.treeview.treeviewNum < 100):
        #     p = [self.treeview.treeviewNum, '1999', '03', '01', '00010001']
        #     self.treeview.insert('', index=END, values=tuple(p))
        #     self.treeview.treeviewNum += 1

    ### ----------函数区----------
    def timer_handler(self):
        """
        用定时器接收树莓派数据过程，定时间隔：3s
        :return:
        """
        global figureHeight, figureWidth, timer_time, showPoints
        t3 = threading.Timer(timer_time, self.timer_handler)
        t3.start()

        # ************结果显示位置*****************
        # 这里需要添加一个线程监听树莓派传过来的数据
        # 波形窗口宽result_display_width，高result_display_height
        point_size = 3  # 点的直径
        print("定时器：", self.new_data)

        plot2_width = figureWidth - axisDistance

        if len(self.new_data) != 0:
            self.detectCount += 1  # 检测次数+1
            threshold = self.new_data[1]  # 检测阈值
            threshold_x, threshold_y = self.compute_coordinate(0, threshold)
            # 阈值对象
            if self.thresholdLine:
                self.Plot2.delete(self.thresholdLine)
            self.thresholdLine = self.Plot2.create_line(threshold_x, threshold_y, threshold_x + plot2_width,
                                                        threshold_y, fill='#FF0000',
                                                        width=2)
            # Plot.create_text(axisDistance / 2, threshold_y, text="阈\n值\n", font=("Purisa", 10))
            # Plot.create_text(axisDistance / 2, threshold_y - 80, text="有\n攻\n击\n", font=("Purisa", 10))
            # Plot.create_text(axisDistance / 2, threshold_y + 80, text="无\n攻\n击\n", font=("Purisa", 10))
            # threshold_x, threshold_y = self.compute_coordinate(0, threshold)

            # print("get data!" + " " + str(self.new_data[1]) + " " + str(self.new_data[0]))
            # 输出检测结果
            # 当前时间字符串
            # print("self.intrusionFlag",self.intrusionFlag)
            now_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
            self.detectInformationScrolledText.insert("end", time_str + ": " + "Get feature value " + str(
                round(self.new_data[0],3)) + '\n')
            # 判断是否异常
            if self.new_data[0] > threshold:
                # 报警
                self.detectInformationScrolledText.insert("end", time_str + ": " + "Intrusion detected!" + '\n',
                                                          'error')
                self.detectInformationScrolledText.tag_config('error', foreground='red')

                if self.intrusionFlag == 0:
                    # 开始入侵记录入侵时间，第几次检测
                    self.intrusionFlag = 1
                    self.intrusionBeginTime = now_time
                    self.treeview.insert('', index=END, iid=self.treeview.treeviewNum, values=(
                    self.treeview.treeviewNum, time_str, '',round(self.new_data[0],3), 0))
                else:
                    self.intrusionFlag = 1
                    self.treeview.set(self.treeview.treeviewNum,column=self.columns[-1],value=(now_time - self.intrusionBeginTime).seconds)

                # 输出
                self.detectInformationScrolledText.see("end")
                self.FeaturePlotList.append(self.new_data)
                # print("FeaturePlotList",self.FeaturePlotList)
                x, y = self.compute_coordinate(len(self.FeaturePlotList) - 1, self.new_data[0])
                if len(self.FeaturePlotList) == 1:
                    self.Plot2.create_oval(x - point_size, y - point_size, x + point_size, y + point_size, outline='black',
                                           fill='blue',
                                           width=1)
                else:
                    self.Plot2.create_oval(x - point_size, y - point_size, x + point_size, y + point_size, outline='black',
                                           fill='blue',
                                           width=1)
                    x_old, y_old = self.compute_coordinate(len(self.FeaturePlotList) - 2,
                                                           self.FeaturePlotList[len(self.FeaturePlotList) - 2][0])
                    # 连接两点
                    self.Plot2.create_line(x_old, y_old, x, y, fill='black',
                                           width=2)

                # print("data_list长度",len(self.FeaturePlotList))
                if len(self.FeaturePlotList) == showPoints:
                    x1 = self.FeaturePlotList[-1]
                    self.FeaturePlotList = []
                    self.FeaturePlotList.append(x1)
                    self.Plot2.delete(tk.ALL)
                    self.Plot2.create_line(0, (figureHeight - axisDistance + 2),
                                           (figureWidth - axisDistance),
                                           (figureHeight - axisDistance + 2),
                                           fill='black',
                                           width=4)  # 横轴
            else:
                # 结束入侵
                if self.intrusionFlag==1:
                    #设置入侵结束时间
                    self.treeview.set(self.treeview.treeviewNum,column=self.columns[2],value=time_str)
                    self.treeview.treeviewNum += 1
                # 标志位清零
                self.intrusionFlag = 0

    # 计算给定电压值对应像素点位置，y:特征值，index：在列表中的序号，返回相对于画布的坐标
    def compute_coordinate(self, index, y):
        """

        :param index:
        :param y:
        :return:
        """
        global showPoints, axisDistance

        plot2_height = figureHeight
        plot2_width = figureWidth - axisDistance
        # y轴零点对应坐标，y轴最大值对应坐标，x轴每页显示几个数据

        yaxis_min = 0
        yaxis_max = 20  # y轴最大值

        y_set = (int)((yaxis_max - y) / (yaxis_max - yaxis_min) * (plot2_height - axisDistance))
        x_set = (int)(plot2_width / (showPoints - 1) * index)
        return x_set, y_set

    # 监听蓝牙端口线程
    def thread_server_listen(self):
        global bluetoothPort
        bt = bluetooth_server_conn.BluetoothConnection()
        bt.server_bind(bluetoothPort)
        while True:
            # print('Waiting to receive data……')
            try:
                client_sock, address = bt.server_sock.accept()  # 阻塞等待连接
                print('Success connect!')
                print("Accepted connection from ", address)
                while True:
                    newdata = client_sock.recv(30).decode()  # 不断接收数据，每次接收缓冲区1024字节
                    if newdata == "":
                        break
                    # print("received [%s]" % newdata)
                    bt.data.append(newdata)
                    if len(bt.data) == 2:
                        self.new_data = []
                        for i in range(len(bt.data)):
                            self.new_data.append(float(bt.data[i]))
                        bt.data = []
                    # print("new_data", self.new_data)
            except Exception as e:
                print('Disconnect!', e)
                continue  # 报错后返回阻塞等待连接的状态


class attackViewFrame(Frame):
    """
    攻击者视角框架
    """

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw)
        self.master = master

        # 初始化变量
        self.logo={}  #存放图片
        self.buff_size = 20  # 缓冲区大小
        self.selectDeviceAddress = None  # 选中设备地址
        self.cycleFindDeviceFlag = tk.IntVar(value=0)  # 循环发送标志位
        self.deviceList = tk.StringVar()  # 可用从机设备列表

        # 初始化组件
        self.createWidget()  # 创建子组件


    ### ----------组件区----------

    def createWidget(self):



        # 配置区
        self.setFrame = tk.ttk.LabelFrame(self)
        self.setFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.setFrame_Init()

        # 数据显示区，显示监听的数据
        self.dataFrame = tk.ttk.LabelFrame(self)
        self.dataFrame.grid(row=0, column=1, padx=5, sticky=tk.NSEW)
        self.dataFrame_Init()

        # 设备列表区
        self.deviceFrame = tk.ttk.LabelFrame(self)
        self.deviceFrame.grid(row=1, column=0, sticky=tk.NSEW)
        self.deviceFrame_Init()
        # 数据发送区
        self.sendFrame = tk.ttk.LabelFrame(self)
        self.sendFrame.grid(row=1, column=1, padx=5, sticky=tk.NSEW)
        self.sendFrame_Init()
        # print(self.dataFrame.winfo_screenwidth())

    def sendFrame_Init(self):
        """
        发送区初始化
        :return:
        """
        padx = 5
        pady = 5
        # 选中设备地址文本
        self.selectDeviceAddressLable = ttk.Label(self.sendFrame, text="当前设备地址：")
        self.selectDeviceAddressLable.pack(side=TOP, anchor=W, padx=padx, pady=pady)

        # 选中设备操作选项卡
        selectDeviceOperationNotebook = tk.ttk.Notebook(self.sendFrame)
        selectDeviceOperationNotebook.pack(fill='both', expand=True, padx=padx, pady=pady)
        selectDeviceOperation = ['快捷指令', '读取寄存器', '修改寄存器']  # 选项卡名称
        selectDeviceOperation_Quick = Frame(self.sendFrame)
        selectDeviceOperation_Quick.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Quick, text=selectDeviceOperation[0])
        selectDeviceOperation_Read = Frame(self.sendFrame)
        selectDeviceOperation_Read.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Read, text=selectDeviceOperation[1])
        selectDeviceOperation_Write = Frame(self.sendFrame)
        selectDeviceOperation_Write.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Write, text=selectDeviceOperation[2])

        # 快捷指令界面
        # 寻址指令
        sendFrame_findAddress = tk.Frame(selectDeviceOperation_Quick)
        sendFrame_findAddress.pack(side=TOP, fill=X, padx=padx, pady=pady)
        findAddressLabel = tk.Label(sendFrame_findAddress, text="寻址指令")
        findAddressLabel.pack(side=LEFT, padx=padx, pady=pady)
        ##！！！ 这里没有判断deviceListBox元素是否为0，得改
        findAddressButton = tk.Button(sendFrame_findAddress, text="发送",
                                      command=lambda: self.sendReadDeviceAddressCommand(self.selectDeviceAddress))
        findAddressButton.pack(side=LEFT, padx=padx, pady=pady)
        # 开关继电器指令
        sendFrame_operateRelay = tk.Frame(selectDeviceOperation_Quick)
        sendFrame_operateRelay.pack(side=TOP, fill=X, padx=padx, pady=pady)
        operateRelayLable = tk.Label(sendFrame_operateRelay, text="操作继电器")
        operateRelayLable.pack(side=LEFT, padx=padx, pady=pady)
        connectRelayButton = tk.Button(sendFrame_operateRelay, text='吸合',
                                       command=lambda: self.connectRelay(self.selectDeviceAddress))
        connectRelayButton.pack(side=LEFT, padx=padx, pady=pady)
        disconnectRelayButton = tk.Button(sendFrame_operateRelay, text='断开',
                                          command=lambda: self.disconnectRelay(self.selectDeviceAddress))
        disconnectRelayButton.pack(side=LEFT, padx=padx, pady=pady)

    def setFrame_Init(self):
        """
            配置区 配置网络ip
            :return:
        """
        ### 默认入侵设备是服务器，电脑是客户端
        width=30
        padx=5
        pady=5
        ##  IP
        intrusionIPLable = ttk.Label(self.setFrame, width=width, text="Server's IP:")
        intrusionIPLable.grid(row=0, column=0, sticky=W, padx=padx, pady=pady)  # 添加串口号标签
        self.intrusionIP = tk.StringVar(value="10.1.1.10")  # 端口号字符串
        self.intrusionIPCombobox = tk.Entry(self.setFrame, width=width, textvariable=self.intrusionIP)
        self.intrusionIPCombobox.grid(row=0, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        ## 端口号
        intrusionPortLable = ttk.Label(self.setFrame, width=width, text="Server's port:")
        intrusionPortLable.grid(row=1, column=0, sticky=W, padx=padx, pady=pady)  # 添加串口号标签
        self.intrusionPort = tk.IntVar(value=8000)  # 端口号字符串
        self.intrusionPortCombobox = tk.Entry(self.setFrame, width=width, textvariable=self.intrusionPort)
        self.intrusionPortCombobox.grid(row=1, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        # 连接断开按钮
        serialOpenButton = tk.ttk.Button(self.setFrame, text="连接服务器", command=lambda:ThreadFunc(self.connectServer))
        serialOpenButton.grid(row=2, column=0, padx=padx, pady=pady)
        serialCloseButton = tk.ttk.Button(self.setFrame, text="断开连接", command=lambda:ThreadFunc(self.disconnectServer))
        serialCloseButton.grid(row=2, column=1, padx=padx, pady=pady)


        # TCP/IP 状态标志
        self.TCPSocketStateLabel=tk.Label(self.setFrame,text="\n\n入侵设备未连接\n\n")
        self.TCPSocketStateLabel.grid(row=3, column=0, columnspan=2, padx=padx, pady=pady)

        # 监听按钮
        serialScanButton = tk.ttk.Button(self.setFrame, text="开始监听", command=lambda: ThreadFunc(self.listen))
        serialScanButton.grid(row=4, column=0, columnspan=2, padx=padx, pady=pady)

        # 监听logo
        imgSize=50
        imgName=['connecting','connect','disconnect']
        for i in imgName:
            self.logo[i]=ImageTk.PhotoImage(Image.open("resource/"+i+".png").resize((imgSize,imgSize)))
        self.logoLabel = tk.Label(self.setFrame,image=None)
        self.logoLabel.grid(row=5, column=0, columnspan=2, padx=padx, pady=pady)

    def dataFrame_Init(self):
        """
        数据显示区 初始化
        :return:
        """
        ## 新建excel 组件，记录发送或接收的解析后的指令
        columns = ("序号", "时间", "地址码", "功能码", "数据段")
        self.treeview = MyTreeview(master=self.dataFrame,setcolumn=columns,columns=columns,height=15, show="headings")  # 表格
        self.treeview.pack(side=TOP, fill=BOTH)

        while (self.treeview.treeviewNum < 100):
            p = [self.treeview.treeviewNum, '1999', '03', '01', '00010001']
            self.treeview.insert('', index=END, values=tuple(p))
            self.treeview.treeviewNum += 1

    ### ----------函数区----------
    def deviceFrame_Init(self):
        """
        设备列表区初始化
        :return:
        """
        padx = 5
        pady = 5
        ## 设备列表
        deviceLable = ttk.Label(self.deviceFrame, text="设备列表")
        deviceLable.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)

        # 寻找设备按钮
        finddeviceButton = ttk.Button(self.deviceFrame, text="寻找设备", command=self.findDeviceThread)
        finddeviceButton.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        self.cycleFindDeviceButton = ttk.Checkbutton(self.deviceFrame, text="循环发送", variable=self.cycleFindDeviceFlag)
        self.cycleFindDeviceButton.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)

        # 设置设备列表窗口
        # self.deviceList.set((11, 22, 33, 44, 354, 534, 534, 534, 53, 45, 34, 534, 5, 34, 5, 34, 5, 34, 5, 3453))  # 为变量设置值
        # 创建Listbox
        self.deviceListBox = tk.Listbox(self.deviceFrame, height=16, listvariable=self.deviceList, selectmode='browse')
        self.deviceListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        self.deviceListBox.bind('<Double-Button-1>', self.changeSelectDevice)

    def connectServer(self):
        global tcp_socket
        # 连接服务器
        try:
            if (tcp_socket==None):
                tcp_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP 连接对象
            # 修改界面状态
            self.TCPSocketStateLabel['text']="\n\n正在连接到入侵设备，请稍候……\n\n"
            self.logoLabel.config(image=self.logo.get('connecting'))

            server_addr = (self.intrusionIP.get(), self.intrusionPort.get())
            tcp_socket.connect(server_addr)
            res = messagebox.showinfo(title='成功提示', message='连接成功！')
            # 修改界面状态
            self.TCPSocketStateLabel['text']="\n\n入侵设备连接成功！\n 设备IP："+self.intrusionIP.get()+"\n 设备端口："+ self.intrusionPort.get()
            self.logoLabel.config(image=self.logo.get('connect'))
            print("Socket successfully connected to port " + str(
                self.intrusionPort.get()) + " on ip " + self.intrusionIP.get())
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            # 修改界面状态
            self.TCPSocketStateLabel['text'] = "\n\n入侵设备连接失败\n\n"
            self.logoLabel.config(image=self.logo.get('disconnect'))

    def disconnectServer(self):
        global tcp_socket
        try:
            if (tcp_socket):
                tcp_socket.shutdown(2)
                self.TCPSocketStateLabel['text'] = "\n\n入侵设备已断开连接\n\n"
                self.logoLabel.config(image=self.logo.get('disconnect'))
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)


    def listen(self):
        try:
            # 监听数据
            while True:
                data = tcp_socket.recv(self.buff_size)
                print(data)
                # 更新excel表
                self.treeview.insert('', index=END,
                                     values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(data))
                self.treeview.treeviewNum+=1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)

    def generateReadDeviceAddressCommand(self, num: int):
        """
        生成读设备地址的指令
        :return: 寻址指令字符串
        """
        try:
            findaddress_str = b''
            findaddress_data = Crc16Add(hex(num)[2:].zfill(2) + "0301000001")
            findaddress_str = findaddress_str + findaddress_data
            return findaddress_str
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)


    def findDevice(self):
        """
        发送单个寻址指令，寻址范围0-255
        :param args: 第一个参数是串口号，后面的参数
        :return: 从机地址列表
        """
        try:
            cycle = 0
            cycle_max = 1
            while (cycle < cycle_max):
                if self.cycleFindDeviceFlag.get() == 0:
                    cycle += 1
                ListAddress = []
                for i in range(1, 256):  # 1-255地址轮询
                    data1 = self.generateReadDeviceAddressCommand(i)
                    #tcp 发送
                    tcp_socket.send(data1)
                    time1 = time.perf_counter()
                    while True:
                        if ((time.perf_counter() - time1) * 1000) > 50:
                            break
                    return_data = tcp_socket.recv(self.buff_size)  # 获取tcp接收数据
                    if return_data:
                        return_data=str(return_data.hex()) #bytes转str
                        # 更新excel表
                        # self.treeview.insert('', index=END,
                        #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                        #                          return_data))
                        # self.treeview.treeviewNum += 1
                        # 更新设备列表框
                        ListAddress += [return_data[0:2]]
                        self.deviceList.set(tuple(ListAddress))
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def findDeviceThread(self):
        t = threading.Thread(target=self.findDevice)
        print(self.cycleFindDeviceFlag.get())
        t.setDaemon(True)
        t.start()

    def changeSelectDevice(self, event):
        """
        :param event: 鼠标双击设备列表，改变当前选中设备
        :return:
        """
        try:
            activeDeviceIndex = self.deviceListBox.curselection()[0]
            self.selectDeviceAddress = self.deviceListBox.get(activeDeviceIndex, activeDeviceIndex)[0]
            self.selectDeviceAddressLable.config(text="当前设备地址：0x" + str(self.selectDeviceAddress))
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def sendReadDeviceAddressCommand(self, num: str):
        try:
            data1 = self.generateReadDeviceAddressCommand(int(num))
            # tcp 发送
            tcp_socket.send(data1)
            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break
            return_data = tcp_socket.recv(self.buff_size)  # 获取tcp接收数据
            if return_data:
                return_data = str(return_data.hex())  # bytes转str
                # 更新excel表
                # self.treeview.insert('', index=END,
                #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                #                          return_data))
                # self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def connectRelay(self, num):
        try:
            send_data = b''
            send_data = send_data + Crc16Add(str(num) + "050000ff00")
            # tcp 发送
            tcp_socket.send(send_data)
            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break
            return_data = tcp_socket.recv(self.buff_size)  # 获取tcp接收数据
            if return_data:
                return_data = str(return_data.hex())  # bytes转str
                # 更新excel表
                # self.treeview.insert('', index=END,
                #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                #                          return_data))
                # self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def disconnectRelay(self, num):
        try:
            send_data = b''
            send_data = send_data + Crc16Add(str(num) + "0500000000")
            # tcp 发送
            tcp_socket.send(send_data)
            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break
            return_data = tcp_socket.recv(self.buff_size)  # 获取tcp接收数据
            if return_data:
                return_data = str(return_data.hex())  # bytes转str
                # 更新excel表
                # self.treeview.insert('', index=END,
                #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                #                          return_data))
                # self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)


class MyTreeview(tk.ttk.Treeview):
    """
    封装treeView
    """
    def __init__(self,master=None,setcolumn=None,**kw):
        # 注意：滚动条是以master为基准，需要单独创一个frame包着treeView，否则滚动条会跑偏
        super().__init__(master,**kw)
        self.master=master
        self.treeviewNum=0 #数据总条数

        self.selectTreeviewItems=None
        self.setcolumn=setcolumn


        self.createWidget()# 初始化子组件


    def createWidget(self):
        """
        创建子组件
        :return:
        """
        # 新建右键功能组件
        # 右键弹出区
        self.button3Menu = tk.Menu(self, tearoff=False)

        items=[""]

        self.button3Menu.add_command(label="删除当前数据", command=self.clear)
        self.button3Menu.add_command(label="清除所有", command=self.clearAll)


        ## 新建excel组件
        # 添加滚动条
        # 滚动条初始化（scrollBar为垂直滚动条，scrollBarx为水平滚动条）
        scrollBar = tk.Scrollbar(self.master)
        scrollBarx = tk.Scrollbar(self.master, orient=HORIZONTAL)

        self.config(yscrollcommand = scrollBar.set)
        self.config(xscrollcommand = scrollBarx.set)


        # 靠右，充满Y轴
        scrollBar.pack(side=RIGHT, fill=Y)
        # 靠下，充满X轴
        scrollBarx.pack(side=BOTTOM, fill=X)
        self.pack(side=TOP, fill=BOTH)

        for i in self.setcolumn:
            # print(i)
            self.column(i, anchor='center')  # 表示列,不显示
            self.heading(i, text=i)  # 显示表头

        self.bind_class("Treeview", "<Button-3>", self.popup)
        self.bind_class("Treeview", "<<TreeviewSelect>>", self.onTreeviewSelect)

        # 而当用户操纵滚动条的时候，自动调用 Treeview 组件的 yview()与xview() 方法
        # 即滚动条与页面内容的位置同步
        scrollBar.config(command=self.yview)
        scrollBarx.config(command=self.xview)

        # button=tk.ttk.Button(self.dataFrame)
        # button.pack(side=TOP,fill=BOTH)


    def onTreeviewSelect(self,event):
        """
        选中多行，返回选中的iid
        :param event:
        :return:
        """
        self.selectTreeviewItems = self.selection()
        # 若要获得值, treeview.get(iid)

    def clear(self):
        """
        清除单条treeView 项
        :return:
        """
        try:
            if self.selectTreeviewItems != None:
                if (messagebox.askokcancel(title='确认删除', message='是否确认删除以下'+str(len(self.selectTreeviewItems))+"条数据", default=messagebox.OK)):
                    # default=messagebox.CANCEL，指定默认焦点位置，另 ABORT/RETRY/IGNORE/OK/CANCEL/YES/NO
                    for i in self.selectTreeviewItems:
                        self.delete(i)
                    res = messagebox.showinfo(title='成功提示', message='删除成功')
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)

    def popup(self, event):
        """
        右击treeview 删除
        :param event:
        :return:
        """
        self.button3Menu.post(event.x_root, event.y_root)

    def clearAll(self):
        try:
            if self.selectTreeviewItems != None:
                if (messagebox.askokcancel(title='确认删除', message='是否确认清空所有数据', default=messagebox.OK)):
                    for item in self.get_children():
                        self.delete(item)
                    res = messagebox.showinfo(title='成功提示', message='清除成功')
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
    def export(self,sheet_name="sheet1"):
        """
        导出单个excel表
        :return:
        """

        # 获取选择窗口
        # 打开选择文件夹
        excel_name = asksaveasfilename(initialfile="Excel01", defaultextension='.xlsx',
                                        filetypes=[('XLSX files', '.xlsx'), ('all files', '.*')])
        try:
            if (excel_name != ""):
                with pd.ExcelWriter(excel_name) as writer:
                    ExporTreeview(writer,self,sheet_name=sheet_name)
                res = messagebox.showinfo(title='成功提示', message='Excel已保存')
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)

if __name__ == "__main__":
    root = Tk()
    root.title("物理控制、检测、入侵一体化平台")
    root.geometry("1600x800+0+0")
    # root.resizable(0,0) #不可调整大小

    # 选项卡组件
    app = Application(master=root)



    root.mainloop()
