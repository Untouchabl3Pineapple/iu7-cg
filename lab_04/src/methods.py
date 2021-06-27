from math import floor, fabs, cos, sin, radians, pi, sqrt
from pixel import draw_pixels


def bresenham_circle(xc, yc, r, color, canvas, draw):
    x = 0
    y = r

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)

    delta = 2 * (1 - r)

    while x < y:
        if delta <= 0:
            d = 2 * (delta + y) - 1
            x += 1

            if d >= 0:
                y -= 1
                delta += 2 * (x - y + 1)
            else:
                delta += x + x + 1
        else:
            d = 2 * (delta - x) - 1
            y -= 1

            if d < 0:
                x += 1
                delta += 2 * (x - y + 1)
            else:
                delta += 1 - y - y

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)


def bresenham_ellipse(xc, yc, ra, rb, color, canvas, draw):
    x = 0
    y = rb

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)

    sqr_ra = ra * ra
    sqr_rb = rb * rb
    delta = sqr_rb - sqr_ra * (rb + rb + 1)

    while y >= 0:
        if delta <= 0:
            d = 2 * delta + sqr_ra * (y + y + 2)
            x += 1
            delta += sqr_rb * (x + x + 1)

            if d >= 0:
                y -= 1
                delta += sqr_ra * (-y - y + 1)
        else:
            d = 2 * delta + sqr_rb * (-x - x + 2)
            y -= 1
            delta += sqr_ra * (-y - y + 1)

            if d < 0:
                x += 1
                delta += sqr_rb * (x + x + 1)

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)


def canonical_circle(xc, yc, r, color, canvas, draw):
    sqr_r = r ** 2

    border = round(xc + r / sqrt(2))

    for x in range(xc, border + 1):
        y = yc + sqrt(sqr_r - (x - xc) ** 2)

        if draw:
            draw_pixels(canvas, [x, y, color], xc, yc, circle=True)


def canonical_ellipse(xc, yc, ra, rb, color, canvas, draw):
    sqr_ra = ra * ra
    sqr_rb = rb * rb

    border_x = round(xc + ra / sqrt(1 + sqr_rb / sqr_ra))
    border_y = round(yc + rb / sqrt(1 + sqr_ra / sqr_rb))

    for x in range(xc, border_x + 1):
        y = yc + sqrt(sqr_ra * sqr_rb - (x - xc) ** 2 * sqr_rb) / ra

        if draw:
            draw_pixels(canvas, [x, y, color], xc, yc, circle=False)

    for y in range(border_y, yc - 1, -1):
        x = xc + sqrt(sqr_ra * sqr_rb - (y - yc) ** 2 * sqr_ra) / rb

        if draw:
            draw_pixels(canvas, [x, y, color], xc, yc, circle=False)


def midpoint_circle(xc, yc, r, color, canvas, draw):
    x = r
    y = 0

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)

    delta = 1 - r

    while y < x:
        y += 1

        if delta >= 0:
            x -= 1
            delta -= x + x

        delta += y + y + 1

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=True)


def midpoint_ellipse(xc, yc, ra, rb, color, canvas, draw):
    sqr_ra = ra * ra
    sqr_rb = rb * rb

    border = round(ra / sqrt(1 + sqr_rb / sqr_ra))

    x = 0
    y = rb

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)

    delta = sqr_rb - round(sqr_ra * (rb - 1 / 4))
    while x < border:
        if delta > 0:
            y -= 1
            delta -= sqr_ra * y * 2

        x += 1
        delta += sqr_rb * (x + x + 1)

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)

    border = round(rb / sqrt(1 + sqr_ra / sqr_rb))

    x = ra
    y = 0

    if draw:
        draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)

    delta = sqr_ra - round(sqr_rb * (x - 1 / 4))
    while y < border:
        if delta > 0:
            x -= 1
            delta -= 2 * sqr_rb * x

        y += 1
        delta += sqr_ra * (y + y + 1)

        if draw:
            draw_pixels(canvas, [x + xc, y + yc, color], xc, yc, circle=False)


def parameter_circle(xc, yc, r, color, canvas, draw):
    step = 1 / r

    i = 0
    while i <= pi / 4 + step:
        x = xc + round(r * cos(i))
        y = yc + round(r * sin(i))

        if draw:
            draw_pixels(canvas, [x, y, color], xc, yc, circle=True)
        i += step


def parameter_ellipse(xc, yc, ra, rb, color, canvas, draw):
    if ra > rb:
        step = 1 / ra
    else:
        step = 1 / rb

    i = 0
    while i <= pi / 2 + step:
        x = xc + round(ra * cos(i))
        y = yc + round(rb * sin(i))

        if draw:
            draw_pixels(canvas, [x, y, color], xc, yc, circle=False)

        i += step