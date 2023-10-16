#!/usr/bin/env python3

import VisualLog.MatplotlibZoom as MatplotlibZoom
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from ALogAnalyze.UI import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ArrayPlot:

    def __init__(self, ui: Ui_MainWindow, MainWindow: QMainWindow,  config: dict):
        self.ui = ui
        self.config = config
        self.MainWindow = MainWindow

        ui.APRunPushButton.clicked.connect(self.RunClick)
        ui.APDataPlainTextEdit.setPlainText(
'''
32,32,34,36,38,40,42,44,46,
48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,
80,82,84,86,88,90,92,94,98,102,106,110,114,118,122,126,127,
128,130,132,134,136,138,140,142,146,150,154,158,162,166,170,174,174,
176,178,182,186,190,194,198,202,206,210,214,218,222,226,230,234,234,
238,242,246,250,254,258,262,266,272,278,284,290,296,302,308,314,314,
320,326,332,338,344,350,356,362,368,374,380,386,392,398,404,410,410,
420,428,436,444,452,460,468,476,484,492,500,508,516,524,532,540,540,
550,562,574,586,598,610,622,634,646,658,670,682,694,706,718,730,730,
744,758,772,786,800,814,828,842,856,870,884,898,912,926,940,954,954,
972,990,1008,1026,1044,1062,1080,1098,1116,1134,1152,1170,1188,1206,1224,1242,1242,
1264,1286,1308,1330,1352,1374,1396,1418,1440,1462,1484,1506,1528,1550,1572,1594,1594,
1624,1654,1684,1714,1744,1774,1804,1834,1864,1894,1924,1954,1984,2014,2044,2074,2074,
2110,2146,2182,2218,2254,2290,2326,2362,2398,2434,2470,2506,2542,2578,2614,2650,2650,
2692,2734,2776,2818,2860,2902,2944,2986,3028,3070,3112,3154,3196,3238,3280,3290,3300,
3310,3320,3330,3340,3350,3360,3370,3380,3392,3404
'''
            )

    def RunClick(self):
        print("RunClick")

        dataString = self.ui.APDataPlainTextEdit.toPlainText()
        if not "," in dataString:
            print("please check data array format")
            return

        self.dataList = eval("[" + dataString + "]")
        print(self.dataList)

        MatplotlibZoom.Show(callback=self.defaultShowCallback, rows = 1, cols = 1)

    def defaultShowCallback(self, fig: Figure, index):
        # https://matplotlib.org/stable/api/
        ax: Axes = fig.get_axes()[index]
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        ax.plot(range(len(self.dataList)), self.dataList)

        for i in range(len(self.dataList)):
            # 圆点
            ax.plot(i, self.dataList[i], 'o')
            # 虚线
            # ax.plot([i, i], [self.dataList[i], 0], linestyle = 'dotted')
