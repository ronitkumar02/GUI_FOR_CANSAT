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
        
         # Load and register the custom font
        font_id = QFontDatabase.addApplicationFont("icons\\SpaceGrotesk-Regular.ttf")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        
        # Set font for all widgets
        font = self.font()  # Get the default font
        font.setFamily(font_family)  # Change this to the desired font family
        font.setPointSize(12)  # Change this to the desired font size
        set_font(self, font)
        
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
        self.timer1.timeout.connect(self.raw_data_update)
        
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
            data = pd.read_csv('STARDUST_data.csv')
            global x
            # Clear axes
            self.ax.cla()
            # Plot acceleration data
            x = data.tail(20)['x_axis']
            acc_x = data.tail(20)['acc_x']
            self.ax.plot(x, acc_x, label="Acc_x")
            acc_y = data.tail(20)['acc_y']
            self.ax.plot(x, acc_y, label="Acc_y")
            acc_z = data.tail(20)['acc_z']
            self.ax.plot(x, acc_z, label="Acc_z")
           #self.ax.set(xlabel='x-axis', ylabel='Acceleration')
            self.ax.legend()
            
            # Plot analog temperature data
            self.ax1.cla()
            mag_x = data.tail(20)['mag_x']
            self.ax1.plot(x, mag_x, label="Mag_x")
            mag_y = data.tail(20)['mag_y']
            self.ax1.plot(x, mag_y, label="Mag_y")
            mag_z = data.tail(20)['mag_z']
            self.ax1.plot(x, mag_z, label="Mag_z")
            #self.ax1.set(xlabel='x-axis', ylabel='Analog Temperature')
            self.ax1.legend()
            
            # Plot gyro data
            self.ax2.cla()
            gyro_x = data.tail(20)["gyro_x"]
            self.ax2.plot(x, gyro_x, label="Gyro_x")
            gyro_y = data.tail(20)['gyro_y']
            self.ax2.plot(x, gyro_y, label="Gyro_y")
            gyro_z = data.tail(20)['gyro_z']
            self.ax2.plot(x, gyro_z, label="gyro_z")
            #self.ax2.set(xlabel='x-axis', ylabel='...')
            self.ax2.legend()
            
            # Plot velocity data
            self.ax3.cla()
            vel_x = data.tail(20)["vel_x"]
            vel_y = data.tail(20)['vel_y']
            self.ax3.plot(x, vel_x, label="Vel_x")
            vel_z = data.tail(20)['vel_z']
            self.ax3.plot(x, vel_y, label="Vel_y")
            self.ax3.plot(x, vel_z, label="Vel_z")
            #self.ax3.set(xlabel='x-axis', ylabel='')
            self.ax3.legend()
            
            # Plot humidity and pressure data
            self.ax4.cla()
            humidity = data.tail(20)['humidity']
            self.ax4.plot(x, humidity, label="Humidity")
            pressure = data.tail(20)['pressure']
            self.ax4.plot(x, pressure, label="Pressure")
            #self.ax4.set(xlabel='x-label', ylabel='y-label')
            self.ax4.legend()
            
            # Plot gas data
            self.ax5.cla()
            gasR = data.tail(20)['gasResistance']
            self.ax5.plot(x, gasR, label="GasR")
            #self.ax5.set(xlabel='x-label', ylabel='y-label')
            self.ax5.legend()
        
        # Create animation
        self.ani = FuncAnimation(plt.gcf(), animate, interval=1000)
        self.ax = plt.subplot(231)
        ## self.ax.set(xlabel='x-label', ylabel='y-label')
        self.ax1 = plt.subplot(232)
        # #self.ax1.set(xlabel='x-label', ylabel='y-label')
        self.ax2 = plt.subplot(233)
        # #self.ax2.set(xlabel='x-label', ylabel='y-label')
        self.ax3 = plt.subplot(234)
        # #self.ax3.set(xlabel='x-label', ylabel='y-label')
        self.ax4 = plt.subplot(235)
        # #self.ax4.set(xlabel='x-label', ylabel='y-label')
        self.ax5 = plt.subplot(236)
        # #self.ax5.set(xlabel='x-label', ylabel='y-label')
        plt.tight_layout()
        self.canvas.draw()

    # Function to update more data
    def more_data_update(self):  # Get the latest row
        if not data.tail(1).empty:  # Check if DataFrame is not empty
            # Extract values from the latest row
            pitch = data.tail(1)['pitch'].values[0]
            yaw = data.tail(1)['yaw'].values[0]
            roll = data.tail(1)['roll'].values[0]
            temperature = data.tail(1)['temperature'].values[0]
            altitude = data.tail(1)['altitude'].values[0]
            gyro_rpm = data.tail(1)['gyro_rpm'].values[0]
            status_text = (f'''ROLL:\t\t{roll}
PITCH:\t\t{pitch}
YAW:\t\t{yaw}
Temperature:\t{temperature}
Gyro rpm:\t{gyro_rpm}
Altitude:\t\t{altitude}''')
            self.more_data.setText(status_text)
    
    # Function to update battery status
    def battery_update(self):
        # battery = psutil.sensors_battery()
        battery_percentage = data.tail(1)['battery'].values[0]
        self.battery.setValue(battery_percentage)
    
    # Function to update latitude  and longitude
    def latitude_longitude_update(self):
        longitude=data.tail(1)['longitude'].values[0]
        latitude=data.tail(1)['latitude'].values[0]
        if self.latitude and self.longitude:
            self.latitude.setText(f'Latitude: {latitude}')
            self.longitude.setText(f'Longitude: {longitude}')
        else:
            print("Latitude or longitude label not found.")
    
    # Function to update status display
    def update_status(self):
        if not data.tail(1).empty:  # Check if DataFrame is not empty
            # Extract values from the latest row
            shunt_voltage = data.tail(1)['shunt_voltage'].values[0]
            current_ma = data.tail(1)['current_ma'].values[0]
            bus_voltage = data.tail(1)['bus_voltage'].values[0]
            power_mw = data.tail(1)['power_mw'].values[0]
            status_text = (f'''Status:
                           
Shunt Voltage (V):\t\t{shunt_voltage}
Current (mA):\t\t{current_ma}
Bus Voltage (V):\t\t{bus_voltage}
Power (mW):\t\t{power_mw}''')
            self.status.setText(status_text)
    
    # Function for button click event
    def on_button_click(self):
        print("STARDUST")
    
    def update_voltage_satellties(self):
        self.top_voltage.setText(f'Top Voltage:\t {data.tail(1)["top_voltage"].values[0]}')
        self.pack_voltage.setText(f'Pack Voltage:\t {data.tail(1)["pack_voltage"].values[0]}')
        self.bottom_voltage.setText(f'Bottom Voltage:\t {data.tail(1)["bottom_voltage"].values[0]}')
        self.no_of_satellties.setText(f'No of Satellties: \t{data.tail(1)["number_of_satellites"].values[0]}')

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
        
    def raw_data_update(self):
        raw_data_text = (f'''Roll: 0.009
Yaw: 0.514
Pitch: 0.3
Acc X: 0.254
Acc Y: 0.858
Acc Z: 0.345
Mag X: 0.74
Mag Y: 0.237
Mag Z: 0.486
Gyro X: 0.308
Gyro Y: 0.993
Gyro Z: 0.32
Vel X: 0.578
Vel Y: 0.736
Vel Z: 0.666
Descent Rate: 0.749
State: 0.264
Temperature: 0.31
Gyro Rpm: 0.546
Humidity: 0.253
Pressure: 0.059
Battery: 33
Gas Resistance: 0.566
Altitude: 0.63
Current Ma: 0.871
Bus Voltage: 0.97
Shunt Voltage: 0.561
Power Mw: 0.599
Pack Voltage: 0.354
Bottom Voltage: 0.552
Top Voltage: 0.722
Second: 38
Minute: 6
Hour: 0
Day: 12
Month: 4
Year: 2024
Number Of Satellites: 0.891
Latitude: 0.697
Longitude: 0.51

''')
        if self.open_dial.isChecked():
                        # Assuming self.raw_data is a Tkinter Label widget
            # Assuming self.raw_data is a QLabel widget
            current_font = self.raw_data.font()
            current_font.setPointSize(10)  # Set font size to 15px

            self.raw_data.setFont(current_font)  # Set the font for the QLabel widget
            
            lines = raw_data_text.split('\n')
            each_length = len(lines) // 3
            column1 = "\n".join(lines[:each_length])
            column2 = "\n".join(lines[each_length:each_length*2])
            column3 = "\n".join(lines[each_length*2:])

            # Set the text of the GUI element with two columns side by side
            max_length = max(len(column1), len(column2),len(column3))
            column1_padded = column1.ljust(max_length, ' ')
            column2_padded = column2.ljust(max_length, ' ')
            column3_padded = column3.ljust(max_length, ' ')

            # Combine columns side by side
            combined_text = '\n'.join([f"{col1}\t\t{col2}\t\t{col3}" for col1, col2 , col3 in zip(column1_padded.split('\n'), column2_padded.split('\n'),column3_padded.split('\n'))])

            # Set the text of the GUI element
            self.raw_data.setText(combined_text)
        else:
            current_font = self.raw_data.font()
            current_font.setPointSize(7)  # Set font size to 15px

            self.raw_data.setFont(current_font)  # Set the font for the QLabel widget

            # Split the text into two parts
            lines = raw_data_text.split('\n')
            each_length = len(lines) // 2
            column1 = "\n".join(lines[:each_length])
            column2 = "\n".join(lines[each_length:])

            # Set the text of the GUI element with two columns side by side
            max_length = max(len(column1), len(column2))
            column1_padded = column1.ljust(max_length, ' ')
            column2_padded = column2.ljust(max_length, ' ')

            # Combine columns side by side with consistent tab spacing
            combined_text = '\n'.join([f"{col1}\t\t{col2}" for col1, col2 in zip(column1_padded.split('\n'), column2_padded.split('\n'))])

            print(combined_text)
            self.raw_data.setText(combined_text)


# Main block
if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()