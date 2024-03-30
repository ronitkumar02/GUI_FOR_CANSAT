import sys
# import os
from datetime import datetime
from itertools import count

import matplotlib.pyplot as plt
import pandas as pd
import psutil
# import requests
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FingureCanvas
from PyQt5 import QtGui, uic
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
class UI(QMainWindow) :
    def __init__(self):
        super(UI  ,self).__init__()
        uic.loadUi("stardust_ui.ui"  ,self)
        self.setWindowTitle("S.T.A.R.D.U.S.T")
        self.setWindowIcon(QtGui.QIcon('icons\\black.png'))
        self.time=self.findChild(QLCDNumber  ,"time")
        self.timer=QTimer()
        self.timer.timeout.connect(self.lcd_num)
        self.timer.start(100)
        self.lcd_num()

        self.graph=self.findChild(QFrame  ,"frame")
        self.horizontaLayout=QHBoxLayout(self.graph)
        self.horizontaLayout.setObjectName("horizontaLayout")
        self.figure=plt.figure()
        self.canvas=FingureCanvas(self.figure)
        self.horizontaLayout.addWidget(self.canvas)
        self.PlotOnCanvas()

        self.gps=self.findChild(QLabel  ,"gps_pics")
        # key=AIzaSyDaeKlbjo69f-dMB03MABOg7iz3i_Rl5Q4
        # url = "https://maps.googleapis.com/maps/api/staticmap?center=13.0226992  ,77.5733936&zoom=13&size=600x300&maptype=roadmap&key=&"#.format(13.0226992  ,77.5733936)
        # response = requests.get(url)
        # pixmap = QPixmap()
        # pixmap.loadFromData(response.content)
        # self.gps.setPixmap(pixmap)
    #     else:
    # Display an error message if the pixmap could not be loaded
        # self.gps.setText("Error: Could not load map")
        # self.gps.setPixmap(pixmap)
        self.view = QWebEngineView()
        self.view.setUrl(QUrl("https://maps.google.com/maps?q=&api=AIzaSyDaeKlbjo69f-dMB03MABOg7iz3i_Rl5Q4"))
        self.horizontaLayout=QHBoxLayout(self.gps)
        self.horizontaLayout.setObjectName("horizontaLayou")
        self.horizontaLayout.addWidget(self.view)

        self.raw_data=self.findChild(QLabel  ,"raw_data")
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.raw_data_info)
        self.timer1.start(1000)

        self.battery=self.findChild(QProgressBar  ,"battery")
        self.battery.setRange(0  , 100)

        self.button=self.findChild(QPushButton  ,"button_1")
        self.button.clicked.connect(self.on_button_click)

        self.open_dial=self.findChild(QPushButton  ,"open_dialbox")
        self.open_dial.clicked.connect(self.expanded)
        self.showMaximized()
    
    def lcd_num(self):
        time=datetime.now()
        formatted_time=time.strftime("%H:%M:%S:%f")
        self.time.setDigitCount(15)
        self.time.setSegmentStyle(QLCDNumber.Flat)
        self.time.display(formatted_time)
    
    def PlotOnCanvas(self):
        self.x_vals = []
        self.y_vals = []
        plt.plot()
        self.index = count()
        plt.style.use('seaborn-whitegrid')
        def animate(i):
            global data
            data = pd.read_csv('data.csv')
            global x 
            x= data.tail(20)['x_value']
            y1 = data.tail(20)['total_1']
            self.ax.cla()
            self.ax.plot(x, y1, label="two")
            y9 = data.tail(20)['total_2']
            self.ax.plot(x, y9, label="one")
            y7 = data.tail(20)['total_3']
            self.ax.plot(x, y7, label="three")
            self.ax.set(xlabel='x-axis'  , ylabel='Pressure')
            self.ax.legend()
            
            y2 = data.tail(20)['total_2']
            self.ax1.cla()
            self.ax1.plot(x, y2, label="two")
            y9 = data.tail(20)['total_1']
            self.ax1.plot(x, y9, label="three")
            y9 = data.tail(20)['total_3']
            self.ax1.plot(x, y9, label="three")
            self.ax1.set(xlabel='x-axis', ylabel='Analog Temperature')
            self.ax1.legend()
            
            
            y3=data.tail(20)["total_1"]
            self.ax2.cla()
            self.ax2.plot(x, y1, label="two")
            y9 = data.tail(20)['total_2']
            self.ax2.plot(x, y9, label="one")
            y7 = data.tail(20)['total_3']
            self.ax2.plot(x, y7, label="three")
            self.ax2.set(xlabel='x-axis'  , ylabel='Humidity')
            self.ax2.legend()
            
            
            y4=data.tail(20)["total_1"]
            self.ax3.cla()
            y9 = data.tail(20)['total_2']
            self.ax3.plot(x, y9, label="one")
            y7 = data.tail(20)['total_3']
            self.ax3.plot(x, y7, label="three")
            self.ax3.plot(x  ,y3  ,label="two")
            self.ax3.set(xlabel='x-axis'  , ylabel='Temperature')
            self.ax3.legend()
            
            self.ax4.cla()
            y9 = data.tail(20)['total_2']
            self.ax4.plot(x, y9, label="one")
            self.ax4.plot(x  ,y7  ,label="two")
            self.ax4.set(xlabel='x-label'  , ylabel='y-label')
            self.ax4.legend()
            
            self.ax5.cla()
            y9 = data.tail(20)['total_2']
            self.ax5.plot(x  ,y2  ,label="two")
            self.ax5.set(xlabel='x-label'  , ylabel='y-label')
            self.ax5.legend()

        self.ani=FuncAnimation(plt.gcf(),animate,interval=1000)
        self.ax=plt.subplot(231)
        self.ax.set(xlabel='x-label'  , ylabel='y-label')
        self.ax1=plt.subplot(232)
        self.ax1.set(xlabel='x-label'  , ylabel='y-label')
        self.ax2=plt.subplot(233)
        self.ax2.set(xlabel='x-label'  , ylabel='y-label')
        self.ax3=plt.subplot(234)
        self.ax3.set(xlabel='x-label'  , ylabel='y-label')
        self.ax4=plt.subplot(235)
        self.ax4.set(xlabel='x-label'  , ylabel='y-label')
        self.ax5=plt.subplot(236)
        self.ax5.set(xlabel='x-label'  , ylabel='y-label')
        plt.tight_layout()
        self.canvas.draw()
    
    def raw_data_info(self):
        battery = psutil.sensors_battery()
        battery_percentage = battery.percent
        self.battery.setValue(battery_percentage)

    def on_button_click(self):
        print("STARDUST")

    def expanded(self):
        self.hlayout=self.findChild(QHBoxLayout  ,"horizontalLayout_4")
        if self.open_dial.isChecked():
            self.hlayout.setStretch(0,0)
        else:
            self.hlayout.setStretch(0,50)

app=QApplication(sys.argv)
UIWindow=UI()
app.exec_()