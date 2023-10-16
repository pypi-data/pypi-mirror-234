#!/usr/bin/env python3

import importlib
import re
import os

from ALogAnalyze.UI import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Plugin:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow, config: dict):
        self.ui               = ui
        self.gridLayout       = ui.DFGridLayout
        self.config           = config
        self.MainWindow       = MainWindow

        # Plugins
        ui.PSPluginsComboBox.currentIndexChanged.connect(self.PSPluginsChanged)
        ui.PSRunPushButton.clicked.connect(self.PSRunClick)

        self.initPlugins()

    def initPlugins(self):
        self.plugins     = {}
        self.firstPlugin = ""

        for f in self.getPluginFiles(os.path.dirname(__file__) + "/Plugins"):
            moduleFile   = f.split(".")[0]
            moduleString = moduleFile
            matchObj     = re.match(r'\d{4}[_]?', moduleFile)
            if matchObj:
                moduleString = moduleFile.replace(matchObj.group(0), "")

                self.plugins[moduleString] = moduleFile

                if self.firstPlugin == "":
                    self.firstPlugin = moduleString
 
        self.pluginsKeys = list(self.plugins.keys())
        # self.ui.PSPluginsComboBox.addItems(self.pluginsKeys)
        self.ui.PSPluginsComboBox.addItems(self.plugins.values())
        self.fillePSGridLayout(self.ui.PSGridLayout, self.getClazzArgs(self.firstPlugin))

    def fillePSGridLayout(self, gridLayout: QGridLayout, keyValues: dict):
        if len(keyValues) == 0:
            return

        i = 0
        for key in keyValues.keys():
            label = QLabel(key)
            value = QLineEdit(keyValues[key])
            gridLayout.addWidget(label, i, 0, 1, 1)
            gridLayout.addWidget(value, i, 1, 1, 1)

            if "/" in keyValues[key] or "\\" in keyValues[key]:
                button = QPushButton("Select File ...")
                button.clicked.connect(self.PSPluginsArgsClicked)
                gridLayout.addWidget(button, i, 2, 1, 1)

            i += 1

    def PSPluginsArgsClicked(self):
        print("PSPluginsClicked")
        row, col = self.findWidgetPosition(self.ui.PSGridLayout)

        fileName,fileType = QFileDialog.getOpenFileName(None, "select file", os.getcwd(), "All Files(*);;Text Files(*.txt)")
        if (len(fileName) > 0):
            print(fileName)
            print(fileType)

            edit: QLineEdit = self.ui.PSGridLayout.itemAtPosition(row, col - 1).widget()
            edit.setText(fileName)


    def findWidgetPosition(self, gridLayout):
        print(gridLayout.rowCount())
        print(gridLayout.columnCount())
        for i in range(gridLayout.rowCount()):
            for j in range(gridLayout.columnCount()):
                if gridLayout.itemAtPosition(i, j) != None and (gridLayout.itemAtPosition(i, j).widget() == self.MainWindow.sender()):
                    return (i, j)

        return (-1, -1)

    def getClazzArgs(self, moduleString):
        # import file
        module   = importlib.import_module("ALogAnalyze.Plugins." + self.plugins[moduleString])
        # get class
        clazz    = getattr(module, moduleString)
        # get class doc
        clazzDoc = clazz.__doc__

        # 从类注释中获取类参数及参数说明，格式@argument: argument doc
        keyValues = {}
        for arg in clazzDoc.split("\n"):
            keyValue = arg.strip().split(":")
            if len(keyValue) == 2 and keyValue[0].strip().startswith("@"):
                key = keyValue[0].strip().replace("@", "")
                matchObj     = re.match(r'(.*)\((.*)\)', key)
                if matchObj:
                    keyValue = matchObj.groups()
                    keyValues[keyValue[0]] = keyValue[1]

        return keyValues

    def PSRunClick(self):
        print("PSRunClick")

        keyValues = {}
        for i in range(self.ui.PSGridLayout.rowCount()):
            if self.ui.PSGridLayout.itemAtPosition(i, 0) == None:
                continue

            key = self.ui.PSGridLayout.itemAtPosition(i, 0).widget().text()
            value = self.ui.PSGridLayout.itemAtPosition(i, 1).widget().text()
            if not os.path.exists(value):
                if "/" in value or "\\" in value:
                    if (os.path.exists("src/ALogAnalyze")):
                        value = "src/ALogAnalyze/" + value

                    if not os.path.exists(value):
                        value = os.path.dirname(__file__) + "/" + value

            keyValues[key] = value

        print(keyValues)

        self.getClazzWithRun(self.pluginsKeys[self.ui.PSPluginsComboBox.currentIndex()], keyValues)

    def getClazzWithRun(self, moduleString, args):
        # import file
        module = importlib.import_module("ALogAnalyze.Plugins." + self.plugins[moduleString])
        # get class
        clazz  = getattr(module, moduleString)
        # new class
        clazz(args)

    def PSPluginsChanged(self):
        pluginsIndex = self.ui.PSPluginsComboBox.currentIndex()

        # clear
        item_list = list(range(self.ui.PSGridLayout.count()))
        item_list.reverse()# 倒序删除，避免影响布局顺序

        for i in item_list:
            item = self.ui.PSGridLayout.itemAt(i)
            self.ui.PSGridLayout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()

        # fill gridlayout
        self.fillePSGridLayout(self.ui.PSGridLayout, self.getClazzArgs(self.pluginsKeys[pluginsIndex]))

        print(self.pluginsKeys[pluginsIndex])

    def getFiles(self, path) :
        for (dirpath, dirnames, filenames) in os.walk(path) :
            dirpath   = dirpath
            dirnames  = dirnames
            filenames = filenames
            return filenames

        return []

    def getPluginFiles(self, dirpath):
        plugins = self.getFiles(dirpath)
        plugins.remove("__init__.py")
        plugins.sort()

        return plugins
