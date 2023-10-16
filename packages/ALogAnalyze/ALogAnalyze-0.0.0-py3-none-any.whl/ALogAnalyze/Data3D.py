#!/usr/bin/env python3

import datetime
import re
import os

from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D

from ALogAnalyze.UI import *

import VisualLog.LogParser as LogParser
import VisualLog.MatplotlibZoom as MatplotlibZoom

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Data3D:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow,  config: dict):
        self.ui = ui
        self.config = config
        self.MainWindow = MainWindow

        data3DTemplate = []
        for i in self.config["Data3D"]:
            data3DTemplate.append(i["name"])

        self.ui.D3DTypesComboBox.addItems(data3DTemplate)
        self.ui.D3DTypesComboBox.setCurrentIndex(0)
        self.filleD3DGridLayout(self.ui.D3DGridLayout)
        self.ui.D3DRunPushButton.clicked.connect(self.D3DRunClick)
        self.ui.D3DParsePushButton.clicked.connect(self.D3DParseClick)
        self.ui.D3DTypesComboBox.currentIndexChanged.connect(self.D3DTypesChanged)

    def D3DTypesChanged(self):
        # clear
        item_list = list(range(self.ui.D3DGridLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.ui.D3DGridLayout.itemAt(i)
            self.ui.D3DGridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        # fill gridlayout
        self.filleD3DGridLayout(self.ui.D3DGridLayout)

    def getD3DInfoData(self):
        keyValues = {}
        for i in range(self.ui.D3DGridLayout.rowCount()):
            if self.ui.D3DGridLayout.itemAtPosition(i, 0) == None:
                continue

            key = self.ui.D3DGridLayout.itemAtPosition(i, 0).widget().text()
            textEdit = self.ui.D3DGridLayout.itemAtPosition(i, 1).widget()
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

    def D3DParseClick(self):
        print("D3DParseClick")

        keyValues: dict = self.getD3DInfoData()
        print(keyValues)

        self.D3DParseData(keyValues)

    def D3DParseData(self, keyValues: dict):
        self.ui.D3DInfoPlainTextEdit.clear()

        lineInfos = LogParser.logFileParser(
                keyValues["File Path"],
                # r'(\d+)\s+(\d+)\s+(\d+)',
                keyValues["Data Regex"]
            )
        
        for info in lineInfos:
            # print(info)
            line = ""
            for i in range(len(info)):
                if isinstance(info[i], datetime.datetime):
                    line += info[i].strftime("%Y-%m-%d %H:%M:%S.%f") + ", "
                elif i == (len(info) - 1):
                    line += str(info[i])
                else:
                    line += str(info[i]) + ", "

            self.ui.D3DInfoPlainTextEdit.appendPlainText(line)
        
        return lineInfos

    def D3DRunClick(self):
        print("D3DRunClick")

        keyValues = self.getD3DInfoData()
        lineInfos = self.D3DParseData(keyValues)
        MatplotlibZoom.Show(callback=self.defaultShowCallback, rows = 1, cols = 1, d3=True, args=[lineInfos, keyValues])

        # fig: Figure = plot.figure()
        # ax: Axes3D = fig.add_subplot(111, projection='3d')
        # ax.cla()
        # # ax = plt.axes(projection='3d')
        # ax.set_xlabel('x-axis')
        # ax.set_ylabel('y-axis')
        # ax.set_zlabel('z-axis')
        # ax.view_init(elev=45, azim=45)

        # # ValueError: data type must provide an itemsize
        # # 输入的数据是字符串导致，需要整形、浮点型数据
        # # 
        # # b: blue
        # # c: cyan
        # # g: green
        # # k: black
        # # m: magenta
        # # r: red
        # # w: white
        # # y: yellow

        # # start point with other
        # ax.scatter3D(lineInfos[0][0], lineInfos[0][1], lineInfos[0][2], cmap='b')
        # ax.scatter3D([s[0] for s in lineInfos[1:]], [s[1] for s in lineInfos[1:]], [s[2] for s in lineInfos[1:]], cmap='r')
        # # line
        # ax.plot3D([s[0] for s in lineInfos], [s[1] for s in lineInfos], [s[2] for s in lineInfos], 'gray')

        # plot.show()

    def filleD3DGridLayout(self, gridLayout: QGridLayout):
        d3DType = self.ui.D3DTypesComboBox.currentIndex()
        keyValues = self.config["Data3D"][d3DType]
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
                button.clicked.connect(self.Data3DArgsClicked)
                gridLayout.addWidget(button, i, 2, 1, 1)
            else:
                value = QLineEdit(keyValues[key])

            gridLayout.addWidget(label, i, 0, 1, 1)
            gridLayout.addWidget(value, i, 1, 1, 1)

            i += 1

    def Data3DArgsClicked(self):
        print("PSPluginsClicked")

        row, col = self.findWidgetPosition(self.ui.D3DGridLayout)

        fileName,fileType = QFileDialog.getOpenFileName(None, "select file", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        if (len(fileName) > 0):
            print(fileName)
            print(fileType)

            edit: QLineEdit = self.ui.D3DGridLayout.itemAtPosition(row, col - 1).widget()
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

        lineInfos = args[0]
        keyValues = args[1]
        dataIndex = eval("[" + keyValues["Data Index"].strip() + "]")
        x = dataIndex[0]
        y = dataIndex[1]
        z = dataIndex[2]

        ax: Axes3D = fig.get_axes()[index]

        # ax = plt.axes(projection='3d')
        ax.set_xlabel('x-axis')
        ax.set_ylabel('y-axis')
        ax.set_zlabel('z-axis')
        ax.view_init(elev=45, azim=45)

        # ValueError: data type must provide an itemsize
        # 输入的数据是字符串导致，需要整形、浮点型数据
        # 
        # b: blue
        # c: cyan
        # g: green
        # k: black
        # m: magenta
        # r: red
        # w: white
        # y: yellow

        # start point
        ax.scatter3D(lineInfos[0][x], lineInfos[0][y], lineInfos[0][z], cmap='b')
        # second pointer with other
        ax.scatter3D([s[x] for s in lineInfos[1:]], [s[y] for s in lineInfos[1:]], [s[z] for s in lineInfos[1:]], cmap='r')
        # line
        ax.plot3D([s[x] for s in lineInfos], [s[y] for s in lineInfos], [s[z] for s in lineInfos], 'gray')
