from math import floor, fabs


def get_color(color, light):
    return color + (light, light, light)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def dda(beg_point, end_point, color, step_count=False):
    dx = end_point[0] - beg_point[0]
    dy = end_point[1] - beg_point[1]

    if dx == 0 and dy == 0:
        return [[round(beg_point[0]), round(beg_point[1]), color]]

    l = abs(dx) if abs(dx) >= abs(dy) else abs(dy)

    dx /= l
    dy /= l

    x = beg_point[0]
    y = beg_point[1]

    points = [[round(x), round(y), color]]
    steps = 0

    i = 1
    while i <= l:
        if step_count:
            x_buf = x
            y_buf = y

        x += dx
        y += dy

        if step_count == False:
            points.append([round(x), round(y), color])

        elif round(x_buf) != round(x) and round(y_buf) != round(y):
            steps += 1

        i += 1

    if step_count:
        return steps
    else:
        return points


def bresenham_float(beg_point, end_point, color, step_count=False):
    dx = end_point[0] - beg_point[0]
    dy = end_point[1] - beg_point[1]

    if dx == 0 and dy == 0:
        return [[beg_point[0], beg_point[1], color]]

    x_sign = sign(dx)
    y_sign = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        exchange = 1
    else:
        exchange = 0

    e = dy / dx - 0.5

    x = beg_point[0]
    y = beg_point[1]
    points = []

    x_buf = x
    y_buf = y
    steps = 0

    i = 0
    while i <= dx:
        if step_count == False:
            points.append([x, y, color])

        if e >= 0:
            if exchange:
                x += x_sign
            else:
                y += y_sign

            e -= 1

        if exchange:
            y += y_sign
        else:
            x += x_sign

        e += dy / dx
        i += 1

        if step_count:
            if x_buf != x and y_buf != y:
                steps += 1

            x_buf = x
            y_buf = y

    if step_count:
        return steps
    else:
        return points


def bresenham_int(beg_point, end_point, color, step_count=False):
    dx = end_point[0] - beg_point[0]
    dy = end_point[1] - beg_point[1]

    if dx == 0 and dy == 0:
        return [[beg_point[0], beg_point[1], color]]

    x_sign = sign(dx)
    y_sign = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        exchange = 1
    else:
        exchange = 0

    two_dy = 2 * dy
    two_dx = 2 * dx

    e = two_dy - dx

    x = beg_point[0]
    y = beg_point[1]
    points = []

    x_buf = x
    y_buf = y
    steps = 0

    i = 0
    while i <= dx:
        if step_count == False:
            points.append([x, y, color])

        if e >= 0:
            if exchange == 1:
                x += x_sign
            else:
                y += y_sign

            e -= two_dx

        if exchange == 1:
            y += y_sign
        else:
            x += x_sign

        e += two_dy
        i += 1

        if step_count:
            if x_buf != x and y_buf != y:
                steps += 1

            x_buf = x
            y_buf = y

    if step_count:
        return steps
    else:
        return points


def bresenham_antialiased(beg_point, end_point, color, step_count=False):
    dx = end_point[0] - beg_point[0]
    dy = end_point[1] - beg_point[1]

    if dx == 0 and dy == 0:
        return [[beg_point[0], beg_point[1], color]]

    x_sign = sign(dx)
    y_sign = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        exchange = 1
    else:
        exchange = 0

    I = 255

    m = dy / dx
    w = 1 - m
    e = 0.5

    x = beg_point[0]
    y = beg_point[1]
    points = []

    x_buf = x
    y_buf = y
    steps = 0

    i = 0
    while i <= dx:
        if step_count == False:
            points.append([x, y, get_color(color, I * e)])

        if e < w:
            if exchange == 0:
                x += x_sign
            else:
                y += y_sign

            e += m

        else:
            x += x_sign
            y += y_sign
            e -= w

        i += 1

        if step_count:
            if x_buf != x and y_buf != y:
                steps += 1

            x_buf = x
            y_buf = y

    if step_count:
        return steps
    else:
        return points


def wu(one_point, two_point, color, step_count=False):
    x1 = one_point[0]
    y1 = one_point[1]
    x2 = two_point[0]
    y2 = two_point[1]

    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return [[x1, x2, color]]

    m = 1
    I = 255
    step = 1
    steps = 0
    points = []

    if abs(dy) >= abs(dx):
        if dy != 0:
            m = dx / dy

        m1 = m

        if y1 > y2:
            m1 *= -1
            step *= -1

        bord = round(y2) - 1 if dy < dx else round(y2) + 1

        for y in range(round(y1), bord, step):
            d1 = x1 - floor(x1)
            d2 = 1 - d1

            if step_count == False:
                points.append([int(x1) + 1, y, get_color(color, round(fabs(d2) * I))])
                points.append([int(x1), y, get_color(color, round(fabs(d1) * I))])

            elif y < round(y2) and int(x1) != int(x1 + m):
                steps += 1

            x1 += m1
    else:
        if dx != 0:
            m = dy / dx

        m1 = m

        if x1 > x2:
            step *= -1
            m1 *= -1

        bord = round(x2) - 1 if dy > dx else round(x2) + 1

        for x in range(round(x1), bord, step):
            d1 = y1 - floor(y1)
            d2 = 1 - d1

            if step_count == False:
                points.append([x, int(y1) + 1, get_color(color, round(fabs(d2) * I))])
                points.append([x, int(y1), get_color(color, round(fabs(d1) * I))])

            elif x < round(x2) and int(y1) != int(y1 + m):
                steps += 1

            y1 += m1

    if step_count:
        return steps
    else:
        return points
