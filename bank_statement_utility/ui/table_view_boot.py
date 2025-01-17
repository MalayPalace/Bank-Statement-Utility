import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.constants import *

app = ttk.Window()
colors = app.style.colors

coldata = [
    {"text": "LicenseNumber", "stretch": True},
    "CompanyName",
    {"text": "UserCount", "stretch": True},
]

rowdata = [
    ('A123', 'IzzyCo', 12),
    ('A136', 'Kimdee Inc.', 45),
    ('A158', 'Farmadding Co.', 36)
]

dt = Tableview(
    master=app,
    coldata=coldata,
    rowdata=rowdata,
    paginated=True,
    searchable=True,
    bootstyle=PRIMARY,
    # autofit=True,
    # autoalign=False,
    stripecolor=(colors.light, None),
)
# dt.pack(fill=BOTH, expand=True, padx=10, pady=10)
dt.pack(fill=BOTH, expand=True)

app.mainloop()