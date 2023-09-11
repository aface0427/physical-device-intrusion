from tkinter import ttk, messagebox
import tkinter as tk
from DeviceEntity.Breaker import Breaker
from DeviceEntity.Energymeter import EnergyMeter, EnergyMeterState
from Utils.ThreadUtil import ThreadFunc


class Branch:
    def __init__(self, name: str, breaker: Breaker, meter: EnergyMeter, voltThreshold: float, elecThreshold: float,
                 activePowerThreshold: float):
        self.branchFrame = None
        self.gateway = None
        self.name = name  # 支路x
        self.breaker = breaker
        self.meter = meter

        self.voltThreshold = voltThreshold  # 限额
        self.elecThreshold = elecThreshold  # 限额
        self.activePowerThreshold = activePowerThreshold  # 限额

        self.bindDevices()

    def bindDevices(self):
        # 设置支路设备
        self.meter.bindBranch(self)
        self.breaker.bindBranch(self)

    def ruleDetectAndBehave(self) -> bool:
        """
        TODO 判断并实现限额规则
        """
        if self.meter.measureVoltValStringVar.get() > self.voltThreshold or self.meter.measureElecValStringVar.get() > self.elecThreshold or self.meter.measureActivePowerValStringVar.get() > self.activePowerThreshold:
            self.breaker.close(self.gateway.getSocket())
            self.branchFrame.stateButton.configure(bg='red')
            self.branchFrame.energyMeter.state = EnergyMeterState.Off
            self.branchFrame.energyMeter.stateValueStringVar.set("关")
            print(self.name,'超过阈值')
            messagebox.showinfo(title='断路提示', message=[self.name,'超过阈值！'])

            return True
        return False

    def createFrame(self, master):
        self.branchFrame = BranchFrame(self, master=master)
        return self.branchFrame


class BranchFrame(ttk.LabelFrame):
    def __init__(self, branch: Branch, master=None, **kw):
        super().__init__(master, **kw)
        self.branch = branch
        self.configure(text=branch.name + "(" + branch.meter.type.__str__() + ")")
        self.energyMeter = branch.meter

        self.activePowerValLabel = None
        self.activePowerLabel = None
        self.measureElecValLabel = None
        self.measureElecLabel = None
        self.measureVoltValLabel = None
        self.measureVoltLabel = None
        self.stateButton = None
        self.stateLabel = None
        self.createWidget()

    def createWidget(self):
        width = 30
        padx = 5
        pady = 5
        # 之路状态
        self.stateLabel = ttk.Label(self, width=width, text="支路状态")
        self.stateLabel.grid(row=0, column=0, padx=padx, pady=pady)
        self.stateButton = tk.Button(self, textvariable=self.energyMeter.stateValueStringVar,
                                     command=lambda: ThreadFunc(self.turnOther), bg="green", width=20)
        self.stateButton.grid(row=0, column=1, padx=padx, pady=pady)

        # 量测电压
        self.measureVoltLabel = ttk.Label(self, width=width, text="量测电压")
        self.measureVoltLabel.grid(row=1, column=0, padx=padx, pady=pady)
        self.measureVoltValLabel = tk.Label(self, textvariable=self.energyMeter.measureVoltValStringVar,
                                            state='disabled')
        self.measureVoltValLabel.grid(row=1, column=1, padx=padx, pady=pady)

        # 量测电流
        self.measureElecLabel = ttk.Label(self, width=width, text="量测电流")
        self.measureElecLabel.grid(row=2, column=0, padx=padx, pady=pady)
        self.measureElecValLabel = tk.Label(self, textvariable=self.energyMeter.measureElecValStringVar,
                                            state='disabled')
        self.measureElecValLabel.grid(row=2, column=1, padx=padx, pady=pady)

        # 有功功率
        self.activePowerLabel = ttk.Label(self, width=width, text="有功功率")
        self.activePowerLabel.grid(row=3, column=0, padx=padx, pady=pady)
        self.activePowerValLabel = tk.Label(self, textvariable=self.energyMeter.measureActivePowerValStringVar,
                                            state='disabled')
        self.activePowerValLabel.grid(row=3, column=1, padx=padx, pady=pady)

    def turnOther(self):
        """
        切换相反状态
        :return:
        """
        if self.energyMeter.stateValueStringVar.get() == "开":
            print("正在关闭")
            self.branch.breaker.close(self.branch.gateway.getSocket())
            print("关闭成功")
            self.stateButton.configure(bg="red")
            self.energyMeter.state = EnergyMeterState.Off
            self.energyMeter.stateValueStringVar.set("关")
        else:
            print("正在打开")
            self.branch.breaker.open(self.branch.gateway.getSocket())
            print("打开成功")
            self.stateButton.configure(bg="green")
            self.energyMeter.state = EnergyMeterState.On
            self.energyMeter.stateValueStringVar.set("开")
