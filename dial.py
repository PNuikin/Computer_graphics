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


r = int(input())
img = Image.new('RGB', (1100, 1100), (255, 255, 255))
buf = 550
img.putpixel((0 + buf, r + buf), (255, 0, 0))
delta = 3 - 2 * r
y = r
x = 0
while abs(x - y) > 1:
    if delta <= 0:
        img.putpixel((x + 1 + buf, y + buf), (255, 0, 0))
        img.putpixel((y + buf, x + 1 + buf), (255, 0, 0))
        img.putpixel((-(x + 1) + buf, -y + buf), (255, 0, 0))
        img.putpixel((-y + buf, -(x + 1) + buf), (255, 0, 0))
        img.putpixel((-(x + 1) + buf, y + buf), (255, 0, 0))
        img.putpixel((y + buf, -(x + 1) + buf), (255, 0, 0))
        img.putpixel(((x + 1) + buf, -y + buf), (255, 0, 0))
        img.putpixel((-y + buf, (x + 1) + buf), (255, 0, 0))
        delta += 4 * x + 6
        x += 1
    else:
        img.putpixel((x + 1 + buf, y - 1 + buf), (255, 0, 0))
        img.putpixel((y - 1 + buf, x + 1 + buf), (255, 0, 0))
        img.putpixel((-(x + 1) + buf, -(y - 1) + buf), (255, 0, 0))
        img.putpixel((-(y - 1) + buf, -(x + 1) + buf), (255, 0, 0))
        img.putpixel((-(x + 1) + buf, (y - 1) + buf), (255, 0, 0))
        img.putpixel(((y - 1) + buf, -(x + 1) + buf), (255, 0, 0))
        img.putpixel(((x + 1) + buf, -(y - 1) + buf), (255, 0, 0))
        img.putpixel((-(y - 1) + buf, (x + 1) + buf), (255, 0, 0))
        delta += 4 * x - 4 * y + 10
        x += 1
        y -= 1
for i in range(-6, 7):
    x1 = buf + round(r * np.sin(np.radians(30) * i))
    y1 = buf + round(r * np.cos(np.radians(30) * i))
    x2 = buf + round(r * 0.75 * np.sin(np.radians(30) * i))
    y2 = buf + round(r * 0.75 * np.cos(np.radians(30) * i))
    draw_line(x1, y1, x2, y2)
for i in range(-30, 31):
    x1 = buf + round(r * np.sin(np.radians(6) * i))
    y1 = buf + round(r * np.cos(np.radians(6) * i))
    x2 = buf + round(r * 0.90 * np.sin(np.radians(6) * i))
    y2 = buf + round(r * 0.90 * np.cos(np.radians(6) * i))
    draw_line(x1, y1, x2, y2)
imshow(np.asarray(img))
plt.show()
