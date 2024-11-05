from PIL import Image
import re

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
    img.putpixel((x, y), (255, 255, 255))
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
        img.putpixel((x, y), (255, 255, 255))

def parse_obj(filename):
    with open(filename, 'rt') as f:
        vertices = []
        faces = []
        for line in f:
            mtch =  re.match("^v ([^ ]*) ([^ ]*) ([^ ]*)", line)
            if mtch is not None:
                x = float(mtch[1]) + img.width / 2
                y = float(mtch[2]) + img.height / 2
                z = float(mtch[3]) + img.height / 2
                vertices.append((x, y, z))
            mtch = re.match("^f [ \t]*([^ ]*) ([^ ]*) ([^ ]*)", line)
            if mtch is not None:
                faces.append((vertices[int(mtch[1]) - 1], vertices[int(mtch[2]) - 1], vertices[int(mtch[3]) - 1]))
    return vertices, faces

#def draw_face():

img = Image.new('RGB', (200, 200), 'black')
vertices, faces = parse_obj("diamond.obj")

for f in faces:
    l = len(f)
    for i in range(l):
        draw_line(round(f[i][0]), round(f[i][1]), round(f[(i + 1) % l][0]), round(f[(i + 1) % l][1]))

rotate_1 = [[][][]]



img.save("diamond.png")