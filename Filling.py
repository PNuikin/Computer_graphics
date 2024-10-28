import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from PIL import Image
import numpy as np
from numpy.ma.core import append


y_min = 100000000
y_max = -1


def draw_line(x1, y1, x2, y2, color):
    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y = x1, y1
    error, t = el / 2, 0
    img.putpixel((x, y), color)
    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1
        img.putpixel((x, y), color)

def Draw_Border():
    global vessels, nuber_vessels
    for i in range(nuber_vessels):
        draw_line(vessels[i][0], vessels[i][1], vessels[(i + 1) % nuber_vessels][0], vessels[(i + 1) % nuber_vessels][1],
                  (255, 0, 0))


def Calculate_X(y, Pi, Pi1):
    return (y - Pi[1]) * (Pi1[0] - Pi[0]) / (Pi1[1] - Pi[1]) + Pi[0]

def Extreme():
    global y_min, y_max, vessels
    for i in vessels:
        if y_min > i[1]:
            y_min = i[1]
        if y_max < i[1]:
            y_max = i[1]

def Line_Filling():
    global y_min, y_max, nuber_vessels, vessels
    for y in range(y_min, y_max):
        border = []
        for i in range(nuber_vessels):
            if vessels[i][1] != vessels[(i + 1) % (nuber_vessels)][1]:
                if max(vessels[i][1], vessels[(i + 1) % (nuber_vessels)][1]) >= y > min(vessels[i][1], vessels[(i + 1) % (nuber_vessels)][1]):
                    x = Calculate_X(y, vessels[i], vessels[(i + 1) % (nuber_vessels)])
                    border.append(x)
        for j in range(0, len(border), 2):
            draw_line(round(border[j]), y, round(border[j + 1]), y, (0, 0, 255))



img = Image.new('RGB', (200, 200), (255, 255, 255))

vessels = [(80, 0), (62, 54), (0, 54), (50, 90), (30, 148), (80, 112), (130, 148), (110, 90), (160, 54), (98, 54)]
nuber_vessels = len(vessels)
Extreme()

Line_Filling()

Draw_Border()

img.save('test_filling.png')
