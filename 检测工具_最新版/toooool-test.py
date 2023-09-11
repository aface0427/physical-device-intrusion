#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/30 22:29
# @File    : toooool.py
# @Description :

# 修改字体
import csv
import datetime
import os
import pickle
import re
import socket
import threading
import time
import tkinter as tk
import webbrowser
from random import randint, random
from tkinter import Frame, font,Tk, LEFT, BOTH, END, BOTTOM, X, Y, HORIZONTAL, RIGHT, TOP, W, CENTER, scrolledtext, DISABLED, \
    NORMAL
from tkinter import messagebox, filedialog, simpledialog, colorchooser
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename

import pandas as pd
import serial.tools.list_ports

import serial
from PIL import Image, ImageTk

import bluetooth_server_conn
from common import ThreadFunc, ExporTreeview, create_ToolTip, SetMenu, findAllChildrens, findTypeChildrens, \
    bindButtonDisable, translator
from modbus_comm import Crc16Add, splitCommand
# 全局重要变量
language = 'Chinese'
SerialPort = serial.Serial() #串口对象
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP 连接对象
timer_time = 3  # 曲线图显示数据时间间隔




# 检测视角曲线有关变量
figureHeight = 320  # 实时检测特征曲线图高
figureWidth = 730  # 实时检测特征曲线图宽
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
        # 全局字体
        self.newLanguageWindow = None

        self.tool={}
        self.englishFilename = 'english.pkl'
        self.chineseFilename = 'chinese.pkl'
        # 读取
        if os.path.isfile(self.englishFilename):
            with open(self.englishFilename,'rb') as f:
                self.languageEnglishDict=pickle.load(f)
        else:
            self.languageEnglishDict={} #英文库

        if os.path.isfile(self.chineseFilename):
            with open(self.chineseFilename,'rb') as f:
                self.languageChineseDict=pickle.load(f)
        else:
            self.languageChineseDict={} #中文库


        self.createMenu()  # 创建菜单栏
        self.createToolbar() #创建工具栏
        self.createWidget()  # 创建子组件
        self.setFont()

        # 大西交logo
        self.xjtuLogo = ImageTk.PhotoImage(Image.open("resource/xjtu.jpg"))
        xjtuLogo_label = tk.Label(self, image=self.xjtuLogo)
        xjtuLogo_label.place(relx=0.90, rely=0)

    ### ----------组件区----------
    def setFont(self):
        """
        设置全局字体
        :return:
        """
        global myfont
        childrens=findAllChildrens(self)
        for child in childrens:
            if 'font' in child.config():
                child.config(font=myfont)
            if ('style' in child.config()) and (child.widgetName.split('::')[0]=='ttk'):
                typea=child.widgetName.split('::')[-1].capitalize()
                print('m.T'+typea)
                sb = ttk.Style()
                # if typea=='Labelframe':
                #     typea='LabelFrame'
                if typea[0]=='T':
                    sb.configure('font.' + typea, font=myfont)
                    child.config(style='font.' + typea)
                else:
                    sb.configure('font.T'+typea, font=myfont)
                    child.config(style='font.T' + typea)
        #设置标题

        style = ttk.Style()
        style.configure('TNotebook.Tab', font=myfont)
        style.configure('Treeview.Heading', font=myfont)

    def createMenu(self):
        ## 菜单栏
        menus = ['文件', '设置', '帮助']
        items = [['保存……','全部保存……','-','删除选中数据……','全部删除……'],
                 ['选择语言'],
                 ['使用说明']]
        callbacks = [[self.export, self.exportAll,'-',self.delete,self.deleteAll],
                     [self.changeLanguage],
                     [self.help]]

        self.menubar = SetMenu(master=self.master,setMenus=menus,items=items,callbacks=callbacks)

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
        self.attackViewFrame = attackViewFrame(self.viewNotebook)
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

    def changeLanguage(self):
        """
        修改语言
        :return: 弹出修改语言对话框
        """
        global language

        if language=='Chinese':
            res = messagebox.askokcancel(title='语言设置', message='是否切换语言至英文？', default=messagebox.CANCEL) # default=messagebox.CANCEL，指定默认焦点位置，另 ABORT/RETRY/IGNORE/OK/CANCEL/YES/NO
            if res:
                language='English'

                # 可能出现修改语言的地方
                languageOptionsList = ['message', 'title', 'text', 'label']

                # 英文库中没有存语言时：
                # 目的 保存英文库和更新显示
                if not self.languageEnglishDict:
                    #查找所有子组件
                    widgets=findAllChildrens(self)

                    # print(widgets)


                    #遍历子组件
                    for widget in widgets:
                        # 遍历子组件options
                        languageEnglishOptionsDict = {} # 记录当前组件
                        languageChineseOptionsDict={}
                        for widget_option,widget_value in widget.config().items():

                            if widget_option in languageOptionsList:
                                # print(widget_value[-1])
                                # 中文文本
                                v_chinese=widget_value[-1]

                                # 记录下现在的组件和对应中文文本
                                languageChineseOptionsDict[widget_option] = v_chinese


                                # 翻译
                                if v_chinese=='':
                                    v_english=v_chinese
                                else:
                                    #print(v_chinese)
                                    v_english = translator(v_chinese)
                                    #print(v_english)

                                # 对应组件options修改成英文
                                widget[widget_option]=v_english
                                widget.update()


                                # 记录下现在的组件和对应英文文本
                                languageEnglishOptionsDict[widget_option] = v_english


                        # 保存库
                        if languageEnglishOptionsDict:
                            self.languageEnglishDict[widget]=languageEnglishOptionsDict

                        if languageChineseOptionsDict:
                            self.languageChineseDict[widget]=languageChineseOptionsDict



                    # # 保存库
                    # with open(self.englishFilename, 'wb') as f:
                    #     pickle.dump(self.languageEnglishDict, f)
                    #     # 关闭文件
                    #     f.close()
                    #     print("保存英文库成功！")
                    #
                    # with open(self.chineseFilename, 'wb') as f:
                    #     pickle.dump(self.languageChineseDict, f)
                    #     # 关闭文件
                    #     f.close()
                    #     print("保存中文库成功！")

                else:
                    for widget,options_dict in self.languageEnglishDict.items():
                        for k,v in options_dict.items():
                            widget[k]=v



        elif language=='English':
            res = messagebox.askokcancel(title='Language Set', message='Whether to switch languages to Chinese?', default=messagebox.CANCEL) # default=messagebox.CANCEL，指定默认焦点位置，另 ABORT/RETRY/IGNORE/OK/CANCEL/YES/NO
            if res:
                language='Chinese'
                for widget, options_dict in self.languageChineseDict.items():
                    for k, v in options_dict.items():
                        widget[k] = v
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
            self.newLanguageWindow.resizable(False,False)
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
        self.deviceOperateList=tk.StringVar()  #操作设备列表

        # 初始化组件
        self.createWidget()  # 创建子组件

        # 监听端口状态
        # ThreadFunc(self.listenSerialState) #别开 ，开了卡

        self.scanSerial()  # 扫描端口



    ### ----------组件区----------

    def createWidget(self):

        # 配置区
        self.setFrame = tk.ttk.LabelFrame(self,text='配置区')
        self.setFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.setFrame_Init()
        # 数据显示区
        self.dataFrame = tk.ttk.LabelFrame(self,text='数据区',width=100)
        self.dataFrame.grid(row=0, column=1, padx=5, sticky=tk.NSEW)
        self.dataFrame_Init()

        # 设备列表区
        self.deviceFrame = tk.ttk.LabelFrame(self,text='设备列表区')
        self.deviceFrame.grid(row=1, column=0, sticky=tk.NSEW)
        self.deviceFrame_Init()
        # 数据发送区
        self.sendFrame = tk.ttk.LabelFrame(self,text='指令区')
        self.sendFrame.grid(row=1, column=1, padx=5, sticky=tk.NSEW)
        self.sendFrame_Init()
        # print(self.dataFrame.winfo_screenwidth())


        # 绑定按钮，当一个按钮按下时，其他按钮失能
        bindButtonDisable(self,tk.Button,tk.ttk.Button)

    ### ----------方法区----------

    def deviceFrame_Init(self):
        """
        设备列表区初始化
        :return:
        """
        padx = 5
        pady = 5

        ### 操作设备列表，可增减
        self.deviceOperateFrame = tk.Frame(self.deviceFrame)
        self.deviceOperateFrame.pack(side=LEFT, fill=BOTH)

        ## 操作设备列表
        deviceOperateLabel = ttk.Label(self.deviceOperateFrame, text="操作设备列表")
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
        self.deviceOperateListBox = tk.Listbox(self.deviceOperateFrame, height=16, listvariable=self.deviceOperateList,
                                               selectmode='browse')
        self.deviceOperateListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        self.deviceOperateListBox.bind('<Button-1>', self.changeSelectDevice)

        # 一键导入寻找到的设备
        # 创建Listbox
        self.importDeviceOperateListBox = ttk.Button(self.deviceOperateFrame, command=self.importDeviceOperateList,
                                                     text="<<一键导入<<")
        self.importDeviceOperateListBox.grid(row=1, column=3, columnspan=1, padx=padx, pady=pady)

        ###寻址后相应设备列表
        self.deviceRespondFrame = tk.Frame(self.deviceFrame)
        self.deviceRespondFrame.pack(side=LEFT, fill=BOTH,pady=pady)

        ## 应答设备列表
        deviceRespondLabel = ttk.Label(self.deviceRespondFrame, text="应答设备列表")
        deviceRespondLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady*2)

        ## 寻找设备按钮
        finddeviceButton = ttk.Button(self.deviceRespondFrame, text="寻找设备", command=lambda: ThreadFunc(self.findDevice))
        finddeviceButton.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        self.cycleFindDeviceButton = ttk.Checkbutton(self.deviceRespondFrame, text="循环发送",
                                                     variable=self.cycleFindDeviceFlag)
        self.cycleFindDeviceButton.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 设置设备列表窗口
        # self.deviceRespondList.set((11, 22, 33, 44, 354, 534, 534, 534, 53, 45, 34, 534, 5, 34, 5, 34, 5, 34, 5, 3453))  # 为变量设置值
        # 创建Listbox
        self.deviceRespondListBox = tk.Listbox(self.deviceRespondFrame, height=16, listvariable=self.deviceRespondList,
                                               selectmode='browse')
        self.deviceRespondListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        # self.deviceRespondListBox.bind('<Button-1>', self.changeSelectDevice)
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
        ##！！！ 这里没有判断deviceRespondListBox元素是否为0，得改
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
        width = 15
        ## 串口号
        self.set1Frame=Frame(self.setFrame)
        self.set1Frame.pack()
        serialportLable = ttk.Label(self.set1Frame, width=width, text="串口号:")
        serialportLable.grid(row=0, column=0, sticky=W, padx=padx, pady=pady)  # 添加串口号标签
        self.serialport = tk.StringVar()  # 端口号字符串
        self.serialportCombobox = ttk.Combobox(self.set1Frame, width=width, textvariable=self.serialport,
                                               state='readonly')
        self.serialportCombobox.grid(row=0, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        ##波特率
        BaudrateLable = ttk.Label(self.set1Frame, width=width, text="波特率:")
        BaudrateLable.grid(row=1, column=0, sticky=W, padx=padx, pady=pady)  # 添加波特率标签
        self.baudrate = tk.StringVar()  # 波特率绑定字符串
        self.baudrateCombobox = ttk.Combobox(self.set1Frame, width=width, textvariable=self.baudrate, state='readonly')
        self.baudrateCombobox['values'] = (1200, 2400, 4800, 9600, 14400, 19200, 38400, 43000, 57600, 76800, 115200)
        self.baudrateCombobox.current(3)
        self.baudrateCombobox.grid(row=1, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        ##数据位
        bytesizeLabel = ttk.Label(self.set1Frame, width=width, text="数据位:")
        bytesizeLabel.grid(row=2, column=0, sticky=W, padx=padx, pady=pady)
        self.bytesize = tk.IntVar()  # 波特率绑定字符串
        self.bytesizeCombobox = ttk.Combobox(self.set1Frame, width=width, textvariable=self.bytesize, state='readonly')
        self.bytesizeCombobox['values'] = (5, 6, 7, 8)
        self.bytesizeCombobox.current(3)
        self.bytesizeCombobox.grid(row=2, column=1, padx=padx, pady=pady)

        ## 校验位
        parityLabel = ttk.Label(self.set1Frame, width=width, text="校验位:")
        parityLabel.grid(row=3, column=0, sticky=W, padx=padx, pady=pady)
        self.parity = tk.StringVar()
        self.parityCombobox = ttk.Combobox(self.set1Frame, width=width, textvariable=self.parity, state='readonly')
        self.parityCombobox['values'] = ('N', 'E', 'O', 'M', 'S')
        self.parityCombobox.current(0)
        self.parityCombobox.grid(row=3, column=1, padx=padx, pady=pady)

        ## 停止位
        stopbitsLabel = ttk.Label(self.set1Frame, width=width, text="停止位:")
        stopbitsLabel.grid(row=4, column=0, sticky=W, padx=padx, pady=pady)
        self.stopbits = tk.DoubleVar()
        self.stopbitsCombobox = ttk.Combobox(self.set1Frame, width=width, textvariable=self.stopbits, state='readonly')
        self.stopbitsCombobox['values'] = (1, 1.5, 2)
        self.stopbitsCombobox.current(0)
        self.stopbitsCombobox.grid(row=4, column=1, padx=padx, pady=pady)

        #串口操作框架
        self.serialOperateFrame=Frame(self.set1Frame)
        self.serialOperateFrame.grid(row=5, column=0,columnspan=2,padx=padx, pady=pady)


        # 扫描可用串口按钮
        serialScanButton = tk.ttk.Button(self.serialOperateFrame, text="扫描可用串口", command=self.scanSerial)
        serialScanButton.grid(row=1, column=0, columnspan=1, padx=padx, pady=pady*2)

        # 开启关闭串口按钮
        serialOpenButton = tk.ttk.Button(self.serialOperateFrame, text="打开串口", command=self.openSerial)
        serialOpenButton.grid(row=1, column=1, padx=padx, pady=pady*2)
        serialCloseButton = tk.ttk.Button(self.serialOperateFrame, text="关闭串口", command=self.closeSerial)
        serialCloseButton.grid(row=1, column=2, padx=padx, pady=pady*2)



        # 监听串口状态
        # 端口状态
        self.serialPortStateLabel = tk.Label(self.serialOperateFrame)
        self.serialPortStateLabel.grid(row=7, column=0, columnspan=2, padx=padx, pady=pady)

        # 放个串口灯

    def dataFrame_Init(self):
        """
        数据显示区 初始化
        :return:
        """
        ## 新建excel 组件，记录发送或接收的解析后的指令
        columns = ("序号", "时间", "地址码", "功能码", "数据", "类型")

        self.treeview = MyTreeview(master=self.dataFrame, columnWidth=110,setcolumn=columns, columns=columns, height=15,
                                   show="headings")  # 表格
        self.treeview.pack(side=TOP, fill=BOTH)

        while (self.treeview.treeviewNum < 100):
            p = [self.treeview.treeviewNum, '1999', '03', '01', '00010001']
            self.treeview.insert('', index=END, values=tuple(p))
            self.treeview.treeviewNum += 1

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
            # if SerialPort.isOpen():
            #     SerialPort.close()
            SerialPort.port = self.serialportCombobox.get()
            SerialPort.baudrate = int(self.baudrateCombobox.get())
            SerialPort.bytesize = int(self.bytesizeCombobox.get())
            SerialPort.parity = self.parityCombobox.get()
            SerialPort.stopbits = float(self.stopbitsCombobox.get())
            SerialPort.timeout = 0.1
            SerialPort.writeTimeout =0.1
            SerialPort.open()
            self.serialPortStateLabel.config(text="串口状态：已开启")


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
                        self.treeview.treeviewNum += 1
                        # 更新设备列表框
                        ListAddress += [str_return_data[0:2]]
                        self.deviceRespondList.set(tuple(ListAddress))
        except Exception as e:
            res = messagebox.showerror(title='Error', message=e)
            print(e)

    def findDeviceThread(self):
        t = threading.Thread(target=self.findDevice)
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
            while(True):
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
        self.logo={} #连接logo
        self.intrusionBeginTime = None  # 开始入侵时间



        self.createWidget()  # 创建子组件
        self.t_timer = threading.Timer(timer_time, self.timer_handler)
        self.t_timer.start()  # 开启定时器，定时显示数据到曲线图
        t_bluetooth_listen = threading.Thread(target=self.thread_server_listen)
        t_bluetooth_listen.start()  # 开启蓝牙数据监听

    ### ----------组件区----------
    def createWidget(self):
        global figureHeight, figureWidth
        padx = 15
        pady = 15

        # 设置区
        self.setFrame=tk.LabelFrame(self)
        self.setFrame.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)
        # 状态标志
        self.bluetoothStateLabel = tk.Label(self.setFrame, text="\n\n检测设备未连接\n\n")
        self.bluetoothStateLabel.grid(row=3, column=0, columnspan=2, padx=padx, pady=pady)


        # 连接logo
        imgSize = 50
        imgName = ['bluetooth_connecting', 'bluetooth_connect', 'bluetooth_disconnect']
        for i in imgName:
            self.logo[i] = ImageTk.PhotoImage(Image.open("resource/" + i + ".png").resize((imgSize, imgSize)))
        self.logoLabel = tk.Label(self.setFrame, image=self.logo['bluetooth_disconnect'])
        self.logoLabel.grid(row=5, column=0, columnspan=2, padx=padx, pady=pady)

        self.bluetoothStateLabel.config(text="\n\n正在连接到检测设备……\n\n", width=30)
        self.logoLabel.config(image=self.logo['bluetooth_connecting'])


        ## 检测信息窗口

        detectInformationFrame = tk.LabelFrame(self)
        detectInformationFrame.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)
        detectInformationLabel = tk.Label(detectInformationFrame, text="检测信息",)
        detectInformationLabel.pack(side=TOP, anchor=W, fill=X)
        self.detectInformationScrolledText = scrolledtext.ScrolledText(detectInformationFrame, wrap=tk.WORD,height=20,width=50)
        self.detectInformationScrolledText.pack(side=TOP, fill=X)

        ## 特征曲线图窗口
        featureCurveFrame = tk.LabelFrame(self)
        featureCurveFrame.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)
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
        countIntrusionFrame.grid(row=1, column=0, columnspan=3, padx=padx, pady=pady)

        self.treeview = MyTreeview(master=countIntrusionFrame, columnWidth=300,setcolumn=self.columns, columns=self.columns, height=15,
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

            else:
                # 结束入侵
                if self.intrusionFlag==1:
                    #设置入侵结束时间
                    self.treeview.set(self.treeview.treeviewNum,column=self.columns[2],value=time_str)
                    self.treeview.treeviewNum += 1
                # 标志位清零
                self.intrusionFlag = 0

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
                self.bluetoothStateLabel.config(text="\n\n连接检测设备成功……\n"+"设备地址："+str(address)+"\n")
                self.logoLabel.config(image=self.logo['bluetooth_connect'])
                while True:
                    self.bluetoothStateLabel.config(text="\n\n正在接收来自检测设备的数据……\n"+"设备地址："+str(address)+"\n")
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
        self.buff_size = 8  # 缓冲区大小
        self.selectDeviceAddress = None  # 选中设备地址
        self.cycleFindDeviceFlag = tk.IntVar(value=0)  # 循环发送标志位
        self.deviceRespondList = tk.StringVar()  # 应答从机设备列表
        self.deviceOperateList= tk.StringVar(value=[]) #操纵从机设备列表
        self.needselfRecvFlag=0 #当需要自己发送自己接收时，关闭监听进程
        self.commandList=[]  # 记录指令
        self.data=None

        # 初始化组件
        self.createWidget()  # 创建子组件


    ### ----------组件区----------

    def createWidget(self):

        # 配置区
        self.setFrame = tk.ttk.LabelFrame(self, text='配置区')
        self.setFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.setFrame_Init()
        # 数据显示区
        self.dataFrame = tk.ttk.LabelFrame(self, text='数据收发区')
        self.dataFrame.grid(row=0, column=1, padx=5, sticky=tk.NSEW)
        self.dataFrame_Init()

        # 设备列表区
        self.deviceFrame = tk.ttk.LabelFrame(self, text='设备列表区')
        self.deviceFrame.grid(row=1, column=0, sticky=tk.NSEW)
        self.deviceFrame_Init()
        # 数据发送区
        self.sendFrame = tk.ttk.LabelFrame(self, text='指令区')
        self.sendFrame.grid(row=1, column=1, padx=5, sticky=tk.NSEW)
        self.sendFrame_Init()

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
        ##！！！ 这里没有判断deviceRespondListBox元素是否为0，得改
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
        self.set1Frame=Frame(self.setFrame)
        self.set1Frame.pack()

        intrusionIPLable = ttk.Label(self.set1Frame, width=width, text="入侵设备 IP:")
        intrusionIPLable.grid(row=0, column=0, sticky=W, padx=padx, pady=pady)  # 添加串口号标签
        self.intrusionIP = tk.StringVar(value="192.168.1.90")  # 端口号字符串
        self.intrusionIPCombobox = tk.Entry(self.set1Frame, width=width, textvariable=self.intrusionIP)
        self.intrusionIPCombobox.grid(row=0, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        ## 端口号
        intrusionPortLable = ttk.Label(self.set1Frame, width=width, text="入侵设备 端口:")
        intrusionPortLable.grid(row=1, column=0, sticky=W, padx=padx, pady=pady)  # 添加串口号标签
        self.intrusionPort = tk.IntVar(value=8000)  # 端口号字符串
        self.intrusionPortCombobox = tk.Entry(self.set1Frame, width=width, textvariable=self.intrusionPort)
        self.intrusionPortCombobox.grid(row=1, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        # 连接断开按钮
        self.serialOpenButton = tk.ttk.Button(self.set1Frame, text="连接服务器", command=lambda:ThreadFunc(self.connectServer))
        self.serialOpenButton.grid(row=2, column=0, padx=padx, pady=pady)
        self.serialCloseButton = tk.ttk.Button(self.set1Frame, text="断开连接", command=lambda:ThreadFunc(self.disconnectServer))
        self.serialCloseButton.grid(row=2, column=1, padx=padx, pady=pady)


        # TCP/IP 状态标志
        self.TCPSocketStateLabel=tk.Label(self.set1Frame,text="\n\n入侵设备未连接\n\n")
        self.TCPSocketStateLabel.grid(row=3, column=0, columnspan=2, padx=padx, pady=pady)

        # 监听按钮
        serialScanButton = tk.ttk.Button(self.set1Frame, text="开始监听", command=lambda: ThreadFunc(self.listen))
        serialScanButton.grid(row=4, column=0, columnspan=2, padx=padx, pady=pady)

        # 监听logo
        imgSize=50
        imgName=['connecting','connect','disconnect','listening']
        for i in imgName:
            self.logo[i]=ImageTk.PhotoImage(Image.open("resource/"+i+".png").resize((imgSize,imgSize)))
        self.logoLabel = tk.Label(self.set1Frame,image=None)
        self.logoLabel.grid(row=5, column=0, columnspan=2, padx=padx, pady=pady)

    def dataFrame_Init(self):
        """
        数据显示区 初始化
        :return:
        """
        ## 新建excel 组件，记录发送或接收的解析后的指令
        columns = ("序号", "时间", "地址码", "功能码", "数据段")
        self.treeview = MyTreeview(master=self.dataFrame,setcolumn=columns,columns=columns,height=18, show="headings")  # 表格
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

        ### 操作设备列表，可增减
        self.deviceOperateFrame = tk.Frame(self.deviceFrame)
        self.deviceOperateFrame.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 操作设备列表
        deviceOperateLabel = ttk.Label(self.deviceOperateFrame, text="操作设备列表")
        deviceOperateLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady)

        #添加设备变量
        self.deviceOperateAdd=tk.StringVar(value="0x")

        deviceOperateAddEntry=tk.Entry(self.deviceOperateFrame,textvariable=self.deviceOperateAdd,width=5)
        deviceOperateAddEntry.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        deviceOperate2Frame=ttk.Frame(self.deviceOperateFrame)
        deviceOperate2Frame.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)

        deviceOperateAddLabel = ttk.Button(deviceOperate2Frame,text="添加从站",command=self.addOperateDevice)
        deviceOperateAddLabel.grid(row=0, column=0, padx=padx, pady=pady)

        deviceOperateDeleteLabel = ttk.Button(deviceOperate2Frame, text="删除从站",command=self.deleteOperateDevice)
        deviceOperateDeleteLabel.grid(row=0, column=1,padx=padx, pady=pady)

        ## 设置设备列表窗口
        # self.deviceOperateList.set([11,22,33,44])  # 为变量设置值
        # 创建Listbox
        self.deviceOperateListBox = tk.Listbox(self.deviceOperateFrame, height=16, listvariable=self.deviceOperateList,
                                               selectmode='browse')
        self.deviceOperateListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        self.deviceOperateListBox.bind('<Button-1>', self.changeSelectDevice)

        # 一键导入寻找到的设备
        # 创建Listbox
        self.importDeviceOperateListBox = ttk.Button(self.deviceOperateFrame,command=self.importDeviceOperateList,text="<<一键导入<<")
        self.importDeviceOperateListBox.grid(row=1, column=3, columnspan=1, padx=padx, pady=pady)

        ###寻址后相应设备列表
        self.deviceRespondFrame=tk.Frame(self.deviceFrame)
        self.deviceRespondFrame.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)


        ## 应答设备列表
        deviceRespondLabel = ttk.Label(self.deviceRespondFrame, text="应答设备列表")
        deviceRespondLabel.grid(row=0, column=0, sticky=tk.NSEW, padx=padx, pady=pady*2.5)

        ## 寻找设备按钮
        finddeviceButton = ttk.Button(self.deviceRespondFrame, text="寻找设备", command=lambda :ThreadFunc(self.findDevice))
        finddeviceButton.grid(row=0, column=1, sticky=tk.NSEW, padx=padx, pady=pady)

        self.cycleFindDeviceButton = ttk.Checkbutton(self.deviceRespondFrame, text="循环发送", variable=self.cycleFindDeviceFlag)
        self.cycleFindDeviceButton.grid(row=0, column=2, sticky=tk.NSEW, padx=padx, pady=pady)

        ## 设置设备列表窗口
        # self.deviceRespondList.set((11, 22, 33, 44, 354, 534, 534, 534, 53, 45, 34, 534, 5, 34, 5, 34, 5, 34, 5, 3453))  # 为变量设置值
        # 创建Listbox
        self.deviceRespondListBox = tk.Listbox(self.deviceRespondFrame, height=16, listvariable=self.deviceRespondList, selectmode='browse')
        self.deviceRespondListBox.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW, padx=padx, pady=pady)
        # self.deviceRespondListBox.bind('<Button-1>', self.changeSelectDevice)

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
        t2=self.deviceRespondListBox.get(0,END) #元组
        if (t2):
          t1 =self.deviceOperateListBox.get(0,END)
          new=tuple(set(t2).difference(set(t1))) #差集
          t1=t1+new
          self.deviceOperateList.set(t1)

    def addOperateDevice(self):
        """
        添加从站
        :return:
        """
        #先判断格式：
        regularExpression = r'0x[0-9a-fA-F]{2}'
        newDevice=self.deviceOperateAdd.get()
        if re.fullmatch(regularExpression,newDevice):
            newDevice=newDevice[2:]
            list1=self.deviceOperateListBox.get(0,END) # 元组
            # print(list1)
            if newDevice not in list1:
                list1=list1+(newDevice,)
            self.deviceOperateList.set(list1)
        else:
            res = messagebox.showerror(title='Error', message="输入格式错误")

    def changeSelectDevice(self, event):
        """
        :param event: 鼠标双击设备列表，改变当前选中设备
        :return:
        """
        #非空
        if self.deviceOperateListBox.curselection():
            activeDeviceIndex = self.deviceOperateListBox.curselection()[0]
            # print(activeDeviceIndex)
            self.selectDeviceAddress = self.deviceOperateListBox.get(activeDeviceIndex, activeDeviceIndex)[0]
            self.selectDeviceAddressLable.config(text="当前设备地址：0x" + str(self.selectDeviceAddress))

    def connectServer(self):
        global tcp_socket
        # 连接服务器
        try:
            # 修改界面状态
            self.TCPSocketStateLabel['text']="\n\n入侵设备连接成功！\n 设备IP："+self.intrusionIP.get()+"\n 设备端口："+ str(self.intrusionPort.get())
            self.logoLabel.config(image=self.logo.get('connect'))
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
            # 监听数据
            self.logoLabel.config(image=self.logo.get('listening'))

            # 设置地址01的01继电器吸合
            # 读取地址02的0100（地址寄存器的地址）
            #读取地址01的0000（继电器状态）
            # 读取地址02的0000（继电器状态）
            # 读取地址03的0000（继电器状态）
            # 读取地址04的0000（继电器状态）
            # 读取地址05的0000（继电器状态）
            # list=['01050001ff00','01050001ff00',
            #       '020301000001','0203020002',
            #       '010300000001','0103020300',
            #       '020300000001', '0203020c03',
            #       '030300000001', '0303020000',
            #       '040300000001', '040302030f',
            #       '050300000001', '050302020e',
            #       ]

            # 研究点1 图3
            list=['010300000001','0103020300',
                   '020300000001', '0203020c03',
                   '030300000001', '0303020000',
                   '040300000001', '040302030f',
                   '050300000001', '050302020e',
                  '060300000001', '060302020e',
                  '010300000001', '0103020f0f',
                  '020300000001', '0203020c03',
                  '030300000001', '0303020000']

            # # 研究点1 图4
            # list=['01050001ff00','01050001ff00',
            #
            #       '020300000001', '0203020c03',
            #       '020f00000010020000', '020f00000010',
            #
            #       '010301000001','0103020001',
            #       '040301000001','0403020004',
            #       '020301000001', '0203020002',
            #       '020300000001', '0203020000',
            #       '050300000001', '050302020e',
            #       ]
            #
            # #研究点2 id、地址码监听
            # list=['01050001ff00','01050001ff00',
            #       '020301000001','0203020002',
            #       '010300000001','0103020300',
            #       '020300000001', '0203020c03',
            #       '030300000001', '0303020000',
            #       '040300000001', '040302030f',
            #       '050300000001', '050302020e',
            #       ]
            #
            # # 研究点2 隐私信息监听
            # list = ['01050001ff00', '01050001ff00',
            #         '020301000001', '0203020002',
            #         '010500010000', '010500010000',
            #         '01050001ff00', '01050001ff00',
            #         '010500010000', '010500010000',
            #         '01050001ff00', '01050001ff00',
            #         '040300000001', '040302030f',
            #         '050300000001', '050302020e',
            #         ]

            date = datetime.datetime.now() + datetime.timedelta(days=-30)
            t = date
            self.dataFrame['text'] = '数据收发区'
            for i in range(len(list)):
                self.data=Crc16Add(list[i])

                if i%2==0:
                    # 主
                    self.treeview.insert('', index=END,
                                         values=(self.treeview.treeviewNum, t) + splitCommand(self.data))
                    self.treeview.treeviewNum += 1
                    t = t + datetime.timedelta(seconds=(50 + randint(1, 10)) / 1000)
                else:
                    # 从
                    self.treeview.insert('', index=END,
                                         values=(self.treeview.treeviewNum, t) + splitCommand(
                                             self.data))
                    self.treeview.treeviewNum += 1
                    t = t + datetime.timedelta(seconds=random()*10+1)


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
            self.commandList=[]
            self.needselfRecvFlag =1
            while (cycle < cycle_max):
                if self.cycleFindDeviceFlag.get() == 0:
                    cycle += 1
                for i in range(1, 256):  # 1-255地址轮询
                    data1 = self.generateReadDeviceAddressCommand(i)
                    # print("data1", data1)
                    #tcp 发送
                    tcp_socket.send(data1)
                    # 更新excel表
                    # self.treeview.insert('', index=END,
                    #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                    #                          data1))
                    # self.treeview.treeviewNum += 1

                    time1 = time.perf_counter()
                    while True:
                        if ((time.perf_counter() - time1) * 1000) > 60:
                            break

                    # return_data=tcp_socket.recv(bufsize=self.buff_size)

                    # 对这段事件获取的列表识别
                    ListAddress =[]
                    for return_data in self.commandList:
                        if return_data:
                            return_data = str(return_data.hex())  # bytes转str
                            # # 更新excel表
                            # self.treeview.insert('', index=END,
                            #                      values=(self.treeview.treeviewNum, datetime.datetime.now()) + splitCommand(
                            #                          return_data))
                            # self.treeview.treeviewNum += 1
                            # 更新设备列表框
                            ListAddress += [return_data[0:2]]
                            self.deviceRespondList.set(tuple(ListAddress))


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
    def __init__(self,master=None,columnWidth=120,setcolumn=None,**kw):
        # 注意：滚动条是以master为基准，需要单独创一个frame包着treeView，否则滚动条会跑偏
        super().__init__(master,**kw)
        self.master=master
        self.treeviewNum=0 #数据总条数

        self.selectTreeviewItems=None
        self.setcolumn=setcolumn
        self.columnWidth=columnWidth

        self.setFont()
        self.createWidget()# 初始化子组件


    def setFont(self):
        self.style_head = ttk.Style()



    def createWidget(self):
        """
        创建子组件
        :return:
        """
        # 新建右键功能组件
        # 右键弹出区

        self.items=["保存","-","删除当前数据","清除所有"]
        self.callbacks=[self.export,"-",self.clear,self.clearAll]

        self.button3Menu =SetMenu(self,items=self.items,callbacks=self.callbacks,tearoff=False)


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
            self.column(i, anchor='center',width=self.columnWidth)  # 表示列,不显示
            self.heading(i, text=i)  # 显示表头

        self.bind("<Button-3>", self.popup)
        self.bind("<Button-1>", self.onTreeviewSelect)

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
        print(self.selectTreeviewItems)
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
    root.geometry("1650x800+0+0")
    # root.resizable(0,0) #不可调整大小
    root.iconphoto(False, tk.PhotoImage(file='resource/hacker.png'))

    myfont = font.Font(root=root, family='宋体+Times New Roman', size=12, weight=font.NORMAL, slant=font.ROMAN, underline=0, overstrike=0)
    fontfamilylist = font.families(root=root) #查看字体
    print(fontfamilylist)

    # 选项卡组件
    app = Application(master=root)



    root.mainloop()
