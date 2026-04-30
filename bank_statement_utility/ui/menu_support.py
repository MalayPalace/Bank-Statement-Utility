import sys
import tkinter as tk
from inspect import getsourcefile
from os.path import dirname

import ttkbootstrap as ttk
from PIL import Image, ImageTk

from bank_statement_utility.ui.manual_entry_page import AddManualEntryPage
from bank_statement_utility.version import __version__


class AboutPage(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
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


class GuidePage(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title("Guide - Supported Bank Formats")
        self.geometry("900x400+200+200")

        # Title Label
        title_label = ttk.Label(self, text="Supported Bank Statement Formats", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Instructions Label
        instruction_label = ttk.Label(
            self,
            text="Below are the format information that the utility supports for various banks. Download statement as prescribed format below:",
            wraplength=950
        )
        instruction_label.pack(pady=5, padx=10)

        # Create a frame to hold the notebook
        notebook_frame = ttk.Frame(self)
        notebook_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create notebook for tabs
        notebook = ttk.Notebook(notebook_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Saving/Current Account Tab
        saving_account_frame = ttk.Frame(notebook)
        notebook.add(saving_account_frame, text="Saving/Current Account")
        self._create_saving_account_table(saving_account_frame)

        # Credit Card Tab
        credit_card_frame = ttk.Frame(notebook)
        notebook.add(credit_card_frame, text="Credit Card")
        self._create_credit_card_table(credit_card_frame)

    def _create_saving_account_table(self, parent):
        """Create table for Saving/Current Account format information"""
        # Saving/Current Account Details
        data = [
            ("HDFC Bank", "Saving/Current Account", "txt", "Download as Delimited (through Netbanking)"),
            ("Kotak Bank", "Saving/Current Account", "csv", "Download as CSV (Check Debit/Credit check box)"),
            ("SBI Bank", "Saving/Current Account", "xls", "Download in MS Excel format"),
            ("Bank of Baroda*", "Saving/Current Account", "xls", "Download in XLS format (Mini Statement)"),
            ("IDBI Bank", "Saving/Current Account", "xls", "Download in XLS format"),
            ("SVC Bank", "Saving/Current Account", "xls", "Download in XLS format"),
        ]

        # Define columns
        columns = ("Bank Name", "Account Type", "File Format", "Download Type")

        # Create Treeview
        tree = ttk.Treeview(parent, columns=columns, height=15, show="headings")

        # Define column headings and widths
        tree.column("Bank Name", width=150, anchor=tk.W)
        tree.column("Account Type", width=150, anchor=tk.W)
        tree.column("File Format", width=100, anchor=tk.W)
        tree.column("Download Type", width=550, anchor=tk.W)

        tree.heading("Bank Name", text="Bank Name")
        tree.heading("Account Type", text="Account Type")
        tree.heading("File Format", text="File Format")
        tree.heading("Download Type", text="Download Type")

        for item in data:
            tree.insert("", "end", values=item)

        # Add scrollbars
        vsb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Add note
        note_label = ttk.Label(
            parent,
            text="* Have observed that Bank of Baroda changes the column format quite frequently, so might have to change config settings.",
            font=("Arial", 9, "italic")
        )
        note_label.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="w")

    def _create_credit_card_table(self, parent):
        """Create table for Credit Card format information"""
        # Credit Card Account Details
        data = [
            ("Kotak Bank", "Credit Card", "pdf", "Statement received through Email"),
            ("SBI Bank", "Credit Card", "pdf", "Statement received through Email"),
            ("Yes Bank", "Credit Card", "pdf", "Statement received through Email"),
            ("HDFC Bank", "Credit Card", "pdf", "Statement received through Email"),
        ]

        # Define columns
        columns = ("Bank Name", "Account Type", "File Format", "Download Type")

        # Create Treeview
        tree = ttk.Treeview(parent, columns=columns, height=15, show="headings")

        # Define column headings and widths
        tree.column("Bank Name", width=150, anchor=tk.W)
        tree.column("Account Type", width=150, anchor=tk.W)
        tree.column("File Format", width=100, anchor=tk.W)
        tree.column("Download Type", width=550, anchor=tk.W)

        tree.heading("Bank Name", text="Bank Name")
        tree.heading("Account Type", text="Account Type")
        tree.heading("File Format", text="File Format")
        tree.heading("Download Type", text="Download Type")

        for item in data:
            tree.insert("", "end", values=item)

        # Add scrollbars
        vsb = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=tree.yview)
        hsb = ttk.Scrollbar(parent, orient=tk.HORIZONTAL, command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        # Add note
        note_label = ttk.Label(
            parent,
            text="* Limitation: Credit Card Statement can have duplicate scenario where transaction can be of same amount on same date with same description and since it doesn't has closing balance, while storing to DB it will be overwritten due to non-uniqueness. Will have to handle such scenario manually.",
            font=("Arial", 9, "italic"),
            wraplength=900
        )
        note_label.grid(row=2, column=0, columnspan=2, pady=10, padx=5, sticky="w")


def quit_app():
    # print('menu_support.quit')
    sys.stdout.flush()
    sys.exit()


def about(root):
    AboutPage(root)


def guide(root):
    GuidePage(root)


def add_manual_entry(root):
    AddManualEntryPage(root)
