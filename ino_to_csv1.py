import csv
import time

# read the .ino file and store the contents in a list
with open('input.ino'  , 'r') as ino_file:
    lines = ino_file.readlines()

# remove any unwanted characters and split the contents into rows
rows = [line.strip().split('  ,') for line in lines]

# write the rows to a .csv file
with open('file.csv'  , 'a'  , newline='') as csv_file:
    writer = csv.writer(csv_file)

    # keep appending new data every second
    while True:
        with open('input.ino'  , 'r') as ino_file:
            lines = ino_file.readlines()
            new_rows = [line.strip().split('  ,') for line in lines]
            writer.writerows(new_rows)
        time.sleep(1)