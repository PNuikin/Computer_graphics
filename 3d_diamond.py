from PIL import Image
import re
import math as m
import numpy as np
from PIL.ImagePalette import random


class point3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def draw_line(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    slope = dy > dx

    if slope:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    error = dx // 2
    y = y1
    y_step = 1 if y1 < y2 else -1

    points = []

    for x in range(x1, x2 + 1):
        coord = (y, x) if slope else (x, y)
        points.append(coord)
        error -= dy
        if error < 0:
            y += y_step
            error += dx

    return points


def parse_obj(filename):
    with open(filename, 'rt') as f:
        vertices = []
        faces = []
        for line in f:
            mtch = re.match("^v ([^ ]*) ([^ ]*) ([^ ]*)", line)
            if mtch is not None:
                x = float(mtch[1])
                y = float(mtch[2])
                z = float(mtch[3])
                vertices.append([x, y, z])
            mtch = re.match("^f [ \t]*([^ ]*) ([^ ]*) ([^ ]*)", line)
            if mtch is not None:
                faces.append([vertices[int(mtch[1]) - 1], vertices[int(mtch[2]) - 1], vertices[int(mtch[3]) - 1]])
    return vertices, faces


def matrix_vector(matrix, vector):
    ans = [0.0, 0.0, 0.0, 0.0]
    for i in range(len(matrix)):
        for j in range(len(vector)):
            ans[i] += matrix[i][j] * vector[j]
    return ans


def center():
    for f in faces:
        l = len(f)
        for i in range(l):
            f[i] = [(f[i][0] + img.width / 2) % img.width, f[i][1] + (img.height / 2) % img.width,
                    (f[i][2] + img.width / 2) % img.width]


def get_plane(point1, point2, point3):
    x1, y1, z1 = point1.x, point1.y, point1.z
    x2, y2, z2 = point2.x, point2.y, point2.z
    x3, y3, z3 = point3.x, point3.y, point3.z

    vector1 = [x2 - x1, y2 - y1, z2 - z1]
    vector2 = [x3 - x1, y3 - y1, z3 - z1]

    normal_vector = [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    ]

    A, B, C = normal_vector[0], normal_vector[1], normal_vector[2]
    D = -(A * x1 + B * y1 + C * z1)

    return A, B, C, D


def del_seq(arr):
    i = len(arr) - 1
    while i > 0:

        if arr[i] == arr[i - 1] + 1:
            arr.pop(i)
            break
        i -= 1
    if len(arr) % 2 == 1:
        arr.pop(len(arr) - 2)
    return arr


def fill2D(vertexes):
    points = dict()
    for i in range(len(vertexes)):
        x1, y1 = round(vertexes[i].x), round(vertexes[i].y)
        x2 = round(vertexes[(i + 1) % len(vertexes)].x)
        y2 = round(vertexes[(i + 1) % len(vertexes)].y)

        if y2 == y1:
            continue

        line = draw_line(x1, y1, x2, y2)
        if y2 > y1:
            line.remove((x1, y1))
        else:
            line.remove((x2, y2))

        for point in line:
            if point[1] in points.keys():
                points[point[1]].append(point[0])
            else:
                points[point[1]] = [point[0]]

    line = []
    for y in points.keys():
        points[y].sort()
        line += [(k, y) for k in range(points[y][0], points[y][-1] + 1)]
    return line


def fill3D(vertexes):
    points = fill2D(vertexes)
    A, B, C, D = get_plane(vertexes[0], vertexes[1], vertexes[2])
    find_z = lambda x, y: int((-D - A * x - B * y) / C) if C != 0 else 0

    new_points = []
    for point in points:
        z = find_z(point[0], point[1])
        new_points.append(point3(point[0], point[1], z))
    return new_points


def update_buffer(points, z_buffer):
    for point in points:
        if point.z < z_buffer[int(point.x)][int(point.y)]:
            z_buffer[int(point.x)][int(point.y)] = point.z


def draw_buffer(image, points, z_buffer, color):
    for point in points:
        if point.z <= z_buffer[int(point.x)][int(point.y)]:
            image.putpixel((int(point.x), int(point.y)), color)


img = Image.new('RGB', (300, 300), 'black')
vertices, faces = parse_obj("diamond.obj")

z_buffer = [[1000 for _ in range(300)] for a in range(300)]

rotate_1 = [[m.cos(m.radians(45)), -m.sin(m.radians(45)), 0, 0],
            [m.sin(m.radians(45)), m.cos(m.radians(45)), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]]
for f in faces:
    l = len(f)
    for i in range(l):
        ans = matrix_vector(rotate_1, [f[i][0], f[i][1], f[i][2], 1])
        f[i] = [ans[0], ans[1], ans[2]]

rotate_2 = [[1, 0, 0, 0],
            [0, m.cos(m.radians(45)), -m.sin(m.radians(45)), 0],
            [0, m.sin(m.radians(45)), m.cos(m.radians(45)), 0],
            [0, 0, 0, 1]]
for f in faces:
    l = len(f)
    for i in range(l):
        ans = matrix_vector(rotate_2, [f[i][0], f[i][1], f[i][2], 1])
        f[i] = [ans[0], ans[1], ans[2]]

rotate_3 = [[m.cos(m.radians(45)), 0, m.sin(m.radians(45)), 0],
            [0, 1, 0, 0],
            [-m.sin(m.radians(45)), 0, m.cos(m.radians(45)), 0],
            [0, 0, 0, 1]]
for f in faces:
    l = len(f)
    for i in range(l):
        ans = matrix_vector(rotate_3, [f[i][0], f[i][1], f[i][2], 1])
        f[i] = [ans[0], ans[1], ans[2]]

center()
new_faces = []
for f in range(len(faces)):
    A = point3(faces[f][0][0], faces[f][0][1], faces[f][0][2])
    B = point3(faces[f][1][0], faces[f][1][1], faces[f][1][2])
    C = point3(faces[f][2][0], faces[f][2][1], faces[f][2][2])
    new_faces.append(fill3D([A, B, C]))
    update_buffer(new_faces[f], z_buffer)

for f in new_faces:
    draw_buffer(img, f, z_buffer, tuple(np.random.choice(range(256), size=3)))

# for f in faces:
#     l = len(f)
#     for i in range(l):
#         draw_line(round(f[i][0]), round(f[i][1]), round(f[(i + 1) % l][0]), round(f[(i + 1) % l][1]))

img.save("diamond.png")
