#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#

import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

import matplotlib.pyplot as plot
from matplotlib.figure import Figure
from matplotlib.axes import Axes

import datetime
import json
import os
import re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ALogAnalyze.UI import *

class ALogAnalyze():
    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow, config: dict) -> None:
        self.customData = {"xlabel": "X", "ylabel": "Y"}
        self.ui         = ui
        self.MainWindow = MainWindow
        self.config     = config
        # print(json.dumps(self.config, indent=4))

        self.initWidgets(self.ui, self.config)

    def initWidgets(self, ui: Ui_MainWindow, config):

        # Android Log Analyze init
        templateDefaultIndex = self.config["default"]
        template = self.config["templates"][templateDefaultIndex]
        templateNames = []
        for i in self.config["templates"]:
            templateNames.append(i["name"])

        print(json.dumps(template, indent=4))
        print(templateNames)

        ui.AATemplateComboBox.addItems(templateNames)
        ui.AATemplateComboBox.setCurrentIndex(templateDefaultIndex)
        ui.AATemplateComboBox.currentIndexChanged.connect(self.AATemplateChanged)

        ui.AAFileSelectPushButton.clicked.connect(self.AAFileSelect)
        ui.AAParseDataPushButton.clicked.connect(self.AAParseData)
        ui.AAPlotCurvePushButton.clicked.connect(self.AAPlotCurve)

        self.setTemplate(template)

    def AAParseData(self):
        print("AAParseData")

        self.ui.AAInfoTextEdit.clear()
        self.template = self.getTemplate()

        self.parseData()

    def AAPlotCurve(self):
        print("AAPlotCurve")

        self.showData()
    
    def AAFileSelect(self):
        print("AAFileSelect")

        fileName,fileType = QtWidgets.QFileDialog.getOpenFileName(None, "select file", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        if (len(fileName) > 0):
            print(fileName)
            print(fileType)
            self.ui.AAFilePathLineEdit.setText(fileName)

    def setTemplate(self, template):
        print("setTemplate")
        
        self.ui.AAFilePathLineEdit.setText(template["filePath"])
        self.ui.AARegexTextEdit.setText(template["regex"])
        self.ui.AAXAxisLineEdit.setText(template["xAxis"])
        self.ui.AADataIndexLineEdit.setText(template["dataIndex"])
    
    def getTemplate(self):
        template = {}

        template["filePath"]  = self.ui.AAFilePathLineEdit.text()
        template["regex"]     = self.ui.AARegexTextEdit.toPlainText().split("\n")
        template["xAxis"]     = eval("[" + self.ui.AAXAxisLineEdit.text() + "]")
        template["dataIndex"] = eval("[" + self.ui.AADataIndexLineEdit.text() + "]")

        for i in range(len(template["xAxis"])):
            if template["xAxis"][i] < 0:
                template["xAxis"][i] = 0

        if len(template["dataIndex"]) == 0:
            template["dataIndex"].append(0)

        print("current template:")
        print(json.dumps(template, indent=4))

        return template

    def AATemplateChanged(self):
        print("AATemplateChanged")

        template = self.config["templates"][self.ui.AATemplateComboBox.currentIndex()]
        self.setTemplate(template)

    def parseData(self):
        # data = "2705    42248   1025"
        # regex = '(\d+)\s+(\d+)\s+(\d+)'
        # pattern = re.compile(regex)
        # m = pattern.match(data)
        # print(m)

        # 电池容量   开路电压  电池电阻
        # {0.1mah, 0.1mv ,0.1mΩ}
        # 2705    42248   1025
        if not os.path.exists(self.template["filePath"]):
            if (os.path.exists("src/ALogAnalyze")):
                self.template["filePath"] = "src/ALogAnalyze/" + self.template["filePath"]
            
            if not os.path.exists(self.template["filePath"]):
                self.template["filePath"] = os.path.dirname(__file__) + "/" + self.template["filePath"]

        print(os.getcwd())
        print(self.template["filePath"])

        self.lineInfos = LogParser.logFileParser(
                self.template["filePath"],
                # r'(\d+)\s+(\d+)\s+(\d+)',
                self.template["regex"]
            )

        for info in self.lineInfos:
            # print(info)
            line = ""
            for i in range(len(info)):
                if isinstance(info[i], datetime.datetime):
                    line += info[i].strftime("%Y-%m-%d %H:%M:%S.%f") + ", "
                elif i == (len(info) - 1):
                    line += str(info[i])
                else:
                    line += str(info[i]) + ", "

            self.ui.AAInfoTextEdit.append(line)

    def showData(self):
        # 清理matplotlib相关绘图，防止出现未知异常报错
        plot.close()

        self.ui.AAInfoTextEdit.clear()
        self.template = self.getTemplate()

        self.parseData()
        MatplotlibZoom.Show(callback=self.defaultShowCallback, rows = 1, cols = 1)

    def defaultShowCallback(self, fig: Figure, index):
        # https://matplotlib.org/stable/api/
        ax: Axes = fig.get_axes()[index]
        ax.set_xlabel(self.customData["xlabel"])
        ax.set_ylabel(self.customData["ylabel"])

        print(self.template)
        print(self.lineInfos[0])

        if len(self.template["xAxis"]) > 0:
            # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线，一行数据中由x轴和y轴组成
            #   1. i表示当前绘制第几条线
            #   2. x表示当前当前x轴索引
            for i in range(len(self.lineInfos[0])):
                if i in self.template["dataIndex"]:
                    # 迭代x轴，主要是获取x轴索引，相当于用第j个x轴绘制第i个y轴
                    for j in range(len(self.template["xAxis"])):
                        x = self.template["xAxis"][j]                                               # 获取x索引
                        if (i == x) and (x in self.template["dataIndex"]):                          # 处理针对X轴绘图
                            # i == x的会进入这个if，但是数组长度不同不会处理
                            # datetime模式，只以日期为X轴，Y轴表示当前计数，正常的模式下X轴不处理
                            if isinstance(self.lineInfos[0][i], datetime.datetime) and len(self.template["xAxis"]) == len(self.lineInfos[0]):
                                pointCount = 0

                                for s in self.lineInfos:
                                    pointCount += 1

                                    # 文字
                                    ax.text(s[x], pointCount + 0.2, str(pointCount), fontsize=9)
                                    # 圆点
                                    ax.plot(s[x], pointCount, 'o')
                                    # 虚线
                                    ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                        else:                                                                       # 用X轴索引数据绘制Y轴
                            # dataIndex表示必须要绘制的图，不一定包括X轴
                            if (i in self.template["dataIndex"]):
                                if isinstance(self.lineInfos[0][i], str):
                                    pointCount = 1

                                    for s in self.lineInfos:
                                        pointCount += 1

                                        # 文字
                                        ax.text(s[x], pointCount + 0.2, s[i], fontsize=9, rotation=90)
                                        # 圆点
                                        ax.plot(s[x], pointCount, 'o')
                                        # 虚线
                                        ax.plot([s[x], s[x]], [pointCount, 0], linestyle = 'dotted')
                                else:
                                    ax.plot([s[x] for s in self.lineInfos], [s[i] for s in self.lineInfos])
                                    for s in self.lineInfos:
                                        ax.plot(s[x], s[i], 'o')

                            # 处理针对X轴绘制垂直线
                            if (x in self.template["dataIndex"]):
                                for s in self.lineInfos:
                                    ax.plot([s[x], s[x]], [s[i], 0], linestyle = 'dotted')
        else:
            # 迭代第一行数据，相当于绘制多少条线，每一列相当于一条线
            for i in range(len(self.lineInfos[0])):
                if i in self.template["dataIndex"]:
                    # ax.plot(range(len(self.lineInfos)), [s[i] for s in self.lineInfos], label = self.labels[i])
                    ax.plot(range(len(self.lineInfos)), [s[i] for s in self.lineInfos])

        ax.legend()
