from tkinter import *
from tkinter.messagebox import showerror

from toplvl_settings import window_settings


def ui(
    window,
    listb_f_set,
    listb_s_set,
    entry_x_val,
    entry_y_val,
    listb_f_cursel,
    listb_s_cursel,
):
    entry_x = Text(window, height=1.4, width=15)
    entry_x.place(x=60, y=50)
    entry_x.insert("1.0", entry_x_val)
    entry_y = Text(window, height=1.4, width=15)
    entry_y.place(x=250, y=50)
    entry_y.insert("1.0", entry_y_val)

    lab_x = Label(
        window,
        text="X:",
        font=("Calibri", 15),
        background="rosy brown",
        foreground="black",
    )
    lab_x.place(x=25, y=48)
    lab_y = Label(
        window,
        text="Y:",
        font=("Calibri", 15),
        background="rosy brown",
        foreground="black",
    )
    lab_y.place(x=217, y=48)

    but_exit = Button(
        window,
        height=3,
        width=20,
        text="Выйти",
        bg="rosy brown",
        command=lambda: window.destroy(),
    )
    but_exit.place(x=10, y=120)
    but_change = Button(
        window,
        height=3,
        width=20,
        text="Изменить",
        bg="rosy brown",
        command=lambda: process(
            window,
            entry_x,
            entry_y,
            listb_f_set,
            listb_s_set,
            listb_f_cursel,
            listb_s_cursel,
        ),
    )
    but_change.place(x=205, y=120)


def get_point_coord(listb_f_set, listb_s_set):
    listb_f_cursel = listb_f_set.curselection()
    listb_s_cursel = listb_s_set.curselection()

    try:
        if len(listb_f_cursel) == 0:
            coord = listb_s_set.get(listb_s_cursel).split(";")

            entry_x_val = coord[0]
            entry_y_val = coord[1]
        else:
            coord = listb_f_set.get(listb_f_cursel).split(";")

            entry_x_val = coord[0]
            entry_y_val = coord[1]

        return entry_x_val, entry_y_val

    except:
        showerror("Ошибка", "Выделите координаты точки для их изменения")
        return


def process(
    window, entry_x, entry_y, listb_f_set, listb_s_set, listb_f_cursel, listb_s_cursel
):
    try:
        x_c = float(entry_x.get("1.0", "end"))
        y_c = float(entry_y.get("1.0", "end"))
    except:
        showerror("Ошибка", "Проверьте правильность вводимых данных", parent=window)
        return

    if len(listb_f_cursel) == 0:
        coord_select_ind = listb_s_cursel[0]
        listb_s_set.delete(coord_select_ind)
        listb_s_set.insert(coord_select_ind, str(x_c) + ";" + str(y_c))
    else:
        coord_select_ind = listb_f_cursel[0]
        listb_f_set.delete(coord_select_ind)
        listb_f_set.insert(coord_select_ind, str(x_c) + ";" + str(y_c))

    window.destroy()


def point_change(window, listb_f_set, listb_s_set):
    cur_coord = get_point_coord(listb_f_set, listb_s_set)

    if cur_coord is not None:
        top_window = Toplevel(window)
        window_settings(top_window, "Изменение координат точки")
        ui(
            top_window,
            listb_f_set,
            listb_s_set,
            cur_coord[0],
            cur_coord[1],
            listb_f_set.curselection(),
            listb_s_set.curselection(),
        )
