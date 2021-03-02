from tkinter import *
from tkinter.messagebox import showerror


def point_delete(window, listb_f_set, listb_s_set):
    listb_f_cursel = listb_f_set.curselection()
    listb_s_cursel = listb_s_set.curselection()

    try:
        if len(listb_f_cursel) == 0:
            listb_s_set.delete(listb_s_cursel)
        else:
            listb_f_set.delete(listb_f_cursel)
    except:
        showerror("Ошибка", "Выделите координаты точки для их удаления")
