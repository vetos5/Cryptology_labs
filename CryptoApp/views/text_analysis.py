import customtkinter as ctk
from tkinter import filedialog, ttk
import pandas as pd
from utils.file_operations import load_text_file, save_data
from utils.analysis import analyze_text
from utils.themes import apply_dark_treeview


class TextAnalysisView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", pady=10)

        self.load_text_button = ctk.CTkButton(self.input_frame, text="Load Text File", command=self.load_text)
        self.load_text_button.pack(side="left", padx=5)

        self.load_csv_button = ctk.CTkButton(self.input_frame, text="Load CSV", command=self.load_csv)
        self.load_csv_button.pack(side="left", padx=5)

        self.analyze_button = ctk.CTkButton(
            self.input_frame,
            text="Analyze",
            command=self.analyze_text,
            fg_color="#2ecc71",
        )
        self.analyze_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(self.input_frame, text="Save Data", command=self.save_data)
        self.save_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(
            self.input_frame,
            text="Clear",
            command=self.clear_text,
            fg_color="#e74c3c",  # Red color
        )
        self.clear_button.pack(side="left", padx=5)

        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.text_label = ctk.CTkLabel(self.text_frame, text="Input Text:")
        self.text_label.pack(anchor="nw", padx=5, pady=5)

        self.text_box = ctk.CTkTextbox(self.text_frame, wrap="word", height=150)
        self.text_box.pack(fill="both", expand=True)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        self.table_label = ctk.CTkLabel(self.table_frame, text="Character Frequency Table:")
        self.table_label.pack(anchor="nw", padx=5, pady=5)

        self.treeview_frame = ctk.CTkFrame(self.table_frame)
        self.treeview_frame.pack(fill="both", expand=True)

        self.treeview = ttk.Treeview(self.treeview_frame, columns=("Character", "Count", "Frequency"), show="headings")
        self.treeview.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.treeview_frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.treeview.configure(yscrollcommand=self.scrollbar.set)

        self.treeview.heading("Character", text="Character")
        self.treeview.heading("Count", text="Count")
        self.treeview.heading("Frequency", text="Frequency")

        apply_dark_treeview(self.treeview)

    def load_text(self):
        """Load text from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            content = load_text_file(file_path)
            self.text_box.delete("1.0", "end")
            self.text_box.insert("1.0", content)

    def load_csv(self):
        """Load CSV data into the Treeview."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                df = pd.read_csv(file_path)

                df['Frequency'] = pd.to_numeric(df['Frequency'], errors='coerce')

                self.treeview.delete(*self.treeview.get_children())

                for index, row in df.iterrows():
                    frequency_value = row['Frequency'] * 100 if pd.notna(row['Frequency']) else 0
                    self.treeview.insert("", "end", values=(row["Character"], row["Count"], f"{frequency_value:.2f}%"))

            except Exception as e:
                print(f"Error loading CSV file: {e}")

    def analyze_text(self):
        """Analyze the text in the text box."""
        content = self.text_box.get("1.0", "end").strip()
        analyze_text(content, self.treeview)

    def save_data(self):
        """Save the analyzed data to a CSV file."""
        save_data(self.treeview)

    def clear_text(self):
        """Clear the text box and the Treeview."""
        self.text_box.delete("1.0", "end")
        self.treeview.delete(*self.treeview.get_children())
