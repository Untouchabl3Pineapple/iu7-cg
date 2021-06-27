from tkinter import *
from tkinter import messagebox
from time import time, sleep
import matplotlib.pyplot as plt
import numpy as np
from math import floor, fabs, cos, sin, radians, pi

from seed import *

C_W = 900
C_H = 780

index_point = 0


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def bresenham_int(beg_point, end_point, color):
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
    i = 0
    while i <= dx:
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
    return points


def click_left(event, figures, img, color_var, points_listbox):
    global index_point
    x = event.x
    y = event.y
    color = "#ff8000"
    set_pixel(img, x, y, color)
    figures[-1][-1].append([x, y])
    index_point += 1
    pstr = "%d. (%d, %d)" % (index_point, x, y)
    points_listbox.insert(END, pstr)

    if len(figures[-1][-1]) == 2:
        points = bresenham_int(figures[-1][-1][0], figures[-1][-1][1], color)
        draw_line(img, points)
        figures[-1][-1].append(points)
        figures[-1].append([figures[-1][-1][1]])


def click_centre(event, figures, img, color_var):
    if len(figures[-1][-1]) == 0:
        messagebox.showwarning("Ошибка", "Незамкнутых фигур нет!")
        return

    if len(figures[-1]) <= 2:
        messagebox.showwarning("Ошибка", "Фигура должна иметь больше 1 ребра!")
        return
    point = figures[-1][0][0]
    figures[-1][-1].append(point)
    color = "#ff8000"
    points = bresenham_int(figures[-1][-1][0], figures[-1][-1][1], color)
    draw_line(img, points)
    figures[-1][-1].append(points)
    figures.append([[]])


def click_right(event, seed_pixel, img, color_var, points_listbox):
    x = event.x
    y = event.y
    seed_pixel[0] = x
    seed_pixel[1] = y
    color = get_color(color_var)
    set_pixel(img, x, y, color)
    pstr = "Seed. (%d, %d)" % (x, y)
    points_listbox.insert(END, pstr)


def draw_point(figures, img, color_var, x_entry, y_entry, points_listbox):
    global index_point

    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except:
        messagebox.showwarning(
            "Ошибка", "Неверно заданны координаты точки!\n" "Ожидался ввод целых чисел."
        )
        return
    color = "#ff8000"
    set_pixel(img, x, y, color)
    figures[-1][-1].append([x, y])
    index_point += 1
    pstr = "%d. (%d, %d)" % (index_point, x, y)
    points_listbox.insert(END, pstr)

    if len(figures[-1][-1]) == 2:
        points = bresenham_int(figures[-1][-1][0], figures[-1][-1][1], color)
        draw_line(img, points)
        figures[-1][-1].append(points)
        figures[-1].append([figures[-1][-1][1]])


def fill_figure(figures, img, canvas, color_var, mode_var, time_entry, seed_pixel):
    if len(figures[-1][0]) != 0:
        messagebox.showwarning("Ошибка", "Не все фигуры замкнуты!")
        return

    if seed_pixel == [-1, -1]:
        messagebox.showwarning("Ошибка", "Отсутствует затравка!")
        return
    mark_color = get_color(color_var)
    border_color = rgb("#ff8000")
    delay = mode_var.get()
    start_time = time()
    seed(img, canvas, seed_pixel, mark_color, border_color, delay)
    end_time = time()
    time_str = str(round(end_time - start_time, 2)) + "s"
    time_entry.delete(0, END)
    time_entry.insert(0, time_str)


def clear_canvas(img, canvas, figures, time_entry, points_listbox, seed_pixel):
    global index_point
    img.put("#ffffff", to=(0, 0, C_W, C_H))
    seed_pixel[0] = -1
    seed_pixel[1] = -1
    index_point = 0
    points_listbox.delete(0, END)
    time_entry.delete(0, END)
    figures.clear()
    figures.append([[]])


def information():
    messagebox.showinfo(
        "Условие задачи",
        "Реализовать алгоритм растрового заполнения сплошных областей с использованием затравочного пиксела.",
    )


window = Tk()
window.title("Lab_06")
window.geometry("1200x780")
window.resizable(False, False)
window["bg"] = "RosyBrown1"

c = Canvas(window, width=C_W, height=C_H, bg="white")
c.place(x=300, y=0)

figures = [[[]]]

color_fg = IntVar()
color_fg.set(2)

t = IntVar()
t.set(0)

label1 = Label(
    window,
    text="Цвет закраски:",
    height="1",
    fg="black",
    bg="RosyBrown1",
    font=("arial", 14),
)
label1.place(x=90, y=10)

label2 = Label(
    window,
    text="Режим закраски:",
    height="1",
    bg="RosyBrown1",
    fg="black",
    font=("arial", 14),
)
label2.place(x=90, y=180)

label3 = Label(
    window,
    text="Построение точки вручную",
    height="1",
    bg="RosyBrown1",
    fg="black",
    font=("arial", 14),
)
label3.place(x=60, y=240)

label4 = Label(window, text="X:", height="1", bg="RosyBrown1", fg="black")
label4.place(x=60, y=265)

label5 = Label(window, text="Y:", height="1", bg="RosyBrown1", fg="black")
label5.place(x=215, y=265)

label6 = Label(
    window, text="Время :", height="1", bg="RosyBrown1", fg="black", font=("arial", 14)
)
label6.place(x=50, y=640)

radbutton1 = Radiobutton(
    window,
    text="Чёрный",
    variable=color_fg,
    value=0,
    height="1",
    bg="RosyBrown1",
    fg="black",
)
radbutton1.place(x=20, y=30)

radbutton2 = Radiobutton(
    window,
    text="Красный",
    variable=color_fg,
    value=1,
    height="1",
    bg="RosyBrown1",
    fg="black",
)
radbutton2.place(x=20, y=60)

radbutton3 = Radiobutton(
    window,
    text="Синий",
    variable=color_fg,
    value=2,
    height="1",
    bg="RosyBrown1",
    fg="black",
)
radbutton3.place(x=20, y=90)

radbutton4 = Radiobutton(
    window,
    text="Зелёный",
    variable=color_fg,
    value=3,
    height="1",
    bg="RosyBrown1",
    fg="black",
)
radbutton4.place(x=20, y=120)

radbutton5 = Radiobutton(
    window,
    text="Жёлтый",
    variable=color_fg,
    value=4,
    height="1",
    bg="RosyBrown1",
    fg="black",
)
radbutton5.place(x=20, y=150)

radbutton11 = Radiobutton(
    window,
    text="Без задержки",
    variable=t,
    value=0,
    height="1",
    bg="RosyBrown1",
    fg="black",
)
radbutton11.place(x=20, y=210)

radbutton11 = Radiobutton(
    window,
    text="С задержкой",
    variable=t,
    value=1,
    height="1",
    bg="RosyBrown1",
    fg="black",
)
radbutton11.place(x=150, y=210)

ent1 = Entry(window, bg="white", fg="black")
ent1.place(x=15, y=295, width=100, height=35)
ent1.insert(0, 200)

ent2 = Entry(window, bg="white", fg="black")
ent2.place(x=170, y=295, width=100, height=35)
ent2.insert(0, 200)

time_entry = Entry(window, bg="white", fg="black")
time_entry.place(width=120, height=35, x=150, y=635)

butn0 = Button(
    text="Построение точки",
    command=lambda: draw_point(figures, img, color_fg, ent1, ent2, points_listbox),
)
butn0.place(x=15, y=340, width=255, height=35)

butn1 = Button(
    text="Замыкание фигуры",
    command=lambda event="<3>": click_centre(event, figures, img, color_fg),
)
butn1.place(x=15, y=540, width=255, height=35)

butn2 = Button(
    text="Закрашивание",
    command=lambda: fill_figure(figures, img, c, color_fg, t, time_entry, seed_pixel),
)
butn2.place(x=15, y=585, width=255, height=35)

butn3 = Button(
    text="Очистка экрана",
    command=lambda: clear_canvas(
        img, c, figures, time_entry, points_listbox, seed_pixel
    ),
)
butn3.place(x=15, y=680, width=255, height=35)

butn4 = Button(text="Условие задачи", command=lambda: information())
butn4.place(x=15, y=725, width=255, height=35)

points_listbox = Listbox(font=("Arial", 16), bg="white", fg="black")
points_listbox.place(width=255, height=145, x=15, y=385)

img = PhotoImage(width=C_W, height=C_H)
c.create_image(C_W // 2, C_H // 2, image=img, state="normal")

seed_pixel = [-1, -1]

c.bind("<1>", lambda event: click_left(event, figures, img, color_fg, points_listbox))
c.bind(
    "<2>", lambda event: click_right(event, seed_pixel, img, color_fg, points_listbox)
)

window.mainloop()
