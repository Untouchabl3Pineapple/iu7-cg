from tkinter import *


def window_settings(window, title):
    window.grab_set()
    window.attributes("-topmost", True)
    window.geometry("400x200+500+300")
    window.title(title)
    window.configure(background="rosy brown")
    window.resizable(False, False)
