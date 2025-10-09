import sys

limit = int(sys.argv[1])
maxrec = limit
n = maxrec % 100
if n != 0:
    maxrec += n

for page in range(0, limit, 100):
    lim = min(100, limit-page)
    print(page, lim)
