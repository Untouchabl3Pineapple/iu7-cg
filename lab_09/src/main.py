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
    global figure

    update_figure(figure)

    x = event.x
    y = event.y

    color = get_line_color()
    color = color.hex

    MainCanvas.create_line(x, y, x + 1, y, fill = color)

    figure.append([x, y])

    if len(figure) >= 2:
        MainCanvas.create_line(figure[-2], figure[-1], fill = color)


def right_click(event):
    global cutter, figure

    if (is_maked(cutter)):
        cutter.clear()
        MainCanvas.delete("all")
        color = get_line_color()
        color = color.hex
        MainCanvas.create_polygon(figure, outline = color, fill = "white")

    x = event.x
    y = event.y

    color = get_cutter_color()
    color = color.hex

    MainCanvas.create_line(x, y, x + 1, y, fill = color)

    cutter.append([x, y])

    if len(cutter) >= 2:
        MainCanvas.create_line(cutter[-2], cutter[-1], fill = color)


def lock_cutter():
    global cutter

    if len(cutter) < 3:
        messagebox.showwarning("Ошибка", "Отсекатель должен иметь более 2 вершин\n")
        return

    if (is_maked(cutter)):
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return
    
    if cutter[0] == cutter[-1]:
        return
        
    color = get_cutter_color()
    color = color.hex

    cutter.append(cutter[0])

    MainCanvas.create_line(cutter[-2], cutter[-1], fill = color)


def lock_figure():
    global figure

    if len(figure) < 3:
        messagebox.showwarning("Ошибка", "Многоугольник должен иметь более 2 вершин\n")
        return

    if (is_maked(figure)):
        messagebox.showerror("Ошибка", "Фигура уже замкнута")
        return
    
    if figure[0] == figure[-1]:
        return
        
    color = get_line_color()
    color = color.hex

    figure.append(figure[0])

    MainCanvas.create_line(figure[-2], figure[-1], fill = color)


def update_figure(figure):
    global cutter

    if (len(figure) > 3 and figure[0] == figure[-1]):
        figure.clear()
        cutter.clear()
        MainCanvas.delete("all")

        return


def add_cutter_point():
    global cutter

    try:
        x = int(XC_entry.get())
        y = int(YC_entry.get())
    except:
        messagebox.showwarning("Ошибка", "Неверно заданны координаты вершины отсекателя\n")
        return
    
    if (is_maked(cutter)):
        cutter.clear()
        MainCanvas.delete("all")
        color = get_line_color()
        color = color.hex
        MainCanvas.create_polygon(figure, outline = color, fill = "white")

    color = get_cutter_color()
    color = color.hex

    MainCanvas.create_line(x, y, x + 1, y, fill = color)

    cutter.append([x, y])

    if len(cutter) >= 2:
        MainCanvas.create_line(cutter[-2], cutter[-1], fill = color)


def add_figure_point():
    global figure

    try:
        x = int(XF_entry.get())
        y = int(YF_entry.get())
    except:
        messagebox.showwarning("Ошибка", "Неверно заданны координаты вершины отрезка\n")
        return
    
    update_figure(figure)

    color = get_line_color()
    color = color.hex

    MainCanvas.create_line(x, y, x + 1, y, fill = color)

    figure.append([x, y])

    if len(figure) >= 2:
        MainCanvas.create_line(figure[-2], figure[-1], fill = color)



















def is_maked(object):
    maked = False

    if (len(object) > 3):
        if ((object[0][0] == object[len(object) - 1][0]) and (object[0][1] == object[len(object) - 1][1])):
            maked = True

    return maked


def solve():
    if (not is_maked(cutter)):
        messagebox.showinfo("Ошибка", "Отсекатель не замкнут")
        return

    if (not is_maked(figure)):
        messagebox.showinfo("Ошибка", "Многоугольник не замкнут")
        return

    if (not check_polygon()):
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником")
        return

    if (len(cutter) < 3):
        messagebox.showinfo("Ошибка", "Не задан отсекатель")
        return

    if (extra_check(figure)):
        messagebox.showinfo("Ошибка", "Отсекаемое должно быть многоугольником")
        return

    result = deepcopy(figure)

    for current_point_index in range(-1, len(cutter) - 1):
        line = [cutter[current_point_index], cutter[current_point_index + 1]]

        position_point = cutter[current_point_index + 1]

        result = sutherland_hodgman_algorithm(line, position_point, result)

        if (len(result) <= 2):
            return

    draw_result_figure(result)


def draw_result_figure(figure_dots):
    fixed_figure = remove_odd_sides(figure_dots)

    color = get_result_color()
    color = color.hex

    for line in fixed_figure:
        MainCanvas.create_line(line[0], line[1], fill = color)


def line_coefficients(x1, y1, x2, y2):
    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c


def lines_intersection(a1, b1, c1, a2, b2, c2):
    opr = a1 * b2 - a2 * b1
    opr1 = (-c1) * b2 - b1 * (-c2)
    opr2 = a1 * (-c2) - (-c1) * a2

    if (opr == 0):
        return -5, -5 # прямые параллельны

    x = opr1 / opr
    y = opr2 / opr

    return x, y


def is_coord_between(left, right, point):
    return (min(left, right) <= point) and (max(left, right) >= point)


def is_point_common(point_l, point_r, inter):
    return is_coord_between(point_l[0], point_r[0], inter[0]) and is_coord_between(point_l[1], point_r[1], inter[1])


def are_lines_connected(line1, line2):

    if ((line1[0][0] == line2[0][0]) and (line1[0][1] == line2[0][1])) \
            or ((line1[1][0] == line2[1][0]) and (line1[1][1] == line2[1][1])) \
            or ((line1[0][0] == line2[1][0]) and (line1[0][1] == line2[1][1])) \
            or ((line1[1][0] == line2[0][0]) and (line1[1][1] == line2[0][1])):
        return True

    return False


def extra_check(object): # чтобы не было пересечений
    
    cutter_lines = []

    for i in range(len(object) - 1):
        cutter_lines.append([object[i], object[i + 1]]) # разбиваю отсекатель на линии

    combinations_lines = list(combinations(cutter_lines, 2)) # все возможные комбинации сторон

    for i in range(len(combinations_lines)):
        line1 = combinations_lines[i][0]
        line2 = combinations_lines[i][1]

        if (are_lines_connected(line1, line2)):
            continue

        a1, b1, c1 = line_coefficients(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
        a2, b2, c2 = line_coefficients(line2[0][0], line2[0][1], line2[1][0], line2[1][1])

        intersection_point = lines_intersection(a1, b1, c1, a2, b2, c2)

        if (is_point_common(line1[0], line1[1], intersection_point)) and (is_point_common(line2[0], line2[1], intersection_point)):
            return True

    return False


def get_vector(point_1, point_2):
    return [point_2[0] - point_1[0], point_2[1] - point_1[1]]


def vector_product(vector_1, vector_2):
    return (vector_1[0] * vector_2[1] - vector_1[1] * vector_2[0])


def scalar_product(vector_1, vector_2):
    return (vector_1[0] * vector_2[0] + vector_1[1] * vector_2[1])


def check_polygon(): # через проход по всем точкам, поворот которых должен быть все время в одну сторону
    if (len(cutter) < 3):
        return False

    temp = vector_product(get_vector(cutter[1], cutter[2]), get_vector(cutter[0], cutter[1]))

    sign = 1 if temp > 0 else -1 # 1 - clockwise; -1 = counterclockwise

    for i in range(3, len(cutter)):
        temp = sign * vector_product(get_vector(cutter[i - 1], cutter[i]), get_vector(cutter[i - 2], cutter[i - 1]))

        if temp < 0:
            return False

    if (extra_check(cutter)):
        return False

    if (sign < 0):
        cutter.reverse()

    return True


def get_normal(point_1, point_2, point_3):
    f_vector = get_vector(point_1, point_2)

    if (f_vector[1]):
        normal = [1, -f_vector[0] / f_vector[1]]
    else:
        normal = [0, 1]

    position_vector = get_vector(point_2, point_3)

    if (scalar_product(position_vector, normal) < 0):
        normal[0] = -normal[0]
        normal[1] = -normal[1]

    return normal


def is_visible(point, f_point, s_point):
    vector_1 = get_vector(f_point, s_point)
    vector_2 = get_vector(f_point, point)

    if (vector_product(vector_1, vector_2) <= 0):
        return True
    else:
        return False


def get_lines_parametric_intersection(line1, line2, normal):
    d = get_vector(line1[0], line1[1])
    w = get_vector(line2[0], line1[0])

    d_scalar = scalar_product(d, normal)
    w_scalar = scalar_product(w, normal)

    t = -w_scalar / d_scalar

    intersection_point = [line1[0][0] + d[0] * t, line1[0][1] + d[1] * t]

    return intersection_point


def sutherland_hodgman_algorithm(cutter_line, position, previous_result):
    current_result = []

    point_1 = cutter_line[0]
    point_2 = cutter_line[1]

    normal = get_normal(point_1, point_2, position)

    previous_vision = is_visible(previous_result[-2], point_1, point_2)

    for current_point_index in range(-1, len(previous_result)):
        current_vision = is_visible(previous_result[current_point_index], point_1, point_2)

        if (previous_vision):
            if (current_vision):
                current_result.append(previous_result[current_point_index])
            else:
                figure_line = [previous_result[current_point_index - 1], previous_result[current_point_index]]

                current_result.append(get_lines_parametric_intersection(figure_line, cutter_line, normal))
        else:
            if (current_vision):
                figure_line = [previous_result[current_point_index - 1], previous_result[current_point_index]]

                current_result.append(get_lines_parametric_intersection(figure_line, cutter_line, normal))

                current_result.append(previous_result[current_point_index])

        previous_vision = current_vision

    return current_result


def make_unique(sides):

    for side in sides:
        side.sort()

    return list(sides)


def is_point_on_side(point, side):
    if abs(vector_product(get_vector(point, side[0]), get_vector(side[1], side[0]))) <= 1e-6:
        if (side[0] < point < side[1] or side[1] < point < side[0]):
            return True

    return False


def get_sides(side, rest_point):
    point_list = [side[0], side[1]]

    for point in rest_point:
        if is_point_on_side(point, side):
            point_list.append(point)

    point_list.sort()

    sections_list = list()

    for i in range(len(point_list) - 1):
        sections_list.append([point_list[i], point_list[i + 1]])

    return sections_list


def remove_odd_sides(figure_points):
    all_sides = list()
    rest_points = figure_points[2:]

    for i in range(len(figure_points)):
        current_side = [figure_points[i], figure_points[(i + 1) % len(figure_points)]]

        all_sides.extend(get_sides(current_side, rest_points))

        rest_points.pop(0)
        rest_points.append(figure_points[i])

    return make_unique(all_sides)


def clear_field():
    global lines
    global cutter
    global figure

    MainCanvas.delete("all")

    lines = []
    cutter = []
    figure = []

    
if __name__ == "__main__":
    window = Tk()

    window.geometry("1370x800")
    window.title("Lab_09")
    window.tk_setPalette("coral")
    window.resizable(FALSE, FALSE)

    MainCanvas = Canvas(window, width=795, height=795, bg = "#ffffff")
    MainCanvas.place(x = 570, y = 0)

    lines = []
    figure = []

    cutter = []

    MainCanvas.bind('<1>', lambda event: left_click(event))
    MainCanvas.bind('<2>', lambda event: right_click(event))


    alg_label = Label(text = "Цвет многоугольника", font=("Arial", 15))
    alg_label.place(x = 15, y = 10)

    line_colour_var = IntVar()
    line_colour_var.set(3)

    black_radiobutton_line = Radiobutton(text = "Черный", variable = line_colour_var, value = 1, font=("Arial", 15))
    black_radiobutton_line.place(x = 15, y = 40)

    red_radiobutton_line = Radiobutton(text = "Красный", variable = line_colour_var, value = 2, font=("Arial", 15))
    red_radiobutton_line.place(x = 15, y = 70)

    blue_radiobutton_line = Radiobutton(text = "Синий", variable = line_colour_var, value = 3, font=("Arial", 15))
    blue_radiobutton_line.place(x = 15, y = 100)

    yellow_radiobutton_line = Radiobutton(text = "Желтый", variable = line_colour_var, value = 4, font=("Arial", 15))
    yellow_radiobutton_line.place(x = 15, y = 130)

    green_radiobutton_line = Radiobutton(text = "Зеленый", variable = line_colour_var, value = 5, font=("Arial", 15))
    green_radiobutton_line.place(x = 15, y = 160)

    orange_radiobutton_line = Radiobutton(text = "Оранжевый", variable = line_colour_var, value = 6, font=("Arial", 15))
    orange_radiobutton_line.place(x = 15, y = 190)


    cutter_color_label = Label(text = "Цвет отсекателя", font=("Arial", 15))
    cutter_color_label.place(x = 200, y = 10)

    cutter_colour_var = IntVar()
    cutter_colour_var.set(1)

    black_radiobutton_cutter = Radiobutton(text = "Черный", variable = cutter_colour_var, value = 1, font=("Arial", 15))
    black_radiobutton_cutter.place(x = 200, y = 40)

    red_radiobutton_cutter = Radiobutton(text = "Красный", variable = cutter_colour_var, value = 2, font=("Arial", 15))
    red_radiobutton_cutter.place(x = 200, y = 70)

    blue_radiobutton_cutter = Radiobutton(text = "Синий", variable = cutter_colour_var, value = 3, font=("Arial", 15))
    blue_radiobutton_cutter.place(x = 200, y = 100)

    yellow_radiobutton_cutter = Radiobutton(text = "Желтый", variable = cutter_colour_var, value = 4, font=("Arial", 15))
    yellow_radiobutton_cutter.place(x = 200, y = 130)

    green_radiobutton_cutter = Radiobutton(text = "Зеленый", variable = cutter_colour_var, value = 5, font=("Arial", 15))
    green_radiobutton_cutter.place(x = 200, y = 160)

    orange_radiobutton_cutter = Radiobutton(text = "Оранжевый", variable = cutter_colour_var, value = 6, font=("Arial", 15))
    orange_radiobutton_cutter.place(x = 200, y = 190)

    color_label = Label(text = "Цвет результата", font=("Arial", 15))
    color_label.place(x = 385, y = 10)

    result_colour_var = IntVar()
    result_colour_var.set(2)

    black_radiobutton_result = Radiobutton(text = "Черный", variable = result_colour_var, value = 1, font=("Arial", 15))
    black_radiobutton_result.place(x = 385, y = 40)

    red_radiobutton_result = Radiobutton(text = "Красный", variable = result_colour_var, value = 2, font=("Arial", 15))
    red_radiobutton_result.place(x = 385, y = 70)

    blue_radiobutton_result = Radiobutton(text = "Синий", variable = result_colour_var, value = 3, font=("Arial", 15))
    blue_radiobutton_result.place(x = 385, y = 100)

    yellow_radiobutton_result = Radiobutton(text = "Желтый", variable = result_colour_var, value = 4, font=("Arial", 15))
    yellow_radiobutton_result.place(x = 385, y = 130)

    green_radiobutton_result = Radiobutton(text = "Зеленый", variable = result_colour_var, value = 5, font=("Arial", 15))
    green_radiobutton_result.place(x = 385, y = 160)

    orange_radiobutton_result = Radiobutton(text = "Оранжевый", variable = result_colour_var, value = 6, font=("Arial", 15))
    orange_radiobutton_result.place(x = 385, y = 190)


    line_label = Label(text = "Построение многоугольника", font=("Arial", 15))
    line_label.place(x = 15, y = 240)

    XF_label = Label(text = "X:", font=("Arial", 15))
    XF_label.place(x = 25, y = 280)

    XF_entry = Entry(window, bg = "#FFF8FB", font=("Arial", 15))
    XF_entry.place(x = 55, y = 280, width = 70)

    YF_label = Label(text = "Y:", font=("Arial", 15))
    YF_label.place(x = 155, y = 280)

    YF_entry = Entry(window, bg = "#FFF8FB", font=("Arial", 15))
    YF_entry.place(x = 185, y = 280, width = 70)

    line_button = Button(text="Построить отрезок", font=("Arial", 15), bg = "#FFF8FB", command = lambda: add_figure_point())
    line_button.place(x=15, y=330, width = 335)


    cutter_label = Label(text = "Построение вершины отсекателя", font=("Arial", 15))
    cutter_label.place(x = 15, y = 390)

    XC_label = Label(text = "X:", font=("Arial", 15))
    XC_label.place(x = 25, y = 430)

    XC_entry = Entry(window, bg = "#FFF8FB", font=("Arial", 15))
    XC_entry.place(x = 55, y = 430, width = 70)

    YC_label = Label(text = "Y:", font=("Arial", 15))
    YC_label.place(x = 155, y = 430)

    YC_entry = Entry(window, bg = "#FFF8FB", font=("Arial", 15))
    YC_entry.place(x = 185, y = 430, width = 70)

    cutter_button = Button(text="Построить вершину отсекателя", font=("Arial", 15), bg = "#FFF8FB", command = lambda: add_cutter_point())
    cutter_button.place(x=15, y=480, width = 335)

    lock_cutter_button = Button(text="Замкнуть отсекатель", font=("Arial", 15), bg = "#FFF8FB", command = lambda: lock_cutter())
    lock_cutter_button.place(x=15, y=560, width = 335)

    lock_figure_button = Button(text="Замкнуть многоугольник", font=("Arial", 15), bg = "#FFF8FB", command = lambda: lock_figure())
    lock_figure_button.place(x=15, y=620, width = 335)

    result_button = Button(text="Отсечь", font=("Arial", 15), bg = "#FFF8FB", command = lambda: solve())
    result_button.place(x=15, y=720, width = 260)

    clear_button = Button(text="Очистить поле", font=("Arial", 15), bg = "#FFF8FB", command = lambda: clear_field())
    clear_button.place(x=285, y=720, width = 260)


    window.mainloop()