from tkinter import *
from tkinter import messagebox
import time
import matplotlib.pyplot as plt
import numpy as np
import colorutils as cu

from methods import *
from pixel import *

dis = 0

C_W = 900
C_H = 780
NUMBER_OF_RUNS = 15
MAX_RADIUS = 10000
STEP = 1000


def lib_ellipse(canvas, xc, yc, ra, rb, color):
    canvas.create_oval(xc - ra, yc - rb, xc + ra, yc + rb, outline=color.hex)
    if color == cu.Color((255, 255, 255)):
        canvas.create_oval(xc - ra, yc - rb, xc + ra, yc + rb, outline=color.hex)


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
    else:
        color = cu.Color((0, 255, 0))

    return color


def draw_figure(
    canvas, color_fg, algorithm, figure, xc_entry, yc_entry, ra_entry, rb_entry
):
    ellipse = figure.get()

    try:
        xc = int(xc_entry.get())
        yc = int(yc_entry.get())
        ra = int(ra_entry.get())

        if ellipse == True:
            rb = int(rb_entry.get())
    except:
        messagebox.showwarning(
            "Ошибка", "Неверно заданны параметры фигуры!\n" "Ожидался ввод целых чисел."
        )
        return

    if ra <= 0 or ellipse and rb <= 0:
        messagebox.showwarning(
            "Ошибка", "Значения полуосей фигуры должны быть больше 0."
        )
        return

    color = get_color(color_fg)
    alg = algorithm.get()

    if ellipse:
        if alg == 0:
            canonical_ellipse(xc, yc, ra, rb, color, canvas, draw=TRUE)
        elif alg == 1:
            parameter_ellipse(xc, yc, ra, rb, color, canvas, draw=TRUE)
        elif alg == 2:
            bresenham_ellipse(xc, yc, ra, rb, color, canvas, draw=TRUE)
        elif alg == 3:
            midpoint_ellipse(xc, yc, ra, rb, color, canvas, draw=TRUE)
        else:
            lib_ellipse(canvas, xc, yc, ra, rb, color)
    else:
        color = get_color(color_fg)
        alg = algorithm.get()

        if alg == 0:
            canonical_circle(xc, yc, ra, color, canvas, draw=TRUE)
        elif alg == 1:
            parameter_circle(xc, yc, ra, color, canvas, draw=TRUE)
        elif alg == 2:
            bresenham_circle(xc, yc, ra, color, canvas, draw=TRUE)
        elif alg == 3:
            midpoint_circle(xc, yc, ra, color, canvas, draw=TRUE)
        else:
            lib_ellipse(canvas, xc, yc, ra, ra, color)
    return


def draw_spectrum_ellipse(canvas, color_fg, algorithm, xc, yc):
    radius_x_entry = ent9
    radius_y_entry = ent10
    st_entr = ent7
    count_figure_entry = ent8

    ra = int(radius_x_entry.get())
    rb = int(radius_y_entry.get())
    step = int(st_entr.get())
    count_fig = int(count_figure_entry.get())

    constant = ra / rb

    while count_fig > 0:
        color = get_color(color_fg)
        alg = algorithm.get()
        if alg == 0:
            canonical_ellipse(xc, yc, ra, rb, color, canvas, draw=True)
        elif alg == 1:
            parameter_ellipse(xc, yc, ra, rb, color, canvas, draw=True)
        elif alg == 2:
            bresenham_ellipse(xc, yc, ra, rb, color, canvas, draw=True)
        elif alg == 3:
            midpoint_ellipse(xc, yc, ra, rb, color, canvas, draw=True)
        else:
            lib_ellipse(canvas, xc, yc, ra, rb, color)

        ra += step
        rb = round(ra / constant)

        count_fig -= 1


def get_necessary_data_for_spectrum(r_beg, r_end, step, count_fig):
    if r_beg == 0:
        r_beg = r_end - (count_fig - 1) * step
    elif step == 0:
        if count_fig == 0:
            step = int(r_end - r_beg) + 1
        else:
            step = int((r_end - r_beg) / (count_fig - 1))
    elif count_fig == 0:
        count_fig = int((r_end - r_beg) / step) + 1

    return r_beg, step, count_fig


def draw_spectrum_circle(canvas, color_fg, algorithm, xc, yc):
    global dis
    beg_radius_entry = ent5
    end_radius_entry = ent6
    step_entry = ent7
    count_figure_entry = ent8

    r_beg, r_end, step, count_fig = 0, 0, 0, 0

    r_beg = int(beg_radius_entry.get())
    r_end = int(end_radius_entry.get())
    step = int(step_entry.get())
    count_fig = 0

    if dis == 0:
        count_fig = int(count_figure_entry.get())

    r, step, count_fig = get_necessary_data_for_spectrum(r_beg, r_end, step, count_fig)

    while count_fig > 0:
        color = get_color(color_fg)
        alg = algorithm.get()
        if alg == 0:
            canonical_circle(xc, yc, r, color, canvas, draw=True)
        elif alg == 1:
            parameter_circle(xc, yc, r, color, canvas, draw=True)
        elif alg == 2:
            bresenham_circle(xc, yc, r, color, canvas, draw=True)
        elif alg == 3:
            midpoint_circle(xc, yc, r, color, canvas, draw=True)
        else:
            lib_ellipse(canvas, xc, yc, r, r, color)

        r += step
        count_fig -= 1


def draw_spectrum(canvas, color_fg, algorithm, figure, xc_entry, yc_entry):
    try:
        xc = int(xc_entry.get())
        yc = int(yc_entry.get())
    except:
        messagebox.showwarning(
            "Ошибка",
            "Неверно заданны координаты центра фигуры!\n" "Ожидался ввод целых чисел.",
        )
        return

    if figure.get() == 1:
        draw_spectrum_ellipse(canvas, color_fg, algorithm, xc, yc)
    else:
        draw_spectrum_circle(canvas, color_fg, algorithm, xc, yc)


def time_comparison(canvas, color_fg, algorithm, figure):
    time_list = []

    xc = C_W // 2
    yc = C_H // 2

    ellipse = figure.get()
    old_algorithm = algorithm.get()

    for i in range(5):
        algorithm.set(i)

        time_start = [0] * (MAX_RADIUS // STEP)
        time_end = [0] * (MAX_RADIUS // STEP)

        for _ in range(NUMBER_OF_RUNS):
            ra = STEP
            rb = STEP

            for j in range(MAX_RADIUS // STEP):
                if ellipse:
                    time_start[j] += time.time()
                    color = get_color(color_fg)
                    alg = algorithm.get()
                    if alg == 0:
                        canonical_ellipse(xc, yc, ra, rb, color, canvas, draw=FALSE)
                    elif alg == 1:
                        parameter_ellipse(xc, yc, ra, rb, color, canvas, draw=FALSE)
                    elif alg == 2:
                        bresenham_ellipse(xc, yc, ra, rb, color, canvas, draw=FALSE)
                    elif alg == 3:
                        midpoint_ellipse(xc, yc, ra, rb, color, canvas, draw=FALSE)
                    else:
                        lib_ellipse(canvas, xc, yc, ra, rb, color)

                    time_end[j] += time.time()

                    rb += STEP
                else:
                    time_start[j] += time.time()
                    color = get_color(color_fg)
                    alg = algorithm.get()
                    if alg == 0:
                        canonical_circle(xc, yc, ra, color, canvas, draw=FALSE)
                    elif alg == 1:
                        parameter_circle(xc, yc, ra, color, canvas, draw=FALSE)
                    elif alg == 2:
                        bresenham_circle(xc, yc, ra, color, canvas, draw=FALSE)
                    elif alg == 3:
                        midpoint_circle(xc, yc, ra, color, canvas, draw=FALSE)
                    else:
                        lib_ellipse(canvas, xc, yc, ra, ra, color)

                    time_end[j] += time.time()

                ra += STEP

            clear_canvas(canvas)

        size = len(time_start)
        time_list.append(
            [(time_end[i] - time_start[i]) / NUMBER_OF_RUNS for i in range(size)]
        )

    algorithm.set(old_algorithm)
    radius_arr = [i for i in range(STEP, MAX_RADIUS + STEP, STEP)]

    plt.figure(figsize=(10, 6))
    plt.rcParams["font.size"] = "12"
    plt.title("Замеры времени для построения фигуры различными методами")

    plt.plot(radius_arr, time_list[0], label="Каноническое уравнение")
    plt.plot(radius_arr, time_list[1], label="Параметрическое уравнение")
    plt.plot(radius_arr, time_list[2], label="Алгоритм Брезенхема")
    plt.plot(radius_arr, time_list[3], label="Алгоритм средней точки")
    plt.plot(radius_arr, time_list[4], label="Библиотечная функция")

    plt.xticks(np.arange(STEP, MAX_RADIUS + STEP, STEP))
    plt.legend()
    plt.xlabel("Длина радиуса")
    plt.ylabel("Время")

    plt.show()


def clear_canvas(canvas):
    canvas.delete("all")


def check_buttons(t, tn):
    if t == 0:
        label14.place_forget()
        label15.place_forget()
        label9.place(x=30, y=535)
        label10.place(x=90, y=535)
        label13.place(x=105, y=585)

        radbutton13.place(x=20, y=605)
        radbutton14.place(x=80, y=605)
        radbutton15.place(x=140, y=605)
        radbutton16.place(x=200, y=605)

        ent9.place_forget()
        ent10.place_forget()
        ent5.place(x=15, y=555, width=50, height=25)
        ent6.place(x=80, y=555, width=50, height=25)

        check_hiding(tn)
    elif t == 1:
        label9.place_forget()
        label10.place_forget()
        label13.place_forget()
        label14.place(x=30, y=535)
        label15.place(x=90, y=535)

        radbutton13.place_forget()
        radbutton14.place_forget()
        radbutton15.place_forget()
        radbutton16.place_forget()

        ent5.place_forget()
        ent6.place_forget()
        ent9.place(x=15, y=555, width=50, height=25)
        ent10.place(x=80, y=555, width=50, height=25)

        ent7.configure(state=NORMAL)
        ent8.configure(state=NORMAL)


def check_hiding(t):
    global dis
    ent5.configure(state=NORMAL)
    ent6.configure(state=NORMAL)
    ent7.configure(state=NORMAL)
    ent8.configure(state=NORMAL)

    if t == 0:
        ent5.configure(state=DISABLED)
        dis = 0
    elif t == 1:
        ent6.configure(state=DISABLED)
        dis = 0
    elif t == 2:
        ent7.configure(state=DISABLED)
        dis = 0
    elif t == 3:
        ent8.configure(state=DISABLED)
        dis = 1


window = Tk()
window.title("lab_04")
window.geometry("1200x780")
window["bg"] = "khaki"

c = Canvas(window, width=C_W, height=C_H, bg="white")
c.place(x=300, y=0)

color_fg = IntVar()
color_fg.set(2)

alg = IntVar()
alg.set(0)

t = IntVar()
t.set(0)

hide = IntVar()
hide.set(0)

label1 = Label(
    window,
    text="Выбор цвета",
    height="4",
    bg="khaki",
    fg="black",
    font=("arial", 14),
)
label1.place(x=95, y=150)

label2 = Label(
    window,
    text="Выбор алгоритма",
    height="4",
    bg="khaki",
    fg="black",
    font=("arial", 14),
)
label2.place(x=75, y=-25)

label3 = Label(
    window,
    text="Построение фигуры",
    height="1",
    bg="khaki",
    fg="black",
    font=("arial", 14),
)
label3.place(x=65, y=350)

label4 = Label(window, text="Xc", height="1", bg="khaki", fg="black")
label4.place(x=30, y=405)

label5 = Label(window, text="Yc", height="1", bg="khaki", fg="black")
label5.place(x=90, y=405)

label6 = Label(window, text="Rx", height="1", bg="khaki", fg="black")
label6.place(x=160, y=405)

label7 = Label(window, text="Ry", height="1", bg="khaki", fg="black")
label7.place(x=225, y=405)

label8 = Label(
    window,
    text="Построение спектра",
    height="1",
    bg="khaki",
    font=("arial", 14),
    fg="black",
)
label8.place(x=65, y=510)

label9 = Label(window, text="Rb", height="1", bg="khaki", fg="black")

label10 = Label(window, text="Re", height="1", bg="khaki", fg="black")

label11 = Label(window, text="Шаг", height="1", bg="khaki", fg="black")
label11.place(x=160, y=535)

label12 = Label(window, text="Кол-во", height="1", bg="khaki", fg="black")
label12.place(x=210, y=535)

label13 = Label(window, text="Скрыть", height="1", bg="khaki", fg="black")

label14 = Label(window, text="Ra", height="1", bg="khaki", fg="black")

label15 = Label(window, text="Rb", height="1", bg="khaki", fg="black")

radbutton1 = Radiobutton(
    window,
    text="Фоновый",
    variable=color_fg,
    value=0,
    height="1",
    bg="khaki",
    fg="black",
)
radbutton1.place(x=20, y=200)

radbutton2 = Radiobutton(
    window,
    text="Чёрный",
    variable=color_fg,
    value=1,
    height="1",
    bg="khaki",
    fg="black",
)
radbutton2.place(x=20, y=230)

radbutton3 = Radiobutton(
    window,
    text="Красный",
    variable=color_fg,
    value=2,
    height="1",
    bg="khaki",
    fg="black",
)
radbutton3.place(x=20, y=260)

radbutton4 = Radiobutton(
    window,
    text="Синий",
    variable=color_fg,
    value=3,
    height="1",
    bg="khaki",
    fg="black",
)
radbutton4.place(x=20, y=290)

radbutton5 = Radiobutton(
    window,
    text="Зелёный",
    variable=color_fg,
    value=4,
    height="1",
    bg="khaki",
    fg="black",
)
radbutton5.place(x=20, y=320)

radbutton6 = Radiobutton(
    window,
    text="Каноническое уравнение",
    variable=alg,
    value=0,
    height="2",
    bg="khaki",
    fg="black",
)
radbutton6.place(x=20, y=20)

radbutton7 = Radiobutton(
    window,
    text="Параметрическое уравнение",
    variable=alg,
    value=1,
    height="2",
    bg="khaki",
    fg="black",
)
radbutton7.place(x=20, y=50)

radbutton8 = Radiobutton(
    window,
    text="Алгоритм Брезенхема",
    variable=alg,
    value=2,
    height="2",
    bg="khaki",
    fg="black",
)
radbutton8.place(x=20, y=80)

radbutton9 = Radiobutton(
    window,
    text="Алгоритм средней точки",
    variable=alg,
    value=3,
    height="2",
    bg="khaki",
    fg="black",
)
radbutton9.place(x=20, y=110)

radbutton10 = Radiobutton(
    window,
    text="Библиотечная функция",
    variable=alg,
    value=4,
    height="2",
    bg="khaki",
    fg="black",
)
radbutton10.place(x=20, y=141)

radbutton11 = Radiobutton(
    window,
    text="Окружность",
    variable=t,
    value=0,
    height="2",
    bg="khaki",
    fg="black",
    command=lambda: check_buttons(t.get(), hide.get()),
)
radbutton11.place(x=20, y=370)

radbutton12 = Radiobutton(
    window,
    text="Эллипс",
    variable=t,
    value=1,
    height="2",
    bg="khaki",
    fg="black",
    command=lambda: check_buttons(t.get(), hide.get()),
)
radbutton12.place(x=150, y=370)

radbutton13 = Radiobutton(
    window,
    text="Rb",
    variable=hide,
    value=0,
    height="1",
    bg="khaki",
    fg="black",
    command=lambda: check_hiding(hide.get()),
)

radbutton14 = Radiobutton(
    window,
    text="Re",
    variable=hide,
    value=1,
    height="1",
    bg="khaki",
    fg="black",
    command=lambda: check_hiding(hide.get()),
)

radbutton15 = Radiobutton(
    window,
    text="Шаг",
    variable=hide,
    value=2,
    height="1",
    bg="khaki",
    fg="black",
    command=lambda: check_hiding(hide.get()),
)

radbutton16 = Radiobutton(
    window,
    text="Кол-во",
    variable=hide,
    value=3,
    height="1",
    bg="khaki",
    fg="black",
    command=lambda: check_hiding(hide.get()),
)

ent1 = Entry(window, bg="white", fg="black")
ent1.place(x=15, y=425, width=50, height=25)
ent1.insert(0, 450)

ent2 = Entry(window, bg="white", fg="black")
ent2.place(x=80, y=425, width=50, height=25)
ent2.insert(0, 390)

ent3 = Entry(window, bg="white", fg="black")
ent3.place(x=150, y=425, width=50, height=25)
ent3.insert(0, 200)

ent4 = Entry(window, bg="white", fg="black")
ent4.place(x=215, y=425, width=50, height=25)
ent4.insert(0, 150)

ent5 = Entry(window, bg="white", fg="black")
ent5.insert(0, 100)

ent6 = Entry(window, bg="white", fg="black")
ent6.insert(0, 340)

ent7 = Entry(window, bg="white", fg="black")
ent7.place(x=150, y=555, width=50, height=25)
ent7.insert(0, 10)

ent8 = Entry(window, bg="white", fg="black")
ent8.place(x=215, y=555, width=50, height=25)
ent8.insert(0, 20)

ent9 = Entry(window, bg="white", fg="black")
ent9.insert(0, 150)

ent10 = Entry(window, bg="white", fg="black")
ent10.insert(0, 100)

butn1 = Button(
    text="Построить фигуру",
    fg="black",
    command=lambda: draw_figure(c, color_fg, alg, t, ent1, ent2, ent3, ent4),
)
butn1.place(x=15, y=460, width=250, height=40)

butn2 = Button(
    text="Построить спектр",
    fg="black",
    command=lambda: draw_spectrum(c, color_fg, alg, t, ent1, ent2),
)
butn2.place(x=15, y=635, width=250, height=40)

butn3 = Button(
    text="Сравнить время",
    fg="black",
    command=lambda: time_comparison(c, color_fg, alg, t),
)
butn3.place(x=15, y=685, width=250, height=35)

butn4 = Button(text="Очистить поле", fg="black", command=lambda: clear_canvas(c))
butn4.place(x=15, y=730, width=250, height=35)

check_hiding(0)
check_buttons(0, hide)
ent5.configure(state=DISABLED)

window.mainloop()
