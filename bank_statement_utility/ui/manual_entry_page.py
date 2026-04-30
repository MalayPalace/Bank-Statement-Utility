import tkinter as tk
from datetime import datetime
from tkinter import messagebox

import ttkbootstrap as ttk

from bank_statement_utility.Constants import BANK_NAMES, ACCOUNT_TYPE
from bank_statement_utility.logger import log
from bank_statement_utility.model.StatementDB import StatementDB
from bank_statement_utility.services.CassandraRepositoryHelper import CassandraRepositoryHelper
from bank_statement_utility.ui.ui_utils import show_alert


class AddManualEntryPage(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title("Add Manual Entry")
        self.geometry("600x550+400+200")
        self.resizable(False, False)

        try:
            self.cass_service = CassandraRepositoryHelper()
        except IOError as ex:
            show_alert("Connection Error", str(ex))
            self.destroy()
            return
        except Exception as err:
            log.error("Unknown error occur. Error:{error}".format(error=err.__str__()),
                      exc_info=True)
            show_alert("Error", "Unknown Error. Check logs for more details.")
            self.destroy()
            return

        # Variables to store form data
        self.bank_name_var = tk.StringVar()
        self.account_type_var = tk.StringVar()
        self.transaction_type_var = tk.StringVar()
        self.amount_var = tk.StringVar()
        self.closing_balance_var = tk.StringVar()

        # Create main frame with padding
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        title_label = ttk.Label(main_frame, text="Add Manual Entry", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Row 1: Bank Name
        ttk.Label(main_frame, text="Bank Name *").grid(row=1, column=0, sticky="w", pady=5)
        self.bank_combobox = ttk.Combobox(main_frame, textvariable=self.bank_name_var, state="readonly", width=30)
        self.bank_combobox['values'] = BANK_NAMES
        self.bank_combobox.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))

        # Row 2: Account Type
        ttk.Label(main_frame, text="Account Type *").grid(row=2, column=0, sticky="w", pady=5)
        account_type_frame = ttk.Frame(main_frame)
        account_type_frame.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        for i, account_type in enumerate(ACCOUNT_TYPE):
            ttk.Radiobutton(account_type_frame, text=account_type, variable=self.account_type_var,
                            value=account_type).pack(side="left", padx=5)

        # Row 3: Date
        ttk.Label(main_frame, text="Transaction Date *").grid(row=3, column=0, sticky="w", pady=5)
        date_frame = ttk.Frame(main_frame)
        date_frame.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d-%m-%Y"))
        self.date_entry = ttk.Entry(date_frame, textvariable=self.date_var, width=27)
        self.date_entry.pack(side="left", padx=(0, 5))
        ttk.Button(date_frame, text="📅", width=3, command=self._open_date_picker).pack(side="left")

        # Row 4: Transaction Type
        ttk.Label(main_frame, text="Transaction Type *").grid(row=4, column=0, sticky="w", pady=5)
        transaction_type_frame = ttk.Frame(main_frame)
        transaction_type_frame.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        ttk.Radiobutton(transaction_type_frame, text="Debit", variable=self.transaction_type_var,
                        value="Debit").pack(side="left", padx=5)
        ttk.Radiobutton(transaction_type_frame, text="Credit", variable=self.transaction_type_var,
                        value="Credit").pack(side="left", padx=5)

        # Row 5: Amount
        ttk.Label(main_frame, text="Amount *").grid(row=5, column=0, sticky="w", pady=5)
        self.amount_entry = ttk.Entry(main_frame, textvariable=self.amount_var, width=30)
        self.amount_entry.grid(row=5, column=1, sticky="ew", pady=5, padx=(10, 0))
        amount_hint = ttk.Label(main_frame, text="e.g., 1000.50 (2 decimal places)", font=("Arial", 8, "italic"),
                                foreground="gray")
        amount_hint.grid(row=5, column=1, sticky="e", pady=(25, 5), padx=(10, 0))

        # Row 6: Description
        ttk.Label(main_frame, text="Description").grid(row=6, column=0, sticky="nw", pady=5)
        self.description_entry = tk.Text(main_frame, height=3, width=30, wrap=tk.WORD)
        self.description_entry.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        self.description_entry.bind('<KeyRelease>', self._on_description_change)
        self.desc_char_label = ttk.Label(main_frame, text="0/250 characters", font=("Arial", 8, "italic"),
                                         foreground="gray")
        self.desc_char_label.grid(row=6, column=1, sticky="e", pady=(70, 5), padx=(10, 0))

        # Row 7: Cheque No
        ttk.Label(main_frame, text="Cheque No").grid(row=7, column=0, sticky="w", pady=5)
        self.cheque_entry = ttk.Entry(main_frame, width=30)
        self.cheque_entry.grid(row=7, column=1, sticky="ew", pady=5, padx=(10, 0))
        self.cheque_entry.bind('<KeyRelease>', self._on_cheque_change)
        self.cheque_char_label = ttk.Label(main_frame, text="0/50 characters", font=("Arial", 8, "italic"),
                                           foreground="gray")
        self.cheque_char_label.grid(row=7, column=1, sticky="e", pady=(25, 5), padx=(10, 0))

        # Row 8: Closing Balance
        ttk.Label(main_frame, text="Closing Balance").grid(row=8, column=0, sticky="w", pady=5)
        self.closing_balance_entry = ttk.Entry(main_frame, textvariable=self.closing_balance_var, width=30)
        self.closing_balance_entry.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        closing_balance_hint = ttk.Label(main_frame, text="e.g., 5000.00 (2 decimal places)",
                                         font=("Arial", 8, "italic"),
                                         foreground="gray")
        closing_balance_hint.grid(row=8, column=1, sticky="e", pady=(25, 5), padx=(10, 0))

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=(30, 0))

        ttk.Button(button_frame, text="Save", command=self._on_save).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", command=self._on_clear).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).pack(side="left", padx=5)

        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)

    def _open_date_picker(self):
        """Open a simple date picker dialog"""
        date_picker_window = tk.Toplevel(self)
        date_picker_window.transient(self)
        date_picker_window.grab_set()
        date_picker_window.title("Select Date")
        date_picker_window.geometry("300x200+400+300")
        date_picker_window.resizable(False, False)

        # Parse current date
        try:
            current_date = datetime.strptime(self.date_var.get(), "%d-%m-%Y")
        except ValueError:
            current_date = datetime.now()

        # Variables for date picker
        year_var = tk.StringVar(value=str(current_date.year))
        month_var = tk.StringVar(value=str(current_date.month))
        day_var = tk.StringVar(value=str(current_date.day))

        # Frame for date picker
        picker_frame = ttk.Frame(date_picker_window, padding="20")
        picker_frame.pack(fill=tk.BOTH, expand=True)

        # Year
        ttk.Label(picker_frame, text="Year:").grid(row=0, column=0, sticky="w", pady=5)
        year_spinbox = ttk.Spinbox(picker_frame, from_=2000, to=2100, textvariable=year_var, width=10)
        year_spinbox.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        # Month
        ttk.Label(picker_frame, text="Month:").grid(row=1, column=0, sticky="w", pady=5)
        month_spinbox = ttk.Spinbox(picker_frame, from_=1, to=12, textvariable=month_var, width=10)
        month_spinbox.grid(row=1, column=1, sticky="ew", pady=5, padx=5)

        # Day
        ttk.Label(picker_frame, text="Day:").grid(row=2, column=0, sticky="w", pady=5)
        day_spinbox = ttk.Spinbox(picker_frame, from_=1, to=31, textvariable=day_var, width=10)
        day_spinbox.grid(row=2, column=1, sticky="ew", pady=5, padx=5)

        def confirm_date():
            try:
                year = int(year_var.get())
                month = int(month_var.get())
                day = int(day_var.get())
                selected_date = datetime(year, month, day)
                self.date_var.set(selected_date.strftime("%d-%m-%Y"))
                date_picker_window.destroy()
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date", parent=date_picker_window)

        # Button frame
        button_frame = ttk.Frame(picker_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(button_frame, text="OK", command=confirm_date).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel", command=date_picker_window.destroy).pack(side="left", padx=5)

        picker_frame.columnconfigure(1, weight=1)

    def _on_description_change(self, event=None):
        """Update character count for description field"""
        current_text = self.description_entry.get("1.0", tk.END).rstrip('\n')
        char_count = len(current_text)
        if char_count > 250:
            self.description_entry.delete("1.0", tk.END)
            self.description_entry.insert("1.0", current_text[:250])
            char_count = 250
        self.desc_char_label.config(text=f"{char_count}/250 characters")

    def _on_cheque_change(self, event=None):
        """Update character count for cheque field"""
        current_text = self.cheque_entry.get()
        char_count = len(current_text)
        if char_count > 50:
            self.cheque_entry.delete(0, tk.END)
            self.cheque_entry.insert(0, current_text[:50])
            char_count = 50
        self.cheque_char_label.config(text=f"{char_count}/50 characters")

    def _validate_form(self):
        """Validate all form fields"""
        # Bank Name validation
        if not self.bank_name_var.get():
            messagebox.showerror("Validation Error", "Please select a Bank Name")
            return False

        # Account Type validation
        if not self.account_type_var.get():
            messagebox.showerror("Validation Error", "Please select Account Type")
            return False

        # Transaction Type validation
        if not self.transaction_type_var.get():
            messagebox.showerror("Validation Error", "Please select Transaction Type")
            return False

        # Amount validation
        amount_text = self.amount_var.get().strip()
        if not amount_text:
            messagebox.showerror("Validation Error", "Please enter an Amount")
            return False

        try:
            amount = float(amount_text)
            # Check if it has exactly 2 decimal places
            if not self._is_valid_decimal(amount_text):
                messagebox.showerror("Validation Error",
                                     "Amount must have exactly 2 decimal places (e.g., 1000.50)")
                return False
        except ValueError:
            messagebox.showerror("Validation Error", "Amount must be a valid decimal number")
            return False

        # Closing Balance validation
        closing_balance_text = self.closing_balance_var.get().strip()
        if closing_balance_text:  # Optional field, but validate if provided
            try:
                closing_balance = float(closing_balance_text)
                # Check if it has exactly 2 decimal places
                if not self._is_valid_decimal(closing_balance_text):
                    messagebox.showerror("Validation Error",
                                         "Closing Balance must have exactly 2 decimal places (e.g., 5000.00)")
                    return False
            except ValueError:
                messagebox.showerror("Validation Error", "Closing Balance must be a valid decimal number")
                return False

        return True

    def _is_valid_decimal(self, value):
        """Check if value has exactly 2 decimal places"""
        try:
            # Remove leading/trailing spaces
            value = value.strip()
            # Split by decimal point
            if '.' not in value:
                return False
            parts = value.split('.')
            if len(parts) != 2:
                return False
            # Check if decimal part has exactly 2 digits
            return len(parts[1]) == 2 and parts[1].isdigit()
        except:
            return False

    def _on_save(self):
        """Handle Save button click"""
        if self._validate_form():
            trans_date = datetime.strptime(self.date_var.get(), '%d-%m-%Y')

            if self.transaction_type_var.get() == "Debit":
                debit_amount = round(float(self.amount_var.get()), 2)
                credit_amount = None
            else:
                credit_amount = round(float(self.amount_var.get()), 2)
                debit_amount = None

            # Get closing balance if provided
            closing_balance = None
            if self.closing_balance_var.get().strip():
                closing_balance = round(float(self.closing_balance_var.get()), 2)

            statement_model = StatementDB(
                self.bank_name_var.get(),
                self.account_type_var.get(),
                trans_date,
                self.description_entry.get("1.0", tk.END).rstrip('\n'),
                debit_amount,
                credit_amount,
                self.cheque_entry.get(),
                closing_balance,
                trans_date,
                None
            )

            # Show confirmation dialog
            confirmation_message = (
                    "Please confirm the details before saving:\n\n" +
                    f"Bank: {statement_model.bank_name}\n" +
                    f"Date: {statement_model.transaction_date}\n" +
                    f"Type: {self.transaction_type_var.get()}\n" +
                    f"Amount: {debit_amount if debit_amount else credit_amount}\n" +
                    f"Description: {statement_model.description}\n" +
                    f"Closing Balance: {statement_model.closing_balance}"
            )

            if messagebox.askyesno("Confirm Entry", confirmation_message):
                log.debug("Saving Record: {record}".format(record=statement_model))
                self.cass_service.insert_data(statement_model)
                show_alert("Success", "Entry saved successfully!")
                self.destroy()

    def _on_clear(self):
        """Handle Clear button click"""
        self.bank_name_var.set('')
        self.account_type_var.set('')
        self.transaction_type_var.set('')
        self.amount_var.set('')
        self.closing_balance_var.set('')
        self.description_entry.delete("1.0", tk.END)
        self.cheque_entry.delete(0, tk.END)
        self.date_var.set(datetime.now().strftime("%d-%m-%Y"))
        self.desc_char_label.config(text="0/250 characters")
        self.cheque_char_label.config(text="0/50 characters")
