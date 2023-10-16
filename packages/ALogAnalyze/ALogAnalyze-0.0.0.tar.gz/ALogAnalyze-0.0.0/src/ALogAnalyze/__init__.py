import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ALogAnalyze.ALogAnalyze import ALogAnalyze
from ALogAnalyze.UI import *

from ALogAnalyze.Config import Config
from ALogAnalyze.Data3D import Data3D
from ALogAnalyze.DiffFrame import DiffFrame
from ALogAnalyze.RegexGenerator import RegexGenerator
from ALogAnalyze.Plugin import Plugin
from ALogAnalyze.DataLive import DataLive
from ALogAnalyze.ArrayPlot import ArrayPlot

def center(MainWindow):  # 定义一个函数使得窗口居中显示
    # 获取屏幕坐标系
    screen = QDesktopWidget().screenGeometry()

    # 获取窗口坐标系
    size    = MainWindow.geometry()
    newLeft = (screen.width() - size.width()) / 2
    newTop  = (screen.height() - size.height()) / 2

    MainWindow.move(int(newLeft),int(newTop))

def main():
    app = QApplication(sys.argv)   # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QMainWindow()     # 创建一个QMainWindow，用来装载你需要的各种组件、控件
  
    ui = Ui_MainWindow()           # ui是Ui_MainWindow()类的实例化对象
    ui.setupUi(MainWindow)         # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow

    MainWindow.setWindowIcon(QIcon(os.path.dirname(__file__) + "/assets/images/icon.png"))
    size = MainWindow.geometry()
    MainWindow.setFixedSize(size.width(), size.height())
    # center(MainWindow)

    config        = Config()
    aLogAnalyze   = ALogAnalyze(ui, MainWindow, config)
    regexGenerotr = RegexGenerator(ui, MainWindow, config)
    plugin        = Plugin(ui, MainWindow, config)
    data3D        = Data3D(ui, MainWindow, config)
    diffFrame     = DiffFrame(ui, MainWindow, config)
    dataLive      = DataLive(ui, MainWindow, config)
    arrayPlot      = ArrayPlot(ui, MainWindow, config)
  
    MainWindow.show()              # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec_())          # 使用exit()或者点击关闭按钮退出QApplicat

if __name__ == "__main__":
    main()
