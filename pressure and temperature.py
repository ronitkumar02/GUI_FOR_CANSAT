import serial
import csv
import time
import datetime


fieldnames = ["x_axis","roll","yaw","pitch","acc_x","acc_y","acc_z","mag_x","mag_y","mag_z","gyro_x","gyro_y","gyro_z","vel_x","vel_y","vel_z","descent_rate","state","temperature","gyro_rpm","humidity","pressure",
              "gasResistance","altitude","current_ma","bus_voltage","shunt_voltage","power_mw","pack_voltage","bottom_voltage","top_voltage","second","minute","hour","day","month","year","number_of_satellites","latitude","longitude"]
x_axis=0
with open('arduinoP&T_data.csv'  , 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file  , fieldnames=fieldnames)
    csv_writer.writeheader()

ser = serial.Serial('COM5',9600) # Change the port name to match your setup
while True:
    with open('STARDUST_data.csv'  , 'a'  , newline='') as csvfile:
        writer = csv.DictWriter(csvfile  ,fieldnames=fieldnames)

        data= ser.readline().decode().strip().split(",")# Read data from the serial port
        info = {
            "x_axis": x_axis  ,
            "Pressure": int(data[0][2:5])  ,
            "Temparature_A": int(data[1][3:5])  ,
            "Humidity":float(data[2][2:6])  ,
            "Temperature":float(data[3][3:6])
        }
        writer.writerow(info) # Write the data to the CSV file\
    csv_file.close()
    print(x_axis  ,data)
    x_axis+=1

    time.sleep(1)
