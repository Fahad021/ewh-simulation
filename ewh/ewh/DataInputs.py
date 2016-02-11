import csv
import math
# import config
with open('../Data/WaterUse.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader)
    a = []
    for row in reader:
        value = row['Gallons/Hour']
        a.append(value)

#  foo = (time of program * TIME_SCALING_FACTOR)%24
foo = ((25 * 1)%24)-1
bar = a[foo]

print(bar)


with open('../Data/AirTemperature.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(reader)
    b = []
    for row in reader:
        value = row['Fahrenheit']
        b.append(value)

alpha = math.ceil((1320 * 1)/24)
beta = b[alpha]

print(beta)

