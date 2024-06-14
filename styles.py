import tkinter as tk

# Основные стили для всех элементов
default_font = ("Helvetica", 12)
title_font = ("Helvetica", 18, "bold")
button_font = ("Helvetica", 12, "bold")

style = {
    "TLabel": {
        "font": default_font,
        "background": "#ffffff",
        "foreground": "#333333",
        "padx": 10,
        "pady": 10
    },
    "TitleLabel": {
        "font": title_font,
        "background": "#4CAF50",
        "foreground": "#ffffff",
        "padx": 20,
        "pady": 20,
        "relief": "flat"
    },
    "TButton": {
        "font": button_font,
        "background": "#4CAF50",
        "foreground": "#ffffff",
        "activebackground": "#45a049",
        "borderwidth": 0,
        "relief": "flat",
        "padx": 10,
        "pady": 10,
        "width": 20
    },
    "TEntry": {
        "font": default_font,
        "background": "#ffffff",
        "foreground": "#333333",
        "borderwidth": 1,
        "relief": "solid",
        "width": 25
    },
    "TFrame": {
        "background": "#ffffff",
    },
    "MainFrame": {
        "background": "#f0f0f0",
        "padx": 20,
        "pady": 20
    }
}
