import datetime
import socket
import time
import serial
from binascii import *
import crcmod
import threading
# from mttkinter import mtTkinter as tk
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import serial.tools.list_ports
from PIL import Image, ImageTk
import bluetooth_server_conn
import sys  # 获取输入参数
import os  # 使用命令行

import modbus_comm

logo_x = 50
logo_y = 130
kongjian_weiyi = 430
kongjian_weiyi_2 = 250

new_data = []  # 包含时间和特征值的二元列表
port = 14
threshold=0
attack_receive_Window=None



# 显示线程
def thread_2():
    global Information_Window, SerialPort, Receive_Window, address_list
    global GUI, main_GUI, new_data, data_list, Information_Window, plot2_height, axis_distance, plot2_width, Plot, Plot2, language, detect_information_Window, attack_receive_Window
    SerialPort = serial.Serial()
    SerialPort.port = 'COM3'
    SerialPort.baudrate = 9600
    SerialPort.timeout = 1
    SerialPort.open()

    #已实现
    GUI = tk.Tk()  # 父容器
    # main_GUI.resizable(0,0) #不可调整大小
    GUI.title("Serial Tool")  # 父容器标题
    GUI.geometry("1050x780")  # 父容器大小

    # 已实现
    # 西交logo位置
    load = Image.open("resource/xjtu.jpg")
    img = ImageTk.PhotoImage(load)
    xjtu = tk.Label(GUI, image=img)
    xjtu.place(x=20, y=3)

    def change_language():
        global language
        # 英语
        if language == '中文':
            language = 'English'
            language_button['text'] = '中文'
            Information['text'] = "Operation information"
            detect_information['text'] = "Detect information"
            option['text'] = "Option"
            choise_language['text'] = 'Please select language:'
            Serial_port_number['text'] = 'Serial port:'
            Baud_rate['text'] = 'Baud rate:'
            Module_address['text'] = 'Slave address:'
            Scan_port['text'] = 'Scan port'
            Stop_send['text'] = 'Stop send'
            find_device['text'] = 'Find device'
            Open_light['text'] = 'Open'
            Close_light['text'] = 'Close'
            Send_signal['text'] = 'Send signal'
            Send['text'] = 'Send instruction'
            Send_button['text'] = 'Send'
            attack_receive['text'] = 'Receive area'
            Receive['text'] = 'Receive area'
            Device_display['text'] = 'Analog display'
            Result_display['text'] = 'Result display'
            switch['text'] = 'Shortcuts'
            for i in list(Device_display_button):
                if i.relay_state_flag:
                    i.button['text'] = 'Close'
                else:
                    i.button['text'] = 'Open'
            notebook.tab(0, text="Master_view")
            notebook.tab(1, text='Attack_view')
            notebook.tab(2, text='Detct_view')
        # 中文
        elif language == 'English':
            language = '中文'
            language_button['text'] = 'English'
            Information['text'] = "操作信息"
            detect_information['text'] = "检测信息"
            option['text'] = "选项"
            choise_language['text'] = '请选择语言：'
            Serial_port_number['text'] = '串口号:'
            Baud_rate['text'] = '波特率:'
            Module_address['text'] = '模块地址:'
            Scan_port['text'] = "扫描端口"
            Stop_send['text'] = '停止发送'
            find_device['text'] = '寻找设备'
            Open_light['text'] = '开'
            Close_light['text'] = '关'
            Send_signal['text'] = '发送信号'
            Send['text'] = '发送指令'
            Send_button['text'] = '发送'
            attack_receive['text'] = '接收区'
            Receive['text'] = '接收区'
            Device_display['text'] = '模拟显示'
            Result_display['text'] = '结果显示'
            switch['text'] = '快捷指令'
            for i in list(Device_display_button):
                if i.relay_state_flag:
                    i.button['text'] = '关闭'
                else:
                    i.button['text'] = '开启'
            notebook.tab(0, text="主控视角")
            notebook.tab(1, text='攻击者视角')
            notebook.tab(2, text='检测者视角')

    # 切换语言
    choise_language = ttk.Label(GUI, text="请选择语言:")
    choise_language.place(x=160, y=5)
    language_button = tk.Button(GUI, text="English", command=change_language, height=1, width=10)
    language_button.place(x=300, y=1)

    notebook = tk.ttk.Notebook(GUI)
    notebook.place(x=10, y=30)

    # ---------------主控视角-----------------------
    main_GUI = tk.Frame(GUI, height=720, width=1000)
    main_GUI.pack(padx=10, pady=30, ipadx=10, ipady=10, expand=True, fill="both")
    # main_GUI.pack(expand=True, fill="both")
    load = Image.open("resource/controller.jpg")
    (img_x, img_y) = load.size
    # 缩放倍数
    times = 1
    load = load.resize((img_x * times, img_y * times))
    controller_img = ImageTk.PhotoImage(load)
    controller = tk.Label(main_GUI, image=controller_img)
    controller.place(x=logo_x, y=logo_y)

    #  ---------------攻击者视角-----------------------
    attack_GUI = tk.Frame(GUI, height=720, width=1000)
    attack_GUI.pack(padx=10, pady=30, ipadx=10, ipady=10, expand=True, fill="both")

    #  黑客logo
    load = Image.open("resource/hacker_red.jpg")
    (img_x, img_y) = load.size
    # 缩放倍数
    times = 1
    load = load.resize((img_x * times, img_y * times))
    hacker_img = ImageTk.PhotoImage(load)
    hacker = tk.Label(attack_GUI, image=hacker_img)
    hacker.place(x=logo_x, y=logo_y)

    attack_receive = tk.LabelFrame(attack_GUI, text="接收区", padx=10,
                                   pady=10)  # 水平，垂直方向上的边距均为10    Information.update()
    attack_receive.update()
    attack_receive.place(x=20 + 600, y=30)
    attack_receive_Window = scrolledtext.ScrolledText(attack_receive, width=34, height=24, padx=10, pady=10,
                                                      wrap=tk.WORD)
    attack_receive_Window.grid()
    # 操作信息位置
    Information = tk.LabelFrame(main_GUI, text="操作信息", padx=10, pady=10)  # 水平，垂直方向上的边距均为10    Information.update()
    Information.update()
    Information.place(x=20 + kongjian_weiyi, y=30)
    Information_Window = scrolledtext.ScrolledText(Information, width=34, height=5, padx=10, pady=10, wrap=tk.WORD)
    Information_Window.grid()

    Send = tk.LabelFrame(main_GUI, text="发送指令", padx=10, pady=5)  # 水平，垂直方向上的边距均为 10
    Send.place(x=350 + kongjian_weiyi, y=30)

    DataSend = tk.StringVar()  # 定义DataSend为保存文本框内容的字符串

    EntrySend = tk.StringVar()
    Send_Window = ttk.Entry(Send, textvariable=EntrySend, width=25)
    Send_Window.grid()

    def WriteData():
        global DataSend
        DataSend = EntrySend.get()
        Information_Window.insert("end", '发送指令为：' + str(DataSend) + '\n')
        Information_Window.see("end")
        SerialPort.write(bytes.fromhex(DataSend))

    Send_button = tk.Button(Send, text="发送", command=WriteData)
    Send_button.grid(pady=5, sticky=tk.E)

    Receive = tk.LabelFrame(main_GUI, text="接收区", padx=10, pady=10)  # 水平，垂直方向上的边距均为 10
    Receive.place(x=350 + kongjian_weiyi, y=150)
    Receive_Window = scrolledtext.ScrolledText(Receive, width=21, height=16, padx=8, pady=10, wrap=tk.WORD)
    Receive_Window.grid()

    option = tk.LabelFrame(main_GUI, text="选项", padx=5, pady=5)  # 水平，垂直方向上的边距均为10
    option.place(x=20 + kongjian_weiyi, y=160, width=300)  # 定位坐标
    # ************创建下拉列表**************
    Serial_port_number = ttk.Label(option, text="串口号:")
    Serial_port_number.grid(column=0, row=0, padx=5, pady=5)  # 添加串口号标签
    Baud_rate = ttk.Label(option, text="波特率:")
    Baud_rate.grid(column=0, row=1, padx=5, pady=5)  # 添加波特率标签
    Module_address = ttk.Label(option, text="模块地址:")
    Module_address.grid(column=0, row=2, padx=5, pady=5)  # 添加波特率标签

    Port = tk.StringVar()  # 端口号字符串
    Port_list = ttk.Combobox(option, width=23, textvariable=Port, state='readonly')

    def scan_serial():
        global ListPorts
        ListPorts = list(modbus_comm.scan_serial())
        if ListPorts:
            Information_Window.insert("end", '请选择端口' + '\n')
            Information_Window.see("end")
            Port_list['values'] = [i[0] for i in ListPorts]
            Port_list.current(0)
        else:
            Port_list['values'] = ["   "]
            Port_list.current(0)
            Information_Window.insert("end", 'No usable port' + '\n')
            Information_Window.see("end")

    def sendFindAddress():
        """
        绑定进程
        :param SerialPort:
        :return:
        """
        if SerialPort.isOpen():
            t = threading.Thread(target=modbus_comm.sendAddress,
                                 args=(SerialPort, Information_Window, Receive_Window, address_list))
            print(address_list)
            t.setDaemon(True)
            t.start()

    def CyclesendFindAddress():
        if SerialPort.isOpen():
            t = threading.Thread(target=modbus_comm.cyclesendAddress,
                                 args=(SerialPort, Information_Window, Receive_Window))
            t.setDaemon(True)
            t.start()

    Port_list.grid(column=1, row=0)  # 设置其在界面中出现的位置  column代表列   row 代表行

    BaudRate = tk.StringVar()  # 波特率字符串
    BaudRate_list = ttk.Combobox(option, width=23, textvariable=BaudRate, state='readonly')
    BaudRate_list['values'] = (1200, 2400, 4800, 9600, 14400, 19200, 38400, 43000, 57600, 76800, 115200)
    BaudRate_list.current(3)
    BaudRate_list.grid(column=1, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行

    switch = tk.LabelFrame(main_GUI, text="快捷指令", padx=10, pady=10)  # 水平，垂直方向上的边距均为 10
    switch.place(x=20 + kongjian_weiyi, y=300, width=300)  # 定位坐标

    # switch2 = tk.LabelFrame(main_GUI, text="", padx=10, pady=10)  # 水平，垂直方向上的边距均为 10
    # switch2.place(x=20, y=320, width=300)  # 定位坐标

    def Close_Serial():
        global flag
        flag = 1

    address = tk.StringVar()
    address_list = ttk.Combobox(option, width=23, textvariable=address, state='readonly')

    address_list.grid(column=1, row=2)

    Scan_port = tk.Button(switch, text="扫描端口", command=scan_serial)
    Scan_port.grid(row=0, column=0, padx=5, pady=5)
    # tk.Button(switch, text="开始采集", command=Open_Serial).grid(row=0, column=1)
    Stop_send = tk.Button(switch, text="停止发送", command=Close_Serial)
    Stop_send.grid(row=1, column=1, padx=5, pady=5)
    find_device = tk.Button(switch, text="寻找设备", command=sendFindAddress)
    find_device.grid(row=0, column=1, padx=5, pady=5)
    Open_light = tk.Button(switch, text="开", command=lambda:modbus_comm.openLight(SerialPort,address_list.get(),Information_Window,Receive_Window))
    Open_light.grid(row=0, column=2, padx=5, pady=5)
    Close_light = tk.Button(switch, text="关", command=lambda:modbus_comm.closeLight(SerialPort,address_list.get(),Information_Window,Receive_Window))
    Close_light.grid(row=0, column=3, padx=5, pady=5)
    Send_signal = tk.Button(switch, text="发送信号", command=CyclesendFindAddress)
    Send_signal.grid(row=1, column=0, padx=5, pady=5)

    # ************继电器模拟显示*****************

    Device_display = tk.LabelFrame(main_GUI, text="模拟显示", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
    Device_display.place(x=20, y=420)
    Figure = tk.Canvas(Device_display, bg="#DCDCDC", height=250, width=940)
    Figure.grid()

    # 添加主机组件
    file_path = "resource/computer.jpg"
    master_width = 100
    master_height = 80
    pil_img = Image.open(file_path)
    master_img = ImageTk.PhotoImage(pil_img.resize((master_width, master_height), Image.ANTIALIAS))
    master = Figure.create_image(70, 125, image=master_img)

    # 添加继电器组件
    relay_num = 7  # 继电器数目
    file_path = "resource/device.jpg"  # 继电器样式
    img1_width = 50
    img1_height = 50
    pil_img = Image.open(file_path)
    img1 = ImageTk.PhotoImage(pil_img.resize((img1_width, img1_height), Image.ANTIALIAS))

    x_loc = 200  # x坐标
    step = 100
    Figure.create_line(70 + master_width / 2, 125, x_loc - img1_width / 2, 125, fill='black', width=5)

    # 创建图片对应按钮类
    ListAddress = ['01', '02', '03', '04', '05', '06', '07']


    Device_display_button = []
    for i in range(relay_num):
        # 添加图片
        Figure.create_image(x_loc + step * i, 125, image=img1)
        # 添加按钮
        bb = modbus_comm.RelayButton(x_loc + step * i,img1_width, ListAddress[i],Figure,Device_display,SerialPort,language,Information_Window,Receive_Window)
        Device_display_button.append(bb)
        # 添加连线
        if i != relay_num - 1:
            Figure.create_line(x_loc + step * i + img1_width / 2, 125, x_loc + step * (i + 1) - img1_width / 2, 125,
                               fill='black', width=5)

    # 检测者视角GUI
    detect_GUI = tk.Frame(GUI, height=720, width=1000)
    detect_GUI.pack(padx=10, pady=30, ipadx=10, ipady=10, expand=True, fill="both")

    #  黑客logo
    load = Image.open("resource/defender.jpg")
    (img_x, img_y) = load.size
    # 缩放倍数
    times = 1
    load = load.resize((img_x * times, img_y * times))
    defender_img = ImageTk.PhotoImage(load)
    defender = tk.Label(detect_GUI, image=defender_img)
    defender.place(x=logo_x, y=logo_y)

    # 操作信息位置
    detect_information = tk.LabelFrame(detect_GUI, text="检测信息", padx=10,
                                       pady=10)  # 水平，垂直方向上的边距均为10    Information.update()
    detect_information.update()
    detect_information.place(x=20 + kongjian_weiyi_2, y=30)
    detect_information_Window = scrolledtext.ScrolledText(detect_information, width=34, height=24, padx=10, pady=10,
                                                          wrap=tk.WORD)
    detect_information_Window.grid()

    result_display_height = 330
    result_display_width = 360

    # 静态窗口
    Result_display = tk.LabelFrame(detect_GUI, text="结果显示", padx=10, pady=10)  # 水平，垂直方向上的边距均为10
    Result_display.place(x=330 + kongjian_weiyi_2, y=30)
    Plot = tk.Canvas(Result_display, bg="#DCDCDC", height=result_display_height, width=result_display_width)
    Plot.pack(fill="x")
    axis_distance = 30  # 坐标轴距离画布边距
    Plot.create_line(axis_distance - 2, 0, axis_distance - 2, result_display_height, fill='black', width=4)  # 纵轴
    Plot.create_line(0, result_display_height - axis_distance + 2, result_display_width,
                     result_display_height - axis_distance + 2, fill='black', width=4)  # 横轴

    # 设置滚动检测窗口
    plot2_height = result_display_height
    plot2_width = result_display_width - axis_distance
    Plot2 = tk.Canvas(Plot, bg="#D3D3D3", height=(plot2_height), width=(plot2_width))
    Plot2.place(x=axis_distance, y=0)
    Plot2.create_line(0, (result_display_height - axis_distance + 2), (result_display_width - axis_distance),
                      (result_display_height - axis_distance + 2), fill='black',
                      width=4)  # 横轴
    # # 画阈值曲线
    # global threshold  # 检测阈值
    # threshold_x, threshold_y = compute_coordinate(0, threshold)
    # trd = Plot2.create_line(threshold_x, threshold_y, threshold_x + plot2_width, threshold_y, fill='#FF0000',
    #                         width=2)
    # notebook 添加选项卡
    notebook.add(main_GUI, text='主控视角')
    notebook.add(attack_GUI, text='攻击者视角')
    notebook.add(detect_GUI, text='检测者视角')
    main_GUI.mainloop()


# 计算给定电压值对应像素点位置，y:特征值，index：在列表中的序号，返回相对于画布的坐标
def compute_coordinate(index, y):
    global xcount_max
    # y轴零点对应坐标，y轴最大值对应坐标，x轴每页显示几个数据
    xcount_max = 20  # 每页最多十条数据
    yaxis_min = 0
    yaxis_max = 20  # y轴最大值

    y_set = (int)((yaxis_max - y) / (yaxis_max - yaxis_min) * (plot2_height - axis_distance))
    x_set = (int)(plot2_width / (xcount_max - 1) * index)
    return x_set, y_set


## 用定时器模拟接收树莓派数据过程
def timer_handler():
    global timer_time
    result_display_height = 330
    result_display_width = 360
    global data_list, t3, plot2_height, axis_distance, plot2_width, Plot, Plot2, trd, detect_information_Window
    t3 = threading.Timer(timer_time, timer_handler)
    t3.start()

    # ************结果显示位置*****************
    # 这里需要添加一个线程监听树莓派传过来的数据
    # 波形窗口宽result_display_width，高result_display_height
    global xcount_max
    point_size = 3  # 点的直径
    print("定时器：",new_data)
    if len(new_data) != 0:
        threshold = new_data[1]  # 检测阈值
        threshold_x, threshold_y = compute_coordinate(0, threshold)
        # 阈值对象
        if trd:
            Plot2.delete(trd)
        trd = Plot2.create_line(threshold_x, threshold_y, threshold_x + plot2_width, threshold_y, fill='#FF0000',
                                width=2)
        # Plot.create_text(axis_distance / 2, threshold_y, text="阈\n值\n", font=("Purisa", 10))
        # Plot.create_text(axis_distance / 2, threshold_y - 80, text="有\n攻\n击\n", font=("Purisa", 10))
        # Plot.create_text(axis_distance / 2, threshold_y + 80, text="无\n攻\n击\n", font=("Purisa", 10))
        threshold_x, threshold_y = compute_coordinate(0, threshold)

        print("get data!" + " " + str(new_data[1]) + " " + str(new_data[0]))
        # 输出检测结果
        # 当前时间字符串
        time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        detect_information_Window.insert("end", time_str + ": " + "Get feature value " + str(new_data[0]) + '\n')
        threshold = new_data[1]
        # 判断是否异常
        if new_data[0] > threshold:
            detect_information_Window.insert("end", time_str + ": " + "Exception detected!" + '\n', 'error')
            detect_information_Window.tag_config('error', foreground='red')
            # # 弹窗警告
            # GUI.messagebox.showwarning('警告', '明日有大雨')

        # 输出
        detect_information_Window.see("end")
        data_list.append(new_data)
        # print("data_list",data_list)
        x, y = compute_coordinate(len(data_list) - 1, new_data[0])
        if len(data_list) == 1:
            Plot2.create_oval(x - point_size, y - point_size, x + point_size, y + point_size, outline='black',
                              fill='blue',
                              width=1)
        else:
            Plot2.create_oval(x - point_size, y - point_size, x + point_size, y + point_size, outline='black',
                              fill='blue',
                              width=1)
            x_old, y_old = compute_coordinate(len(data_list) - 2, data_list[len(data_list) - 2][0])
            # 连接两点
            Plot2.create_line(x_old, y_old, x, y, fill='black',
                              width=2)

        if len(data_list) == xcount_max:
            x1 = data_list[-1]
            data_list = []
            data_list.append(x1)
            Plot2.delete(tk.ALL)
            Plot2.create_line(0, (result_display_height - axis_distance + 2), (result_display_width - axis_distance),
                              (result_display_height - axis_distance + 2),
                              fill='black',
                              width=4)  # 横轴


# 有些数据因为发送太快，会粘到一起
def split_data(data: str):
    split_data_list = []
    st = data.split('.')
    # 一个完整的数据位数
    all_length = len(data)
    length = len(st[0]) + 1 + len(st[-1])
    n = int(all_length / length)
    for i in range(n):
        split_data_list.append(data[length * i:length * (i + 1)])
    return split_data_list


def receive_fingerprint():
    global dataA_initial, dataB_initial,port
    bt = bluetooth_server_conn.BluetoothConnection()
    bt.server_bind(port)
    print('Waiting to receive fingerprint……')
    try:
        client_sock, address = bt.server_sock.accept()  # 阻塞等待连接
        print('Success connect!')
        print("Accepted connection from ", address)
        buffer_size = 10240
        # dataA_initial
        i = 0
        while True:
            newdata = client_sock.recv(buffer_size).decode()  # 不断接收数据，每次接收缓冲区1M字节
            if newdata == "over":
                # print("DataA_initial:", dataA_initial)
                print("DataA_length", len(dataA_initial))
                break
            i = i + 1
            dataA_initial.extend(split_data(newdata))
            print("num:", i)
        # dataB_initial
        i = 0
        while True:
            # 限制发送速度 增大缓冲区
            newdata = client_sock.recv(buffer_size).decode()  # 不断接收数据，每次接收缓冲区10KB
            if newdata == "":
                # print("DataB_initial:", dataB_initial)
                print("DataB_length", len(dataB_initial))
                break
            i = i + 1
            dataB_initial.extend(split_data(newdata))
            print("num:", i)

        # 保存指纹
        with open("fingerprint/dataA_initial.txt", "w") as f:
            for line in dataA_initial:
                f.write(line + '\n')
        with open("fingerprint/dataB_initial.txt", "w") as f:
            for line in dataB_initial:
                f.write(line + '\n')
    except Exception as e:
        print('Disconnect!', e)


def thread_4():
    # 选择主机ip和端口
    port = 8000
    ip = "10.1.1.10"

    # 创建socket
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print('Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
        sys.exit()

    # 连接服务器
    try:
        server_addr = (ip, port)
        tcp_socket.connect(server_addr)
    except Exception as e:
        print(e)
        sys.exit()
    print("Socket successfully connected to port " + str(port) + " on ip " + ip)

    print("正在监听数据……")
    buff_size = 20  # 缓冲区大小
    # 监听数据
    while True:
        data = tcp_socket.recv(buff_size)
        print(data)
        attack_receive_Window.insert("end", str(data.hex()) + '\n')
        attack_receive_Window.see("end")


# 监听端口线程
def thread_server_listen():
    global new_data,port

    bt = bluetooth_server_conn.BluetoothConnection()
    bt.server_bind(port)
    while True:
        print('Waiting to receive data……')
        try:
            client_sock, address = bt.server_sock.accept()  # 阻塞等待连接
            print('Success connect!')
            print("Accepted connection from ", address)
            while True:
                newdata = client_sock.recv(30).decode()  # 不断接收数据，每次接收缓冲区1024字节
                if newdata == "":
                    break
                print("received [%s]" % newdata)
                bt.data.append(newdata)
                if len(bt.data) == 2:
                    new_data = []
                    for i in range(len(bt.data)):
                        new_data.append(float(bt.data[i]))
                    bt.data = []
                print("new_data", new_data)
        except Exception as e:
            print('Disconnect!', e)
            continue  # 报错后返回阻塞等待连接的状态


if __name__ == "__main__":
    timer_time = 3
    trd = None
    language = '中文'
    data_list = []
    dataA_initial = []
    dataB_initial = []

    # 接收指纹值
    # receive_fingerprint()

    # 端口扫描
    t1 = threading.Thread(target=thread_server_listen)
    t1.start()
    # 定时器
    t3 = threading.Timer(timer_time, timer_handler)
    t3.start()
    # 显示
    t2 = threading.Thread(target=thread_2)
    t2.start()
    # 攻击者监听进程
    t4 = threading.Thread(target=thread_4)
    t4.start()
