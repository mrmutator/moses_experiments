import gzip
import sys
import locale

locale.setlocale(locale.LC_ALL,"")


big_name = sys.argv[1]
small_name = sys.argv[2]


count = 0

with gzip.open(big_name, "rb") as big, gzip.open(small_name, "rb") as small:
    next_target = small.readline().strip()
    curr = big.readline().strip()
    while True:
        #c = cmp(curr, next_target)
        if curr == next_target:
            c = 0
        else:
            s = sorted([curr, next_target], cmp=locale.strcoll)
            c = -1 if s[0] == curr else 1

        #print c, curr, "                               ", next_target
        if c > 0:
            next_target = small.readline().strip()
            if not next_target:
                break
        elif c==0:
            count += 1
            next_target = small.readline().strip()
            if not next_target:
                break
        else:
            curr = big.readline().strip()

with open(big_name + ".result", "w") as outfile:
    outfile.write(str(count))





