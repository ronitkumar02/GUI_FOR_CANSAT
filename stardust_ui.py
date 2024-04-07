import sys
from datetime import datetime
from itertools import count

import matplotlib.pyplot as plt
import pandas as pd
import psutil
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FingureCanvas
from PyQt5 import QtGui, uic
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QFontDatabase

def set_font(widget, font):
    widget.setFont(font)
    for child in widget.findChildren(QWidget):
        set_font(child, font)

# Define the UI class which inherits from QMainWindow
class UI(QMainWindow):
    # Initialize the UI
    def __init__(self):
        super(UI, self).__init__()
        # Load the UI file
        uic.loadUi("stardust_ui.ui", self)
        # Set window title and icon
        self.setWindowTitle("S.T.A.R.D.U.S.T")
        self.setWindowIcon(QtGui.QIcon('icons\\black.png'))
        window = self
        
         # Load and register the custom font
        font_id = QFontDatabase.addApplicationFont("SpaceGrotesk-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # Set font for all widgets
        font = window.font()  # Get the default font
        font.setFamily(font_family)  # Change this to the desired font family
        font.setPointSize(12)  # Change this to the desired font size
        set_font(window, font)
        
        # Find and initialize UI elements
        # Set up a timer for updating the time
        self.time = self.findChild(QLCDNumber, "time")
        self.timer = QTimer()
        self.timer.timeout.connect(self.lcd_num)
        self.timer.start(100)
        self.lcd_num()
        
        # Set up the graph display
        self.graph = self.findChild(QFrame, "frame")
        self.horizontaLayout = QHBoxLayout(self.graph)
        self.horizontaLayout.setObjectName("horizontaLayout")
        self.figure = plt.figure()
        self.canvas = FingureCanvas(self.figure)
        self.horizontaLayout.addWidget(self.canvas)
        self.PlotOnCanvas()
        
        # Set up the GPS display
        self.gps = self.findChild(QLabel, "gps_pics")
        self.view = QWebEngineView()
        self.horizontaLayout = QHBoxLayout(self.gps)
        self.horizontaLayout.setObjectName("horizontaLayout")
        self.horizontaLayout.addWidget(self.view)
        # Initialize timer for updating map
        self.map_update_timer = QTimer()
        self.map_update_timer.timeout.connect(self.update_map)
        self.map_update_timer.start(1000)  # Update map every second
        
        # Set up display for raw data
        self.raw_data = self.findChild(QLabel, "raw_data")
        self.timer1 = QTimer()
        self.timer1.start(1000)
        
        # Set up battery display
        self.battery = self.findChild(QProgressBar, "battery")
        self.timer1.timeout.connect(self.battery_update)
        self.battery.setRange(0, 100)
        
        # Set up button click event
        self.button = self.findChild(QPushButton, "button_1")
        self.button.clicked.connect(self.on_button_click)
        
        # Set up expanded view button event
        self.open_dial = self.findChild(QPushButton, "open_dialbox")
        self.open_dial.clicked.connect(self.expanded)
        
        # Set up more data display
        self.more_data = self.findChild(QLabel,"more_data")
        self.timer1.timeout.connect(self.more_data_update)
        # Set up latitude & longitude
        self.longitude = self.findChild(QLabel,"longitude")
        self.latitude = self.findChild(QLabel,"latitude")
        self.timer1.timeout.connect(self.latitude_longitude_update)
        # Set up status display
        self.status = self.findChild(QLabel, "status")
        self.timer1.timeout.connect(self.update_status)
        
        # Set up top pack bottom voltage and no of satellites
        self.top_voltage = self.findChild(QLabel, "top_voltage")
        self.pack_voltage = self.findChild(QLabel, "pack_voltage")
        self.bottom_voltage = self.findChild(QLabel, "bottom_voltage")
        self.no_of_satellties = self.findChild(QLabel, "no_of_satellties")
        self.timer1.timeout.connect(self.update_voltage_satellties)
        
        # Show the UI
        self.showMaximized()
    
    # Update the LCD number with current time
    def lcd_num(self):
        time = datetime.now()
        formatted_time = time.strftime("%H:%M:%S:%f")
        self.time.setDigitCount(15)
        self.time.setSegmentStyle(QLCDNumber.Flat)
        self.time.display(formatted_time)
    
    # Plot data on canvas
    def PlotOnCanvas(self):
        # Define lists for x and y values
        self.x_vals = []
        self.y_vals = []
        plt.plot()
        self.index = count()
        plt.style.use('seaborn-whitegrid')
        
        # Define animation function
        def animate(i):
            global data
            data = pd.read_csv('data.csv')
            global x
            # Clear axes
            self.ax.cla()
            # Plot acceleration data
            x = data.tail(20)['x_value']
            acc_x = data.tail(20)['total_1']
            self.ax.plot(x, acc_x, label="Acc_x")
            acc_y = data.tail(20)['total_2']
            self.ax.plot(x, acc_y, label="Acc_y")
            acc_z = data.tail(20)['total_3']
            self.ax.plot(x, acc_z, label="Acc_z")
            self.ax.set(xlabel='x-axis', ylabel='Acceleration')
            self.ax.legend()
            
            # Plot analog temperature data
            self.ax1.cla()
            mag_x = data.tail(20)['total_2']
            self.ax1.plot(x, mag_x, label="Mag_x")
            mag_y = data.tail(20)['total_1']
            self.ax1.plot(x, mag_y, label="Mag_y")
            mag_z = data.tail(20)['total_3']
            self.ax1.plot(x, mag_z, label="Mag_z")
            self.ax1.set(xlabel='x-axis', ylabel='Analog Temperature')
            self.ax1.legend()
            
            # Plot gyro data
            self.ax2.cla()
            gyro_x = data.tail(20)["total_1"]
            self.ax2.plot(x, gyro_x, label="gyro_x")
            gyro_y = data.tail(20)['total_2']
            self.ax2.plot(x, gyro_y, label="gyro_y")
            gyro_z = data.tail(20)['total_3']
            self.ax2.plot(x, gyro_z, label="gyro_z")
            self.ax2.set(xlabel='x-axis', ylabel='...')
            self.ax2.legend()
            
            # Plot velocity data
            self.ax3.cla()
            vel_x = data.tail(20)["total_1"]
            vel_y = data.tail(20)['total_2']
            self.ax3.plot(x, vel_x, label="Vel_x")
            vel_z = data.tail(20)['total_3']
            self.ax3.plot(x, vel_y, label="Vel_y")
            self.ax3.plot(x, vel_z, label="Vel_z")
            self.ax3.set(xlabel='x-axis', ylabel='')
            self.ax3.legend()
            
            # Plot humidity and pressure data
            self.ax4.cla()
            humidity = data.tail(20)['total_2']
            self.ax4.plot(x, humidity, label="Humidity")
            pressure = data.tail(20)['total_3']
            self.ax4.plot(x, pressure, label="Pressure")
            self.ax4.set(xlabel='x-label', ylabel='y-label')
            self.ax4.legend()
            
            # Plot gas data
            self.ax5.cla()
            gasR = data.tail(20)['total_2']
            self.ax5.plot(x, gasR, label="two")
            self.ax5.set(xlabel='x-label', ylabel='y-label')
            self.ax5.legend()
        
        # Create animation
        self.ani = FuncAnimation(plt.gcf(), animate, interval=1000)
        self.ax = plt.subplot(231)
        self.ax.set(xlabel='x-label', ylabel='y-label')
        self.ax1 = plt.subplot(232)
        self.ax1.set(xlabel='x-label', ylabel='y-label')
        self.ax2 = plt.subplot(233)
        self.ax2.set(xlabel='x-label', ylabel='y-label')
        self.ax3 = plt.subplot(234)
        self.ax3.set(xlabel='x-label', ylabel='y-label')
        self.ax4 = plt.subplot(235)
        self.ax4.set(xlabel='x-label', ylabel='y-label')
        self.ax5 = plt.subplot(236)
        self.ax5.set(xlabel='x-label', ylabel='y-label')
        plt.tight_layout()
        self.canvas.draw()

    # Function to update more data
    def more_data_update(self):
        latest_data = None
        latest_data = pd.read_csv('data.csv')
        latest_data = latest_data.tail(1)  # Get the latest row
        if not latest_data.empty:  # Check if DataFrame is not empty
            # Extract values from the latest row
            x_value = latest_data['x_value'].values[0]
            total_1 = latest_data['total_1'].values[0]
            total_2 = latest_data['total_2'].values[0]
            status_text = (f'''ROLL:\t {total_1}
PITCH: \t {total_2}
YAW:\t {total_2}
Temperature:\t{total_1}
Gyro rpm:\t{total_2}
Altitude:\t{total_2}''')
            self.more_data.setText(status_text)
    
    # Function to update battery status
    def battery_update(self):
        battery = psutil.sensors_battery()
        battery_percentage = battery.percent
        self.battery.setValue(battery_percentage)
    
    # Function to update latitude  and longitude
    def latitude_longitude_update(self):
        if self.latitude and self.longitude:
            self.latitude.setText(f'Latitude: {x.values[0]}')
            self.longitude.setText(f'Longitude: {x.values[0]}')
        else:
            print("Latitude or longitude label not found.")
    
    # Function to update status display
    def update_status(self):
        latest_data = None
        latest_data = pd.read_csv('data.csv')
        latest_data = latest_data.tail(1)  # Get the latest row
        if not latest_data.empty:  # Check if DataFrame is not empty
            # Extract values from the latest row
            x_value = latest_data['x_value'].values[0]
            total_1 = latest_data['total_1'].values[0]
            total_2 = latest_data['total_2'].values[0]
            status_text = (f'''Status:
                            
Shunt Voltage (V):{x_value}  Pack Voltage:{total_2} 
Current (mA): {total_1}      Bottom Voltage (V):{total_2} 
Bus Voltage (V): {total_2}   Top Voltage (V):{total_2}
Power (mW):   {total_1}''')
            self.status.setText(status_text)
    
    # Function for button click event
    def on_button_click(self):
        print("STARDUST")
    
    def update_voltage_satellties(self):
        self.top_voltage.setText(f'Top Voltage: {x.values[0]}')
        self.pack_voltage.setText(f'Pack Voltage: {x.values[0]}')
        self.bottom_voltage.setText(f'Bottom Voltage: {x.values[0]}')
        self.no_of_satellties.setText(f'No of Satellties: {x.values[0]}')
        pass

    # Function for expanded view button event
    def expanded(self):
        self.hlayout = self.findChild(QHBoxLayout, "horizontalLayout_4")
        if self.open_dial.isChecked():
            self.hlayout.setStretch(0, 0)
        else:
            self.hlayout.setStretch(0, 50)
    
    def update_map(self):
        # Replace the example URL with your real-time tracking service URL
        # Construct URL with latitude and longitude parameters
        latitude = 13.0446948 # Replace with actual latitude
        longitude = 77.5733936  # Replace with actual longitude
        url = f"https://maps.google.com/maps/embed/v1/place?api=AIzaSyDaeKlbjo69fdMB03MABOg7iz3i_Rl5Q4&q={latitude},{longitude}"
        self.view.setUrl(QUrl(url))

# Main block
if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()