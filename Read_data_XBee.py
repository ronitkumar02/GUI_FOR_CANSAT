import csv
import time
import datetime
import random
import math
import serial

fieldnames = ["x_axis","roll","yaw","pitch","acc_x","acc_y","acc_z","mag_x","mag_y","mag_z","gyro_x","gyro_y","gyro_z","vel_x","vel_y","vel_z","descent_rate","state","temperature","gyro_rpm","humidity","pressure","battery",
              "gasResistance","altitude","current_ma","bus_voltage","shunt_voltage","power_mw","pack_voltage","bottom_voltage","top_voltage","second","minute","hour","day","month","year","number_of_satellites","latitude","longitude"]

x_axis = 0

ser = serial.Serial('COM5',9600) # Change the port name to match your setup

with open('STARDUST_data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('STARDUST_data.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        current_time = datetime.datetime.now()
        data = ser.readline().decode().strip().split(",")
        info = {
    "x_axis": x_axis,
    "roll":data[0],
    "yaw":data[0],
    "pitch":data[0],
    "acc_x":data[0],
    "acc_y":data[0],
    "acc_z":data[0],
    "mag_x":data[0],
    "mag_y":data[0],
    "mag_z":data[0],
    "gyro_x":data[0],
    "gyro_y":data[0],
    "gyro_z":data[0],
    "vel_x":data[0],
    "vel_y":data[0],
    "vel_z":data[0],
    "descent_rate":data[0],
    "state": random.randint(1, 6),
    "temperature":data[0],
    "gyro_rpm":data[0],
    "humidity":data[0],
    "pressure":data[0],
    "battery": math.ceil(random.random()*100),
    "gasResistance":data[0],
    "altitude":data[0],
    "current_ma":data[0],
    "bus_voltage":data[0],
    "shunt_voltage":data[0],
    "power_mw":data[0],
    "pack_voltage":data[0],
    "bottom_voltage":data[0],
    "top_voltage":data[0],
    "second": current_time.second,
    "minute": current_time.minute,
    "hour": current_time.hour,
    "day": current_time.day,
    "month": current_time.month,
    "year": current_time.year,
    "number_of_satellites":data[0],
    "latitude": data[0],
    "longitude": data[0]
}
        writer.writerow(info)  # Write the data to the CSV file

    print(x_axis,info)
    x_axis += 1
    time.sleep(1)
