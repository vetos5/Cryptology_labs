from tkinter import filedialog
import pandas as pd


def load_text_file(file_path):
    """Load text from a file."""
    with open(file_path, "r", encoding='utf-8') as file:
        return file.read()


def load_csv(self):
    """Load CSV data into the Treeview."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)

            self.treeview.delete(*self.treeview.get_children())

            for index, row in df.iterrows():
                self.treeview.insert("", "end",
                                     values=(row["Character"], row["Count"], f"{row['Frequency'] * 100:.2f}%"))

        except Exception as e:
            print(f"Error loading CSV file: {e}")


def save_data(treeview):
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        rows = []
        for row in treeview.get_children():
            rows.append(treeview.item(row)["values"])
        df = pd.DataFrame(rows, columns=["Character", "Count", "Frequency"])
        df.to_csv(file_path, index=False)
