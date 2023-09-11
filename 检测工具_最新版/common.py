#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 14:50
# @File    : common.py
# @Description : 通用，封装一些函数
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.filedialog import asksaveasfilename

import pandas
import pandas as pd
from pandas import DataFrame, ExcelWriter

from tkinter import *


def ThreadFunc(funcName, *args, **kwargs):
    """
    把函数名封装成多线程,并开启进程
    :param funcName: 函数名
    :return: 返回线程对象
    """
    t = threading.Thread(target=funcName, args=args, kwargs=kwargs)
    t.daemon=True
    t.start()
    # t.join()
    return t


def ExporTreeview(writer: ExcelWriter, treeView: tk.ttk.Treeview, sheet_name="sheet1"):
    """
    导出到excel
    :param writer: ExcelWriter类
    :param treeView: treeView对象
    :param sheet_name: sheet名
    :return:
    """
    selectViewTreeViewHeading = treeView["columns"]
    lst = []
    for row_id in treeView.get_children():
        row = treeView.item(row_id, 'values')
        lst.append(row)
    lst = list(map(list, lst))
    lst.insert(0, selectViewTreeViewHeading)
    # print(lst)
    df = DataFrame(lst)

    df.to_excel(excel_writer=writer, sheet_name=sheet_name, index=False, header=False)


class ToolTip(object):
    """
    鼠标提示条
    """

    def __init__(self, widget):
        self.widget = widget
        self.tip_window = None

    def show_tip(self, tip_text):
        "Display text in a tooltip window"
        if self.tip_window or not tip_text:
            return
        x, y, _cx, cy = self.widget.bbox("insert")
        # get size of widget
        x = x + self.widget.winfo_rootx() + 25
        # calculate to display tooptip
        y = y + cy + self.widget.winfo_rooty() + 25
        # below and to the right
        self.tip_window = tw = tk.Toplevel(self.widget)
        # create new tooltip window
        tw.wm_overrideredirect(True)
        # remove all Window Manager (wm)
        tw.wm_geometry("+%d+%d" % (x, y))
        # create window size

        label = tk.Label(tw, text=tip_text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID,
                         borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


def create_ToolTip(widget, text):
    tooltip = ToolTip(widget)

    def enter(event):
        tooltip.show_tip(text)

    def leave(event):
        tooltip.hide_tip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)




class SetMenu(tk.Menu):
    """
    可设置的menu
    """

    def __init__(self, master=None, setMenus=None, items=None, callbacks=None, cnf={}, **kw):
        super().__init__(master, cnf={}, **kw)
        self.master = master

        self.setMenus = setMenus  # 对于菜单栏而言，其他munu可以忽略
        self.items = items
        self.callbacks = callbacks
        self.set()

    def set(self):
        """
        绑定items名和函数
        :return:
        """

        if (self.setMenus):
            # 一级菜单
            for i, x in enumerate(self.setMenus):
                # 二级菜单
                m = tk.Menu(self, tearoff=0)
                for item, callback in zip(self.items[i], self.callbacks[i]):
                    # 三级菜单（这里用不上，之后扩展可能用上）
                    if isinstance(item, list):
                        sm = tk.Menu(self, tearoff=0)
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
                self.add_cascade(label=x, menu=m)
            self.master.config(menu=self)

        else:
            for item, callback in zip(self.items, self.callbacks):
                if isinstance(item, list):
                    sm = tk.Menu(self, tearoff=0)
                    for subitem, subcallback in zip(item[1:], callback):
                        if subitem == '-':
                            sm.add_separator()
                        else:
                            sm.add_command(label=subitem, command=subcallback, compound='left')
                    self.add_cascade(label=item[0], menu=sm)
                elif item == '-':
                    self.add_separator()
                else:
                    self.add_command(label=item, command=callback, compound='left')



def findAllChildrens(widget: tk.Widget):
    """
    查找一个组件的所有后代
    :param widget:查找一个组件的所有后代
    :return: 所有后代
    """
    currentChildren = []
    for k, v in widget.children.items():
        currentChildren = currentChildren + [v]
        if k != None:
            currentChildren = currentChildren + findAllChildrens(v)
    return currentChildren


def findTypeChildrens(widget: tk.Widget, *args):
    """
    查找一个组件的所有类型为type的后代
    :param widget:查找一个组件的所有后代
    :param args:类型元组
    :return: 所有后代
    """
    currentChildren = []
    for k, v in widget.children.items():
        # print(type(v))
        if isinstance(v, args):
            currentChildren = currentChildren + [v]
        if k != None:
            currentChildren = currentChildren + findTypeChildrens(v, args)
    return currentChildren


class bindButtonDisable():
    """
    当同类组件中一个点击时，其他失能
    :param Widget:
    :return:
    """

    def __init__(self, widget: tk.Widget, *args):
        self.widget = widget
        self.args = args

        self.bindDisable()

    def bindDisable(self):
        x = findTypeChildrens(self.widget, self.args)
        for i in x:
            i.bind('<ButtonPress-1>', self.ButtonPress1Disable)
            i.bind('<ButtonRelease-1>', self.ButtonRelease1Enable)

    def ButtonPress1Disable(self, event):
        # print(type(event.widget))
        x = findTypeChildrens(self.widget, self.args)
        for i in x:
            if i != event.widget:
                i.config(state=tk.DISABLED)
            # print ("awsl")

    def ButtonRelease1Enable(self, event):
        # print(type(event.widget))
        x = findTypeChildrens(self.widget, self.args)
        for i in x:
            if i != event.widget:
                i.config(state=tk.NORMAL)
            # print("awhl")




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

        self.createWidget()# 初始化子组件


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