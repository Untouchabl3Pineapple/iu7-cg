import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.colorchooser import askcolor
from operator import itemgetter
import time


# Returns edges from list of dots
def get_edges(dots_mas):
    print("dots_mas\n")
    print(dots_mas)

    edges = []

    for dots in dots_mas:
        for i in range(len(dots)):
            if i + 1 > len(dots) - 1:
                edges.append([dots[i], dots[0]])
            else:
                edges.append([dots[i], dots[i + 1]])

    print("edges")
    print(edges)
    return edges


# Returns intersections from list of edges
def get_intersections(edges):
    intersections = []

    for i in range(len(edges)):
        x1 = edges[i][0][0]
        y1 = edges[i][0][1]
        x2 = edges[i][1][0]
        y2 = edges[i][1][1]

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_y != 0:
            dx = ((x2 > x1) - (x2 < x1)) * len_x / len_y
            dy = (y2 > y1) - (y2 < y1)

            x1 += dx / 2
            y1 += dy / 2

            for j in range(len_y):
                intersections.append((x1, y1))
                x1 += dx
                y1 += dy

    print("inters")
    # print(intersections)
    return intersections
    

# Fills figure instantly
def fill_figure(self, inter):
    for i in range(0, len(inter), 2):
        draw_inside(self, inter[i], inter[i + 1])


# Fills figure with delay
def fill_delay(self, inter):
    cross1 = inter.pop()
    cross2 = inter.pop()

    draw_inside(self, cross1, cross2)
    x_beg = int(cross1[0] + 0.5)
    x_end = int(cross2[0] - 0.5) + 1
    y = int(cross1[1])
    print("(", x_beg, ";", y, ")", " ", "(", x_end, ";", y, ")")

    if len(inter) > 0:
        self.process = self.canvas.after(self.delay, lambda: fill_delay(self, inter))
    else:
        draw_edges(self)


# Draws line between two dots
def draw_inside(self, dot1, dot2):
    x_beg = int(dot1[0] + 0.5)
    x_end = int(dot2[0] - 0.5) + 1
    y = int(dot1[1])

    self.canvas.create_line(x_beg, y, x_end, y, fill=self.fill_color)


# Draws edges
def draw_edges(self):
    for i in range(len(self.edges)):
        self.canvas.create_line(self.edges[i][0], self.edges[i][1], fill=self.bd_color)


# Main window class
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)

        def click_add_line(event):
            if self.ctrl_pressed == 0:
                add_line(self, event.x, event.y)
            else:
                if len(self.figs) > self.fig_n:
                    x_prev = self.figs[self.fig_n][-1][0]
                    y_prev = self.figs[self.fig_n][-1][1]

                    x = event.x - x_prev
                    y = event.y - y_prev

                    if abs(y) >= abs(x):
                        add_line(self, x_prev, event.y)
                    else:
                        add_line(self, event.x, y_prev)
                else:
                    add_line(self, event.x, event.y)

        def click_end(event):
            if len(self.figs) > self.fig_n:
                if len(self.figs[self.fig_n]) <= 2:
                    clear(self, "tag" + str(self.fig_n))
                else:
                    end(self)

        def press_key(event):
            if event.keysym == "Control_L":
                if self.ctrl_pressed == 0:
                    self.ctrl_pressed = 1

        def release_key(event):
            if event.keysym == "Control_L":
                if self.ctrl_pressed == 1:
                    self.ctrl_pressed = 0

        def moving_line(event):
            self.in_canvas = 1

            if self.drawing == 1:
                if self.ctrl_pressed == 0:
                    cur_pos = (event.x, event.y)

                    self.canvas.delete("new")
                    self.canvas.create_line(
                        self.figs[self.fig_n][-1],
                        cur_pos,
                        fill=self.bd_color,
                        tag="new",
                    )
                else:
                    x_prev = self.figs[self.fig_n][-1][0]
                    y_prev = self.figs[self.fig_n][-1][1]

                    x = event.x - x_prev
                    y = event.y - y_prev

                    if abs(y) >= abs(x):
                        cur_pos = (x_prev, event.y)
                    else:
                        cur_pos = (event.x, y_prev)

                    self.canvas.delete("new")
                    self.canvas.create_line(
                        self.figs[self.fig_n][-1],
                        cur_pos,
                        fill=self.bd_color,
                        tag="new",
                    )

        def in_window(event):
            if self.in_canvas == 0:
                self.canvas.delete("new")
            self.in_canvas = 0

        options_size = 300  # const
        can_x = args[0] - options_size
        can_y = args[1]

        tk.Tk.title(self, "lab_05")
        tk.Tk.geometry(self, str(can_x + options_size) + "x" + str(can_y))

        self.fill_color = "wheat1"
        self.bg_color = "linen"
        self.bd_color = "#000000"

        self.fig_n = 0  # Количество многоугольников
        self.figs = []  # Хранит многоугольники
        self.ctrl_pressed = 0  # Нажат ли ctrl
        self.drawing = 0  # Отображать отрезок до курсора
        self.in_canvas = 0  # Курсор находитсся в canvas
        self.delay = 2  # Задержка
        self.edges = []  # Массив ребер
        self.process = None
        self.table_items = []  # Элементы таблицы

        self.work = ttk.Frame(self)

        self.table = ttk.Treeview(self.work, columns="cdc", height=18)
        self.table.heading("#0", text="X")
        self.table.heading("#1", text="Y")
        self.table.column("#0", width=150)
        self.table.column("#1", width=150)

        self.table.grid(row=0, column=0, sticky="ns")

        self.add = ttk.LabelFrame(self.work, text="\t     Добавить ребро")

        self.var_x = tk.StringVar()
        self.var_y = tk.StringVar()

        self.label_x = ttk.Label(self.add, text="X:")
        self.label_x.grid(row=1, column=0)
        self.entry_x = ttk.Entry(self.add, textvariable=self.var_x, width=10)
        self.entry_x.grid(row=1, column=1)

        self.label_y = ttk.Label(self.add, text="Y:")
        self.label_y.grid(row=1, column=2)
        self.entry_y = ttk.Entry(self.add, textvariable=self.var_y, width=10)
        self.entry_y.grid(row=1, column=3)

        self.button_add = ttk.Button(
            self.add, text="Добавить", command=lambda: get_add(self)
        )
        self.button_add.grid(row=2, column=0, columnspan=2)

        self.button_end = ttk.Button(
            self.add, text="Соединить", command=lambda: click_end(self)
        )
        self.button_end.grid(row=2, column=2, columnspan=2)

        self.add.grid(row=1, column=0, sticky="nsew")
        self.add.grid_columnconfigure(0, weight=1)
        self.add.grid_columnconfigure(1, weight=1)
        self.add.grid_columnconfigure(2, weight=1)
        self.add.grid_columnconfigure(3, weight=1)

        self.color = ttk.LabelFrame(self.work, text="\t     Выбрать цвет")

        self.button_border = ttk.Button(
            self.color, text="Цвет границы", command=lambda: pick_color(self, "bd")
        )
        self.button_border.grid(row=0, column=0)

        self.label_bd = tk.Label(self.color, bg=self.bd_color, width=10)
        self.label_bd.grid(row=0, column=1)

        self.button_fill = ttk.Button(
            self.color, text="Цвет закраски", command=lambda: pick_color(self, "fill")
        )
        self.button_fill.grid(row=1, column=0)

        self.label_fill = tk.Label(self.color, bg=self.fill_color, width=10)
        self.label_fill.grid(row=1, column=1)

        self.color.grid(row=2, column=0, sticky="nsew")
        self.color.grid_columnconfigure(0, weight=1)
        self.color.grid_columnconfigure(1, weight=1)

        self.options = ttk.LabelFrame(self.work, text="\t     Действия")

        self.button_clear = ttk.Button(
            self.options, text="Очистить", command=lambda: clear(self, "all")
        )
        self.button_clear.grid(row=0, column=0)

        self.button_fill = ttk.Button(
            self.options, text="Закрасить", command=lambda: fill(self)
        )
        self.button_fill.grid(row=0, column=1)

        self.delay_var = tk.IntVar()
        self.delay_var.set(0)
        self.delay_cb = ttk.Checkbutton(
            self.options, text="Закрасить с задержкой", variable=self.delay_var
        )
        self.delay_cb.grid(row=1, column=0, columnspan=2)

        self.delay_label = ttk.Label(self.options, text="Задержка (в мс):")
        self.delay_label.grid(row=2, column=0)

        self.delay_str = tk.StringVar()
        self.delay_str.set(str(self.delay))
        self.delay_entry = ttk.Entry(
            self.options, width=10, textvariable=self.delay_str
        )
        self.delay_entry.grid(row=2, column=1)

        self.options.grid(row=3, column=0, sticky="nsew")
        self.options.grid_columnconfigure(0, weight=1)
        self.options.grid_columnconfigure(1, weight=1)

        self.work.pack(side=tk.RIGHT)

        self.canvas = tk.Canvas(self, bg=self.bg_color)
        tk.Tk.bind(self, "<KeyPress>", press_key)
        tk.Tk.bind(self, "<KeyRelease>", release_key)
        tk.Tk.bind(self, "<Motion>", in_window)
        self.canvas.bind("<Button-1>", click_add_line)
        self.canvas.bind("<Button-3>", click_end)
        self.canvas.bind("<Motion>", moving_line)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


def show_time(time):
    messagebox.showinfo("Время работы алгоритма", str(round(time, 6)) + " секунд")


# Calls functions for filling polygon
def fill(self):
    start_time = time.perf_counter()
    self.edges = get_edges(self.figs)
    if len(self.edges) < 3:
        mes("Недостаточно ребер")
        return -1

    intersections = get_intersections(self.edges)

    intersections.sort(key=itemgetter(1, 0))

    print(intersections)

    if int(self.delay_var.get()) == 1:
        try:
            self.delay = int(self.delay_str.get())
        except ValueError:
            mes("Неверная задержка.")
            return -2
        print("DELAY WORK:")
        print("INTERSECTION LEN IS", len(intersections))
        print("intersections are:")
        for i in intersections:
            print(i)
        fill_delay(self, intersections)
    else:
        fill_figure(self, intersections)
        draw_edges(self)
    stop_time = time.perf_counter()
    show_time(stop_time - start_time)


# Picks color
def pick_color(self, name):
    color = askcolor()[1]
    print(color)

    if name == "bd":
        self.bd_color = color
        self.label_bd.configure(bg=color)
    elif name == "fill":
        self.fill_color = color
        self.label_fill.configure(bg=color)


# Creates window with warning
def mes(text):
    messagebox.showinfo("Внимание", text)


# Runs add with manual input
def get_add(self):
    try:
        x = int(self.var_x.get())
        y = int(self.var_y.get())
    except ValueError:
        mes("Неверные данные!")
        return -1

    add_line(self, x, y)


# Adds new dot and connects with previous
def add_line(self, x, y):
    if len(self.figs) <= self.fig_n:
        self.figs.append([])
        self.table_items.append([])

    self.figs[self.fig_n].append((x, y))
    self.table_items[self.fig_n].append(
        self.table.insert("", "end", text=str(x), values=(str(y)))
    )

    if self.drawing == 0:
        self.drawing = 1

    if len(self.figs[self.fig_n]) > 1:
        self.canvas.create_line(
            self.figs[self.fig_n][-1],
            self.figs[self.fig_n][-2],
            fill=self.bd_color,
            tag="tag" + str(self.fig_n),
        )


# Connects last point with first
def end(self):
    if len(self.figs[self.fig_n]) > 2:
        self.canvas.create_line(
            self.figs[self.fig_n][-1],
            self.figs[self.fig_n][0],
            fill=self.bd_color,
            tag="tag" + str(self.fig_n),
        )

        self.table_items[self.fig_n].append(
            self.table.insert("", "end", text="__________", values="__________")
        )

        self.fig_n += 1

        self.drawing = 0
        self.canvas.delete("new")


# Clears obj and resets variables
def clear(self, obj):
    self.drawing = 0
    self.canvas.delete(obj)
    self.canvas.delete("new")
    if self.process is not None:
        self.canvas.after_cancel(self.process)
    self.pix_map = []
    self.edges = []

    if obj == "all":
        self.figs = []
        self.fig_n = 0
        self.table_items = []
        self.table.delete(*self.table.get_children())
    else:
        self.figs.pop()
        for item in self.table_items.pop():
            self.table.delete(item)


if __name__ == "__main__":
    app = Application(1000, 600)
    app.mainloop()
