#!/usr/bin/env python3

import re
import os
import json

from matplotlib.figure import Figure
from matplotlib.axes import Axes

from ALogAnalyze.UI import *

import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

from ALogAnalyze.Config import ComplexEncoder

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from datetime import datetime, date, timedelta


class DiffFrame:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow, config: dict):
        self.ui               = ui
        self.gridLayout       = ui.DFGridLayout
        self.config           = config
        self.MainWindow       = MainWindow
        self.dataTemplate   = []

        for i in config["DiffFrame"]:
            self.dataTemplate.append(i["name"])

        ui.DFTypesComboBox.addItems(self.dataTemplate)
        ui.DFTypesComboBox.setCurrentIndex(0)
        self.filleGridLayout(self.gridLayout)
        ui.DFRunPushButton.clicked.connect(self.RunClick)
        ui.DFParsePushButton.clicked.connect(self.ParseClick)
        ui.DFTypesComboBox.currentIndexChanged.connect(self.TypesChanged)

    def TypesChanged(self):
        # clear
        item_list = list(range(self.gridLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.gridLayout.itemAt(i)
            self.gridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        # fill gridlayout
        self.filleGridLayout(self.gridLayout)

    def getDFInfoData(self):
        keyValues = {}
        for i in range(self.gridLayout.rowCount()):
            if self.gridLayout.itemAtPosition(i, 0) == None:
                continue

            key = self.gridLayout.itemAtPosition(i, 0).widget().text()
            textEdit = self.gridLayout.itemAtPosition(i, 1).widget()
            if isinstance(textEdit, QTextEdit):
                value = textEdit.toPlainText().split("\n")
            else:
                value = textEdit.text()

            if key in ["File Path", "File Path:"] and ("/" in value or "\\" in value):
                if not os.path.exists(value):
                    if (os.path.exists("src/ALogAnalyze")):
                        value = "src/ALogAnalyze/" + value

                    if not os.path.exists(value):
                        value = os.path.dirname(__file__) + "/" + value

            keyValues[key] = value

        return keyValues

    def ParseClick(self):
        print("DFParseClick")

        keyValues: dict = self.getDFInfoData()
        print(keyValues)
        self.ui.DFInfoPlainTextEdit.clear()

        self.ParseData(keyValues)

    def ParseData(self, keyValues: dict):
        self.ui.DFInfoPlainTextEdit.clear()

        lineInfos = LogParser.logFileParser(
                keyValues["File Path"],
                # r'(\d+)\s+(\d+)\s+(\d+)',
                keyValues["Data Regex"]
            )
        
        for info in lineInfos:
            # print(info)
            line = ""
            for i in range(len(info)):
                if isinstance(info[i], datetime):
                    line += info[i].strftime("%Y-%m-%d %H:%M:%S.%f") + ", "
                elif i == (len(info) - 1):
                    line += str(info[i])
                else:
                    line += str(info[i]) + ", "

            self.ui.DFInfoPlainTextEdit.appendPlainText(line)
        

        self.ui.DFInfoPlainTextEdit.appendPlainText("\n\nframe data:")

        self.featuresValue = []
        for value in keyValues["Data Regex"]:
            self.featuresValue.append(value.split("(")[-1].split(")")[0].replace("\\", ""))

        # 提取原始frame间的数据
        tagIndex = eval("int(keyValues[\"Tag Index\"])")
        timeIndex = eval("int(" + keyValues["Time Index"].strip() + ")")
        frameFirst = eval("bool(" + keyValues["Frame First"].strip() + ")")
        rawDataFrames = []
        frame = None
        for s in lineInfos:
            if s[tagIndex] == self.featuresValue[0]:
                if frame != None:
                    rawDataFrames.append(frame)

                frame = []
                frame.append(s)

                continue

            if frame != None:
                frame.append(s)

            # last frame
            if s is lineInfos[-1]:
                rawDataFrames.append(frame)
        
        print(json.dumps(rawDataFrames, indent=4, cls=ComplexEncoder))

        # 移除frame间重复的数据
        frames = []
        for fs in rawDataFrames:
            frame = []

            for i in range(len(fs) - 1):
                # 相同的数据，取第一个
                if frameFirst:
                    if i == 0:                                      # 第一组数据直接加入
                        frame.append(fs[i])

                    if fs[i][tagIndex] != fs[i + 1][tagIndex]:      # 相同的数据拿第一组数据
                        frame.append(fs[i + 1])
                # 相同的数据，取最后一个
                else:
                    if fs[i][tagIndex] != fs[i + 1][tagIndex]:      # 相同的数据拿最后一组数据
                        frame.append(fs[i])
                    
                    if i == ((len(fs) - 1) - 1):                    # 最后一组数据直接加入
                        frame.append(fs[i + 1])

            # 填补有些项缺失的frame
            if len(frame) < len(self.featuresValue):
                tmp = []
                frameKeys = [s[tagIndex] for s in frame]

                for i in range(len(self.featuresValue)):
                    if self.featuresValue[i] in frameKeys:
                        currentFrameIndex = frameKeys.index(self.featuresValue[i])
                        tmp.append(frame[currentFrameIndex])
                    else:
                        if len(tmp) == 0:
                            tmp.append([0, self.featuresValue[i]])
                        else:
                            tmp.append([frame[i - 1][timeIndex], self.featuresValue[i]])
                frame = tmp

            frames.append(frame)
                    
        self.ui.DFInfoPlainTextEdit.appendPlainText(json.dumps(frames, indent=4, cls=ComplexEncoder))
        
        return frames

    def RunClick(self):
        print("DFRunClick")

        self.ui.DFInfoPlainTextEdit.clear()

        keyValues = self.getDFInfoData()
        frames = self.ParseData(keyValues)
        MatplotlibZoom.Show(callback=self.defaultShowCallback, rows = 1, cols = 1, args=[frames, keyValues])

    def filleGridLayout(self, gridLayout: QGridLayout):
        d3DType = self.ui.DFTypesComboBox.currentIndex()
        keyValues = self.config["DiffFrame"][d3DType]
        i = 0

        for key in keyValues.keys():
            if key == "name":
                continue

            label = QLabel(key)

            if key == "Data Regex":
                value = QTextEdit()
                if isinstance(keyValues[key], str):
                    value.setText(keyValues[key])
                else:
                    value.setText("\n".join(keyValues[key]))
                value.setMaximumHeight(90)
            elif key == "File Path":
                value = QLineEdit(keyValues[key])

                button = QPushButton("Select File ...")
                button.clicked.connect(self.ArgsClicked)
                gridLayout.addWidget(button, i, 2, 1, 1)
            else:
                value = QLineEdit(keyValues[key])

            gridLayout.addWidget(label, i, 0, 1, 1)
            gridLayout.addWidget(value, i, 1, 1, 1)

            i += 1

    def ArgsClicked(self):
        print("PSPluginsClicked")

        row, col = self.findWidgetPosition(self.gridLayout)

        fileName,fileType = QFileDialog.getOpenFileName(None, "select file", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        if (len(fileName) > 0):
            print(fileName)
            print(fileType)

            edit: QLineEdit = self.gridLayout.itemAtPosition(row, col - 1).widget()
            edit.setText(fileName)

    def findWidgetPosition(self, gridLayout):
        for i in range(gridLayout.rowCount()):
            for j in range(gridLayout.columnCount()):
                if gridLayout.itemAtPosition(i, j).widget() == self.MainWindow.sender():
                    return (i, j)

        return (-1, -1)

    def defaultShowCallback(self, fig: Figure, index, args=[]):
        if len(args) <= 0:
            return

        frames = args[0]
        keyValues = args[1]
        timeIndex = eval("int(" + keyValues["Time Index"].strip() + ")")
        maxValues = [0]

        ax: Axes = fig.get_axes()[index]

        j = 1
        for fs in frames:
            # 计算差值
            diffFrameTime = [0]
            for i in range(len(fs) - 1):
                # 差值
                diffValue = fs[i + 1][timeIndex] - fs[0][timeIndex]
                if isinstance(diffValue, timedelta):
                    dateDiffValue: timedelta = diffValue
                    diffFrameTime.append(dateDiffValue.total_seconds())

                    diffValue = dateDiffValue.total_seconds()
                else:
                    diffFrameTime.append(diffValue)

                # 自动递增数量
                if (i + 1) >= len(maxValues):
                    maxValues.append(diffValue)

                # 更新最高点，文字要在最高点上面
                if diffValue > maxValues[i + 1]:
                    maxValues[i + 1] = diffValue
            
            print(diffFrameTime)

            # 绘线和点
            ax.plot(range(len(fs)), diffFrameTime, label=str(j))
            ax.scatter(range(len(fs)), diffFrameTime)

            j += 1
        
        print(maxValues)

        # 绘文字在最高点上面
        for i in range(len(maxValues)):
            ax.text(i, maxValues[i] + 0.2, self.featuresValue[i], fontsize=9, rotation=90)
            ax.plot([i, i], [maxValues[i], 0], linestyle = 'dotted')

        ax.legend()
