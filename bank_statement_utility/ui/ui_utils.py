import os
import tkinter
from tkinter import messagebox, Text


def show_alert(alert_title: str, alert_message: str):
    messagebox.showinfo(alert_title, alert_message)


def append_to_text_ln(text_field: Text, text_message: str):
    if text_field:
        text_field.insert(tkinter.END, text_message + os.linesep)
