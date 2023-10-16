#!/usr/bin/env python3

import re

from ALogAnalyze.UI import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class RegexGenerator:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow, config: dict):
        self.ui               = ui
        self.gridLayout       = ui.DFGridLayout
        self.config           = config
        self.MainWindow       = MainWindow
        self.regexTemplateNames = []

        for i in self.config["regexGenerator"]:
            self.regexTemplateNames.append(i["name"])

        ui.RGTemplateComboBox.addItems(self.regexTemplateNames)
        ui.RGTemplateComboBox.currentIndexChanged.connect(self.RGTemplateChanged)
        ui.RGParseDataPushButton.clicked.connect(self.RGParseData)

        RGTemplate = self.config["regexGenerator"][0]
        self.ui.RGInputDataTextEdit.setText("\n".join(RGTemplate["inputData"]))
        self.ui.RGRegexTextEdit.setText(RGTemplate["regex"])
        self.ui.RGDataIndexLineEdit.setText(RGTemplate["dataIndex"])

    def RGTemplateChanged(self):
        print("CGTemplateChanged")

        template = self.config["regexGenerator"][self.ui.RGTemplateComboBox.currentIndex()]
        self.ui.RGInputDataTextEdit.setText("\n".join(template["inputData"]))
        self.ui.RGRegexTextEdit.setText(template["regex"])
        self.ui.RGDataIndexLineEdit.setText(template["dataIndex"])
    
    def RGParseData(self):
        print("RGParseData")

        inputData = self.ui.RGInputDataTextEdit.toPlainText().split("\n")
        regexData = self.ui.RGRegexTextEdit.toPlainText().strip()
        dataIndex = eval("[" + self.ui.RGDataIndexLineEdit.text().strip() + "]")

        lineInfos = []

        print(inputData)
        print(regexData)

        self.ui.RGInfoTextEdit.clear()
        for i in inputData:
            foundList = re.search(regexData, i.strip(), re.M | re.I)
            if foundList:
                output = ""
                # print(foundList.groups())
                dataGroup = foundList.groups()
                for j in range(len(dataGroup)):
                    lineInfos.append(dataGroup[j])

                    if dataGroup[j] == None:
                        output += " | "
                    elif j == (len(dataGroup) - 1):
                        output += dataGroup[j]
                    else:
                        output += dataGroup[j] + " | "

                self.ui.RGInfoTextEdit.append(output)

        for i in range(len(lineInfos)):
            if i in dataIndex:
                self.ui.RGInfoTextEdit.append("index " + str(i) + " : " + lineInfos[i])
