import sys
from datetime import datetime
from itertools import count
import serial
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FingureCanvas
    
from PyQt5 import QtGui, uic
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFontDatabase

def set_font(widget, font):
    widget.setFont(font)
    for child in widget.findChildren(QWidget):
        set_font(child, font)

STATE = ["STARTUP","WAITING","ASCENT","APOGEE","DESCENT","TOUCHDOWM"] #State map

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
        
        # Initialize serial port for communication with XBee
        # self.serial_port = serial.Serial('/dev/ttyUSB0', 9600)  # Example port and baudrate, adjust as needed
        
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
        self.update_map()
        self.update_location_timer = QTimer()
        self.update_location_timer.timeout.connect(self.update_location)
        self.update_location_timer.start(3000)
        
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
        self.cx_on = self.findChild(QPushButton, "cx_on")
        self.cx_on.clicked.connect(self.on_button_cx_on)
        
        self.cal = self.findChild(QPushButton, "cal")
        self.cal.clicked.connect(self.on_button_cal)
        
        self.ee = self.findChild(QPushButton, "ee")
        self.ee.clicked.connect(self.on_button_ee)
        
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
            x = data.tail(20)['x_axis']
            acc_x = data.tail(20)['acc_x']
            self.ax.plot(x, acc_x, label="Acc_x")
            acc_y = data.tail(20)['acc_y']
            self.ax.plot(x, acc_y, label="Acc_y")
            acc_z = data.tail(20)['acc_z']
            self.ax.plot(x, acc_z, label="Acc_z")
            self.ax.legend()


            self.ax1.cla()
            mag_x = data.tail(20)['mag_x']
            self.ax1.plot(x, mag_x, label="Mag_x")
            mag_y = data.tail(20)['mag_y']
            self.ax1.plot(x, mag_y, label="Mag_y")
            mag_z = data.tail(20)['mag_z']
            self.ax1.plot(x, mag_z, label="Mag_z")
            self.ax1.legend()
            
            # Plot gyro data
            self.ax2.cla()
            gyro_x = data.tail(20)["gyro_x"]
            self.ax2.plot(x, gyro_x, label="Gyro_x")
            gyro_y = data.tail(20)['gyro_y']
            self.ax2.plot(x, gyro_y, label="Gyro_y")
            gyro_z = data.tail(20)['gyro_z']
            self.ax2.plot(x, gyro_z, label="gyro_z")
            self.ax2.legend()
            
            # Plot velocity data
            self.ax3.cla()
            vel_x = data.tail(20)["vel_x"]
            vel_y = data.tail(20)['vel_y']
            self.ax3.plot(x, vel_x, label="Vel_x")
            vel_z = data.tail(20)['vel_z']
            self.ax3.plot(x, vel_y, label="Vel_y")
            self.ax3.plot(x, vel_z, label="Vel_z")
            self.ax3.legend()
            
            # Plot humidity and pressure data
            self.ax4.cla()
            humidity = data.tail(20)['humidity']
            self.ax4.plot(x, humidity, label="Humidity")
            pressure = data.tail(20)['pressure']
            self.ax4.plot(x, pressure, label="Pressure")
            self.ax4.legend()
            
            # Plot gas data
            self.ax5.cla()
            gasR = data.tail(20)['gasResistance']
            self.ax5.plot(x, gasR, label="GasR")
            self.ax5.legend()
        
        # Create animation
        self.ani = FuncAnimation(plt.gcf(), animate, interval=1000)
        self.ax = plt.subplot(231)
        self.ax1 = plt.subplot(232)
        self.ax2 = plt.subplot(233)
        self.ax3 = plt.subplot(234)
        self.ax4 = plt.subplot(235)
        self.ax5 = plt.subplot(236)

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
            status_text = (f'''Status:\t{STATE[data.tail(1)['state'].values[0]-1]}
                           
Shunt Voltage (V):\t\t{shunt_voltage}
Current (mA):\t\t{current_ma}
Bus Voltage (V):\t\t{bus_voltage}
Power (mW):\t\t{power_mw}''')
            self.status.setText(status_text)
    
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
        api_key = 'Aviea1dpCl4OJ12L8zcNRJlufYPJS5QFDhK3mea2X-2LVBYkt-NW6GPHysB7bwei'
        latitude =  13.0453132 #data.tail(1)['latitude'].values[0] # Replace with actual latitude
        longitude = 77.5733936 #data.tail(1)['longitude'].values[0]  # Replace with actual longitude

        html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <script type="text/javascript" src="https://www.bing.com/api/maps/mapcontrol?callback=GetMap&key={api_key}"></script>
    </head>
    <style>
        body {{
            margin: 0;
            overflow: hidden; /* Hide overflow to prevent scrollbars */
        }}
    </style>
    <body>
        <div id="myMap" style="position:relative;width:100%;height:100%;"></div>
        <script type="text/javascript">
            var map; // Define map globally
            var pin; // Define pin globally
            
            function GetMap() {{
                var latitude = {latitude}; // Replace with actual latitude
                var longitude = {longitude}; // Replace with actual longitude

                map = new Microsoft.Maps.Map(document.getElementById('myMap'), {{
                    center: new Microsoft.Maps.Location(latitude, longitude),
                    mapTypeId: Microsoft.Maps.MapTypeId.aerial,
                    zoom: 18, // Edit it to adjust the zoom level 
                    showZoomButtons: false,
                }});
                // Add a pushpin for the current location
                pin = new Microsoft.Maps.Pushpin(map.getCenter(), {{
                    color: 'blue',
                }});
                map.entities.push(pin);
            }}
        </script>
    </body>
    </html>
    """
        map_url = QUrl.fromUserInput("data:text/html;charset=utf-8," + html_code.strip())
        self.view.setUrl(map_url)
        
    def update_location(self):
        js_code = f"""
        var latitude = {data.tail(1)['latitude'].values[0]}; // Replace with actual latitude
        var longitude = {data.tail(1)['longitude'].values[0]}; // Replace with actual longitude
        
        // Update the pushpin's location
        pin.setLocation(new Microsoft.Maps.Location(latitude, longitude));
        """
        # Inject JavaScript to update the pushpin's location
        self.view.page().runJavaScript(js_code)

        # You may need to update the center of the map as well if you want it to move with the pushpin
        self.view.page().runJavaScript(f"map.setView({{ center: new Microsoft.Maps.Location(latitude, longitude) }});")

    def raw_data_update(self):
        current_font = self.raw_data.font()
        if self.open_dial.isChecked():
            current_font.setPointSize(9)  # Set font size to 15px
            self.raw_data.setFont(current_font)  # Set the font for the QLabel widget
            
            raw_data_text = (f'''Roll: {data.tail(1)['roll'].values[0]}\tVel Y: {data.tail(1)['vel_y'].values[0]}\t\tState: {STATE[data.tail(1)['state'].values[0]-1]}
Yaw: {data.tail(1)['yaw'].values[0]}\tVel Z: {data.tail(1)['vel_z'].values[0]}\t\tShunt Voltage: {data.tail(1)['shunt_voltage'].values[0]}
Pitch: {data.tail(1)['pitch'].values[0]}\tDescent Rate: {data.tail(1)['vel_z'].values[0]}\tPower Mw: {data.tail(1)['power_mw'].values[0]}
Acc X: {data.tail(1)['acc_x'].values[0]}\tNumber Of Satellites: {data.tail(1)['number_of_satellites'].values[0]}\tPack Voltage: {data.tail(1)['pack_voltage'].values[0]}
Acc Y: {data.tail(1)['acc_y'].values[0]}\tTemperature: {data.tail(1)['temperature'].values[0]}\t\tBottom Voltage: {data.tail(1)['bottom_voltage'].values[0]}
Acc Z: {data.tail(1)['acc_z'].values[0]}\tGyro Rpm: {data.tail(1)['gyro_rpm'].values[0]}\t\tTop Voltage: {data.tail(1)['top_voltage'].values[0]}
Mag X: {data.tail(1)['mag_x'].values[0]}\tHumidity: {data.tail(1)['humidity'].values[0]}\t\tSecond: {data.tail(1)['second'].values[0]}
Mag Y: {data.tail(1)['mag_y'].values[0]}\tPressure: {data.tail(1)['pressure'].values[0]}\t\tMinute: {data.tail(1)['minute'].values[0]}
Mag Z: {data.tail(1)['mag_z'].values[0]}\tBattery: {data.tail(1)['battery'].values[0]}\t\tHour: {data.tail(1)['hour'].values[0]}
Gyro X: {data.tail(1)['gyro_x'].values[0]}\tGas Resistance: {data.tail(1)['gasResistance'].values[0]}\tDay: {data.tail(1)['day'].values[0]}
Gyro Y: {data.tail(1)['gyro_y'].values[0]}\tAltitude: {data.tail(1)['altitude'].values[0]}\t\tMonth: {data.tail(1)['month'].values[0]}
Gyro Z: {data.tail(1)['gyro_z'].values[0]}\tCurrent Ma: {data.tail(1)['current_ma'].values[0]}\t\tYear: {data.tail(1)['year'].values[0]}
Vel X: {data.tail(1)['vel_x'].values[0]}\tBus Voltage: {data.tail(1)['bus_voltage'].values[0]}
Latitude: {data.tail(1)['latitude'].values[0]}\tLongitude: {data.tail(1)['longitude'].values[0]}''')
            
            # Set the text of the GUI element
            self.raw_data.setText(raw_data_text)
        else:
            current_font.setPointSize(6)  # Set font size to 15px
            self.raw_data.setFont(current_font)  # Set the font for the QLabel widget
            raw_data_text = (f'''Roll: {data.tail(1)['roll'].values[0]}\t\tPressure: {data.tail(1)['pressure'].values[0]}
Yaw: {data.tail(1)['yaw'].values[0]}\t\tBattery: {data.tail(1)['battery'].values[0]}
Pitch: {data.tail(1)['pitch'].values[0]}\t\tGas Resistance: {data.tail(1)['gasResistance'].values[0]}
Acc X: {data.tail(1)['acc_x'].values[0]}\t\tAltitude: {data.tail(1)['altitude'].values[0]}
Acc Y: {data.tail(1)['acc_y'].values[0]}\t\tCurrent Ma: {data.tail(1)['current_ma'].values[0]}
Acc Z: {data.tail(1)['acc_z'].values[0]}\t\tBus Voltage: {data.tail(1)['bus_voltage'].values[0]}
Mag X: {data.tail(1)['mag_x'].values[0]}\t\tShunt Voltage: {data.tail(1)['shunt_voltage'].values[0]}
Mag Y: {data.tail(1)['mag_y'].values[0]}\t\tPower Mw: {data.tail(1)['power_mw'].values[0]}
Mag Z: {data.tail(1)['mag_z'].values[0]}\t\tPack Voltage: {data.tail(1)['pack_voltage'].values[0]}
Gyro X: {data.tail(1)['gyro_x'].values[0]}\t\tBottom Voltage: {data.tail(1)['bottom_voltage'].values[0]}
Gyro Y: {data.tail(1)['gyro_y'].values[0]}\t\tTop Voltage: {data.tail(1)['top_voltage'].values[0]}
Gyro Z: {data.tail(1)['gyro_z'].values[0]}\t\tSecond: {data.tail(1)['second'].values[0]}
Vel X: {data.tail(1)['vel_x'].values[0]}\t\tMinute: {data.tail(1)['minute'].values[0]}
Vel Y: {data.tail(1)['vel_y'].values[0]}\t\tHour: {data.tail(1)['hour'].values[0]}
Vel Z: {data.tail(1)['vel_z'].values[0]}\t\tDay: {data.tail(1)['day'].values[0]}
Descent Rate: {data.tail(1)['vel_z'].values[0]}\tMonth: {data.tail(1)['month'].values[0]}
Number Of Satellites: {data.tail(1)['number_of_satellites'].values[0]}\tYear: {data.tail(1)['year'].values[0]}
Temperature: {data.tail(1)['temperature'].values[0]}\t\tState: {STATE[data.tail(1)['state'].values[0]-1]}
Gyro Rpm: {data.tail(1)['gyro_rpm'].values[0]}\t\tLatitude: {data.tail(1)['latitude'].values[0]}
Humidity: {data.tail(1)['humidity'].values[0]}\t\tLongitude: {data.tail(1)['longitude'].values[0]}''')
            self.raw_data.setText(raw_data_text)
            
    def on_button_cx_on(self):
        command = "CX ON\n"  # Command to send to XBee
        self.send_command(command)

    def on_button_cal(self):
        command = "CAL\n"  # Command to send to XBees
        self.send_command(command)

    def on_button_ee(self):
        command = "EE\n"  # Command to send to XBee
        self.send_command(command)
    
    def send_command(self, command):
        try:
            # Send command over serial port
            self.serial_port.write(command.encode())
            print("Command sent:", command.strip())
        except Exception as e:
            print("Error sending command:", e)


# Main block
if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()