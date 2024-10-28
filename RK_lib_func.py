from pylineclip import cohensutherland
from random import randint
import time


start = time.time()
xmin = 200
xmax = 600
ymin = 225
ymax = 575
for i in range(1000000):
    x1 = randint(0,1000)
    y1 = randint(0,1000)
    x2 = randint(0,1000)
    y2 = randint(0,1000)
    x3,y3,x4,y4 = cohensutherland(xmin, ymax, xmax, ymin, x1, y1, x2, y2)
    print(x3,y3,x4,y4)
print('\033[1m', '\033[41m', time.time() - start)
