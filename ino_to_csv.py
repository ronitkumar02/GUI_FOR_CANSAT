import serial
import csv
import time

fieldnames = ["x_value"  , "total_1"  , "total_2"]
x_value=0
with open('arduino_data.csv'  , 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file  , fieldnames=fieldnames)
    csv_writer.writeheader()

ser = serial.Serial('COM5'  , 9600) # Change the port name to match your setup
while True:
    with open('arduino_data.csv'  , 'a'  , newline='') as csvfile:
        writer = csv.DictWriter(csvfile  ,fieldnames=fieldnames)

        data= list(map(int  ,ser.readline().decode().strip().split("  ,")))# Read data from the serial port
        # data= [int(i) for i in data]
        info = {
            "x_value": x_value  ,
            "total_1": data[0]  ,
            "total_2": data[1]
        }
        writer.writerow(info) # Write the data to the CSV file\
    print(x_value  ,data[0]  ,data[1])
    x_value+=1

    time.sleep(1)