import serial
import csv
import time
import datetime


fieldnames = ["x_value"  ,"Pressure"  ,"Temparature_A"  ,"Humidity"  ,"Temperature"]
x_value=0
with open('arduinoP&T_data.csv'  , 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file  , fieldnames=fieldnames)
    csv_writer.writeheader()

ser = serial.Serial('COM5'  , 9600) # Change the port name to match your setup
while True:
    with open('arduinoP&T_data.csv'  , 'a'  , newline='') as csvfile:
        writer = csv.DictWriter(csvfile  ,fieldnames=fieldnames)

        data= ser.readline().decode().strip().split(",")# Read data from the serial port
        # data= [int(i) for i in data]
        info = {
            "x_value": x_value  ,
            "Pressure": int(data[0][2:5])  ,
            "Temparature_A": int(data[1][3:5])  ,
            "Humidity":float(data[2][2:6])  ,
            "Temperature":float(data[3][3:6])
        }
        writer.writerow(info) # Write the data to the CSV file\
    csv_file.close()
    # set the file name and path
    file_path = 'text_file.txt'

    # create and open the file for writing
    # file = open(file_path, 'w')
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    with open(file_path, 'a') as file:
        file.write(f'{data} ({current_time})\n')
        # current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # write the text and current time to the file
        # file.write(f'{text} ({current_time})\n')

    # close the file
    file.close()
    print(x_value  ,data)
    x_value+=1

    time.sleep(1)
