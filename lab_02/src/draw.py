from tkinter.messagebox import showerror

from copy import deepcopy

from geometry import move_loop, rotate_loop, scale_loop


def move(figure, canvas, actions, circle, hyperbole, mx, my):
    try:
        mx, my = float(mx), float(my)
    except:
        showerror("Ошибка", "Некорректно введены координаты")
        return

    move_loop(circle, mx, my)
    move_loop(hyperbole, mx, my)

    actions.append([deepcopy(circle), deepcopy(hyperbole)])

    update_canvas(figure, canvas, circle, hyperbole)


def rotate(figure, canvas, actions, circle, hyperbole, rx, ry, angle):
    try:
        rx, ry, angle = float(rx), float(ry), float(angle)
    except:
        showerror("Ошибка", "Некорректно введены координаты")
        return

    rotate_loop(circle, rx, ry, angle)
    rotate_loop(hyperbole, rx, ry, angle)

    actions.append([deepcopy(circle), deepcopy(hyperbole)])

    update_canvas(figure, canvas, circle, hyperbole)


def scale(figure, canvas, actions, circle, hyperbole, sx, sy, kx, ky):
    try:
        sx, sy, kx, ky = float(sx), float(sy), float(kx), float(ky)
    except:
        showerror("Ошибка", "Некорректно введены координаты")
        return

    scale_loop(circle, sx, sy, kx, ky)
    scale_loop(hyperbole, sx, sy, kx, ky)

    actions.append([deepcopy(circle), deepcopy(hyperbole)])

    update_canvas(figure, canvas, circle, hyperbole)


def step_back(figure, canvas, actions, circle, hyperbole):
    early_obj = len(actions) - 2

    if early_obj >= 0:
        circle[0] = actions[early_obj][0][0].copy()
        circle[1] = actions[early_obj][0][1].copy()

        hyperbole[0] = actions[early_obj][1][0].copy()
        hyperbole[1] = actions[early_obj][1][1].copy()

        actions.pop()

        update_canvas(figure, canvas, circle, hyperbole)


def reset(figure, canvas, actions, circle, hyperbole):
    if len(actions) > 1:
        circle[0] = actions[0][0][0].copy()
        circle[1] = actions[0][0][1].copy()

        hyperbole[0] = actions[0][1][0].copy()
        hyperbole[1] = actions[0][1][1].copy()

        for i in range(1, len(actions)):
            actions.pop()

        update_canvas(figure, canvas, circle, hyperbole)


def update_canvas(figure, canvas, circle, hyperbole):
    x_llim = -60
    x_hlim = 60
    y_llim = -60
    y_hlim = 60

    figure.clear()

    figure.set_xlabel("x", fontsize=14)
    figure.set_ylabel("y", fontsize=14)
    figure.set_xlim([x_llim, x_hlim])
    figure.set_ylim([y_llim, y_hlim])
    figure.grid()

    figure.plot(circle[0], circle[1])
    figure.plot(hyperbole[0], hyperbole[1])

    canvas.draw()
