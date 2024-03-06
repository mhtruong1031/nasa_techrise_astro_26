from random import randint
from math import sin
from csv import DictWriter

x      = [i for i in range(1000)]
sample = [i + 5 * sin(i/2) for i in range(1000)]
for i, val in enumerate(sample):
    if i % 6 == 0:
        sample[i] += randint(0, 1000)

data = {
    "x": x,
    "y": sample
}

with open('sample_data.csv') as f:
    writer = DictWriter(f, fieldnames=["x", "y"])
    writer.writeheader() 
    writer.writerows(data)