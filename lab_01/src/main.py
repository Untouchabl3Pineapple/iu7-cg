"""
    Даны два множества точек на плоскости. Найти пару окружностей
    (каждая из окружностей проходит хотя бы через три различные точки
    одного и того же множества, точки для разных окружностей берутся
    из разных множеств) таких, что прямая, соединяющая центры этих
    окружностей, образует минимальный угол с осью ординат.
"""


from tkinter import *

from task_info import task_info
from point_create import point_create
from point_del import point_delete
from point_change import point_change
from clear_listb import clear_listb
from solve_task import solve_task


def window_settings(root):
    root.geometry("1300x700+100+100")
    root.title("Lab 1")
    root.configure(background="bisque")
    root.resizable(False, False)


def ui(root):
    canvas = Canvas(root, width=694, height=694, bg="pale turquoise", cursor="pencil")
    canvas.place(x=600, y=0)

    lab_f_set = Label(
        root,
        text="Первое множество точек",
        font=("Calibri", 15),
        background="bisque",
        foreground="black",
    )
    lab_f_set.place(x=60, y=5)

    lab_s_set = Label(
        root,
        text="Второе множество точек",
        font=("Calibri", 15),
        background="bisque",
        foreground="black",
    )
    lab_s_set.place(x=330, y=5)

    listb_f_set = Listbox(root, width=30, height=15)
    listb_f_set.place(x=30, y=30)

    listb_s_set = Listbox(root, width=30, height=15)
    listb_s_set.place(x=300, y=30)

    but_task = Button(
        root, height=3, width=20, text="Условие", bg="bisque", command=task_info
    )
    but_task.place(x=30, y=320)

    but_ins_point = Button(
        root,
        height=3,
        width=20,
        text="Добавить точку",
        bg="bisque",
        command=lambda: point_create(root, listb_f_set, listb_s_set),
    )
    but_ins_point.place(x=388, y=320)

    but_del_point = Button(
        root,
        height=3,
        width=20,
        text="Удалить точку",
        bg="bisque",
        command=lambda: point_delete(root, listb_f_set, listb_s_set),
    )
    but_del_point.place(x=388, y=390)

    but_change_point = Button(
        root,
        height=3,
        width=20,
        text="Изменить точку",
        bg="bisque",
        command=lambda: point_change(root, listb_f_set, listb_s_set),
    )
    but_change_point.place(x=388, y=460)

    but_clear_listb = Button(
        root,
        height=3,
        width=20,
        text="Очистить поле",
        bg="bisque",
        command=lambda: clear_listb(root, listb_f_set, listb_s_set),
    )
    but_clear_listb.place(x=388, y=530)

    but_solve_task = Button(
        root,
        height=3,
        width=20,
        text="Решить задачу",
        bg="bisque",
        command=lambda: solve_task(canvas, listb_f_set, listb_s_set),
    )
    but_solve_task.place(x=388, y=610)

    but_exit = Button(
        root,
        height=3,
        width=20,
        text="Выйти",
        bg="bisque",
        command=lambda: root.destroy(),
    )
    but_exit.place(x=30, y=610)


def main():
    root = Tk()

    window_settings(root)
    ui(root)

    root.mainloop()


if __name__ == "__main__":
    main()
