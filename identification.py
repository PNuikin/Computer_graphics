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
    img_new.putpixel((x, y), (255, 0, 0))
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
        img_new.putpixel((x, y), (255, 0, 0))

img_new = Image.new('RGB', (1100, 1100), (255, 255, 255))
img = Image.open('dial.png')
pixels = []
for i in range(img.size[0]):
    for j in range(img.size[1]):
        pixel = img.getpixel((i, j))
        if pixel == (255, 0, 0):
            pixels.append((i, j))
lines = dict()
delta_phi = 1
for pixel in pixels:
    phi = 0
    while phi < 180:
        l = np.sqrt(pixel[0] ** 2 + pixel[1] ** 2)
        d = round(l * np.cos(np.deg2rad((np.rad2deg(np.arctan(pixel[1] / pixel[0])) - 90 + phi) % 90)))
        if (phi, d) not in lines.keys():
            lines[(phi, d)] = set()
        lines[(phi, d)].add(pixel)
        phi += delta_phi
for i in lines.keys():
    if len(lines[i]) > 6:
        print(i)
        print(*lines[i], end='\n')
        lines[i] = list(lines[i])
        for j in range(len(lines[i])):
            draw_line(lines[i][j][0], lines[i][j][1], lines[i][j][0], lines[i][j][1])
imshow(np.asarray(img_new))
plt.show()