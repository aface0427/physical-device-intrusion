import socket
import tkinter as tk
from tkinter import Tk, font, messagebox
from tkinter import ttk
from typing import List

from PIL import ImageTk, Image

from DeviceEntity.Gateway import GateWay

from DeviceEntity.Branch import Branch
from Utils.JsonUtil import BranchListDecode, GatewayDecode, CommonDecode
from Utils.ThreadUtil import ThreadFunc, notifyOtherThread, blockOtherThread

commonConfig = CommonDecode("Config/common.json")
OneLineMaxMeter = commonConfig.get("oneLineMaxMeter")  # 一行显示电表数
interval = commonConfig.get("interval")  # 请求间隔


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.serialCloseButton = None
        self.tcp_socket = None
        self.TCPSocketStateLabel = None
        self.gatewayPortCombobox = None
        self.serialOpenButton = None
        self.gatewayIPCombobox = None
        # self.config(bg='red',height=100,width=100)
        self.pack(side='top', fill='both', expand=True)
        self.branchPool: List[Branch] = []  # 连接池

        # 初始化电表和断路器
        self.branchPool: List[Branch] = BranchListDecode("Config/branch.json")
        print(self.branchPool)
        # 初始化网关
        gateway = GatewayDecode("Config/gateway.json")
        self.gatewayPort = tk.IntVar(value=gateway.port)  # 端口号字符串
        self.gatewayIP = tk.StringVar(value=gateway.ip)  # 端口号字符串
        self.gateway = None

        # 大西交logo
        self.xjtuLogo = ImageTk.PhotoImage(Image.open("Resources/xjtu.jpg"))
        xjtuLogoLabel = tk.Label(self, image=self.xjtuLogo)
        xjtuLogoLabel.place(relx=0.90, rely=0)

        # 初始化组件
        self.configFrame = None
        self.dataFrame = None
        self.createWidget()  # 创建子组件

    def createWidget(self):
        # 配置区
        self.configFrame = tk.ttk.LabelFrame(self, text='配置区')
        self.configFrame.grid(row=0, column=0, sticky=tk.NSEW)
        self.configFrameInit()
        # 电表数据区
        self.dataFrame = tk.ttk.LabelFrame(self, text='电表数据区')
        self.dataFrame.grid(row=1, column=0, padx=5, sticky=tk.NSEW)
        self.dataFrameInit()

    def configFrameInit(self):
        """
        配置网络IP区
        :return:
        """
        width = 30
        padx = 5
        pady = 5
        # 电表为服务器，电脑是客户端

        gatewayIPLabel = ttk.Label(self.configFrame, width=width, text="\t\t网关 IP:")
        gatewayIPLabel.grid(row=0, column=0, padx=padx, pady=pady)  # 添加串口号标签
        self.gatewayIPCombobox = tk.Entry(self.configFrame, width=width, textvariable=self.gatewayIP)
        self.gatewayIPCombobox.grid(row=0, column=1, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        # 端口号
        gatewayPortLabel = ttk.Label(self.configFrame, width=width, text="\t\t网关 端口:")
        gatewayPortLabel.grid(row=0, column=2, padx=padx, pady=pady)  # 添加串口号标签

        self.gatewayPortCombobox = tk.Entry(self.configFrame, width=width, textvariable=self.gatewayPort)
        self.gatewayPortCombobox.grid(row=0, column=3, padx=padx, pady=pady)  # 设置其在界面中出现的位置  column代表列   row 代表行

        # 连接断开按钮
        self.serialOpenButton = tk.ttk.Button(self.configFrame, text="连接网关",
                                              command=lambda: ThreadFunc(self.connectServer))
        self.serialOpenButton.grid(row=0, column=4, padx=padx, pady=pady)

        self.serialCloseButton = tk.ttk.Button(self.configFrame, text="断开连接",
                                               command=lambda: ThreadFunc(self.disConnectServer))
        self.serialCloseButton.grid(row=0, column=5, padx=padx, pady=pady)

        # TCP/IP 状态标志
        self.TCPSocketStateLabel = tk.Label(self.configFrame, text="网关未连接")
        self.TCPSocketStateLabel.grid(row=0, column=6, padx=padx, pady=pady)

    def connectServer(self):
        # 连接服务器
        try:

            # 修改界面状态
            self.TCPSocketStateLabel['text'] = "正在连接网关，请稍候……"

            # 连接网关
            ip = self.gatewayIP.get()
            port = self.gatewayPort.get()
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((ip, port))
            # gateway初始化，支路使能
            self.gateway = GateWay(ip, port, tcp_socket)
            for branch in self.branchPool:
                branch.gateway = self.gateway
            # 开始循环请求数据
            self.circleQueryData(interval)
            # energyMeter=EnergyMeter(ip,port,tcp_socket)
            # self.branchPool.append(energyMeter) #加入连接池
            messagebox.showinfo(title='成功提示', message='连接成功！')

            # 修改界面状态
            self.TCPSocketStateLabel['text'] = " "
            notifyOtherThread()


        except Exception as e:
            messagebox.showerror(title='错误提示', message=str(e))
            # 修改界面状态
            self.TCPSocketStateLabel['text'] = "网关连接失败"

    def disConnectServer(self):
        if self.gateway:
            #阻塞除主函数以外的其他进程
            blockOtherThread()
            #直接删除对象
            self.gateway.disConnect()
            del self.gateway
            self.gateway = None

    def dataFrameInit(self):
        """
        电表数据区
        :return:
        """

        maxNum = len(self.branchPool)

        for i in range(maxNum):
            numi = self.branchPool[i].createFrame(self.dataFrame)
            numi.grid(row=i // OneLineMaxMeter, column=i % OneLineMaxMeter, padx=5, pady=5)

    def circleQueryData(self, interval_):
        for branch in self.branchPool:
            branch.meter.queryInfo(interval_, self.gateway.getSocket())


if __name__ == "__main__":
    root = Tk()
    root.title("上位机")
    allWidth = commonConfig.get("width")
    allHeight = commonConfig.get("height")
    root.geometry("{0}x{1}+0+0".format(str(allWidth), str(allHeight)))
    # root.resizable(0,0) #不可调整大小
    root.iconphoto(False, tk.PhotoImage(file='Resources/hacker.png'))

    # 字体设置
    myfont = font.Font(root=root, family='宋体+Times New Roman', size=12, weight=font.NORMAL, slant=font.ROMAN,
                       underline=False, overstrike=False)
    # fontfamilylist = font.families(root=root) #查看字体
    # print(fontfamilylist)

    # 选项卡组件
    app = Application(master=root)

    # root.protocol("WM_DELETE_WINDOW", quit_me)
    root.mainloop()
