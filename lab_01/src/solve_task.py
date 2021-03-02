from tkinter import *
from tkinter.messagebox import showerror, showinfo

from sympy.geometry import Point, Circle

from math import atan, degrees

from copy import deepcopy


def draw_points(canvas, circles):
    for i in range(len(circles) - 1):
        for j in range(len(circles[i])):
            x = circles[i][j][0]
            y = circles[i][j][1]

            canvas.create_oval(x - 1, y - 1, x + 1, y + 1, width=2)


def draw_circles(canvas, circles):
    for i in range(len(circles) - 1):
        x = circles[i][0][0]
        y = circles[i][0][1]
        r = circles[i][0][2]

        if i == 0:
            canvas.create_oval(x - r, y - r, x + r, y + r, width=1, outline="orchid3")
        else:
            canvas.create_oval(x - r, y - r, x + r, y + r, width=1, outline="salmon1")


def draw_split_line(canvas, circles):
    """
    The equation in question: y = kx + b
    """

    x1 = circles[0][0][0]
    y1 = circles[0][0][1]
    x2 = circles[1][0][0]
    y2 = circles[1][0][1]

    k_l = (y2 - y1) / (x2 - x1)
    b = y1 - k_l * x1

    canvas_width = 694

    x1 = 0
    y1 = -1 * (k_l * x1 + b) + canvas_width
    x2 = canvas_width
    y2 = -1 * (k_l * x2 + b) + canvas_width

    canvas.create_line(x1, y1, x2, y2, fill="green3")


def draw_coords(canvas, magic_circles, circles):
    coord_size = 12
    indent = 5

    for i in range(len(magic_circles) - 1):
        for j in range(len(magic_circles[i])):
            canvas.create_text(
                magic_circles[i][j][0],
                magic_circles[i][j][1] + indent,
                text="({:.1f},{:.1f})".format(circles[i][j][0], circles[i][j][1]),
                font=("Times new roman", coord_size),
            )


def draw_ordinate(canvas, zoom_vars):
    canvas_start_pos = 0
    canvas_width = 694
    indent = 8

    k_z = zoom_vars[0]
    min_x = zoom_vars[1][0]

    x1 = k_z * (-min_x)
    y1 = canvas_width
    x2 = k_z * (-min_x)
    y2 = canvas_start_pos

    canvas.create_line(x1, y1, x2, y2, arrow=LAST)
    canvas.create_text(x2 + indent, y2 + indent, text="y")


def draw_angle(canvas, circles, zoom_vars):
    canvas_width = 694
    coord_size = 12
    indent = 8

    x1 = circles[0][0][0]
    y1 = circles[0][0][1]
    x2 = circles[1][0][0]
    y2 = circles[1][0][1]

    k_l = (y2 - y1) / (x2 - x1)
    b = y1 - k_l * x1

    k_z = zoom_vars[0]
    min_x = zoom_vars[1][0]
    min_y = zoom_vars[1][1]

    x_a = k_z * (-min_x)
    y_a = canvas_width - (k_z * (b - min_y))

    canvas.create_text(
        x_a - indent,
        y_a,
        text="alpha",
        font=("Times new roman", coord_size),
    )


def form_coord_matrix(set_points):
    for i in range(len(set_points)):
        set_points[i] = set_points[i].split(";")

        set_points[i][0] = float(set_points[i][0])
        set_points[i][1] = float(set_points[i][1])


def form_circles_list(circles, set_points):
    for i in range(len(set_points)):
        for j in range(i + 1, len(set_points)):
            for k in range(j + 1, len(set_points)):
                res = Circle(
                    Point(set_points[i][0], set_points[i][1]),
                    Point(set_points[j][0], set_points[j][1]),
                    Point(set_points[k][0], set_points[k][1]),
                )

                if type(res) is Circle:
                    parameters = []
                    circle = []

                    circle.append(float(res.center.x))
                    circle.append(float(res.center.y))
                    circle.append(float(res.radius))

                    parameters.append(circle)

                    parameters.append(set_points[i])
                    parameters.append(set_points[j])
                    parameters.append(set_points[k])

                    circles.append(parameters)


def get_magic_circles(circles):
    """
    The function returns the desired coordinates and radii of the two circles

    The equation in question: y = kx + b
    """

    coords = ["first_circle", "second_circle", "tang"]
    min_angle = 91  # Upper limit of the angle tangent

    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            x1 = circles[i][0][0]
            y1 = circles[i][0][1]
            x2 = circles[j][0][0]
            y2 = circles[j][0][1]

            if x1 == x2:
                continue
            if y1 == y2:
                angle = 90.0
            else:
                k_l = (y2 - y1) / (x2 - x1)
                b = y1 - k_l * x1

                if y1 != b:
                    angle = degrees(atan(abs(x1 / (y1 - b))))
                elif y2 != b:
                    angle = degrees(atan(abs(x2 / (y2 - b))))
                else:
                    continue

            if angle < min_angle:
                min_angle = angle

                coords[0] = deepcopy(circles[i])
                coords[1] = deepcopy(circles[j])
                coords[2] = min_angle

    return coords


def form_canvas_coords(circles):
    canvas_width = 694

    for i in range(len(circles) - 1):
        for j in range(len(circles[i])):
            circles[i][j][1] *= -1
            circles[i][j][1] += canvas_width


def get_zoom_vars(circles):
    canvas_width = 694

    c1x_min = circles[0][0][0] - circles[0][0][2]
    c2x_min = circles[1][0][0] - circles[1][0][2]

    c1x_max = circles[0][0][0] + circles[0][0][2]
    c2x_max = circles[1][0][0] + circles[1][0][2]

    c1y_min = circles[0][0][1] - circles[0][0][2]
    c2y_min = circles[1][0][1] - circles[1][0][2]

    c1y_max = circles[0][0][1] + circles[0][0][2]
    c2y_max = circles[1][0][1] + circles[1][0][2]

    x1 = circles[0][0][0]
    y1 = circles[0][0][1]
    x2 = circles[1][0][0]
    y2 = circles[1][0][1]

    k_l = (y2 - y1) / (x2 - x1)
    b = y1 - k_l * x1

    min_x = min(c1x_min, c2x_min, b)
    min_y = min(c1y_min, c2y_min, b)
    max_x = max(c1x_max, c2x_max, b)
    max_y = max(c1y_max, c2y_max, b)

    k_z = canvas_width / max(abs(max_x - min_x), abs(max_y - min_y))

    return [k_z, [min_x, min_y], [max_x, max_y]]


def zoom(circles, zoom_vars):
    k_z = zoom_vars[0]
    min_x = zoom_vars[1][0]
    min_y = zoom_vars[1][1]

    for i in range(len(circles) - 1):
        circles[i][0][2] *= k_z
        for j in range(len(circles[i])):
            circles[i][j][0] = k_z * (circles[i][j][0] - min_x)
            circles[i][j][1] = k_z * (circles[i][j][1] - min_y)


def solve_task(canvas, listb_f_set, listb_s_set):
    f_set = list(listb_f_set.get(0, END))
    s_set = list(listb_s_set.get(0, END))

    form_coord_matrix(f_set)
    form_coord_matrix(s_set)

    circles = []

    form_circles_list(circles, f_set)
    form_circles_list(circles, s_set)

    if len(circles) < 2:
        showerror("Ошибка", "Для решения задачи нужно задать минимум два круга")
        return

    magic_circles = get_magic_circles(circles)

    if magic_circles[2] == "tang":
        showerror("Ошибка", "Расположение кругов задано некорректно")
        return

    canvas.delete("all")

    showinfo(
        "Информация об угле",
        "Был получен угол alpha в {:.1f} градусов".format(magic_circles[2]),
    )

    zoom_vars = get_zoom_vars(magic_circles)

    draw_angle(canvas, magic_circles, zoom_vars)
    zoom(magic_circles, zoom_vars)
    draw_split_line(canvas, magic_circles)

    form_canvas_coords(magic_circles)

    draw_points(canvas, magic_circles)
    draw_circles(canvas, magic_circles)
    draw_ordinate(canvas, zoom_vars)
    draw_coords(canvas, magic_circles, circles)
