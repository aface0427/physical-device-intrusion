#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/30 22:29
# @File    : toooool.py
# @Description :

# 修改字体
# 树莓派攻击程序


import ttkbootstrap as ttk
from ttkbootstrap import Style

import datetime
import os
import pickle
import re
import socket
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import Frame, font, Tk, LEFT, BOTH, END, BOTTOM, X, Y, HORIZONTAL, RIGHT, TOP, W, CENTER, scrolledtext, \
    DISABLED, \
    NORMAL
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename

import pandas as pd
import serial.tools.list_ports

import serial
from PIL import Image, ImageTk

from common import ThreadFunc, ExporTreeview, create_ToolTip, SetMenu, findAllChildrens
from modbus_comm import Crc16Add, splitCommand

# 全局重要变量
language = 'Chinese'
SerialPort = serial.Serial()  # 串口对象
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 连接对象
timer_time = 3  # 曲线图显示数据时间间隔

# 检测视角曲线有关变量
figureHeight = 340  # 实时检测特征曲线图高
figureWidth = 520  # 实时检测特征曲线图宽
axisDistance = 30  # 坐标轴距离画布边距
# config = configparser.ConfigParser()
# config.read("config.ini", encoding="utf-8")
# bluetoothPort = config.getint('Bluetooth', 'Port')  # 蓝牙端口号
HOST = '192.168.50.144'     # 主机IP地址
PORT = 12356
tcpPort = (HOST, PORT)  # TCP端口号
showPoints = 10  # 每页最多十条数据
x_bottomlimit = 0   # 实时检测特征曲线x轴下限
x_toplimit = 11     # 实时检测特征曲线x轴上限
y_bottomlimit = 0   # 实时检测特征曲线y轴下限
y_toplimit = 41     # 实时检测特征曲线y轴上限限
x_scale = 1     # 实时检测特征曲线x轴刻度
y_scale = 5     # 实时检测特征曲线y轴刻度

# 系统初始化
t_timer = None  # 定时器对象

y_old = 0
y = 0
time_x = 0

class Application(Frame):
    """
    总容器，包括菜单栏、图标、选项卡
    """

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # self.config(bg='red',height=100,width=100)
        self.pack(side='top', fill='both', expand=True)  # 继承
        # 全局字体
        self.newLanguageWindow = None

        self.tool = {}
        self.englishFilename = 'english.pkl'
        self.chineseFilename = 'chinese.pkl'
        # 读取
        if os.path.isfile(self.englishFilename):
            with open(self.englishFilename, 'rb') as f:
                self.languageEnglishDict = pickle.load(f)
        else:
            self.languageEnglishDict = {}  # 英文库

        if os.path.isfile(self.chineseFilename):
            with open(self.chineseFilename, 'rb') as f:
                self.languageChineseDict = pickle.load(f)
        else:
            self.languageChineseDict = {}  # 中文库

        self.createMenu()  # 创建菜单栏
        self.createToolbar()  # 创建工具栏
        self.createWidget()  # 创建子组件
        self.setFont()

        # 大西交logo
        self.xjtuLogo = ImageTk.PhotoImage(Image.open("resource/xjtu_logo.jpg"))
        xjtuLogo_label = tk.Label(self, image=self.xjtuLogo)
        xjtuLogo_label.place(relx=0.84, rely=0.01)

    ### ----------组件区----------
    def setFont(self):
        """
        设置全局字体
        :return:
        """
        global myfont
        childrens = findAllChildrens(self)
        # print("children" + str(childrens))
        for child in childrens:
            # print(type(child))
            if child.config() is not None:
                if 'font' in child.config():
                    child.config(font=myfont)
                if ('style' in child.config()) and (child.widgetName.split('::')[0] == 'ttk'):
                    typea = child.widgetName.split('::')[-1].capitalize()
                    # print('m.T' + typea)
                    sb = ttk.Style()
                    # if typea=='Labelframe':
                    #     typea='LabelFrame'
                    if typea[0] == 'T':
                        sb.configure('font.' + typea, font=myfont)
                        child.config(style='font.' + typea)
                    else:
                        sb.configure('font.T' + typea, font=myfont)
                        child.config(style='font.T' + typea)
        # 设置标题

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=myfont)
        style.configure('Treeview.Heading', font=myfont)

    def createMenu(self):
        ## 菜单栏
        menus = ['文件', '设置', '帮助']
        items = [['保存……', '全部保存……', '-', '删除选中数据……', '全部删除……'],
                 ['选择语言'],
                 ['使用说明']]
        callbacks = [[self.export, self.exportAll, '-', self.delete, self.deleteAll],
                     [self.changeLanguage],
                     [self.help]]

        self.menubar = SetMenu(master=self.master, setMenus=menus, items=items, callbacks=callbacks)

    # 生成工具条
    def createToolbar(self):
        toolframe = tk.Frame(self, height=20, bg='#F7EED6')  # , relief=tk.RAISED)
        toolframe.pack(side=TOP, fill=X)
        imgSize = 20
        toolName = ['save', 'saveAll', 'delete', 'deleteAll']  # 图片文件名
        toolFunc = [self.export, self.exportAll, self.delete, self.deleteAll]  # 图片绑定事件名
        toolButtonTip = ['保存', '全部保存', '删除', '全部删除']  # 图片绑定按钮提示
        toolButton = []  # 图片绑定按钮
        for i in range(len(toolName)):
            self.tool[i] = ImageTk.PhotoImage(Image.open("resource/" + toolName[i] + ".png").resize((imgSize, imgSize)))
            toolButton.append(ttk.Button(toolframe, bootstyle='link', width=20, image=self.tool[i], command=toolFunc[i]))
            toolButton[i].pack(side=LEFT)
            create_ToolTip(toolButton[i], toolButtonTip[i])

    def createWidget(self):
        """
        创建子组件
        :return:
        """

        ## 切换不同视角
        # 标签卡
        # 攻击者视角
        self.attackViewFrame = attackViewFrame(self)
        self.attackViewFrame.pack(fill=BOTH, expand=True)

    ### ----------方法区----------

    def export(self):
        """
        导出单个excel表
        :return:
        """

        # 获取选择窗口
        sn = self.viewNotebook.select().split('.')[-1]
        selectViewTreeView = self.viewNotebook.children[sn].treeview
        sheet_name = self.viewNotebook.tab(self.viewNotebook.select(), option='text')

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
                    for (k, v) in self.viewNotebook.children.items():
                        # print(k,v)
                        selectViewTreeView = v.treeview
                        sheet_name = self.viewNotebook.tab(v, option='text')
                        ExporTreeview(writer, selectViewTreeView, sheet_name=sheet_name)
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

    def changeLanguage(self):
        """
        修改语言
        :return: 弹出修改语言对话框
        """
        pass

    def findLanguageOptions(self):
        """
        查找组件中可能带有修改语言的options
        :return:
        """
        pass

    def createNewLanguageWindow(self):
        """
        产生选择语言窗口
        :return:
        """
        if not self.newLanguageWindow:
            self.newLanguageWindow = tk.Toplevel(self.master)
            self.newLanguageWindow.resizable(False, False)
            self.newLanguageWindow.title("语言设置")
            labelExample = tk.Label(self.newLanguageWindow, text="New Window")
            buttonExample = tk.Button(self.newLanguageWindow, text="New Window button")

            labelExample.pack()
            buttonExample.pack()

    def help(self):
        """
        帮助
        :return: 瞎写几条帮助
        """
        webbrowser.open("http://c.biancheng.net/tkinter/", new=0)
        pass



class attackViewFrame(Frame):
    """
    攻击者视角框架
    """

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw)
        self.master = master

        # 初始化变量
        self.logo = {}  # 存放图片
        self.buff_size = 8  # 缓冲区大小
        self.selectDeviceAddress = None  # 选中设备地址
        self.cycleFindDeviceFlag = tk.IntVar(value=0)  # 循环发送标志位
        self.deviceRespondList = tk.StringVar()  # 应答从机设备列表
        self.deviceOperateList = tk.StringVar(value=[])  # 操纵从机设备列表
        self.needselfRecvFlag = 0  # 当需要自己发送自己接收时，关闭监听进程
        self.commandList = []  # 记录指令
        self.data = None

        # 初始化组件
        self.createWidget()  # 创建子组件

    ### ----------组件区----------

    def createWidget(self):

        # 配置区
        self.setFrame = tk.LabelFrame(self, text='配置区')
        self.setFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.setFrame_Init()
        # 数据显示区
        self.dataFrame = tk.LabelFrame(self, text='数据收发区')
        self.dataFrame.grid(row=1, column=0, sticky=tk.NSEW)
        self.dataFrame_Init()

        # 设备列表区
        # self.deviceFrame = tk.LabelFrame(self, text='设备列表区')
        # self.deviceFrame.grid(row=1, column=0, sticky=tk.NSEW)
        # self.deviceFrame_Init()
        # 数据发送区
        # self.sendFrame = tk.LabelFrame(self, text='指令区')
        # self.sendFrame.grid(row=1, column=1, padx=5, sticky=tk.NSEW)
        # self.sendFrame_Init()

    def sendFrame_Init(self):
        """
        发送区初始化
        :return:
        """
        padx = 5
        pady = 5
        # 选中设备地址文本
        self.selectDeviceAddressLable = ttk.Label(self.sendFrame, text="当前设备地址：", font=('微软雅黑', 12))
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
        findAddressLabel = ttk.Label(sendFrame_findAddress, text="寻址指令", font=('微软雅黑', 12))
        findAddressLabel.pack(side=LEFT, padx=padx, pady=pady)
        ##！！！ 这里没有判断deviceRespondListBox元素是否为0，得改
        findAddressButton = tk.Button(sendFrame_findAddress, text="发送",
                                      command=lambda: self.sendReadDeviceAddressCommand(self.selectDeviceAddress), height=1, width=6, font=('微软雅黑', 15))
        findAddressButton.pack(side=LEFT, padx=padx, pady=pady)
        # 开关继电器指令
        sendFrame_operateRelay = tk.Frame(selectDeviceOperation_Quick)
        sendFrame_operateRelay.pack(side=TOP, fill=X, padx=padx, pady=pady)
        operateRelayLable = ttk.Label(sendFrame_operateRelay, text="操作继电器", font=('微软雅黑', 12))
        operateRelayLable.pack(side=LEFT, padx=padx, pady=pady)
        connectRelayButton = tk.Button(sendFrame_operateRelay, text='吸合',
                                       command=lambda: self.connectRelay(self.selectDeviceAddress), height=1, width=6, font=('微软雅黑', 15))
        connectRelayButton.pack(side=LEFT, padx=padx, pady=pady)
        disconnectRelayButton = tk.Button(sendFrame_operateRelay, text='断开',
                                          command=lambda: self.disconnectRelay(self.selectDeviceAddress), height=1, width=6, font=('微软雅黑', 15))
        disconnectRelayButton.pack(side=LEFT, padx=padx, pady=pady)

    # 下拉列表框绑定事件
    def callback(self, event):
        self.deviceOperateAdd.set(self.deviceListCombobox1.get())

    def setFrame_Init(self):
        """
            配置区 配置网络ip
            :return:
        """
        ### 默认入侵设备是服务器，电脑是客户端
        width = 15
        padx = 5
        pady = 5
        ##  IPf9
        # self.set1Frame = Frame(self.setFrame)
        # self.set1Frame.pack()

        self.operate1Frame = tk.LabelFrame(self.setFrame)
        self.operate1Frame.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady, ipady=20)

        selectDeviceOperationNotebook = tk.ttk.Notebook(self.setFrame)
        selectDeviceOperationNotebook.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
        selectDeviceOperation = ['访问控制区', '应答伪造区']  # 选项卡名称
        self.operate2Frame = Frame(self.setFrame)
        self.operate2Frame.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
        selectDeviceOperationNotebook.add(self.operate2Frame, text=selectDeviceOperation[0])
        self.operate3Frame = Frame(self.setFrame)
        self.operate3Frame.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
        selectDeviceOperationNotebook.add(self.operate3Frame, text=selectDeviceOperation[1])

        ## 串口号
        self.set1Frame = tk.Frame(self.operate1Frame)
        self.set1Frame.pack(side=TOP, fill=X, padx=10)
        intrusionIPLable = ttk.Label(self.set1Frame, width=width, text="入侵设备 IP:", font=('微软雅黑', 12))
        intrusionIPLable.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)  # 添加串口号标签
        self.intrusionIP = tk.StringVar(value="10.1.1.20")  # 端口号字符串
        self.intrusionIPCombobox = ttk.Entry(self.set1Frame, width=13, textvariable=self.intrusionIP, font=15)
        self.intrusionIPCombobox.grid(row=0, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        ## 端口号
        # self.set2Frame = tk.Frame(self.operate1Frame)
        # self.set2Frame.pack(side=TOP, fill=X, padx=10)
        intrusionPortLable = ttk.Label(self.set1Frame, width=width, text="入侵设备 端口:", font=('微软雅黑', 12))
        intrusionPortLable.grid(row=1, column=0, sticky=tk.NSEW, padx=padx, pady=pady)  # 添加串口号标签
        self.intrusionPort = tk.IntVar(value=8080)  # 端口号字符串
        self.intrusionPortCombobox = ttk.Entry(self.set1Frame, width=13, textvariable=self.intrusionPort, font=15)
        self.intrusionPortCombobox.grid(row=1, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        # TCP/IP 状态标志
        self.TCPSocketStateLabel = tk.ttk.Label(self.set1Frame, text="\n\n入侵设备未连接\n\n", foreground='grey',
                                                font=15)
        self.TCPSocketStateLabel.grid(row=2, column=0, columnspan=2, padx=7)

        # 连接断开按钮
        self.set3Frame = tk.Frame(self.operate1Frame)
        self.set3Frame.pack(side=TOP, fill=X, padx=10, pady=30)
        self.serialOpenButton = tk.ttk.Button(self.set3Frame, text="连接服务器",
                                              command=lambda: ThreadFunc(self.connectServer), width=10)
        self.serialOpenButton.grid(row=0, column=0, padx=13, pady=pady)
        self.serialCloseButton = tk.ttk.Button(self.set3Frame, text="断开连接",
                                               command=lambda: ThreadFunc(self.disconnectServer), width=10)
        self.serialCloseButton.grid(row=0, column=1, padx=13, pady=pady)

        # 监听按钮
        serialScanButton = tk.ttk.Button(self.set3Frame, text="开始监听", command=lambda: ThreadFunc(self.listen), width=10)
        serialScanButton.grid(row=0, column=3, columnspan=2, padx=13, pady=pady)

        # 监听logo
        imgSize = 50
        imgName = ['connecting', 'connect', 'disconnect', 'listening']
        for i in imgName:
            self.logo[i] = ImageTk.PhotoImage(Image.open("resource/" + i + ".png").resize((imgSize, imgSize)))
        self.logoLabel = tk.Label(self.set1Frame, image=None)
        self.logoLabel.grid(row=0, column=2, rowspan=2, columnspan=2, padx=10, pady=pady)

        ## 选中设备地址文本
        self.set1Frame = tk.Frame(self.operate2Frame)
        self.set1Frame.pack(side=TOP, fill=X, padx=10, pady=pady)
        self.selectDeviceAddressLable = ttk.Label(self.set1Frame, text="当前设备地址：", font=('微软雅黑', 12))
        self.selectDeviceAddressLable.pack(side=LEFT, padx=padx, pady=pady)
        # self.deviceOperateAdd = tk.StringVar(value="0x")
        # self.deviceOperateAddEntry1 = tk.Entry(self.set1Frame, textvariable=self.deviceOperateAdd, width=7)
        self.deviceOperateAdd = tk.StringVar(value="")
        self.deviceOperateAddEntry1 = tk.Entry(self.set1Frame, width=7, textvariable=self.deviceOperateAdd)
        self.deviceOperateAddEntry1.pack(side=LEFT, padx=padx, pady=pady, ipady=5)

        ## 寻找设备按钮
        self.set2Frame = tk.Frame(self.operate2Frame)
        self.set2Frame.pack(side=TOP, fill=X, padx=10, pady=pady)
        deviceList = ttk.Label(self.set2Frame, text="设备列表", font=('微软雅黑', 12))
        deviceList.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 设备列表
        self.deviceList = tk.StringVar()  # 绑定字符串
        self.deviceListCombobox1 = ttk.Combobox(self.set2Frame, width=5, state='readonly',
                                                font=('微软雅黑', 12))
        self.deviceListCombobox1.grid(row=0, column=2, sticky=tk.NSEW, padx=24.50, pady=pady)
        self.deviceListCombobox1.bind('<<ComboboxSelected>>', self.callback)

        finddeviceButton = ttk.Button(self.set2Frame, text="寻找设备",
                                      command=lambda: ThreadFunc(self.findDevice))
        finddeviceButton.grid(row=0, column=3, sticky=tk.NSEW, padx=10, pady=pady)

        self.cycleFindDeviceButton = ttk.Checkbutton(self.set2Frame, text="循环发送",
                                                     variable=self.cycleFindDeviceFlag)
        self.cycleFindDeviceButton.grid(row=0, column=4, sticky=tk.NSEW, padx=10, pady=pady)

        # 寻址指令
        self.set3Frame = tk.Frame(self.operate2Frame)
        self.set3Frame.pack(side=TOP, fill=X, padx=10)
        findAddressLabel = ttk.Label(self.set3Frame, text="寻址指令", font=("微软雅黑", 13))
        findAddressLabel.pack(side=LEFT, padx=padx, pady=pady)
        ##！！！ 这里没有判断deviceRespondListBox元素是否为0，得改
        findAddressButton = tk.ttk.Button(self.set3Frame, text="发送",
                                          command=lambda: self.sendReadDeviceAddressCommand(self.deviceOperateAddEntry1.get()))
        findAddressButton.pack(side=LEFT, padx=21.50, pady=pady)

        # 开关继电器指令
        self.set4Frame = tk.Frame(self.operate2Frame)
        self.set4Frame.pack(side=TOP, fill=X, padx=10)
        operateRelayLable = ttk.Label(self.set4Frame, text="操作继电器", font=("微软雅黑", 13))
        operateRelayLable.pack(side=LEFT, padx=padx, pady=pady)
        connectRelayButton = tk.ttk.Button(self.set4Frame, text='吸合',
                                           command=lambda: self.connectRelay(self.deviceOperateAddEntry1.get()))
        connectRelayButton.pack(side=LEFT, padx=padx, pady=pady)
        disconnectRelayButton = tk.ttk.Button(self.set4Frame, text='断开',
                                              command=lambda: self.disconnectRelay(self.deviceOperateAddEntry1.get()))
        disconnectRelayButton.pack(side=LEFT, padx=padx, pady=pady)

        # 请求指令栏和应答指令栏
        # self.set5Frame = tk.Frame(self.operate2Frame)
        # self.set5Frame.pack(side=TOP, fill=X, padx=10)
        # self.sendFrame_requestOrder = tk.Frame(self.set5Frame)
        # self.sendFrame_requestOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
        # self.sendFrame_request = tk.ttk.LabelFrame(self.sendFrame_requestOrder, text="请求栏", width=420, height=50)
        # self.sendFrame_request.pack(fill="x", expand=True)
        # self.sendFrame_request.propagate(False)  # 不自动根据子组件改变自身大小
        # self.sendFrame_requestFrame = tk.Frame(self.sendFrame_request)
        # self.sendFrame_requestFrame.pack(fill='both')
        # self.requestCommand = tk.ttk.Label(self.sendFrame_requestFrame, text="此处为请求指令信息", foreground='grey',
        #                                    font=8)
        # self.requestCommand.pack()
        #
        # self.set6Frame = tk.Frame(self.operate2Frame)
        # self.set6Frame.pack(side=TOP, fill=X, padx=10)
        # sendFrame_returnOrder = tk.Frame(self.set6Frame)
        # sendFrame_returnOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
        # sendFrame_return = tk.ttk.LabelFrame(sendFrame_returnOrder, text="应答栏", width=420, height=50)
        # sendFrame_return.pack(fill='x', expand=True)
        # sendFrame_return.propagate(False)
        # sendFrame_returnFrame = tk.Frame(sendFrame_return)
        # sendFrame_returnFrame.pack(fill='both')
        # self.returnCommand = tk.ttk.Label(sendFrame_returnFrame, text="此处为应答指令信息", foreground='grey', font=8)
        # self.returnCommand.pack()

        ## 应答伪造区标签
        set1Frame = tk.Frame(self.operate3Frame)
        set1Frame.pack(side=TOP, fill=X, padx=padx, pady=pady)
        set2Frame = tk.Frame(set1Frame)
        set2Frame.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        sendFrame_answerForgeOrder1 = tk.Frame(set2Frame)
        sendFrame_answerForgeOrder1.pack(side=TOP, fill=X, padx=padx, pady=pady)
        sendFrame_findAddress = ttk.Label(sendFrame_answerForgeOrder1, text="待发送指令", font=('微软雅黑', 12))
        sendFrame_findAddress.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        self.findAddressAddEntry = tk.Entry(sendFrame_answerForgeOrder1, width=17, font=15)
        self.findAddressAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=20)
        sendFrame_answerForgeOrder2 = tk.Frame(set2Frame)
        sendFrame_answerForgeOrder2.pack(side=TOP, fill=X, padx=padx, pady=pady)
        self.sendFrame_answerForge = ttk.Label(sendFrame_answerForgeOrder2, text="应答伪造指令", font=('微软雅黑', 12))
        self.sendFrame_answerForge.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        self.answerOrderAddEntry = tk.Entry(sendFrame_answerForgeOrder2, width=17, font=15)
        self.answerOrderAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=padx)

        # 懒得输入了
        self.findAddressAddEntry.insert(0, "010301000001")
        self.answerOrderAddEntry.insert(0, "000000000")

        # 指令绑定按钮
        orderBindAddLabel = ttk.Button(set1Frame, text="一键绑定", command=self.orderBindOperation)
        orderBindAddLabel.grid(row=0, column=2, rowspan=2, columnspan=2, padx=padx, pady=pady)

        # 应答伪造区列表
        self.answerForgeFrame2 = tk.Frame(self.operate3Frame)
        self.answerForgeFrame2.pack(side=TOP, fill=BOTH)
        columns = ("序号", "时间", "发送指令", "伪造指令")
        self.treeview1 = MyTreeview(master=self.answerForgeFrame2, setcolumn=columns, columns=columns, height=9,
                                    show="headings")  # 表格
        self.treeview1.pack(side=TOP, fill=BOTH)
        self.dic_list = {}

    def dataFrame_Init(self):
        """
        数据显示区 初始化
        :return:
        """
        ## 新建excel 组件，记录发送或接收的解析后的指令
        columns = ("序号", "时间", "地址码", "功能码", "数据段")
        self.treeview = MyTreeview(master=self.dataFrame, setcolumn=columns, columns=columns, height=13,
                                   show="headings")  # 表格
        self.treeview.pack(side=TOP, fill=BOTH)

        # while (self.treeview.treeviewNum < 100):
        #     p = [self.treeview.treeviewNum, '1999', '03', '01', '00010001']
        #     self.treeview.insert('', index=END, values=tuple(p))
        #     self.treeview.treeviewNum += 1

    ### ----------函数区----------
    def deviceFrame_Init(self):
        """
        设备列表区初始化
        :return:
        """
        padx = 5
        pady = 5

        selectDeviceOperationNotebook = tk.ttk.Notebook(self.deviceFrame)
        selectDeviceOperationNotebook.pack(fill='both', expand=True, padx=padx, pady=pady)
        selectDeviceOperation = ['访问控制区', '应答伪造区']  # 选项卡名称
        selectDeviceOperation_Control = Frame(self.deviceFrame)
        selectDeviceOperation_Control.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Control, text=selectDeviceOperation[0])
        selectDeviceOperation_Return = Frame(self.deviceFrame)
        selectDeviceOperation_Return.pack(fill='both', expand=True)
        selectDeviceOperationNotebook.add(selectDeviceOperation_Return, text=selectDeviceOperation[1])

        ###寻址后相应设备列表
        self.deviceRespondFrame = tk.Frame(selectDeviceOperation_Control)
        self.deviceRespondFrame.pack(side=LEFT, fill=BOTH, pady=pady)

        ## 应答设备列表
        deviceRespondLabel = ttk.Label(self.deviceRespondFrame, text="应答设备列表", font=('微软雅黑',12))
        deviceRespondLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady * 2)

        ## 寻找设备按钮
        finddeviceButton = ttk.Button(self.deviceRespondFrame, text="寻找设备",
                                      command=lambda: ThreadFunc(self.findDevice))
        finddeviceButton.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        self.cycleFindDeviceButton = ttk.Checkbutton(self.deviceRespondFrame, text="循环发送",
                                                     variable=self.cycleFindDeviceFlag)
        self.cycleFindDeviceButton.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 设置设备列表窗口
        # self.deviceRespondList.set((11, 22, 33, 44, 354, 534, 534, 534, 53, 45, 34, 534, 5, 34, 5, 34, 5, 34, 5, 3453))  # 为变量设置值
        # 创建Listbox
        self.deviceRespondListBox = tk.Listbox(self.deviceRespondFrame, height=15, listvariable=self.deviceRespondList,
                                               selectmode='browse')
        self.deviceRespondListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        # self.deviceRespondListBox.bind('<Button-1>', self.changeSelectDevice)

        # 一键导入寻找到的设备
        # 创建Listbox
        self.importDeviceOperateListBox = ttk.Button(self.deviceRespondFrame, command=self.importDeviceOperateList,
                                                     text=">>\n一\n键\n导\n入\n>>")
        self.importDeviceOperateListBox.grid(row=1, column=3, columnspan=1, padx=padx * 2, pady=pady)

        ### 操作设备列表，可增减
        self.deviceOperateFrame = tk.Frame(selectDeviceOperation_Control)
        self.deviceOperateFrame.pack(side=LEFT, fill=BOTH)

        ## 操作设备列表
        deviceOperateLabel = ttk.Label(self.deviceOperateFrame, text="操作设备列表", font=('微软雅黑',12))
        deviceOperateLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)

        # 添加设备变量
        self.deviceOperateAdd = tk.StringVar(value="0x")

        deviceOperateAddEntry = tk.Entry(self.deviceOperateFrame, textvariable=self.deviceOperateAdd, width=5)
        deviceOperateAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        deviceOperate2Frame = ttk.Frame(self.deviceOperateFrame)
        deviceOperate2Frame.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)

        deviceOperateAddLabel = ttk.Button(deviceOperate2Frame, text="添加从站", command=self.addOperateDevice)
        deviceOperateAddLabel.grid(row=0, column=0, padx=padx, pady=pady)

        deviceOperateDeleteLabel = ttk.Button(deviceOperate2Frame, text="删除从站", command=self.deleteOperateDevice)
        deviceOperateDeleteLabel.grid(row=0, column=1, padx=padx, pady=pady)

        deviceOperateDeleteLabel.grid(row=0, column=3, padx=padx, pady=pady)

        ## 设置设备列表窗口
        # self.deviceOperateList.set([11,22,33,44])  # 为变量设置值
        # 创建Listbox
        self.deviceOperateListBox = tk.Listbox(self.deviceOperateFrame, height=15, listvariable=self.deviceOperateList,
                                               selectmode='browse')
        self.deviceOperateListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        self.deviceOperateListBox.bind('<Button-1>', self.changeSelectDevice)

        ###应答伪造区
        self.answerForgeFrame = tk.Frame(selectDeviceOperation_Return)
        self.answerForgeFrame.pack(side=LEFT, fill=BOTH, pady=pady)

        ## 应答伪造区标签
        sendFrame_answerForgeOrder1 = tk.Frame(self.answerForgeFrame)
        sendFrame_answerForgeOrder1.pack(side=TOP, fill=X, padx=padx, pady=pady)
        sendFrame_findAddress = ttk.Label(sendFrame_answerForgeOrder1, text="待发送指令", font=('微软雅黑', 12))
        sendFrame_findAddress.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        sendFrame_answerForgeOrder2 = tk.Frame(self.answerForgeFrame)
        sendFrame_answerForgeOrder2.pack(side=TOP, fill=X, padx=padx)
        self.findAddressAddEntry = tk.Entry(sendFrame_answerForgeOrder2, width=30, font=15)
        self.findAddressAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=padx)
        sendFrame_answerForgeOrder3 = tk.Frame(self.answerForgeFrame)
        sendFrame_answerForgeOrder3.pack(side=TOP, fill=X, padx=padx, pady=pady)
        self.sendFrame_answerForge = ttk.Label(sendFrame_answerForgeOrder3, text="应答伪造指令", font=('微软雅黑', 12))
        self.sendFrame_answerForge.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        sendFrame_answerForgeOrder4 = tk.Frame(self.answerForgeFrame)
        sendFrame_answerForgeOrder4.pack(side=TOP, fill=X, padx=padx)
        self.answerOrderAddEntry = tk.Entry(sendFrame_answerForgeOrder4, width=30, font=15)
        self.answerOrderAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=padx)

        # 懒得输入了
        self.findAddressAddEntry.insert(0, "010301000001")
        self.answerOrderAddEntry.insert(0, "000000000")

        # 指令绑定按钮
        sendFrame_answerForgeOrder5 = tk.Frame(self.answerForgeFrame)
        sendFrame_answerForgeOrder5.pack(side=TOP, fill=X, padx=padx, pady=pady)
        orderBindAddLabel = ttk.Button(sendFrame_answerForgeOrder5, text="一键绑定", command=self.orderBindOperation)
        orderBindAddLabel.grid(row=0, column=0, padx=padx, pady=pady)

        # 应答伪造区列表
        self.answerForgeFrame1 = tk.Frame(selectDeviceOperation_Return, width=50)
        self.answerForgeFrame1.pack(side=LEFT, fill=BOTH, pady=pady)
        self.answerForgeFrame2 = tk.Frame(selectDeviceOperation_Return)
        self.answerForgeFrame2.pack(side=LEFT, fill=BOTH, pady=pady)
        columns = ("序号", "时间", "发送指令", "伪造指令")
        self.treeview1 = MyTreeview(master=self.answerForgeFrame2, setcolumn=columns, columns=columns, height=16,
                                    show="headings")  # 表格
        self.treeview1.pack(side=TOP, fill=BOTH)
        self.dic_list = {}

    def orderBindOperation(self):
        """
        指令绑定
        :return:
        """
        try:
            findaddress_str1 = b''  # bytes只能包含ASCII字符
            findaddress_data1 = Crc16Add(self.findAddressAddEntry.get())  # 从输入框获取
            findaddress_str1 = findaddress_str1 + findaddress_data1
            findaddress_str2 = b''  # bytes只能包含ASCII字符
            findaddress_data2 = Crc16Add(self.answerOrderAddEntry.get())  # 从输入框获取
            findaddress_str2 = findaddress_str2 + findaddress_data2

            # 更新excel表
            self.treeview1.insert('', index=END, values=(self.treeview1.treeviewNum, datetime.datetime.now()) + (
            str(findaddress_str1.hex()),) + (str(findaddress_str2.hex()),))
            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break
            self.treeview1.treeviewNum += 1

            # 更新列表字典
            dic = {self.findAddressAddEntry.get(): self.answerOrderAddEntry.get()}
            self.dic_list.update(dic)

        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def deleteOperateDevice(self):
        """
        删除从站
        :return:
        """
        # 非空
        if self.deviceOperateListBox.curselection():
            activeDeviceIndex = self.deviceOperateListBox.curselection()[0]
            # print(activeDeviceIndex)
            self.deviceOperateListBox.delete(activeDeviceIndex)
            self.selectDeviceAddress = None
            self.selectDeviceAddressLable.config(text="当前设备地址：")

    def importDeviceOperateList(self):
        # 获得寻址设备列表
        t2 = self.deviceRespondListBox.get(0, END)  # 元组
        if (t2):
            t1 = self.deviceOperateListBox.get(0, END)
            new = tuple(set(t2).difference(set(t1)))  # 差集
            t1 = t1 + new
            self.deviceOperateList.set(t1)

    def addOperateDevice(self):
        """
        添加从站
        :return:
        """
        # 先判断格式：
        regularExpression = r'0x[0-9a-fA-F]{2}'
        newDevice = self.deviceOperateAdd.get()
        if re.fullmatch(regularExpression, newDevice):
            newDevice = newDevice[2:]
            list1 = self.deviceOperateListBox.get(0, END)  # 元组
            # print(list1)
            if newDevice not in list1:
                list1 = list1 + (newDevice,)
            self.deviceOperateList.set(list1)
        else:
            res = messagebox.showerror(title='Error', message="输入格式错误")

    def changeSelectDevice(self, event):
        """
        :param event: 鼠标双击设备列表，改变当前选中设备
        :return:
        """
        # 非空
        if self.deviceOperateListBox.curselection():
            activeDeviceIndex = self.deviceOperateListBox.curselection()[0]
            # print(activeDeviceIndex)
            self.selectDeviceAddress = self.deviceOperateListBox.get(activeDeviceIndex, activeDeviceIndex)[0]
            self.selectDeviceAddressLable.config(text="当前设备地址：0x" + str(self.selectDeviceAddress))

    def connectServer(self):
        global tcp_socket
        # 连接服务器
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 连接对象
            # 修改界面状态
            self.TCPSocketStateLabel['text'] = "\n\n正在连接到入侵设备，请稍候……\n\n"
            self.logoLabel.config(image=self.logo.get('connecting'))

            server_addr = (self.intrusionIP.get(), self.intrusionPort.get())
            tcp_socket.connect(server_addr)
            res = messagebox.showinfo(title='成功提示', message='连接成功！')
            # 修改界面状态
            self.TCPSocketStateLabel[
                'text'] = "\n\n入侵设备连接成功！\n 设备IP：" + self.intrusionIP.get() + "\n 设备端口：" + str(
                self.intrusionPort.get())
            self.logoLabel.config(image=self.logo.get('connect'))
            # 不能再连了
            self.serialOpenButton.config(state=DISABLED)
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            # 修改界面状态
            self.TCPSocketStateLabel['text'] = "\n\n入侵设备连接失败\n\n"
            self.logoLabel.config(image=self.logo.get('disconnect'))

    def disconnectServer(self):
        global tcp_socket
        try:
            # 直接暴力断开就完了，报异常不给他看
            if (tcp_socket):
                tcp_socket.shutdown(2)
                tcp_socket.close()
                self.TCPSocketStateLabel['text'] = "\n\n入侵设备已断开连接\n\n"
                self.logoLabel.config(image=self.logo.get('disconnect'))
                self.serialOpenButton.config(state=NORMAL)
        except Exception as e:
            pass
            # res = messagebox.showerror(title='Error', message=e)

    def listen(self):
        # try:
        # 监听数据
        self.logoLabel.config(image=self.logo.get('listening'))
        while True:
            self.data = tcp_socket.recv(self.buff_size)
            print("接收到:" + str(datetime.datetime.now()))

            for a in self.dic_list.keys():
                findaddress_str1 = b''  # bytes只能包含ASCII字符
                findaddress_data1 = Crc16Add(a)
                findaddress_str1 = findaddress_str1 + findaddress_data1
                if str(findaddress_str1.hex()) == str(self.data.hex()):
                    findaddress_str2 = b''  # bytes只能包含ASCII字符
                    findaddress_data2 = Crc16Add(self.dic_list[a])
                    findaddress_str2 = findaddress_str2 + findaddress_data2

                    tcp_socket.send(findaddress_str2)

            # if self.data:
            #     tcp_socket.send(b'' + Crc16Add('000000000'))
            #     print("发送完:" + str(datetime.datetime.now()))

            # print(data)
            # 更新excel表
            self.treeview.insert('', index=END,
                                 values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(self.data))
            self.treeview.treeviewNum += 1

            if self.needselfRecvFlag == 1:
                self.commandList.append(self.data)

    # except Exception as e:
    #     res = messagebox.showerror(title='Error', message=e)

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
            self.commandList = []
            self.needselfRecvFlag = 1
            while (cycle < cycle_max):
                if self.cycleFindDeviceFlag.get() == 0:
                    cycle += 1
                for i in range(1, 256):  # 1-255地址轮询
                    data1 = self.generateReadDeviceAddressCommand(i)
                    # print("data1", data1)
                    # tcp 发送
                    tcp_socket.send(data1)
                    # 更新excel表
                    # self.treeview.insert('', index=END,
                    #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                    #                          data1))
                    # self.treeview.treeviewNum += 1

                    time1 = time.perf_counter()
                    time.sleep(0.1)
                    while True:
                        if ((time.perf_counter() - time1) * 1000) > 60:
                            break

                    # return_data=tcp_socket.recv(bufsize=self.buff_size)

                    # 对这段事件获取的列表识别
                    ListAddress = []
                    for return_data in self.commandList:
                        if return_data:
                            return_data = str(return_data.hex())  # bytes转str
                            # # 更新excel表
                            # self.treeview.insert('', index=END,
                            #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                            #                          return_data))
                            # self.treeview.treeviewNum += 1
                            # 更新设备列表框
                            self.deviceListCombobox1['values'] = ('01', '02', '03', '04', '05', '06')

            self.needselfRecvFlag = 0
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)

    def sendReadDeviceAddressCommand(self, num: str):
        try:
            data1 = self.generateReadDeviceAddressCommand(int(num))

            # tcp 发送
            tcp_socket.send(data1)
            # # 更新excel表
            # self.treeview.insert('', index=END,
            #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
            #                          data1))

            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break

            # return_data = self.data

            # if return_data:
            #     return_data = str(return_data.hex())  # bytes转str
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
            # # 更新excel表
            # self.treeview.insert('', index=END,
            #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
            #                          send_data))

            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break

            # return_data = self.data
            #
            # if return_data:
            #     return_data = str(return_data.hex())  # bytes转str
            #     # 更新excel表
            #     self.treeview.insert('', index=END,
            #                          values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
            #                              return_data))
            #     self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def disconnectRelay(self, num):
        try:
            send_data = b''
            send_data = send_data + Crc16Add(str(num) + "0500000000")
            # tcp 发送
            tcp_socket.send(send_data)
            # # 更新excel表
            # self.treeview.insert('', index=END,
            #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
            #                          send_data))

            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break

            # return_data = tcp_socket.recv(self.buff_size)  # 非阻塞！！！获取tcp接收数据
            #
            # if return_data:
            #     return_data = str(return_data.hex())  # bytes转str
            #     # 更新excel表
            #     self.treeview.insert('', index=END,
            #                          values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
            #                              return_data))
            #     self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)


class MyTreeview(tk.ttk.Treeview):
    """
    封装treeView
    """

    def __init__(self, master=None, columnWidth=120, setcolumn=None, **kw):
        # 注意：滚动条是以master为基准，需要单独创一个frame包着treeView，否则滚动条会跑偏
        super().__init__(master, **kw)
        self.master = master
        self.treeviewNum = 0  # 数据总条数

        self.selectTreeviewItems = None
        self.setcolumn = setcolumn
        self.columnWidth = columnWidth

        # self.setFont()
        self.createWidget()  # 初始化子组件

    def setFont(self):
        self.style_head = ttk.Style()

    def createWidget(self):
        """
        创建子组件
        :return:
        """
        # 新建右键功能组件
        # 右键弹出区

        self.items = ["保存", "-", "删除当前数据", "清除所有"]
        self.callbacks = [self.export, "-", self.clear, self.clearAll]

        self.button3Menu = SetMenu(self, items=self.items, callbacks=self.callbacks, tearoff=False)

        ## 新建excel组件
        # 添加滚动条
        # 滚动条初始化（scrollBar为垂直滚动条，scrollBarx为水平滚动条）
        scrollBar = tk.Scrollbar(self.master)
        scrollBarx = tk.Scrollbar(self.master, orient=HORIZONTAL)

        self.config(yscrollcommand=scrollBar.set)
        self.config(xscrollcommand=scrollBarx.set)

        # 靠右，充满Y轴
        scrollBar.pack(side=RIGHT, fill=Y)
        # 靠下，充满X轴
        scrollBarx.pack(side=BOTTOM, fill=X)
        self.pack(side=TOP, fill=BOTH)

        for i in self.setcolumn:
            # print(i)
            self.column(i, anchor='center', width=self.columnWidth)  # 表示列,不显示
            self.heading(i, text=i)  # 显示表头

        self.bind("<Button-3>", self.popup)
        self.bind("<ButtonRelease-1>", self.onTreeviewSelect)

        # 而当用户操纵滚动条的时候，自动调用 Treeview 组件的 yview()与xview() 方法
        # 即滚动条与页面内容的位置同步
        scrollBar.config(command=self.yview)
        scrollBarx.config(command=self.xview)

        # button=tk.ttk.Button(self.dataFrame)
        # button.pack(side=TOP,fill=BOTH)

    def onTreeviewSelect(self, event):
        """
        选中多行，返回选中的iid
        :param event:
        :return:
        """
        self.selectTreeviewItems = self.selection()
        print(self.selectTreeviewItems)
        # 若要获得值, treeview.get(iid)

    def clear(self):
        """
        清除单条treeView 项
        :return:
        """
        try:
            if self.selectTreeviewItems != None:
                if (messagebox.askokcancel(title='确认删除',
                                           message='是否确认删除以下' + str(len(self.selectTreeviewItems)) + "条数据",
                                           default=messagebox.OK)):
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

    def export(self, sheet_name="sheet1"):
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
                    ExporTreeview(writer, self, sheet_name=sheet_name)
                res = messagebox.showinfo(title='成功提示', message='Excel已保存')
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)


def quit_me():
    global root
    print('quit')
    print("fdas" + str(t_timer))
    # 关闭定时器进程
    if t_timer:
        t_timer.cancel()
    print(threading.enumerate())

    root.quit()
    root.destroy()


if __name__ == "__main__":
    style = Style(theme='newtheme')
    root = style.master
    # root = Tk()
    root.title("物理入侵平台")
    root.geometry("915x760+0+0")
    # root.resizable(0,0) #不可调整大小
    root.iconphoto(False, tk.PhotoImage(file='resource/hacker.png'))

    # 字体设置
    myfont = font.Font(root=root, family='宋体+Times New Roman', size=12, weight=font.NORMAL, slant=font.ROMAN,
                       underline=0, overstrike=0)
    # fontfamilylist = font.families(root=root) #查看字体
    # print(fontfamilylist)

    # 选项卡组件
    app = Application(master=root)

    # root.protocol("WM_DELETE_WINDOW", quit_me)
    root.mainloop()
