import csv

with open('/Users/nathanlevin/Desktop/Bsc AE/Year 2 2020:21/Q2/Project_WP4:WP5/Project_Github/MainWing_a0.00_v10.00ms.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        print(row[0])
        #print(row[0],row[1],row[2],)
