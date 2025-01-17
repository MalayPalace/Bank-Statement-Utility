import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk

class TableView:
    def __init__(self, root):
        self.root = root
        self.root.title("Table View with Sort and Filter")

        # Sample data for the table
        self.data = [
            {"Name": "Alice", "Age": 25, "Job": "Engineer"},
            {"Name": "Bob", "Age": 30, "Job": "Doctor"},
            {"Name": "Charlie", "Age": 22, "Job": "Artist"},
            {"Name": "David", "Age": 28, "Job": "Teacher"},
            {"Name": "Eva", "Age": 26, "Job": "Nurse"}
        ]

        self.sort_directions = {"Name": None, "Age": None, "Job": None}  # Keeps track of sort direction

        # Filter Entry
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", self.update_table)
        filter_label = tk.Label(root, text="Filter:")
        filter_label.pack(side=tk.LEFT, padx=10)
        filter_entry = tk.Entry(root, textvariable=self.filter_var)
        filter_entry.pack(side=tk.LEFT)

        # Create a Frame for the Treeview with border
        tree_frame = tk.Frame(root, bd=2, relief=tk.SOLID)  # Add border and style
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create the Treeview widget inside the Frame
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Age", "Job"), show="headings")
        self.tree.heading("Name", text="Name", command=lambda: self.sort_column("Name"))
        self.tree.heading("Age", text="Age", command=lambda: self.sort_column("Age"))
        self.tree.heading("Job", text="Job", command=lambda: self.sort_column("Job"))
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Create tags for alternating row colors (simulating borders)
        self.tree.tag_configure('evenrow', background='lightgray')
        self.tree.tag_configure('oddrow', background='white')

        # Initial table population
        self.update_table()

    def update_table(self, *args):
        # Clear existing table entries
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Filter the data based on the filter entry
        filtered_data = [item for item in self.data if self.filter_var.get().lower() in str(item).lower()]

        # Insert filtered data into the table with alternating row colors
        for i, item in enumerate(filtered_data):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(item["Name"], item["Age"], item["Job"]), tags=(tag,))

    def sort_column(self, col):
        # Determine current sort direction and toggle it
        direction = self.sort_directions[col]
        if direction is None or direction == "asc":
            reverse = False
            self.sort_directions[col] = "desc"
        else:
            reverse = True
            self.sort_directions[col] = "asc"

        # Sort the data by column
        self.data = sorted(self.data, key=lambda x: x[col], reverse=reverse)
        self.update_table()

        # Update the headers with appropriate sorting icons
        self.update_sort_icons()

    def update_sort_icons(self):
        # Define up and down arrows
        up_arrow = " ↑"
        down_arrow = " ↓"

        # Reset all headers to their default text
        self.tree.heading("Name", text="Name", command=lambda: self.sort_column("Name"))
        self.tree.heading("Age", text="Age", command=lambda: self.sort_column("Age"))
        self.tree.heading("Job", text="Job", command=lambda: self.sort_column("Job"))

        # Update the header with the sorting icon based on the sort direction
        for col in self.sort_directions:
            if self.sort_directions[col] == "asc":
                self.tree.heading(col, text=col + down_arrow, command=lambda c=col: self.sort_column(c))
            elif self.sort_directions[col] == "desc":
                self.tree.heading(col, text=col + up_arrow, command=lambda c=col: self.sort_column(c))

# Create the main window
root = tk.Tk()
app = TableView(root)
root.mainloop()