from tkinter import *
from tkinter.messagebox import showerror

from toplvl_settings import window_settings


def ui(window, listb_f_set, listb_s_set):
    var = IntVar()

    f_set_select = Radiobutton(
        window, text="Очистить первое множество", bg="rosy brown", value=1, variable=var
    )
    f_set_select.place(x=10, y=10)
    s_set_select = Radiobutton(
        window, text="Очистить второе множество", bg="rosy brown", value=2, variable=var
    )
    s_set_select.place(x=10, y=40)
    t_set_select = Radiobutton(
        window, text="Очистить оба множества", bg="rosy brown", value=3, variable=var
    )
    t_set_select.place(x=10, y=70)

    but_exit = Button(
        window,
        height=3,
        width=20,
        text="Выйти",
        bg="rosy brown",
        command=lambda: window.destroy(),
    )
    but_exit.place(x=10, y=120)
    but_clear = Button(
        window,
        height=3,
        width=20,
        text="Очистить",
        bg="rosy brown",
        command=lambda: process(window, var, listb_f_set, listb_s_set),
    )
    but_clear.place(x=205, y=120)


def process(window, var, listb_f_set, listb_s_set):
    var_val = var.get()

    if var_val == 1:
        listb_f_set.delete(0, END)
    elif var_val == 2:
        listb_s_set.delete(0, END)
    elif var_val == 3:
        listb_f_set.delete(0, END)
        listb_s_set.delete(0, END)
    else:
        showerror("Ошибка", "Выберите нужное вам поле", parent=window)
        return

    window.destroy()


def clear_listb(window, listb_f_set, listb_s_set):
    top_window = Toplevel(window)
    window_settings(top_window, "Очистка полей")
    ui(top_window, listb_f_set, listb_s_set)
