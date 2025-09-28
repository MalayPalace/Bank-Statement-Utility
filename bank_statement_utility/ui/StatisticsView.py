import tkinter as tk

import ttkbootstrap as ttk

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
        ttk.Label(self, text="Bank Name", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="e")
        ttk.Label(self, text="Type", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, pady=8, sticky="e")
        ttk.Label(self, text="From", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=8)
        ttk.Label(self, text="To", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=10, pady=8, sticky="e")
        ttk.Label(self, text="Balance", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=10, pady=8, sticky="e")

        self.latest_labels = {}
        self.oldest_labels = {}

        self.__get_data_and_populate()

        # Add legend at the bottom
        legend_text = "*For Credit-Card. Balance will show Outstanding Amount."
        legend_label = ttk.Label(self, text=legend_text, wraplength=400, font=("Arial", 9, "italic"))
        legend_label.grid(row=1000, column=0, columnspan=5, padx=10, pady=16, sticky="w")

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

            ttk.Label(self, text=bank_name).grid(row=i, column=0, padx=10, pady=6, sticky="e")
            ttk.Label(self, text=source).grid(row=i, column=1, padx=10, pady=6, sticky="e")
            ttk.Label(self, text=oldest_date).grid(row=i, column=2, padx=10, pady=6, sticky="e")
            ttk.Label(self, text=latest_date, background=bg).grid(row=i, column=3, padx=10, pady=6, sticky="e")

            balance_btn = ttk.Button(self, text="Show Balance")
            balance_btn.grid(row=i, column=4, padx=10, pady=6, sticky="e")

            def make_show_balance_callback(row=i, bank=bank_name, src=source, btn=balance_btn):
                def callback():
                    btn.grid_remove()
                    balance = self.__fetch_balance(bank, src)
                    ttk.Label(self, text=balance).grid(row=row, column=4, padx=10, pady=6, sticky="e")

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
