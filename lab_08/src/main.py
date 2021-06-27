from tkinter import *
from tkinter import messagebox
from math import *
import matplotlib.pyplot as plt
import matplotlib
from numpy import *
from colorutils import *
from time import *
from copy import *
from itertools import *

CANVAS_WIDTH = 795

is_cutter_set = False


def get_cutter_color():
    colours = []
    colours.append(Color((0, 0, 0)))
    colours.append(Color((255, 0, 0)))
    colours.append(Color((0, 0, 255)))
    colours.append(Color((255, 255, 0)))
    colours.append(Color((0, 255, 0)))
    colours.append(Color((255, 128, 0)))
    color_num = cutter_colour_var.get()
    color = colours[color_num - 1]

    return color


def get_line_color():
    colours = []
    colours.append(Color((0, 0, 0)))
    colours.append(Color((255, 0, 0)))
    colours.append(Color((0, 0, 255)))
    colours.append(Color((255, 255, 0)))
    colours.append(Color((0, 255, 0)))
    colours.append(Color((255, 128, 0)))
    color_num = line_colour_var.get()
    color = colours[color_num - 1]

    return color


def get_result_color():
    colours = []
    colours.append(Color((0, 0, 0)))
    colours.append(Color((255, 0, 0)))
    colours.append(Color((0, 0, 255)))
    colours.append(Color((255, 255, 0)))
    colours.append(Color((0, 255, 0)))
    colours.append(Color((255, 128, 0)))
    color_num = result_colour_var.get()
    color = colours[color_num - 1]

    return color


def left_click(event):
    x = event.x
    y = event.y

    color = get_line_color()
    color = color.hex

    MainCanvas.create_line(x, y, x + 1, y, fill=color)

    lines[-1].append([x, y])

    if len(lines[-1]) == 2:
        MainCanvas.create_line(lines[-1][0], lines[-1][1], fill=color)

        lines[-1].append(color)
        lines.append([])


def right_click(event):
    global cutter

    update_cutter()

    x = event.x
    y = event.y

    color = get_cutter_color()
    color = color.hex

    MainCanvas.create_line(x, y, x + 1, y, fill=color)

    cutter.append([x, y])

    if len(cutter) >= 2:
        MainCanvas.create_line(cutter[-2], cutter[-1], fill=color)


def lock_cutter():
    global cutter

    if len(cutter) < 3:
        messagebox.showwarning("Ошибка", "Отсекатель должен иметь более 2 вершин\n")
        return

    if cutter[0] == cutter[-1]:
        return

    color = get_cutter_color()
    color = color.hex

    cutter.append(cutter[0])

    MainCanvas.create_line(cutter[-2], cutter[-1], fill=color)


def update_cutter():
    global cutter

    if len(cutter) > 3 and cutter[0] == cutter[-1]:
        MainCanvas.delete("all")
        draw_lines()
        cutter.clear()

        return


def draw_lines():
    for line in lines:
        if len(line) != 0:
            MainCanvas.create_line(line[0], line[1], fill=line[2])


def add_line():
    try:
        xs = int(XS_entry.get())
        ys = int(YS_entry.get())
        xe = int(XE_entry.get())
        ye = int(YE_entry.get())
    except:
        messagebox.showwarning("Ошибка", "Неверно заданны координаты отрезка\n")
        return

    color = get_line_color()
    color = color.hex

    MainCanvas.create_line([xs, ys], [xe, ye], fill=color)

    lines[-1].append([xs, ys])
    lines[-1].append([xe, ye])
    lines[-1].append(color)
    lines.append([])


def add_cutter_point():
    global cutter

    try:
        x = int(XC_entry.get())
        y = int(YC_entry.get())
    except:
        messagebox.showwarning(
            "Ошибка", "Неверно заданны координаты вершины отсекателя\n"
        )
        return

    update_cutter()

    color = get_cutter_color()
    color = color.hex

    MainCanvas.create_line(x, y, x + 1, y, fill=color)

    cutter.append([x, y])

    if len(cutter) >= 2:
        MainCanvas.create_line(cutter[-2], cutter[-1], fill=color)


def find_starting_point():
    y_max = cutter[0][1]
    index = 0

    for i in range(len(cutter)):
        if cutter[i][1] > y_max:
            y_max = cutter[i][1]
            index = i

    cutter.pop()

    for i in range(index):
        cutter.append(cutter.pop(0))

    cutter.append(cutter[0])

    if cutter[-2][0] > cutter[1][0]:
        cutter.reverse()


def solve():
    if len(cutter) < 3:
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if not check_polygon():
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    color = get_cutter_color()
    color = color.hex

    MainCanvas.create_polygon(cutter, outline=color, fill="white")

    find_starting_point()

    for line in lines:
        if line:
            cyrus_beck_algorithm(line, len(cutter))


def line_coefficients(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c


def lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1 * b2 - a2 * b1
    opr1 = (-c1) * b2 - b1 * (-c2)
    opr2 = a1 * (-c2) - (-c1) * a2

    if opr == 0:
        return -5, -5  # прямые параллельны

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def is_coord_between(left, right, point):
    return (min(left, right) <= point) and (max(left, right) >= point)


def is_point_common(point_l, point_r, inter):
    return is_coord_between(point_l[0], point_r[0], inter[0]) and is_coord_between(
        point_l[1], point_r[1], inter[1]
    )


def are_lines_connected(line1, line2):

    if (
        ((line1[0][0] == line2[0][0]) and (line1[0][1] == line2[0][1]))
        or ((line1[1][0] == line2[1][0]) and (line1[1][1] == line2[1][1]))
        or ((line1[0][0] == line2[1][0]) and (line1[0][1] == line2[1][1]))
        or ((line1[1][0] == line2[0][0]) and (line1[1][1] == line2[0][1]))
    ):
        return True

    return False


def extra_check():  # чтобы не было пересечений

    cutter_lines = []

    for i in range(len(cutter) - 1):
        cutter_lines.append([cutter[i], cutter[i + 1]])  # разбиваю отсекатель на линии

    combinations_lines = list(
        combinations(cutter_lines, 2)
    )  # все возможные комбинации сторон

    for i in range(len(combinations_lines)):
        line1 = combinations_lines[i][0]
        line2 = combinations_lines[i][1]

        if are_lines_connected(line1, line2):
            continue

        a1, b1, c1 = line_coefficients(
            line1[0][0], line1[0][1], line1[1][0], line1[1][1]
        )
        a2, b2, c2 = line_coefficients(
            line2[0][0], line2[0][1], line2[1][0], line2[1][1]
        )

        intersection_point = lines_intersection(a1, b1, c1, a2, b2, c2)

        if (is_point_common(line1[0], line1[1], intersection_point)) and (
            is_point_common(line2[0], line2[1], intersection_point)
        ):
            return True

    return False


def get_vector(point_1, point_2):
    return [point_2[0] - point_1[0], point_2[1] - point_1[1]]


def vector_product(vector_1, vector_2):
    return vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0]


def scalar_product(vector_1, vector_2):
    return vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1]


def check_polygon():  # через проход по всем точкам, поворот которых должен быть все время в одну сторону
    if len(cutter) < 3:
        return False

    temp = vector_product(
        get_vector(cutter[1], cutter[2]), get_vector(cutter[0], cutter[1])
    )

    sign = 1 if temp > 0 else -1  # 1 - clockwise; -1 = counterclockwise

    for i in range(3, len(cutter)):
        temp = sign * vector_product(
            get_vector(cutter[i - 1], cutter[i]),
            get_vector(cutter[i - 2], cutter[i - 1]),
        )

        if temp < 0:
            return False

    check = extra_check()

    if check:
        return False

    return True


def get_normal(point_1, point_2, point_3):
    f_vector = get_vector(point_1, point_2)

    if f_vector[1]:
        normal = [1, -f_vector[0] / f_vector[1]]
    else:
        normal = [0, 1]

    position_vector = get_vector(point_2, point_3)

    if scalar_product(position_vector, normal) < 0:
        normal[0] = -normal[0]
        normal[1] = -normal[1]

    return normal


def cyrus_beck_algorithm(line, cutter_len):
    point_1 = line[0]
    point_2 = line[1]

    d = [point_2[0] - point_1[0], point_2[1] - point_1[1]]

    t_top = 0
    t_bottom = 1

    for i in range(-2, cutter_len - 2):
        normal = get_normal(cutter[i], cutter[i + 1], cutter[i + 2])

        w = [point_1[0] - cutter[i][0], point_1[1] - cutter[i][1]]

        d_scalar = scalar_product(d, normal)
        w_scalar = scalar_product(w, normal)

        if d_scalar == 0:
            if w_scalar < 0:
                return
            else:
                continue

        t = -w_scalar / d_scalar

        if d_scalar > 0:
            if t <= 1:
                t_top = max(t_top, t)
            else:
                return
        elif d_scalar < 0:
            if t >= 0:
                t_bottom = min(t_bottom, t)
            else:
                return

        if t_top > t_bottom:
            break

    if t_top <= t_bottom:
        color = get_result_color()
        color = color.hex

        point_1_result = [
            round(point_1[0] + d[0] * t_top),
            round(point_1[1] + d[1] * t_top),
        ]
        point_2_result = [
            round(point_1[0] + d[0] * t_bottom),
            round(point_1[1] + d[1] * t_bottom),
        ]

        MainCanvas.create_line(point_1_result, point_2_result, fill=color)


def clear_field():
    global lines
    global cutter

    MainCanvas.delete("all")

    lines = [[]]
    cutter = []


if __name__ == "__main__":
    window = Tk()

    window.geometry("1370x800")
    window.title("Lab_08")
    window.tk_setPalette("coral")
    window.resizable(FALSE, FALSE)

    MainCanvas = Canvas(window, width=845, height=795, bg="#ffffff")
    MainCanvas.place(x=520, y=0)

    lines = [[]]

    cutter = []

    MainCanvas.bind("<1>", lambda event: left_click(event))
    MainCanvas.bind("<2>", lambda event: right_click(event))
    MainCanvas.bind("<3>", lambda: lock_cutter())

    alg_label = Label(text="Цвет отрезка", font=("Arial", 15))
    alg_label.place(x=15, y=10)

    line_colour_var = IntVar()
    line_colour_var.set(3)

    black_radiobutton_line = Radiobutton(
        text="Черный", variable=line_colour_var, value=1, font=("Arial", 15)
    )
    black_radiobutton_line.place(x=15, y=40)

    red_radiobutton_line = Radiobutton(
        text="Красный", variable=line_colour_var, value=2, font=("Arial", 15)
    )
    red_radiobutton_line.place(x=15, y=70)

    blue_radiobutton_line = Radiobutton(
        text="Синий", variable=line_colour_var, value=3, font=("Arial", 15)
    )
    blue_radiobutton_line.place(x=15, y=100)

    yellow_radiobutton_line = Radiobutton(
        text="Желтый", variable=line_colour_var, value=4, font=("Arial", 15)
    )
    yellow_radiobutton_line.place(x=15, y=130)

    green_radiobutton_line = Radiobutton(
        text="Зеленый", variable=line_colour_var, value=5, font=("Arial", 15)
    )
    green_radiobutton_line.place(x=15, y=160)

    orange_radiobutton_line = Radiobutton(
        text="Оранжевый", variable=line_colour_var, value=6, font=("Arial", 15)
    )
    orange_radiobutton_line.place(x=15, y=190)

    cutter_color_label = Label(text="Цвет отсекателя", font=("Arial", 15))
    cutter_color_label.place(x=200, y=10)

    cutter_colour_var = IntVar()
    cutter_colour_var.set(1)

    black_radiobutton_cutter = Radiobutton(
        text="Черный", variable=cutter_colour_var, value=1, font=("Arial", 15)
    )
    black_radiobutton_cutter.place(x=200, y=40)

    red_radiobutton_cutter = Radiobutton(
        text="Красный", variable=cutter_colour_var, value=2, font=("Arial", 15)
    )
    red_radiobutton_cutter.place(x=200, y=70)

    blue_radiobutton_cutter = Radiobutton(
        text="Синий", variable=cutter_colour_var, value=3, font=("Arial", 15)
    )
    blue_radiobutton_cutter.place(x=200, y=100)

    yellow_radiobutton_cutter = Radiobutton(
        text="Желтый", variable=cutter_colour_var, value=4, font=("Arial", 15)
    )
    yellow_radiobutton_cutter.place(x=200, y=130)

    green_radiobutton_cutter = Radiobutton(
        text="Зеленый", variable=cutter_colour_var, value=5, font=("Arial", 15)
    )
    green_radiobutton_cutter.place(x=200, y=160)

    orange_radiobutton_cutter = Radiobutton(
        text="Оранжевый", variable=cutter_colour_var, value=6, font=("Arial", 15)
    )
    orange_radiobutton_cutter.place(x=200, y=190)

    color_label = Label(text="Цвет результата", font=("Arial", 15))
    color_label.place(x=385, y=10)

    result_colour_var = IntVar()
    result_colour_var.set(2)

    black_radiobutton_result = Radiobutton(
        text="Черный", variable=result_colour_var, value=1, font=("Arial", 15)
    )
    black_radiobutton_result.place(x=385, y=40)

    red_radiobutton_result = Radiobutton(
        text="Красный", variable=result_colour_var, value=2, font=("Arial", 15)
    )
    red_radiobutton_result.place(x=385, y=70)

    blue_radiobutton_result = Radiobutton(
        text="Синий", variable=result_colour_var, value=3, font=("Arial", 15)
    )
    blue_radiobutton_result.place(x=385, y=100)

    yellow_radiobutton_result = Radiobutton(
        text="Желтый", variable=result_colour_var, value=4, font=("Arial", 15)
    )
    yellow_radiobutton_result.place(x=385, y=130)

    green_radiobutton_result = Radiobutton(
        text="Зеленый", variable=result_colour_var, value=5, font=("Arial", 15)
    )
    green_radiobutton_result.place(x=385, y=160)

    orange_radiobutton_result = Radiobutton(
        text="Оранжевый", variable=result_colour_var, value=6, font=("Arial", 15)
    )
    orange_radiobutton_result.place(x=385, y=190)

    line_label = Label(text="Построение отрезка", font=("Arial", 15))
    line_label.place(x=15, y=240)

    start_label = Label(text="Начало", font=("Arial", 15))
    start_label.place(x=25, y=280)

    XS_label = Label(text="X:", font=("Arial", 15))
    XS_label.place(x=120, y=280)

    XS_entry = Entry(window, bg="#FFF8FB", font=("Arial", 15))
    XS_entry.place(x=150, y=280, width=70)

    YS_label = Label(text="Y:", font=("Arial", 15))
    YS_label.place(x=250, y=280)

    YS_entry = Entry(window, bg="#FFF8FB", font=("Arial", 15))
    YS_entry.place(x=280, y=280, width=70)

    end_label = Label(text="Конец", font=("Arial", 15))
    end_label.place(x=25, y=320)

    XE_label = Label(text="X:", font=("Arial", 15))
    XE_label.place(x=120, y=320)

    XE_entry = Entry(window, bg="#FFF8FB", font=("Arial", 15))
    XE_entry.place(x=150, y=320, width=70)

    YE_label = Label(text="Y:", font=("Arial", 15))
    YE_label.place(x=250, y=320)

    YE_entry = Entry(window, bg="#FFF8FB", font=("Arial", 15))
    YE_entry.place(x=280, y=320, width=70)

    line_button = Button(
        text="Построить отрезок",
        font=("Arial", 15),
        bg="#FFF8FB",
        command=lambda: add_line(),
    )
    line_button.place(x=15, y=370, width=230)

    cutter_label = Label(text="Построение вершины отсекателя", font=("Arial", 15))
    cutter_label.place(x=15, y=430)

    XC_label = Label(text="X:", font=("Arial", 15))
    XC_label.place(x=25, y=470)

    XC_entry = Entry(window, bg="#FFF8FB", font=("Arial", 15))
    XC_entry.place(x=55, y=470, width=70)

    YC_label = Label(text="Y:", font=("Arial", 15))
    YC_label.place(x=155, y=470)

    YC_entry = Entry(window, bg="#FFF8FB", font=("Arial", 15))
    YC_entry.place(x=185, y=470, width=70)

    cutter_button = Button(
        text="Построить вершину отсекателя",
        font=("Arial", 15),
        bg="#FFF8FB",
        command=lambda: add_cutter_point(),
    )
    cutter_button.place(x=15, y=520, width=230)

    lock_button = Button(
        text="Замкнуть отсекатель",
        font=("Arial", 15),
        bg="#FFF8FB",
        command=lambda: lock_cutter(),
    )
    lock_button.place(x=15, y=550, width=230)

    result_button = Button(
        text="Отсечь", font=("Arial", 15), bg="#FFF8FB", command=lambda: solve()
    )
    result_button.place(x=15, y=720, width=230)

    clear_button = Button(
        text="Очистить поле",
        font=("Arial", 15),
        bg="#FFF8FB",
        command=lambda: clear_field(),
    )
    clear_button.place(x=15, y=750, width=230)

    window.mainloop()