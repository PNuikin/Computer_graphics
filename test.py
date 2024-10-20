import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from PIL import Image
import numpy as np

def draw_line(x1, y1, x2, y2):
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
    error, t = el/2, 0
    img.putpixel((x, y), (255, 0, 0))
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
        img.putpixel((x, y), (255, 0, 0))

img = Image.new('RGB', (1100, 1100), (255, 255, 255))
draw_line(100, 100, 600, 600)
draw_line(600, 600, 400, 800)
draw_line(400, 800, 100, 100)
img.save('test_id.png')
