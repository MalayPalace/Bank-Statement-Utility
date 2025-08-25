import sys
import tkinter as tk
from inspect import getsourcefile
from os.path import dirname

import ttkbootstrap as ttk
from PIL import Image, ImageTk
from bank_statement_utility.version import __version__


class AboutPage(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("About")
        self.geometry("450x260+628+344")

        # Load and display the application icon
        execution_path = dirname(getsourcefile(lambda: 0))
        icon_image = Image.open(execution_path[:len(execution_path) - 3] + "/icon.png")
        icon_image = icon_image.resize((78, 78))
        self.icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label = ttk.Label(self, image=self.icon_photo)
        icon_label.pack(pady=5)

        # Display the application description
        description_label1 = ttk.Label(self, text="Bank-Statment-Utility developed out of my personal need to")
        description_label2 = ttk.Label(self, text="store (and process) bank statements to track expenses or to")
        description_label3 = ttk.Label(self, text=" just search specific refund/charge/expense etc across all")
        description_label4 = ttk.Label(self, text="bank (refer supported banks in main screen) I personally have")
        description_label5 = ttk.Label(self, text="accounts.")
        description_label1.pack(pady=2)
        description_label2.pack(pady=0)
        description_label3.pack(pady=0)
        description_label4.pack(pady=0)
        description_label5.pack(pady=0)

        # Display credits
        credits_label = ttk.Label(self, font="-size 8", text="Developed by: Malay Shah")
        credits_label.pack(pady=1)

        # version credits
        version_label = ttk.Label(self, font="-size 8", text="Version " + __version__)
        version_label.pack(pady=1)


def quit_app():
    # print('menu_support.quit')
    sys.stdout.flush()
    sys.exit()


def about(root):
    about_page = AboutPage(root)
