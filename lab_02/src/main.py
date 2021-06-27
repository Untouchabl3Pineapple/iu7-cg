from tkinter import *

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from copy import deepcopy

from geometry import get_circle_dots_coords, get_hyperbole_dots_coords
from draw import *


def window_settings(root):
    root.geometry("1300x710+100+100")
    root.title("Lab 2")
    root.configure(background="pink")
    root.resizable(False, False)


def ui(root):
    pic = plt.Figure(figsize=(7, 7), dpi=100)
    pic.set_facecolor("pink")

    canvas = FigureCanvasTkAgg(pic, root)
    canvas.get_tk_widget().place(x=500, y=0)

    figure = pic.add_subplot(111)

    circle = get_circle_dots_coords()
    hyperbole = get_hyperbole_dots_coords()

    update_canvas(figure, canvas, circle, hyperbole)

    actions = [[deepcopy(circle), deepcopy(hyperbole)]]

    lab_mov = Label(
        root,
        text="ПЕРЕМЕЩЕНИЕ",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_mov.place(x=143, y=20)

    lab_mx = Label(
        root,
        text="mX",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_mx.place(x=110, y=80)
    lab_my = Label(
        root,
        text="mY",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_my.place(x=280, y=80)

    ent_mx = Entry(root, bd=0, width=15)
    ent_mx.place(x=50, y=110)
    ent_my = Entry(root, bd=0, width=15)
    ent_my.place(x=217, y=110)

    but_mov = Button(
        root,
        height=2,
        width=34,
        text="Переместить",
        bg="pink",
        command=lambda: move(
            figure, canvas, actions, circle, hyperbole, ent_mx.get(), ent_my.get()
        ),
    )
    but_mov.place(x=50, y=150)

    lab_rot = Label(
        root,
        text="ВРАЩЕНИЕ",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_rot.place(x=157, y=220)

    lab_rx = Label(
        root,
        text="rX",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_rx.place(x=90, y=280)
    lab_ry = Label(
        root,
        text="rY",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_ry.place(x=195, y=280)
    lab_ang = Label(
        root,
        text="Угол º",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_ang.place(x=290, y=280)

    ent_rx = Entry(root, bd=0, width=10)
    ent_rx.place(x=50, y=310)
    ent_ry = Entry(root, bd=0, width=10)
    ent_ry.place(x=156, y=310)
    ent_ang = Entry(root, bd=0, width=10)
    ent_ang.place(x=262, y=310)

    but_rot = Button(
        root,
        height=2,
        width=34,
        text="Вращать",
        bg="pink",
        command=lambda: rotate(
            figure,
            canvas,
            actions,
            circle,
            hyperbole,
            ent_rx.get(),
            ent_ry.get(),
            ent_ang.get(),
        ),
    )
    but_rot.place(x=50, y=350)

    lab_scal = Label(
        root,
        text="МАСШТАБИРОВАНИЕ",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_scal.place(x=125, y=420)

    lab_sx = Label(
        root,
        text="sX",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_sx.place(x=75, y=480)
    lab_sy = Label(
        root,
        text="sY",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_sy.place(x=155, y=480)
    lab_kx = Label(
        root,
        text="kX",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_kx.place(x=235, y=480)
    lab_ky = Label(
        root,
        text="kY",
        font=("Calibri", 15),
        background="pink",
        foreground="black",
    )
    lab_ky.place(x=315, y=480)

    ent_sx = Entry(root, bd=0, width=7)
    ent_sx.place(x=50, y=510)
    ent_sy = Entry(root, bd=0, width=7)
    ent_sy.place(x=129, y=510)
    ent_kx = Entry(root, bd=0, width=7)
    ent_kx.place(x=210, y=510)
    ent_ky = Entry(root, bd=0, width=7)
    ent_ky.place(x=289, y=510)

    but_scal = Button(
        root,
        height=2,
        width=34,
        text="Масштабировать",
        bg="pink",
        command=lambda: scale(
            figure,
            canvas,
            actions,
            circle,
            hyperbole,
            ent_sx.get(),
            ent_sy.get(),
            ent_kx.get(),
            ent_ky.get(),
        ),
    )
    but_scal.place(x=50, y=550)

    but_bstep = Button(
        root,
        height=1,
        width=34,
        text="Шаг назад",
        bg="pink",
        command=lambda: step_back(figure, canvas, actions, circle, hyperbole),
    )
    but_bstep.place(x=50, y=630)
    but_reset = Button(
        root,
        height=1,
        width=34,
        text="Сброс",
        bg="pink",
        command=lambda: reset(figure, canvas, actions, circle, hyperbole),
    )
    but_reset.place(x=50, y=660)


def main():
    root = Tk()

    window_settings(root)
    ui(root)

    root.mainloop()


if __name__ == "__main__":
    main()