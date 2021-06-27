from tkinter import Tk, ttk, Radiobutton, Canvas, Label, Entry, Button, DISABLED, IntVar
from draw import WINDOW_HEIGHT, WINDOW_WIDTH, CANVAS_WIDTH, CANVAS_HEIGHT
from draw import draw_line, clear_canvas, draw_spectrum
from comparisons import time_comparison, step_comparison

def main():
    window = Tk()
    window.title("Лабораторная работа №3")
    window.geometry("%dx%d" %(WINDOW_WIDTH, WINDOW_HEIGHT))
    window.resizable(False, False)
    window["bg"] = "pale turquoise"  

    canvas = Canvas(window, width = CANVAS_WIDTH, height = CANVAS_HEIGHT, bg = "white")
    canvas.place(x = 0, y = 0)


    Label(text = "Цвет линий", font = ("Arial", 16, "bold"), bg = "pale turquoise",
        fg = "black").place(width = 305, height = 30, x = CANVAS_WIDTH + 10, y = 10)

    color_fg = IntVar()
    color_fg.set(3)

    Radiobutton(text = "Фоновый", variable = color_fg, value = 0,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 110, height = 20, x = CANVAS_WIDTH + 20, y = 50)

    Radiobutton(text = "Чёрный", variable = color_fg, value = 1,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 110, height = 20, x = CANVAS_WIDTH + 20, y = 70)

    Radiobutton(text = "Красный", variable = color_fg, value = 2,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 110, height = 20, x = CANVAS_WIDTH + 20, y = 90)

    Radiobutton(text = "Синий", variable = color_fg, value = 3,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 110, height = 20, x = CANVAS_WIDTH + 180, y = 50)

    Radiobutton(text = "Зелёный", variable = color_fg, value = 4,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 110, height = 20, x = CANVAS_WIDTH + 180, y = 70)

    Radiobutton(text = "Жёлтый", variable = color_fg, value = 5,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 110, height = 20, x = CANVAS_WIDTH + 180, y = 90)


    Label(text = "Алгоритмы построения", font = ("Arial", 16, "bold"), bg = "pale turquoise",
        fg = "black").place(width = 305, height = 30, x = CANVAS_WIDTH + 10, y = 120)

    algorithm = IntVar()
    algorithm.set(0)

    Radiobutton(text = "ЦДА", variable = algorithm, value = 0,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 250, height = 20, x = CANVAS_WIDTH + 20, y = 160)

    Radiobutton(text = "Брезенхем (float)", variable = algorithm, value = 1,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 250, height = 20, x = CANVAS_WIDTH + 20, y = 180)

    Radiobutton(text = "Брезенхем (int)", variable = algorithm, value = 2,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 250, height = 20, x = CANVAS_WIDTH + 20, y = 200)

    Radiobutton(text = "Брезенхем (с устр. ступ.)", variable = algorithm, value = 3,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 280, height = 20, x = CANVAS_WIDTH + 20, y = 220)

    Radiobutton(text = "Ву", variable = algorithm, value = 4,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 250, height = 20, x = CANVAS_WIDTH + 20, y = 240)

    Radiobutton(text = "Библиотечная функция", variable = algorithm, value = 5,
        font = ("Arial", 16), bg = "pale turquoise", fg = "#29293d", anchor = "w").\
        place(width = 250, height = 20, x = CANVAS_WIDTH + 20, y = 260)


    Label(text = "Построение отрезка", font = ("Arial", 16, "bold"), bg = "pale turquoise",
        fg = "black").place(width = 305, height = 30, x = CANVAS_WIDTH + 10, y = 290)


    Label(text = "x0\ty0\tx1\ty1", font = ("Arial", 16), bg = "pale turquoise",
        fg = "#29293d").place(width = 260, height = 20, x = CANVAS_WIDTH + 30, y = 330)

    x_beg_entry = Entry(font = ("Arial", 16))
    x_beg_entry.place(width = 65, height = 30, x = CANVAS_WIDTH + 30, y = 360)

    y_beg_entry = Entry(font = ("Arial", 16))
    y_beg_entry.place(width = 65, height = 30, x = CANVAS_WIDTH + 95, y = 360)

    x_end_entry = Entry(font = ("Arial", 16))
    x_end_entry.place(width = 65, height = 30, x = CANVAS_WIDTH + 160, y = 360)

    y_end_entry = Entry(font = ("Arial", 16))
    y_end_entry.place(width = 65, height = 30, x = CANVAS_WIDTH + 225, y = 360)

    # Button(highlightbackground = "#7575a3", highlightthickness = 30, fg = "pale turquoise", state = DISABLED).\
    #     place(width = 260, height = 30,  x = CANVAS_WIDTH + 30, y = 400)

    Button(text = "Построить", font = ("Arial", 16),
        command = lambda: draw_line(canvas, color_fg, algorithm,
            x_beg_entry, y_beg_entry, x_end_entry, y_end_entry)).\
        place(width = 256, height = 26,  x = CANVAS_WIDTH + 32, y = 402)


    Label(text = "Построение спектра", font = ("Arial", 16, "bold"), bg = "pale turquoise",
        fg = "black").place(width = 305, height = 30, x = CANVAS_WIDTH + 10, y = 440)

    Label(text = "Угол поворота", font = ("Arial", 16), bg = "pale turquoise",
        fg = "#29293d").place(width = 150, height = 30, x = CANVAS_WIDTH + 30, y = 480)

    angle_entry = Entry(font = ("Arial", 16))
    angle_entry.place(width = 100, height = 30, x = CANVAS_WIDTH + 190, y = 480)

    Label(text = "Длина отрезка", font = ("Arial", 16), bg = "pale turquoise",
        fg = "#29293d").place(width = 150, height = 30, x = CANVAS_WIDTH + 30, y = 510)

    radius_entry = Entry(font = ("Arial", 16))
    radius_entry.place(width = 100, height = 30, x = CANVAS_WIDTH + 190, y = 510)

    # Button(highlightbackground = "#7575a3", highlightthickness = 30, fg = "pale turquoise", state = DISABLED).\
    #     place(width = 260, height = 30,  x = CANVAS_WIDTH + 30, y = 550)

    Button(text = "Построить", font = ("Arial", 16),
        command = lambda: draw_spectrum(canvas, color_fg, algorithm, angle_entry, radius_entry)).\
        place(width = 256, height = 26,  x = CANVAS_WIDTH + 32, y = 552)


    # Button(highlightbackground = "#7575a3", highlightthickness = 30, fg = "pale turquoise", state = DISABLED).\
    #     place(width = 260, height = 35,  x = CANVAS_WIDTH + 30, y = 595)

    Button(text = "Сравнить время работы алгоритмов", font = ("Arial", 16),
        command = lambda: time_comparison(canvas, color_fg, algorithm, angle_entry, radius_entry)).\
        place(width = 256, height = 31,  x = CANVAS_WIDTH + 32, y = 597)


    # Button(highlightbackground = "#7575a3", highlightthickness = 30, fg = "pale turquoise", state = DISABLED).\
    #     place(width = 260, height = 35,  x = CANVAS_WIDTH + 30, y = 635)

    Button(text = "Сравнить ступенчатости", font = ("Arial", 16),
        command = lambda: step_comparison(canvas, angle_entry, radius_entry)).\
        place(width = 256, height = 31,  x = CANVAS_WIDTH + 32, y = 637)


    # Button(highlightbackground = "#7575a3", highlightthickness = 30, fg = "pale turquoise", state = DISABLED).\
    #     place(width = 260, height = 40,  x = CANVAS_WIDTH + 30, y = 685)

    Button(text = "Очистить экран", font = ("Arial", 16),
        command = lambda: clear_canvas(canvas)).\
        place(width = 256, height = 36,  x = CANVAS_WIDTH + 32, y = 687)

    angle_entry.insert(0, 10)
    radius_entry.insert(0, 300)

    x_beg_entry.insert(0, 200)
    y_beg_entry.insert(0, 200)

    x_end_entry.insert(0, 700)
    y_end_entry.insert(0, 300)

    window.mainloop()

if __name__ == "__main__":
    main()
