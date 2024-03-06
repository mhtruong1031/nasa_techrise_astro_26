from random import randint
from math import sin
from csv import DictWriter

def main() -> None:
    n = 1000

    x      = [i for i in range(n)]
    sample = [i + 5 * sin(i/2) for i in range(n)]
    for i, val in enumerate(sample):
        if i % 6 == 0:
            sample[i] += randint(0, n)

    data = {
        "x": x,
        "y": sample
    }

    with open('sample_data.csv') as f:
        writer = DictWriter(f, fieldnames=["x", "y"])
        writer.writeheader() 
        writer.writerows(data)

if __name__ == '__main__':
    main()