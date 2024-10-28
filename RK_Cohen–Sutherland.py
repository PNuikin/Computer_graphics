from random import randint
import time

Rec_v_x = [0 for _ in range(4)]
Rec_v_y = [0 for _ in range(4)]
Rec_x_left = 0
Rec_x_right = 0
Rec_y_bottom = 0
Rec_y_top = 0


def Set_RecBorder(x_left, y_bottom, x_right, y_top):  # Задаем границы области и координаты вершин прямоугольника
    global Rec_x_left, Rec_x_right, Rec_y_bottom, Rec_y_top
    if x_left >= x_right or y_bottom >= y_top:
        raise RuntimeError('Incorrect coordinates')
    Rec_x_left = Rec_v_x[0] = Rec_v_x[1] = x_left
    Rec_x_right = Rec_v_x[2] = Rec_v_x[3] = x_right
    Rec_y_bottom = Rec_v_y[1] = Rec_v_y[2] = y_bottom
    Rec_y_top = Rec_v_y[3] = Rec_v_y[0] = y_top


def Code(x, y):  # Кодируем вершину относительно границ области
    i = 0
    if x < Rec_x_left:
        i += 1
    elif x > Rec_x_right:
        i += 2
    if y < Rec_y_bottom:
        i += 4
    elif y > Rec_y_top:
        i += 8
    return i


def SC_Algorithm(x0, y0, x1, y1):  # Алгоритм Сезерленда-Коэна
    x_start = x0
    y_start = y0  # Координаты и код начала отрезка
    code_start = Code(x_start, y_start)
    x_end = x1
    y_end = y1  # Координаты и код конца отрезка
    code_end = Code(x_end, y_end)
    dx = x_end - x_start
    dy = y_end - y_start  # Приращения координат
    if dx != 0:
        dydx = dy / dx
    else:
        if dy == 0:
            if code_start == code_end == 0:
                return [x_start, y_start, x_end, y_end]  # Ситуация когда отрезок из 1 точки внутри окна
            else:
                return [None, None, None, None]  # Ситуация когда отрезок из 1 точки вне окна
    if dy != 0:
        dxdy = dx / dy
    for i in range(5):
        if code_start & code_end:  # Отрезок целиком вне окна
            return [None, None, None, None]
        if code_start == code_end == 0:  # Целиком внутри ока
            return [x_start, y_start, x_end, y_end]
        if not code_start:  # Если начало отрезка внутри окна меняем его с концом
            x_start, x_end = x_end, x_start
            y_start, y_end = y_end, y_start
            code_start, code_end = code_end, code_start
        if code_start & 1:  # Пересечение с левой стороной окна
            y_start = y_start + dydx * (Rec_x_left - x_start)
            x_start = Rec_x_left
        elif code_start & 2:  # Пересечение с правой стороной окна
            y_start = y_start + dydx * (Rec_x_right - x_start)
            x_start = Rec_x_right
        elif code_start & 4:  # Пересечение с нижней стороной окна
            x_start = x_start + dxdy * (Rec_y_bottom - y_start)
            y_start = Rec_y_bottom
        elif code_start & 8:  # Пересечение с верхней стороной окна
            x_start = x_start + dxdy * (Rec_y_top - y_start)
            y_start = Rec_y_top
        code_start = Code(x_start, y_start)  # Пересчитываем код начала отрезка


start = time.time()
Set_RecBorder(200, 225, 600, 575)
for i in range(1000000):
    x1 = randint(0, 1000)
    y1 = randint(0, 1000)
    x2 = randint(0, 1000)
    y2 = randint(0, 1000)
    ans = SC_Algorithm(x1, y1, x2, y2)
    print(*ans)
print('\033[1m', '\033[41m', time.time() - start)
