import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap import LIGHT, SUCCESS

from .ui_utils import show_alert
from ..logger import log
from ..services.CassandraRepositoryHelper import CassandraRepositoryHelper


class StatisticsView(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Statistics")
        # self.geometry("430x320+285+375")
        self.resizable(True, True)
        self.minsize(200, 200)

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

        # Header
        ttk.Label(self, text="Bank Name", font=("Arial", 10, "bold"), justify="center").grid(row=0, column=0, padx=10,
                                                                                             pady=8, sticky="e")
        ttk.Label(self, text="Type", font=("Arial", 10, "bold"), justify="center").grid(row=0, column=1, padx=10,
                                                                                        pady=8, sticky="e")
        ttk.Label(self, text="From", font=("Arial", 10, "bold"), justify="center").grid(row=0, column=2, padx=10,
                                                                                        pady=8)
        ttk.Label(self, text="To", font=("Arial", 10, "bold"), justify="center").grid(row=0, column=3, padx=10, pady=8,
                                                                                      sticky="e")
        ttk.Label(self, text="Balance", font=("Arial", 10, "bold"), justify="center").grid(row=0, column=4, padx=10,
                                                                                           pady=8, sticky="e")

        self.latest_labels = {}
        self.oldest_labels = {}

        self.__get_data_and_populate()

        # Add legend at the bottom
        legend_text = "*For Credit-Card. Balance will show Outstanding Amount."
        legend_label = ttk.Label(self, text=legend_text, wraplength=400, font=("Arial", 9, "italic"))
        legend_label.grid(row=1000, column=0, columnspan=5, padx=10, pady=16, sticky="w")

    def format_currency_indian(self, amount):
        """Format a number into Indian currency format with commas (thousand, lakh, crore)
        and prefix with the Rupee symbol. Returns a string like "-₹ 1,23,45,678.90".
        Non-numeric inputs are returned as-is.
        """
        if amount is None:
            return "--"
        try:
            # Accept Decimal, float, int or numeric string
            from decimal import Decimal, InvalidOperation
            if isinstance(amount, Decimal):
                val = float(amount)
            else:
                val = float(amount)
        except Exception:
            return str(amount)

        negative = val < 0
        val = abs(val)
        whole = int(val)
        frac = int(round((val - whole) * 100))

        s = str(whole)
        if len(s) > 3:
            last3 = s[-3:]
            rest = s[:-3]
            parts = []
            # split rest in 2-digit groups from the right
            while len(rest) > 2:
                parts.insert(0, rest[-2:])
                rest = rest[:-2]
            if rest:
                parts.insert(0, rest)
            formatted_whole = ','.join(parts) + ',' + last3
        else:
            formatted_whole = s

        sign = '-' if negative else ''
        # place negative sign before the rupee symbol for readability
        if sign:
            return f"-{chr(8377)} {formatted_whole}.{frac:02d}"
        else:
            return f"{chr(8377)} {formatted_whole}.{frac:02d}"

    def __get_data_and_populate(self):
        result = self.cass_service.get_min_max_date_by_bank_source_ordered()

        from datetime import date

        for i, record in enumerate(result, start=1):
            bank_name = record['bank_name']
            source = record['source']
            latest_date_obj = record['max_date'].date() if record['max_date'] else None
            oldest_date = record['min_date'].date().strftime('%d-%m-%Y') if record['min_date'] else "--"

            if latest_date_obj:
                days_diff = (date.today() - latest_date_obj).days
                if days_diff <= 31:
                    bg = "pale green"
                elif days_diff <= 122:
                    bg = "orange"
                else:
                    bg = "red"
                latest_date = latest_date_obj.strftime('%d-%m-%Y')
            else:
                bg = "white"
                latest_date = "--"

            bank_entry = ttk.Entry(self, width=10, bootstyle=LIGHT, justify='center')
            bank_entry.insert(0, bank_name)
            bank_entry.config(state='readonly')
            bank_entry.grid(row=i, column=0, padx=10, pady=6, sticky="e")

            type_entry = ttk.Entry(self, width=10, bootstyle=LIGHT, justify='center')
            type_entry.insert(0, source)
            type_entry.config(state='readonly')
            type_entry.grid(row=i, column=1, padx=10, pady=6, sticky="e")

            oldest_entry = ttk.Entry(self, width=12, bootstyle=LIGHT, justify='center')
            oldest_entry.insert(0, oldest_date)
            oldest_entry.config(state='readonly')
            oldest_entry.grid(row=i, column=2, padx=10, pady=6, sticky="e")

            latest_entry = tk.Entry(self, width=12, justify='center')
            latest_entry.insert(0, latest_date)
            # apply the background color to readonly entries
            latest_entry.config(state='readonly')
            try:
                latest_entry.config(readonlybackground=bg)
            except Exception:
                # some themes may not support readonlybackground; ignore
                pass
            latest_entry.grid(row=i, column=3, padx=10, pady=6, sticky="e")

            balance_btn = ttk.Button(self, text="Show Balance")
            balance_btn.grid(row=i, column=4, padx=10, pady=6, sticky="e")

            def make_show_balance_callback(row=i, bank=bank_name, src=source, btn=balance_btn):
                def callback():
                    btn.grid_remove()
                    balance = self.__fetch_balance(bank, src)
                    formatted = self.format_currency_indian(balance)
                    bal_entry = ttk.Entry(self, width=12, justify='right')
                    bal_entry.insert(0, formatted)
                    bal_entry.config(state='readonly')
                    bal_entry.grid(row=row, column=4, padx=10, pady=6, sticky="e")

                return callback

            balance_btn.config(command=make_show_balance_callback())

    def __fetch_balance(self, bank_name, source):
        try:
            if source == "Creditcard":
                log.info("Fetching outstanding balance for Bank:{bank} Source:{source}".format(bank=bank_name,
                                                                                               source=source))
                return self.cass_service.get_outstanding_balance(bank_name, source)
            else:
                log.info(
                    "Fetching latest balance for Bank:{bank} Source:{source}".format(bank=bank_name, source=source))
                return self.cass_service.get_latest_balance(bank_name, source)
        except Exception as err:
            log.error("Error fetching latest balance for Bank:{bank} Source:{source} Error:{error}".format(
                bank=bank_name, source=source, error=err.__str__()), exc_info=True)
            show_alert("Error", "Error Occured while fetching balance. Check logs for more details.")
            return 0
