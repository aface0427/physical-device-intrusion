#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/30 22:29
# @File    : toooool.py
# @Description :
import math

# 修改字体

import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from pymysql import connect as connect_mysql
import sys
import datetime
import os
import pickle
import re
import socket
from textwrap import fill
import threading
import time
import tkinter as tk
from turtle import width
from urllib import request
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

import bluetooth_server_conn
import tcp_server_conn
from common import ThreadFunc, ExporTreeview, create_ToolTip, SetMenu, findAllChildrens, findTypeChildrens, \
    bindButtonDisable
from modbus_comm import Crc16Add, splitCommand
import configparser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

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
HOST = '10.18.18.92'     # 主机IP地址
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
threshold_old=0
y = 0
time_x = 0
connection = connect_mysql(host='localhost', user='root', password='123456', db='19bdxx')
cursor = connection.cursor()
# 线路潮流表格
sql = "drop table if exists physical_intrusion;"  # 初始化表结构（建表）
cursor.execute(sql)
connection.commit()
sql = "create table physical_intrusion(id INT AUTO_INCREMENT,Time VARCHAR(20),X float(4),PRIMARY KEY(id));"
cursor.execute(sql)
connection.commit()

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
        self.viewNotebook = tk.ttk.Notebook(self)
        self.viewNotebook.pack(side=TOP, fill=BOTH, expand=True)

        viewAngle = ['控制中心', '检测设备']
        # 控制中心视角容器
        self.controlViewFrame = controlViewFrame(self.viewNotebook)
        self.controlViewFrame.pack(fill=BOTH, expand=True)
        # 检测设备视角
        self.detectViewFrame = detectViewFrame(self.viewNotebook)
        self.detectViewFrame.pack(fill=BOTH, expand=True)

        # 关联标签卡选项与视角容器
        self.viewNotebook.add(self.controlViewFrame, text=viewAngle[0])
        self.viewNotebook.add(self.detectViewFrame, text=viewAngle[1])

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


class controlViewFrame(Frame):
    """
    控制中心视角框架
    """

    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw)
        self.master = master

        # 初始化变量
        self.selectDeviceAddress = None  # 选中设备地址
        self.cycleFindDeviceFlag = tk.IntVar(value=0)  # 循环发送标志位s
        self.deviceRespondList = tk.StringVar()  # 可用从机设备列表
        self.deviceOperateList = tk.StringVar()  # 操作设备列表

        # 初始化组件
        self.createWidget()  # 创建子组件

        # 监听端口状态
        # ThreadFunc(self.listenSerialState) #别开 ，开了卡

        self.scanSerial()  # 扫描端口

    ### ----------组件区----------

    def createWidget(self):

        # 配置区
        self.setFrame = tk.LabelFrame(self, text='配置区')
        self.setFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.setFrame_Init()
        # 数据显示区
        self.dataFrame = tk.LabelFrame(self, text='数据收发区', width=100)
        self.dataFrame.grid(row=1, column=0, pady=5, sticky=tk.NSEW)
        self.dataFrame_Init()

        # # 设备列表区
        # self.deviceFrame = tk.LabelFrame(self, text='设备列表区')
        # self.deviceFrame.grid(row=1, column=0, sticky=tk.NSEW)
        # self.deviceFrame_Init()
        # # 数据发送区
        # self.sendFrame = tk.LabelFrame(self, text='指令区')
        # self.sendFrame.grid(row=1, column=1, padx=5, sticky=tk.NSEW)
        # self.sendFrame_Init()
        # print(self.dataFrame.winfo_screenwidth())

        # 绑定按钮，当一个按钮按下时，其他按钮失能
        bindButtonDisable(self, tk.Button, tk.ttk.Button)

    ### ----------方法区----------

    # def deviceFrame_Init(self):
    #     """
    #     设备列表区初始化
    #     :return:
    #     """
    #     padx = 5
    #     pady = 5
    #
    #     ###寻址后相应设备列表
    #     self.deviceRespondFrame = tk.Frame(self.deviceFrame)
    #     self.deviceRespondFrame.pack(side=LEFT, fill=BOTH, pady=pady)
    #
    #     ## 应答设备列表
    #     deviceRespondLabel = ttk.Label(self.deviceRespondFrame, text="应答设备列表", font=("微软雅黑", 13))
    #     deviceRespondLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady * 2)
    #
    #     ## 寻找设备按钮
    #     finddeviceButton = ttk.Button(self.deviceRespondFrame, text="寻找设备",
    #                                   command=lambda: ThreadFunc(self.findDevice))
    #     finddeviceButton.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
    #
    #     self.cycleFindDeviceButton = ttk.Checkbutton(self.deviceRespondFrame, text="循环发送",
    #                                                  variable=self.cycleFindDeviceFlag)
    #     self.cycleFindDeviceButton.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)
    #
    #     ## 设置设备列表窗口
    #     # self.deviceRespondList.set((11, 22, 33, 44, 354, 534, 534, 534, 53, 45, 34, 534, 5, 34, 5, 34, 5, 34, 5, 3453))  # 为变量设置值
    #     # 创建Listbox
    #     self.deviceRespondListBox = tk.Listbox(self.deviceRespondFrame, height=16, listvariable=self.deviceRespondList,
    #                                            selectmode='browse')
    #     self.deviceRespondListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
    #     # self.deviceRespondListBox.bind('<Button-1>', self.changeSelectDevice)
    #
    #     # 一键导入寻找到的设备
    #     # 创建Listbox
    #     self.importDeviceOperateListBox = tk.ttk.Button(self.deviceRespondFrame, command=self.importDeviceOperateList,
    #                                                  text=">>\n一\n键\n导\n入\n>>")
    #     self.importDeviceOperateListBox.grid(row=1, column=3, columnspan=1, padx=padx *2, pady=pady)
    #
    #     ### 操作设备列表，可增减
    #     self.deviceOperateFrame = tk.Frame(self.deviceFrame)
    #     self.deviceOperateFrame.pack(side=LEFT, fill=BOTH)
    #
    #     ## 操作设备列表
    #     deviceOperateLabel = ttk.Label(self.deviceOperateFrame, text="操作设备列表", font=("微软雅黑", 13))
    #     deviceOperateLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
    #
    #     # 添加设备变量
    #     self.deviceOperateAdd = tk.StringVar(value="0x")
    #
    #     deviceOperateAddEntry = tk.Entry(self.deviceOperateFrame, textvariable=self.deviceOperateAdd, width=5)
    #     deviceOperateAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
    #
    #     deviceOperate2Frame = ttk.Frame(self.deviceOperateFrame)
    #     deviceOperate2Frame.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)
    #
    #     deviceOperateAddLabel = ttk.Button(deviceOperate2Frame, text="添加从站", command=self.addOperateDevice)
    #     deviceOperateAddLabel.grid(row=0, column=0, padx=padx, pady=pady)
    #
    #     deviceOperateDeleteLabel = ttk.Button(deviceOperate2Frame, text="删除从站", command=self.deleteOperateDevice)
    #     deviceOperateDeleteLabel.grid(row=0, column=1, padx=padx, pady=pady)
    #
    #     deviceOperateDeleteLabel.grid(row=0, column=3, padx=padx, pady=pady)
    #
    #     ## 设置设备列表窗口
    #     # self.deviceOperateList.set([11,22,33,44])  # 为变量设置值
    #     # 创建Listbox
    #     self.deviceOperateListBox = tk.Listbox(self.deviceOperateFrame, height=16, listvariable=self.deviceOperateList,
    #                                            selectmode='browse')
    #     self.deviceOperateListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
    #     self.deviceOperateListBox.bind('<Button-1>', self.changeSelectDevice)

    # def sendFrame_Init(self):
    #     """
    #     发送区初始化
    #     :return:
    #     """
    #     padx = 5
    #     pady = 5
    #     # 选中设备地址文本
    #     self.selectDeviceAddressLable = ttk.Label(self.sendFrame, text="当前设备地址：", font=('微软雅黑', 12))
    #     self.selectDeviceAddressLable.pack(side=TOP, anchor=W, padx=padx, pady=pady)
    #
    #     # 选中设备操作选项卡
    #
    #     selectDeviceOperationNotebook = tk.ttk.Notebook(self.sendFrame)
    #     selectDeviceOperationNotebook.pack(fill='both', expand=True, padx=padx, pady=pady)
    #     selectDeviceOperation = ['快捷指令', '操作寄存器']  # 选项卡名称
    #     selectDeviceOperation_Quick = Frame(self.sendFrame)
    #     selectDeviceOperation_Quick.pack(fill='both', expand=True)
    #     selectDeviceOperationNotebook.add(selectDeviceOperation_Quick, text=selectDeviceOperation[0])
    #     selectDeviceOperation_Operation = Frame(self.sendFrame)
    #     selectDeviceOperation_Operation.pack(fill='both', expand=True)
    #     selectDeviceOperationNotebook.add(selectDeviceOperation_Operation, text=selectDeviceOperation[1])
    #
    #     # 快捷指令界面
    #     # 寻址指令
    #     sendFrame_findAddress = tk.Frame(selectDeviceOperation_Quick)
    #     sendFrame_findAddress.pack(side=TOP, fill=X, padx=padx, pady=pady)
    #     findAddressLabel = ttk.Label(sendFrame_findAddress, text="寻址指令", font=("微软雅黑", 13))
    #     findAddressLabel.pack(side=LEFT, padx=padx, pady=pady)
    #     ##！！！ 这里没有判断deviceRespondListBox元素是否为0，得改
    #     findAddressButton = tk.ttk.Button(sendFrame_findAddress, text="发送",
    #                                   command=lambda: self.sendReadDeviceAddressCommand(self.selectDeviceAddress))
    #     findAddressButton.pack(side=LEFT, padx=padx, pady=pady)
    #     # 开关继电器指令
    #     sendFrame_operateRelay = tk.Frame(selectDeviceOperation_Quick)
    #     sendFrame_operateRelay.pack(side=TOP, fill=X, padx=padx, pady=pady)
    #     operateRelayLable = ttk.Label(sendFrame_operateRelay, text="操作继电器", font=("微软雅黑", 13))
    #     operateRelayLable.pack(side=LEFT, padx=padx, pady=pady)
    #     connectRelayButton = tk.ttk.Button(sendFrame_operateRelay, text='吸合',
    #                                    command=lambda: self.connectRelay(self.selectDeviceAddress))
    #     connectRelayButton.pack(side=LEFT, padx=padx, pady=pady)
    #     disconnectRelayButton = tk.ttk.Button(sendFrame_operateRelay, text='断开',
    #                                       command=lambda: self.disconnectRelay(self.selectDeviceAddress))
    #     disconnectRelayButton.pack(side=LEFT, padx=padx, pady=pady)
    #
    #     # 快捷指令的请求指令栏和应答指令栏
    #     self.sendFrame_requestOrder = tk.Frame(selectDeviceOperation_Quick)
    #     self.sendFrame_requestOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
    #     self.sendFrame_request = tk.ttk.LabelFrame(self.sendFrame_requestOrder, text="请求栏", width=700, height=60)
    #     self.sendFrame_request.pack(fill="x", expand=True)
    #     self.sendFrame_request.propagate(False)  # 不自动根据子组件改变自身大小
    #     self.sendFrame_requestFrame = tk.Frame(self.sendFrame_request)
    #     self.sendFrame_requestFrame.pack(fill='both')
    #     self.requestCommand = tk.ttk.Label(self.sendFrame_requestFrame, text="此处为请求指令信息", foreground='grey',font=15)
    #     # requestCommand.pack(side=LEFT, padx=padx, pady=pady)
    #     self.requestCommand.pack()
    #     # self.requestCommand.config(text="当前设备地址")
    #
    #     sendFrame_returnOrder = tk.Frame(selectDeviceOperation_Quick)
    #     sendFrame_returnOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
    #     sendFrame_return = tk.ttk.LabelFrame(sendFrame_returnOrder, text="应答栏", width=700, height=60)
    #     sendFrame_return.pack(fill='x', expand=True)
    #     sendFrame_return.propagate(False)
    #     sendFrame_returnFrame = tk.Frame(sendFrame_return)
    #     sendFrame_returnFrame.pack(fill='both')
    #     self.returnCommand = tk.ttk.Label(sendFrame_returnFrame, text="此处为应答指令信息", foreground='grey',font=15)
    #     # returnCommand.pack(side=LEFT, padx=padx, pady=pady)
    #     self.returnCommand.pack()
    #
    #     # 操作寄存器界面
    #     sendFrame_operateAddress = tk.Frame(selectDeviceOperation_Operation)
    #     sendFrame_operateAddress.pack(side=TOP, fill=X, padx=padx, pady=pady)
    #     operateAddressButton = tk.ttk.Button(sendFrame_operateAddress, text="发送请求指令",
    #                                      command=lambda: self.sendOperateDeviceAddressCommand(
    #                                          self.selectDeviceAddress))  # 单独写一个函数
    #     operateAddressButton.pack(side=LEFT, fill=BOTH, padx=padx , pady=pady)
    #
    #     # # 操作寄存器的请求发送框和应答栏
    #     sendFrame_operaterequestOrder = tk.Frame(selectDeviceOperation_Operation)
    #     sendFrame_operaterequestOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
    #     sendFrame_operaterequest = ttk.Label(sendFrame_operaterequestOrder, text="待发送指令", font=("微软雅黑", 12))
    #     sendFrame_operaterequest.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
    #     self.OperateAddEntry = tk.ttk.Entry(sendFrame_operaterequestOrder, width=70)
    #     self.OperateAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
    #
    #     sendFrame_operatereturnOrder = tk.Frame(selectDeviceOperation_Operation)
    #     sendFrame_operatereturnOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
    #     sendFrame_operatereturn = tk.ttk.LabelFrame(sendFrame_operatereturnOrder, text="应答栏", width=700, height=60)
    #     sendFrame_operatereturn.pack(fill='x', expand=True)
    #     sendFrame_operatereturn.propagate(False)
    #     sendFrame_operatereturnFrame = tk.Frame(sendFrame_operatereturn)
    #     sendFrame_operatereturnFrame.pack(fill='both')
    #     self.operatereturnCommand = tk.ttk.Label(sendFrame_operatereturnFrame, text="此处为应答指令信息", foreground='grey',font=15)
    #     self.operatereturnCommand.pack()

    #下拉列表框绑定事件
    def callback(self, event):
        self.deviceOperateAdd.set(self.deviceListCombobox1.get())

    def setFrame_Init(self):
        """
            配置区 初始化
            :return:
        """
        # ************创建下拉列表**************
        padx = 5
        pady = 5
        width = 12
        self.operate1Frame = tk.LabelFrame(self.setFrame)
        self.operate1Frame.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady, ipadx=10)
        self.operate2Frame = tk.LabelFrame(self.setFrame)
        self.operate2Frame.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady, ipadx=10)

        ## 串口号
        self.set1Frame = tk.Frame(self.operate1Frame)
        self.set1Frame.pack(side=TOP, fill=X, padx=10)
        serialportLable = ttk.Label(self.set1Frame, width=width, text="串口号:", font=('微软雅黑', 12))
        serialportLable.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)  # 添加串口号标签
        self.serialport = tk.StringVar()  # 端口号字符串
        self.serialportCombobox = ttk.Combobox(self.set1Frame, width=width, textvariable=self.serialport,
                                               state='readonly', font=('微软雅黑', 12))
        self.serialportCombobox.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)  # 设置其在界面中出现的位置

        ##波特率
        self.set2Frame = tk.Frame(self.operate1Frame)
        self.set2Frame.pack(side=TOP, fill=X, padx=10)
        BaudrateLable = ttk.Label(self.set2Frame, width=width, text="波特率:", font=('微软雅黑', 12))
        BaudrateLable.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)  # 添加波特率标签
        self.baudrate = tk.StringVar()  # 波特率绑定字符串
        self.baudrateCombobox = ttk.Combobox(self.set2Frame, width=width, textvariable=self.baudrate, state='readonly',
                                             font=('微软雅黑', 12))
        self.baudrateCombobox['values'] = (1200, 2400, 4800, 9600, 14400, 19200, 38400, 43000, 57600, 76800, 115200)
        self.baudrateCombobox.current(3)
        self.baudrateCombobox.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)  # 设置其在界面中出现的位置

        ##数据位
        self.set3Frame = tk.Frame(self.operate1Frame)
        self.set3Frame.pack(side=TOP, fill=X, padx=10)
        bytesizeLabel = ttk.Label(self.set3Frame, width=width, text="数据位:", font=('微软雅黑', 12))
        bytesizeLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        self.bytesize = tk.IntVar()  # 波特率绑定字符串
        self.bytesizeCombobox = ttk.Combobox(self.set3Frame, width=width, textvariable=self.bytesize, state='readonly',
                                             font=('微软雅黑', 12))
        self.bytesizeCombobox['values'] = (5, 6, 7, 8)
        self.bytesizeCombobox.current(3)
        self.bytesizeCombobox.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 校验位
        self.set4Frame = tk.Frame(self.operate1Frame)
        self.set4Frame.pack(side=TOP, fill=X, padx=10)
        parityLabel = ttk.Label(self.set4Frame, width=width, text="校验位:", font=('微软雅黑', 12))
        parityLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        self.parity = tk.StringVar()
        self.parityCombobox = ttk.Combobox(self.set4Frame, width=width, textvariable=self.parity, state='readonly',
                                           font=('微软雅黑', 12))
        self.parityCombobox['values'] = ('N', 'E', 'O', 'M', 'S')
        self.parityCombobox.current(0)
        self.parityCombobox.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 停止位
        self.set5Frame = tk.Frame(self.operate1Frame)
        self.set5Frame.pack(side=TOP, fill=X, padx=10)
        stopbitsLabel = ttk.Label(self.set5Frame, width=width, text="停止位:", font=('微软雅黑', 12))
        stopbitsLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        self.stopbits = tk.DoubleVar()
        self.stopbitsCombobox = ttk.Combobox(self.set5Frame, width=width, textvariable=self.stopbits, state='readonly',
                                             font=('微软雅黑', 12))
        self.stopbitsCombobox['values'] = (1, 1.5, 2)
        self.stopbitsCombobox.current(0)
        self.stopbitsCombobox.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        # 串口操作框架
        self.set6Frame = tk.Frame(self.operate1Frame)
        self.set6Frame.pack(side=TOP, fill=X, padx=10)
        # 扫描可用串口按钮
        serialScanButton = tk.ttk.Button(self.set6Frame, text="扫描可用串口", width=13,
                                     command=self.scanSerial)
        serialScanButton.grid(row=0, column=0, columnspan=1, padx=padx, pady=pady * 2)

        # 开启关闭串口按钮
        self.count = 0
        self.serialOpenButton = tk.ttk.Button(self.set6Frame, text="打开串口", width=13,
                                          command=self.openSerial)
        self.serialOpenButton.grid(row=0, column=1, padx=padx * 3, pady=pady * 2)

        self.serialPortStateLabel = tk.ttk.Label(self.set6Frame)
        self.serialPortStateLabel.grid(row=1, column=0, columnspan=2, padx=padx, pady=pady)

        ## 选中设备地址文本
        self.set1Frame = tk.Frame(self.operate2Frame)
        self.set1Frame.pack(side=TOP, fill=X, padx=10, pady=pady)
        self.selectDeviceAddressLable = ttk.Label(self.set1Frame, text="当前设备地址：", font=('微软雅黑', 12))
        self.selectDeviceAddressLable.pack(side=LEFT, padx=padx, pady=pady)
        self.deviceOperateAdd = tk.StringVar(value="")
        self.deviceOperateAddEntry1 = tk.Entry(self.set1Frame, width=7, textvariable=self.deviceOperateAdd)
        self.deviceOperateAddEntry1.pack(side=LEFT, padx=padx, pady=pady, ipady=5)

        ## 寻找设备按钮
        self.set2Frame = tk.Frame(self.operate2Frame)
        self.set2Frame.pack(side=TOP, fill=X, padx=10, pady=pady)
        deviceList1 = ttk.Label(self.set2Frame,text="设备列表", font=('微软雅黑', 12))
        deviceList1.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 设备列表
        self.deviceList = tk.StringVar()  # 绑定字符串
        self.deviceListCombobox1 = ttk.Combobox(self.set2Frame, width=9, state='readonly',
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
        self.set5Frame = tk.Frame(self.operate2Frame)
        self.set5Frame.pack(side=TOP, fill=X, padx=10)
        self.sendFrame_requestOrder = tk.Frame(self.set5Frame)
        self.sendFrame_requestOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
        self.sendFrame_request = tk.ttk.LabelFrame(self.sendFrame_requestOrder, text="请求栏", width=520, height=50)
        self.sendFrame_request.pack(fill="x", expand=True)
        self.sendFrame_request.propagate(False)  # 不自动根据子组件改变自身大小
        self.sendFrame_requestFrame = tk.Frame(self.sendFrame_request)
        self.sendFrame_requestFrame.pack(fill='both')
        self.requestCommand = tk.ttk.Label(self.sendFrame_requestFrame, text="此处为请求指令信息", foreground='grey', font=12)
        self.requestCommand.pack()

        self.set6Frame = tk.Frame(self.operate2Frame)
        self.set6Frame.pack(side=TOP, fill=X, padx=10)
        sendFrame_returnOrder = tk.Frame(self.set6Frame)
        sendFrame_returnOrder.pack(side=TOP, fill=X, padx=padx, pady=pady)
        sendFrame_return = tk.ttk.LabelFrame(sendFrame_returnOrder, text="应答栏", width=520, height=50)
        sendFrame_return.pack(fill='x', expand=True)
        sendFrame_return.propagate(False)
        sendFrame_returnFrame = tk.Frame(sendFrame_return)
        sendFrame_returnFrame.pack(fill='both')
        self.returnCommand = tk.ttk.Label(sendFrame_returnFrame, text="此处为应答指令信息", foreground='grey', font=12)
        self.returnCommand.pack()

    def dataFrame_Init(self):
        """
        数据显示区 初始化
        :return:
        """
        ## 新建excel 组件，记录发送或接收的解析后的指令
        columns = ("序号", "时间", "地址码", "功能码", "数据", "类型")

        self.treeview = MyTreeview(master=self.dataFrame, columnWidth=110, setcolumn=columns, columns=columns,
                                   height=15,
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
            self.count += 1
            # 设置串口开启/关闭状态
            if self.count % 2 == 1:
                self.serialOpenButton.config(text="关闭串口")
                SerialPort.port = self.serialportCombobox.get()
                SerialPort.baudrate = int(self.baudrateCombobox.get())
                SerialPort.bytesize = int(self.bytesizeCombobox.get())
                SerialPort.parity = self.parityCombobox.get()
                SerialPort.stopbits = float(self.stopbitsCombobox.get())
                SerialPort.timeout = 0.1
                SerialPort.writeTimeout = 0.1
                SerialPort.open()
                self.serialPortStateLabel.config(text="串口状态：已打开")
            else:
                self.serialOpenButton.config(text="打开串口")
                if SerialPort.isOpen():
                    SerialPort.close()
                self.serialPortStateLabel.config(text="串口状态：已关闭")

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
                self.serialPortStateLabel.config(text="串口状态：已关闭")

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
            Data1 = self.generateReadDeviceAddressCommand(int(num))
            self.requestCommand.config(text=str(Data1.hex()))
            SerialPort.write(Data1)
            self.treeview.insert('', index=END,
                                 values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                     str(Data1.hex())) + (
                                            "发送",))
            self.treeview.treeviewNum += 1
            time1 = time.perf_counter()
            while True:
                if ((time.perf_counter() - time1) * 1000) > 50:
                    break
            len_return_data = SerialPort.inWaiting()  # 获取缓冲数据（接收数据）长度
            # self.returnCommand.config(len_return_data)
            if len_return_data:
                return_data = SerialPort.read(len_return_data)  # 读取缓冲数据
                # bytes(2进制)转换为hex(16进制)，应注意Python3.7与Python2.7此处转换的不同，并转为字符串后截取所需数据字段，再转为10进制
                str_return_data = str(return_data.hex())
                self.returnCommand.config(text=str_return_data)
                # 更新excel表
                self.treeview.insert('', index=END,
                                     values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                         str_return_data) + ("接收",))
                self.treeview.treeviewNum += 1
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def sendOperateDeviceAddressCommand(self, num: str):  # 新增操作寄存器按钮绑定事件函数
        try:
            findaddress_str = b''  # bytes只能包含ASCII字符
            findaddress_data = Crc16Add(self.OperateAddEntry.get())  # 从输入框获取
            findaddress_str = findaddress_str + findaddress_data
            SerialPort.write(findaddress_str)
            self.treeview.insert('', index=END,
                                 values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                     str(findaddress_str.hex())) + (
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
                self.operatereturnCommand.config(text=str_return_data)
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
                for i in range(1, 8):  # 1-255地址轮询
                    data1 = self.generateReadDeviceAddressCommand(i)
                    self.treeview.insert('', index=END,
                                         values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                             str(data1.hex())) + ("发送",))
                    self.treeview.yview_moveto(1.0)
                    self.treeview.treeviewNum += 1
                    SerialPort.write(data1)
                    time1 = time.perf_counter()
                    time.sleep(0.1)
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
                        self.treeview.yview_moveto(1.0)
                        self.treeview.treeviewNum += 1
                        # 更新设备列表框
                        # ListAddress += [str_return_data[0:2]]
                        # self.deviceRespondList.set(tuple(ListAddress))
                        self.deviceListCombobox1['values'] = ('01', '02', '03', '04', '05', '06')

        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def findDeviceThread(self):
        t = threading.Thread(target=self.findDevice)
        t.setDaemon(True)
        t.start()

    def connectRelay(self, num):
        send_data = b''
        send_data = send_data + Crc16Add(str(num) + "050000ff00")
        SerialPort.write(send_data)

        print(splitCommand(str(send_data.hex())))
        self.treeview.insert('', index=END,
                             values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                 str(send_data.hex())) + ("发送",))
        self.treeview.yview_moveto(1.0)
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
            self.treeview.yview_moveto(1.0)

    def disconnectRelay(self, num):
        try:
            send_data = b''
            send_data = send_data + Crc16Add(str(num) + "0500000000")
            SerialPort.write(send_data)
            self.treeview.insert('', index=END,
                                 values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                                     str(send_data.hex())) + ("发送",))
            self.treeview.treeviewNum += 1
            self.treeview.yview_moveto(1.0)
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
                self.treeview.yview_moveto(1.0)
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)

    def listenSerialState(self):
        try:
            while (True):
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
        global timer_time, t_timer
        super().__init__(master, cnf={}, **kw)
        self.master = master
        self.IntrusionTreeviewNum = 0  # 入侵统计表格条数
        self.FeaturePlotList = []  # 待显示数据列表
        self.thresholdLine = None  # 阈值曲线对象
        self.new_data = []  # 蓝牙传输单个数据
        self.intrusionFlag = 0  # 入侵标志位
        self.detectCount = 0  # 总检测次数
        self.logo = {}  # 连接logo
        self.intrusionBeginTime = None  # 开始入侵时间

        self.createWidget()  # 创建子组件
        t_timer = threading.Timer(timer_time, self.timer_handler)
        t_timer.daemon=True
        t_timer.start()  # 开启定时器，定时显示数据到曲线图
        t_bluetooth_listen = threading.Thread(target=self.thread_server_listen)
        t_bluetooth_listen.daemon=True
        t_bluetooth_listen.start()  # 开启蓝牙数据监听

    ### ----------组件区----------
    def createWidget(self):
        global figureHeight, figureWidth
        padx = 15
        pady = 15

        # 设置区
        self.frame1 = tk.LabelFrame(self)
        self.frame1.pack(side=TOP, padx=5, pady=5)
        self.setFrame = tk.LabelFrame(self.frame1)
        # self.setFrame.grid(row=0, column=0, sticky=NW, pady=5)
        self.setFrame.pack(side=LEFT, padx=5, pady=5)
        # 状态标志
        self.bluetoothStateLabel = tk.Label(self.setFrame, text="\n\n检测设备未连接\n\n", height=1)
        # self.bluetoothStateLabel.grid(row=0, column=0, columnspan=2, padx=padx, pady=pady)
        self.bluetoothStateLabel.pack(side=TOP, anchor=CENTER, fill=X, padx=5, pady=5)
        # 连接logo
        imgSize = 40
        imgName = ['bluetooth_connecting', 'bluetooth_connect', 'bluetooth_disconnect']
        for i in imgName:
            self.logo[i] = ImageTk.PhotoImage(Image.open("resource/" + i + ".png").resize((imgSize, imgSize)))
        self.logoLabel = tk.Label(self.setFrame, image=self.logo['bluetooth_disconnect'])
        self.logoLabel.pack(side=TOP, anchor=CENTER, fill=X)
        # self.logoLabel.grid(row=1, column=0, columnspan=2, padx=padx, pady=pady)

        self.bluetoothStateLabel.config(text="\n\n正在连接到检测设备……\n\n", width=10, height=3)
        self.logoLabel.config(image=self.logo['bluetooth_connecting'])

        ## 检测信息窗口
        detectInformationFrame = tk.LabelFrame(self.setFrame)
        # detectInformationFrame.grid(row=1, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        detectInformationFrame.pack(side=TOP, padx=5, pady=5)
        detectInformationLabel = tk.Label(detectInformationFrame, text="检测信息")
        detectInformationLabel.pack(side=TOP, anchor=W, fill=X)
        self.detectInformationScrolledText = scrolledtext.ScrolledText(detectInformationFrame, wrap=tk.WORD, height=15,
                                                                       width=40)
        self.detectInformationScrolledText.pack(side=TOP, fill=X)

        ## 特征曲线图窗口
        self.featureCurveFrame = tk.LabelFrame(self.frame1)
        # self.featureCurveFrame.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)
        self.featureCurveFrame.pack(side=LEFT, padx=5, pady=10)
        featureCurveLabel = tk.Label(self.featureCurveFrame, text="实时检测特征曲线")
        featureCurveLabel.pack(side=TOP)

        self.fig = plt.figure(figsize=(4.5, 3), dpi=115)  # 创建空画布
        self.ax = plt.subplot(1, 1, 1)
        self.ax.spines['right'].set_color('none')   # 设置右边无边框
        self.ax.spines['top'].set_color('none')     # 设置上边无边框
        plt.xlim((x_bottomlimit, x_toplimit))   # 设置横坐标范围
        plt.ylim((y_bottomlimit, y_toplimit))   # 设置纵坐标范围
        my_x_ticks = np.arange(x_bottomlimit, x_toplimit, x_scale)  # 设置横坐标刻度
        my_y_ticks = np.arange(y_bottomlimit, y_toplimit, y_scale)  # 设置纵坐标刻度
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.featureCurveFrame)  # 空画布显示在界面上
        self.canvas.draw()
        # 包装定位canvas
        self.canvas.get_tk_widget().pack()
        # 将matplotlib的左下角导航工具栏显示出来
        # toolbar = NavigationToolbar2Tk(canvas, root)
        # toolbar.update()

        # 统计入侵信息表格
        # (入侵序号，入侵开始时间，入侵结束时间，持续时间，检测次数）
        ## 新建excel 组件，记录发送或接收的解析后的指令
        self.columns = ("序号", "入侵开始时间", "入侵结束时间", "特征值", "入侵持续时间/秒")
        countIntrusionFrame = Frame(self)
        # countIntrusionFrame.grid(row=1, column=0, columnspan=3, padx=padx, pady=pady)
        countIntrusionFrame.pack(side=TOP, pady=5)

        self.treeview = MyTreeview(master=countIntrusionFrame, columnWidth=175, setcolumn=self.columns,
                                   columns=self.columns, height=15,
                                   show="headings")  # 表格
        self.treeview.pack()

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
        global figureHeight, figureWidth, timer_time, showPoints, t_timer, y, y_old, time_x
        t_timer = threading.Timer(timer_time, self.timer_handler)
        t_timer.daemon = True
        t_timer.start()

        # ************结果显示位置*****************
        # 这里需要添加一个线程监听树莓派传过来的数据
        print("定时器：", self.new_data)

        if len(self.new_data) != 0:
            self.detectCount += 1  # 检测次数+1
            threshold = self.new_data[1]  # 检测阈值
            now_time = datetime.datetime.now()
            time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')
            self.detectInformationScrolledText.insert("end", time_str + ": " + "Get feature value " + str(
                round(self.new_data[0], 3)) + '\n')
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
                        self.treeview.treeviewNum, time_str, '', round(self.new_data[0], 3), 0))
                    self.treeview.yview_moveto(1.0)
                else:
                    self.intrusionFlag = 1
                    self.treeview.set(self.treeview.treeviewNum, column=self.columns[-1],
                                      value=(now_time - self.intrusionBeginTime).seconds)

            else:
                # 结束入侵
                if self.intrusionFlag == 1:
                    # 设置入侵结束时间
                    self.treeview.set(self.treeview.treeviewNum, column=self.columns[2], value=time_str)
                    self.treeview.treeviewNum += 1
                # 标志位清零
                self.intrusionFlag = 0

            # 输出
            self.detectInformationScrolledText.see("end")
            self.FeaturePlotList.append(self.new_data)
            if time_x % 10 == 0:
                plt.cla()   # 清除之前的曲线
                time_x = 0
                self.ax.plot([x_bottomlimit, x_toplimit], [threshold, threshold], color="red", linestyle='--')  # 阈值曲线
                plt.xlim((x_bottomlimit, x_toplimit))  # 设置横坐标范围
                plt.ylim((y_bottomlimit, y_toplimit))  # 设置纵坐标范围
                my_x_ticks = np.arange(x_bottomlimit, x_toplimit, x_scale)  # 设置横坐标刻度
                my_y_ticks = np.arange(y_bottomlimit, y_toplimit, y_scale)  # 设置纵坐标刻度
                plt.xticks(my_x_ticks)
                plt.yticks(my_y_ticks)
                y_old = self.new_data[0]
                y = self.new_data[0]
                self.ax.plot([0, 11], [threshold, threshold], color="red", linestyle='--')
                self.ax.plot([time_x, (time_x + 1)], [y_old, y], color="black")
                self.canvas.draw()
            else:
                y_old = y
                y = self.new_data[0]
                self.ax.plot([time_x, (time_x + 1)], [y_old, y], color="black")     # 连接两点的曲线
                self.canvas.draw()
            time_x = time_x + 1

        # ************存入数据库中*****************
        connection = connect_mysql(host='localhost', user='root', password='123456', db='19bdxx')
        cursor = connection.cursor()
        try:
            if len(self.new_data) > 0:
                if self.new_data[0] > 0:
                    sql_count = "select count(*) from physical_intrusion;"
                    cursor.execute(sql_count)
                    connection.commit()
                    count = cursor.fetchone()[0]
                    tupTime = time.localtime(time.time())
                    stadardTime = time.strftime("%H:%M:%S", tupTime)  # 时：分: 秒
                    if count < 11:
                        sql = "insert into physical_intrusion(Time,X) values(" + "\"" + str(stadardTime) + "\"" + ","+ "\"" + str(float(self.new_data[0])) +"\"" + ");"
                        cursor.execute(sql)
                        connection.commit()
                    else:
                        sql_delete = "delete from physical_intrusion where id = (select id from (select min(id) id from physical_intrusion)t1);"
                        cursor.execute(sql_delete)
                        connection.commit()
                        sql = "insert into physical_intrusion(Time,X) values(" + "\"" + str(
                            stadardTime) + "\"" + "," + "\"" + str(float(self.new_data[0])) + "\"" + ");"
                        # sql = "insert into physical_intrusion(X) values(" + "\"" + str(
                        #     float(self.new_data[0])) + "\"" + ");"
                        cursor.execute(sql)
                        connection.commit()
        except:
            sql = "insert into physical_intrusion(X) values(0);"
            cursor.execute(sql)
            connection.commit()

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
        yaxis_max = 50  # y轴最大值

        y_set = (int)((yaxis_max - y) / (yaxis_max - yaxis_min) * (plot2_height - axisDistance))
        x_set = (int)(plot2_width / (showPoints - 1) * index)
        return x_set, y_set

    # 监听TCP/IP端口线程
    def thread_server_listen(self):
        # global bluetoothPort
        # bt = bluetooth_server_conn.BluetoothConnection()    # 创建蓝牙对象
        # bt.server_bind(bluetoothPort)   # 蓝牙绑定地址端口
        global tcpPort
        tcp = tcp_server_conn.TcpConnection()
        tcp.server_bind(tcpPort)

        while True:
            # print('Waiting to receive data……')

            # client_sock, address = bt.server_sock.accept()  # 阻塞等待连接
            client_sock, address = tcp.server_sock.accept()  # 阻塞等待连接
            self.bluetoothStateLabel.config(text="\n\n连接检测设备成功……\n" + "设备地址：" + str(address) + "\n")
            self.logoLabel.config(image=self.logo['bluetooth_connect'])
            while True:
                self.bluetoothStateLabel.config(
                    text="\n\n正在接收来自检测设备的数据……\n" + "设备地址：" + str(address) + "\n")
                newdata = client_sock.recv(30).decode()  # 不断接收数据，每次接收缓冲区 1024 字节
                if newdata == "":
                    break
                # print("received [%s]" % newdata)
                tcp.data.append(newdata)
                if len(tcp.data) == 2:
                    self.new_data = []
                    for i in range(len(tcp.data)):
                        self.new_data.append(float(tcp.data[i]))
                    tcp.data = []
                # print("new_data", self.new_data)



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
    # print('quit')
    # print("fdas" + str(t_timer))
    # # 关闭定时器进程
    # if t_timer:
    #     t_timer.cancel()
    # print(threading.enumerate())

    plt.close('all')

    root.quit()
    root.destroy()


if __name__ == "__main__":
    style = Style(theme='newtheme')
    print(style.theme)
    root = style.master
    # root = Tk()
    root.title("物理控制、检测一体化平台")
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

    root.protocol("WM_DELETE_WINDOW", quit_me)
    root.mainloop()
