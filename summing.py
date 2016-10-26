import glob
import sys

d = sys.argv[1]

files = glob.glob(d + "*.sub.gz.result")

sum = 0


for f in files:
    with open(f, "r") as infile:
        x = int(infile.read().strip())
        sum += x

with open(d + "total.txt", "w") as outfile:
    outfile.write(str(sum))