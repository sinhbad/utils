#!/usr/bin/python3
import sys
import csv
output = ""
with open(sys.argv[1], "r") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=";")
    header = csvreader.__next__()
    for row in csvreader:
        for propi in range(len(row)):
            if (row[propi] != ""):
                output += "{0}: {1}\n".format(header[propi], row[propi])
        output += "{0}\n".format("=" * 50)
print(output)

