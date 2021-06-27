import colorutils as cu


def set_pixel(canvas, x, y, color):
    canvas.create_line(x, y, x + 1, y, fill=color.hex)


def reflect_dots_diag(dots, xc, yc):
    count_dots = len(dots)

    for i in range(count_dots):
        dots.append([dots[i][1] - yc + xc, dots[i][0] - xc + yc, dots[i][2]])


def reflect_dots_Oy(dots, xc):
    count_dots = len(dots)

    for i in range(count_dots):
        dots.append([-(dots[i][0] - xc) + xc, dots[i][1], dots[i][2]])


def reflect_dots_Ox(dots, yc):
    count_dots = len(dots)

    for i in range(count_dots):
        dots.append([dots[i][0], -(dots[i][1] - yc) + yc, dots[i][2]])


def draw_pixels(canvas, dot, xc, yc, circle=True):
    dots = [dot]

    if circle:
        reflect_dots_diag(dots, xc, yc)

    reflect_dots_Oy(dots, xc)
    reflect_dots_Ox(dots, yc)

    if dots[0][2] == cu.Color((255, 255, 255)):
        for _ in range(6):
            for i in dots:
                set_pixel(canvas, i[0], i[1], i[2])
    else:
        for i in dots:
            set_pixel(canvas, i[0], i[1], i[2])