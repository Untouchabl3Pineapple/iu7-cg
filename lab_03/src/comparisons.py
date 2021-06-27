import matplotlib.pyplot as plt
import numpy as np
import colorutils as cu
import time
from math import cos, sin, radians, pi
from tkinter import messagebox

from algorithms import *

from draw import CANVAS_WIDTH, CANVAS_HEIGHT, add_line, clear_canvas

NUMBER_OF_RUNS = 50

def step_comparison(canvas, angle_entry, radius_entry):
    try:
        radius = int(radius_entry.get())
    except:
        messagebox.showwarning("Ошибка", 
            "Неверно заданна длина отрезка для построения спектра!\n"
            "Ожидался ввод целого числа.")
        return

    if radius <= 0:
        messagebox.showwarning("Ошибка", 
            "Длина отрезка для построения спектра должна быть больше 0.")
        return

    x_centre = CANVAS_WIDTH / 2
    y_centre = CANVAS_HEIGHT / 2
    centre_point = [x_centre, y_centre]

    color = (255, 255, 255)

    dda_list = []
    bres_float_list = []
    bres_int_list = []
    bres_antial_list = []
    wu_list = []

    angle = 0
    angle_rot = radians(2)
    angle_list = [i for i in range(0, 91, 2)]
    
    while angle <= pi / 2 + 0.01:
        x = x_centre + cos(angle) * radius
        y = y_centre + sin(angle) * radius

        dda_list.append(dda(centre_point, [x, y], color, step_count = True))
        bres_float_list.append(bresenham_float(centre_point, [x, y], color, step_count = True))
        bres_int_list.append(bresenham_int(centre_point, [x, y], color, step_count = True))
        bres_antial_list.append(bresenham_antialiased(centre_point, [x, y], color, step_count = True))
        wu_list.append(wu(centre_point, [x, y], color, step_count = True))

        angle += angle_rot

    plt.figure(figsize = (10, 6))
    plt.rcParams['font.size'] = '14'

    plt.plot(angle_list, dda_list, label = 'ЦДА')
    plt.plot(angle_list, bres_float_list, linestyle = '--', label = 'Брезенхем\n(float/int)')
    plt.plot(angle_list, bres_antial_list, label = 'Брезенхем\n(с устранением\nступенчатости)',
        linestyle = '-.')
    plt.plot(angle_list, wu_list, label = 'Ву', linestyle = ':')

    plt.title("Исследование ступенчатости.\n{0} - длина отрезка".format(radius))
    plt.legend()
    plt.xticks(np.arange(91, step = 5))
    plt.ylabel("Колличество ступенек")
    plt.xlabel("Угол в градусах")
    plt.show()

def time_comparison(canvas, color_fg, algorithm, angle_entry, radius_entry):
    try:
        angle_rot = int(angle_entry.get())
    except:
        messagebox.showwarning("Ошибка", 
            "Неверно задан угол поворота для построения спектра!\n"
            "Ожидался ввод целого числа.")
        return

    try:
        radius = int(radius_entry.get())
    except:
        messagebox.showwarning("Ошибка", 
            "Неверно заданна длина отрезка для построения спектра!\n"
            "Ожидался ввод целого числа.")
        return

    if angle_rot == 0:
        messagebox.showwarning("Ошибка", 
            "Угол поворота для построения спектра не должен равняться 0.")
        return
    elif abs(angle_rot) > 360:
        messagebox.showwarning("Ошибка", 
            "Угол поворота для построения спектра не должен превышать 360 градусов (по модулю).")
        return
    elif radius <= 0:
        messagebox.showwarning("Ошибка", 
            "Длина отрезка для построения спектра должна быть больше 0.")
        return

    time_list = []

    x_centre = CANVAS_WIDTH / 2
    y_centre = CANVAS_HEIGHT / 2
    centre_point = [x_centre, y_centre]

    old_algorithm = algorithm.get()

    for i in range(0, 6):
        time_start = 0
        time_end = 0

        for _ in range(NUMBER_OF_RUNS):
            angle = 0
            algorithm.set(i)

            while (angle < 2 * pi):
                x = x_centre + cos(angle) * radius
                y = y_centre + sin(angle) * radius

                end_point = [x, y]
                
                time_start += time.time()
                add_line(canvas, color_fg, algorithm, centre_point, end_point, draw = False)
                time_end += time.time()

                angle += radians(angle_rot)

            clear_canvas(canvas)

        res_time = (time_end - time_start) / NUMBER_OF_RUNS
        time_list.append(res_time)

    algorithm.set(old_algorithm)

    plt.figure(figsize = (10, 6))
    plt.rcParams['font.size'] = '12'
    plt.title("Замеры времени для построения спектров различными методами")

    positions = np.arange(6)
    methods = ["ЦДА", "Брезенхем\n(float)", "Брезенхем\n(int)",
               "Брезенхем\n(с устранением\n ступенчатости)", "Ву", "Библиотечная\nфункция"]

    plt.xticks(positions, methods)
    plt.ylabel("Время")

    plt.bar(positions, time_list, align = "center", alpha = 1)

    plt.show()
