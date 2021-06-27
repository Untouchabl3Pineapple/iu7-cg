from math import cos, sin, radians


def get_circle_dots_coords():
    """
    Return format: [[x_coords][y_coords]]
    """

    circle = [[], []]
    degrs = 360
    r = 20

    for i in range(degrs + 1):
        circle[0].append(cos(radians(i)) * r)
        circle[1].append(sin(radians(i)) * r)

    return circle


def get_hyperbole_dots_coords():
    """
    Return format: [[x_coords][y_coords]]
    """

    hyperbole = [[], []]
    right_lim = 1
    left_lim = 30
    dot = 0.5
    k = 30

    while right_lim < left_lim:
        hyperbole[0].append(right_lim)
        hyperbole[1].append(k / right_lim)

        right_lim += dot

    return hyperbole


def move_loop(object, mx, my):
    dots_numb = len(object[0])

    for j in range(dots_numb):
        object[0][j] += mx
        object[1][j] += my


def rotate_loop(object, rx, ry, angle):
    dots_numb = len(object[0])

    for j in range(dots_numb):
        x_copy = object[0][j]
        y_copy = object[1][j]

        object[0][j] = (
            rx
            + (x_copy - rx) * cos(radians(angle))
            - (y_copy - ry) * sin(radians(angle))
        )
        object[1][j] = (
            ry
            + (y_copy - ry) * cos(radians(angle))
            + (x_copy - rx) * sin(radians(angle))
        )


def scale_loop(object, sx, sy, kx, ky):
    dots_numb = len(object[0])

    for j in range(dots_numb):
        object[0][j] = sx + kx * (object[0][j] - sx)
        object[1][j] = sy + ky * (object[1][j] - sy)