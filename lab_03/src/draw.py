from tkinter import messagebox
from math import cos, sin, radians, pi
import colorutils as cu

from algorithms import *

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 740

CANVAS_WIDTH = WINDOW_HEIGHT + 150
CANVAS_HEIGHT = WINDOW_HEIGHT

def set_pixel(canvas, x, y, color):
    canvas.create_line(x, y, x + 1, y, fill = color.hex)

def lib_alg(canvas, one_point, two_point, color):
    canvas.create_line(one_point, two_point, fill = color.hex)

def get_color(color_fg):
    col_fg = color_fg.get()

    if col_fg == 0:
        color = cu.Color((255, 255, 255))
    elif col_fg == 1:
        color = cu.Color((0, 0, 0))
    elif col_fg == 2:
        color = cu.Color((255, 0, 0))
    elif col_fg == 3:
        color = cu.Color((0, 0, 255))
    elif col_fg == 4:
        color = cu.Color((0, 255, 0))
    else:
        color = cu.Color((255, 255, 0))
    
    return color

def add_line(canvas, color_fg, algorithm, one_point, two_point, draw = True):
    color = get_color(color_fg)
    alg = algorithm.get()

    if alg == 0:
        points = dda(one_point, two_point, color)
    elif alg == 1:
        points = bresenham_float(one_point, two_point, color)
    elif alg == 2:
        points = bresenham_int(one_point, two_point, color)
    elif alg == 3:
        points = bresenham_antialiased(one_point, two_point, color)
    elif alg == 4:
        points = wu(one_point, two_point, color)
    else:
        loops = 1
        if color == cu.Color((255, 255, 255)):
            loops = 10
        for i in range(loops):
            lib_alg(canvas, one_point, two_point, color)
        return

    if draw:
        loops = 1
        if color == cu.Color((255, 255, 255)):
            loops = 10
        for i in range(loops):
            for i in points:
                set_pixel(canvas, i[0], i[1], i[2])
    
def draw_line(canvas, color_fg, algorithm, x_beg_entry, y_beg_entry, x_end_entry, y_end_entry):
    try:
        x_beg = int(x_beg_entry.get())
        y_beg = int(y_beg_entry.get())
    except:
        messagebox.showwarning("Ошибка", 
            "Неверно заданны координаты начала отрезка!\n"
            "Ожидался ввод целлых чисел.")
        return
    
    try:
        x_end = int(x_end_entry.get())
        y_end = int(y_end_entry.get())
    except:
        messagebox.showwarning("Ошибка", 
            "Неверно заданны координаты конца отрезка!\n"
            "Ожидался ввод целых чисел.")
        return

    add_line(canvas, color_fg, algorithm, [x_beg, y_beg], [x_end, y_end])

def draw_spectrum(canvas, color_fg, algorithm, angle_entry, radius_entry):
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

    angle_rot = radians(angle_rot)
    angle =  0

    x_centre = CANVAS_WIDTH / 2
    y_centre = CANVAS_HEIGHT / 2

    while (angle < 2 * pi):
        x_end = x_centre + cos(angle) * radius
        y_end = y_centre + sin(angle) * radius

        add_line(canvas, color_fg, algorithm, [x_centre, y_centre], [x_end, y_end])

        angle += angle_rot
    
def clear_canvas(canvas):
    canvas.delete("all")
