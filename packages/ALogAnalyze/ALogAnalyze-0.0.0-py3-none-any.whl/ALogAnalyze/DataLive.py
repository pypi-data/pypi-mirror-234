#!/usr/bin/env python3

import subprocess
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import _thread
import queue
import re
import datetime
import os

from ALogAnalyze.UI import *
from ALogAnalyze.ShellCMD import Shell

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class DataLive:

    """
    利用MediaPipe绘制手掌

    """

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow,  config: dict):
        self.ui = ui
        self.config = config
        self.MainWindow = MainWindow

        dataLiveTemplate = []
        for i in self.config["DataLive"]:
            dataLiveTemplate.append(i["name"])

        self.ui.DLTypesComboBox.addItems(dataLiveTemplate)
        self.ui.DLTypesComboBox.setCurrentIndex(0)
        self.filleDLGridLayout(self.ui.DLGridLayout)
        self.ui.DLRunPushButton.clicked.connect(self.DLRunClick)
        self.ui.DLParsePushButton.clicked.connect(self.DLParseClick)
        self.ui.DLTypesComboBox.currentIndexChanged.connect(self.DLTypesChanged)

        self.frames = queue.Queue()
        self.parseDataRuning = False
        self.x = []
        self.y = []

    def DLTypesChanged(self):
        # clear
        item_list = list(range(self.ui.DLGridLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.ui.DLGridLayout.itemAt(i)
            self.ui.DLGridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        # fill gridlayout
        self.filleDLGridLayout(self.ui.DLGridLayout)

    def getDLInfoData(self):
        keyValues = {}
        for i in range(self.ui.DLGridLayout.rowCount()):
            if self.ui.DLGridLayout.itemAtPosition(i, 0) == None:
                continue

            key = self.ui.DLGridLayout.itemAtPosition(i, 0).widget().text()
            textEdit = self.ui.DLGridLayout.itemAtPosition(i, 1).widget()
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

    def DLParseClick(self):
        print("DLParseClick")

        if not self.parseDataRuning:
            self.parseDataRuning = True
            keyValues: dict = self.getDLInfoData()
            print(keyValues)

            self.DLParseData(keyValues)
        else:
            self.parseDataRuning = False

    def DLParseData(self, keyValues: dict):
        print("DLParseData")

        if len(Shell("adb", "devices").split("\n")) > 1:
            _thread.start_new_thread(self.logcat, (self.capture, keyValues))
        else:
            print("please plugin your device")

    def DLRunClick(self):
        print("DLRunClick")

        if len(Shell("adb", "devices").split("\n")) <= 1:
            print("please plugin your device")
            return

        if not self.parseDataRuning:
            self.DLParseClick()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        self.fig.canvas.mpl_connect('key_press_event', self.controller)
        self.ani = animation.FuncAnimation(self.fig, self.change_plot, interval=1000 / 10)

        plt.show()

    def filleDLGridLayout(self, gridLayout: QGridLayout):
        d3DType = self.ui.DLTypesComboBox.currentIndex()
        keyValues = self.config["DataLive"][d3DType]
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

        row, col = self.findWidgetPosition(self.ui.DLGridLayout)

        fileName,fileType = QFileDialog.getOpenFileName(None, "select file", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        if (len(fileName) > 0):
            print(fileName)
            print(fileType)

            edit: QLineEdit = self.ui.DLGridLayout.itemAtPosition(row, col - 1).widget()
            edit.setText(fileName)

    def findWidgetPosition(self, gridLayout):
        for i in range(gridLayout.rowCount()):
            for j in range(gridLayout.columnCount()):
                if gridLayout.itemAtPosition(i, j).widget() == self.MainWindow.sender():
                    return (i, j)

        return (-1, -1)

    def controller(self, event):
        print('press', event.key)

        if event.key == "a":
            if self.parseDataRuning:
                self.parseDataRuning = False
                plt.close()

    def change_plot(self, args):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        self.ax.cla()

        while not self.frames.empty():
            frame = self.frames.get()
            print(frame)
            self.x.append(frame[0])
            self.y.append(frame[1])

        # self.ax.plot(self.x, [1] * len(self.x))
        self.ax.scatter(self.x, [1] * len(self.x))

        for i in range(len(self.x)):
            self.ax.text(self.x[i], 1 + 0.05, self.y[i], fontsize=9, rotation=90)
            self.ax.plot([self.x[i], self.x[i]], [1, 0], linestyle = 'dotted')

    def capture(self, line, config):
        for i in config["Data Regex"]:
            datePattern       = re.compile(i)
            matchDatePattern  = datePattern.match(line)
            if matchDatePattern:
                lineInfo = self.defaultLineCallback(matchDatePattern.groups())
                print(lineInfo)
                self.frames.put(lineInfo)

    def defaultLineCallback(self, lineInfo):
        lineInfoFixed = []
        today_year    = str(datetime.date.today().year)
        # print(lineInfo)

        for index in range(len(lineInfo)):
            data       = None
            dateRegex  = "(\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}\.\d*)"
            floatRegex = "[-]?\d*\.\d*"
            intRegex   = "[-]?\d+"

            datePattern       = re.compile(dateRegex)
            floatPattern      = re.compile(floatRegex)
            intPattern        = re.compile(intRegex)
            matchDatePattern  = datePattern.match(lineInfo[index])
            matchFloatPattern = floatPattern.match(lineInfo[index])
            matchIntPattern   = intPattern.match(lineInfo[index])

            if matchDatePattern:
                timeString = today_year + "-" + lineInfo[index]
                data = datetime.datetime.strptime(timeString, "%Y-%m-%d %H:%M:%S.%f")
            elif matchFloatPattern:
                data = eval("float(lineInfo[index].strip())")
            elif matchIntPattern:
                data = eval("int(lineInfo[index].strip())")
            else:
                data = lineInfo[index].strip()

            lineInfoFixed.append(data)

        return lineInfoFixed


    def logcat(self, func, config):
        cmd = config["cmd"]

        if "dmesg" in cmd:
            Shell("adb", "root")

        screenData = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while True:
            line = screenData.stdout.readline()

            if not self.parseDataRuning:
                print("exit parse data")
                break

            if line == b'' or subprocess.Popen.poll(screenData) == 0:
                screenData.stdout.close()
                break

            func(line.decode('utf-8').strip(), config)

if __name__ == "__main__":
    pass
