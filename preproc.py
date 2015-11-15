# Association Rules Mining - hw3
# Advanced Database Systems
# Pedro Ferro Freitas - pff2108
# Roberto Jose de Amorim - rja2139

import csv
from collections import defaultdict
from sys import argv

data_file = argv[1]    # DOHMH_New_York_City_Restaurant_Inspection_Results.csv
index = int(argv[2])   # 0
data = int(argv[3])    # 10

sets = defaultdict(set)

try:
    with open(data_file, 'rb') as csvfile:
        sourcedata = csv.reader(csvfile, delimiter=',')
        for row in sourcedata:
            if row[data] == '':
                continue
            sets[row[index]].add(row[data])
except IOError:
    print "File not found!"
    exit(1)

output = file("INTEGRATED-DATASET.csv", "w")
for key in sets.keys():
    output.write(','.join(list(sets[key])) + "\n")

output.flush()

#print len(sets)

