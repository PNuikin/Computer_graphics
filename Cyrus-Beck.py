import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from PIL import Image
import numpy as np
from numpy.ma.core import append

Win_v_x = []
Win_v_y = []
Win_border_norms_x = []
Win_border_norms_y = []
nuber_vessels = 0


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

def Set_WinBorder(vessels):  # Задаем границы области и координаты вершин прямоугольника
    global Win_v_x, Win_v_y, nuber_vessels
    for vessel in vessels:
        Win_v_x.append(vessel[0])
        Win_v_y.append(vessel[1])
    nuber_vessels = len(Win_v_x)
    for i in range(nuber_vessels):
        Win_border_norms_y.append(-(Win_v_x[(i + 1) % nuber_vessels] - Win_v_x[i]))
        Win_border_norms_x.append((Win_v_y[(i + 1) % nuber_vessels] - Win_v_y[i]))

def Draw_Border():
    for i in range(nuber_vessels):
        draw_line(Win_v_x[i], Win_v_y[i], Win_v_x[(i + 1) % nuber_vessels], Win_v_y[(i + 1) % nuber_vessels], (255, 0, 0))

def CB_Algorithm(x0, y0, x1, y1):
    t0 = 0
    t1 = 1
    dx = x1 - x0
    dy = y1 - y0
    xn = x0
    yn = y0
    for i in range(nuber_vessels):
        Qx = x0 - Win_v_x[i]
        Qy = y0 - Win_v_y[i]
        Pn = dx * Win_border_norms_x[i] + dy * Win_border_norms_y[i]
        Qn = Qx * Win_border_norms_x[i] + Qy * Win_border_norms_y[i]
        if Pn == 0:
            if Qn < 0:
                return []
        else:
            r = - Qn / Pn
            if Pn < 0:
                if r < 0:
                    return []
                if r < t1:
                    t1 = r
            else:
                if r > 1:
                    return []
                if r > t0:
                    t0 = r
    if t0 > t1:
        return []
    else:
        if t0 > 0:
            x0 = xn + t0 * dx
            y0 = yn + t0 * dy
        if t1 < 1:
            x1 = xn + t1 * dx
            y1 = yn + t1 * dy
    return [x0, y0, x1, y1]


img = Image.new('RGB', (800, 800), (255, 255, 255))

Set_WinBorder([(100, 100), (300, 400), (500, 600), (700, 600), (750, 200)])

coords = CB_Algorithm(0, 0, 800, 800)
if coords:
    coords = [round(coords[i]) for i in range(len(coords))]
    draw_line(coords[0], coords[1], coords[2], coords[3], (0, 255, 0))

coords = CB_Algorithm(700, 400, 300, 790)
if coords:
    coords = [round(coords[i]) for i in range(len(coords))]
    draw_line(coords[0], coords[1], coords[2], coords[3], (0, 255, 255))

coords = CB_Algorithm(250, 300, 500, 550)
if coords:
    coords = [round(coords[i]) for i in range(len(coords))]
    draw_line(coords[0], coords[1], coords[2], coords[3], (0, 0, 0))

coords = CB_Algorithm(0, 0, 180, 790)
if coords:
    coords = [round(coords[i]) for i in range(len(coords))]
    draw_line(coords[0], coords[1], coords[2], coords[3], (0, 0, 0))

Draw_Border()

img.save('test_CB.png')

