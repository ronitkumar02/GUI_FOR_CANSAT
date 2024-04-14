import csv
import time
import datetime
import random
import math
import serial

fieldnames = ["x_axis","roll","yaw","pitch","acc_x","acc_y","acc_z","mag_x","mag_y","mag_z","gyro_x","gyro_y","gyro_z","vel_x","vel_y","vel_z","descent_rate","state","temperature","gyro_rpm","humidity","pressure","battery",
              "gasResistance","altitude","current_ma","bus_voltage","shunt_voltage","power_mw","pack_voltage","bottom_voltage","top_voltage","second","minute","hour","day","month","year","number_of_satellites","latitude","longitude"]

x_axis = 0

# ser = serial.Serial('COM5',9600) # Change the port name to match your setup

with open('STARDUST_data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()

while True:
    with open('STARDUST_data.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        current_time = datetime.datetime.now()
        # Generating random data for each column
        # data = ser.readline().decode().strip().split(",")
        info = {
    "x_axis": x_axis,
    "roll": round(random.random(), 3),
    "yaw": round(random.random(), 3),
    "pitch": round(random.random(), 3),
    "acc_x": round(random.random(), 3),
    "acc_y": round(random.random(), 3),
    "acc_z": round(random.random(), 3),
    "mag_x": round(random.random(), 3),
    "mag_y": round(random.random(), 3),
    "mag_z": round(random.random(), 3),
    "gyro_x": round(random.random(), 3),
    "gyro_y": round(random.random(), 3),
    "gyro_z": round(random.random(), 3),
    "vel_x": round(random.random(), 3),
    "vel_y": round(random.random(), 3),
    "vel_z": round(random.random(), 3),
    "descent_rate": round(random.random(), 3),
    "state": random.randint(1, 6),
    "temperature": round(random.random(), 3),
    "gyro_rpm": round(random.random(), 3),
    "humidity": round(random.random(), 3),
    "pressure": round(random.random(), 3),
    "battery": math.ceil(random.random()*100),
    "gasResistance": round(random.random(), 3),
    "altitude": round(random.random(), 3),
    "current_ma": round(random.random(), 3),
    "bus_voltage": round(random.random(), 3),
    "shunt_voltage": round(random.random(), 3),
    "power_mw": round(random.random(), 3),
    "pack_voltage": round(random.random(), 3),
    "bottom_voltage": round(random.random(), 3),
    "top_voltage": round(random.random(), 3),
    "second": current_time.second,
    "minute": current_time.minute,
    "hour": current_time.hour,
    "day": current_time.day,
    "month": current_time.month,
    "year": current_time.year,
    "number_of_satellites": round(random.random(), 3),
    "latitude": round(random.random(), 6)*100,
    "longitude": round(random.random(), 6)*100
}
        writer.writerow(info)  # Write the data to the CSV file

    print(x_axis,info)
    x_axis += 1
    time.sleep(1)
