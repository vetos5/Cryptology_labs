import tkinter.ttk as ttk


def apply_dark_treeview(treeview):
    """Apply dark theme settings to the Treeview widget."""
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#1e1e1e",
                    fieldbackground="#1e1e1e",
                    foreground="white",
                    font=("Arial", 10, "bold"),
                    rowheight=30,
                    borderwidth=0)
    style.map("Treeview", background=[("selected", "#2e2e2e")])

    style.configure("Treeview.Heading",
                    font=("Arial", 12, "bold"),
                    foreground="white",
                    background="#1e1e1e",
                    borderwidth=0)

    treeview.tag_configure("evenrow", background="#2e2e2e", foreground="white")
    treeview.tag_configure("oddrow", background="#1e1e1e", foreground="white")

    treeview.column("Character", width=150, anchor="center", minwidth=150)
    treeview.column("Count", width=100, anchor="center", minwidth=100)
    treeview.column("Frequency", width=150, anchor="center", minwidth=150)