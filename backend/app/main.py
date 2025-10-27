from time import sleep
import sys

print(sys.argv)

limit = int(sys.argv[-1])

n = 0
while True:
    print(n)
    n += 1
    sleep(1)
    if n == limit:
        exit()
