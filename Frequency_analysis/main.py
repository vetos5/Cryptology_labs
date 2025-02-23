import customtkinter as ctk
from tkinter import filedialog, ttk
import pandas as pd
from collections import Counter


class FrequencyTableApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Frequency Table App")
        self.geometry("800x600")

        self.menu_frame = ctk.CTkFrame(self, height=40)
        self.menu_frame.pack(fill="x", side="top")

        self.hamburger_button = ctk.CTkButton(self.menu_frame, text="☰", width=40, command=self.toggle_menu)
        self.hamburger_button.pack(side="left", padx=10)

        self.side_menu = ctk.CTkFrame(self.menu_frame, height=40, fg_color="#2e2e2e")

        self.text_analysis_button = ctk.CTkButton(self.side_menu, text="Text Analysis", width=100, command=self.switch_to_text_analysis)
        self.text_analysis_button.pack(side="left", padx=10)

        self.other_program_button = ctk.CTkButton(self.side_menu, text="Other Program", width=100, command=self.switch_to_other_program)
        self.other_program_button.pack(side="left", padx=10)

        self.about_button = ctk.CTkButton(self.side_menu, text="About", width=100, command=self.show_about)
        self.about_button.pack(side="left", padx=10)

        self.side_menu.pack_forget()

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.input_frame = ctk.CTkFrame(self.content_frame)
        self.input_frame.pack(fill="x", pady=10)

        self.input_label = ctk.CTkLabel(self.input_frame, text="Text Analysis:", anchor="w")
        self.input_label.pack(side="left", padx=5)

        self.input_entry = ctk.CTkEntry(self.input_frame, width=300, placeholder_text="Enter file path or text...")
        self.input_entry.pack(side="left", padx=5)

        self.load_text_button = ctk.CTkButton(self.input_frame, text="Load Text File", command=self.load_text_file)
        self.load_text_button.pack(side="left", padx=5)

        self.analyze_button = ctk.CTkButton(self.input_frame, text="Analyze", command=self.analyze_text)
        self.analyze_button.pack(side="left", padx=5)

        self.text_frame = ctk.CTkFrame(self.content_frame)
        self.text_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)

        self.text_box = ctk.CTkTextbox(self.text_frame, wrap="word")
        self.text_box.pack(fill="both", expand=True)

        self.placeholder_text = "Text will appear here..."
        self.show_placeholder()

        self.text_box.bind("<KeyPress>", self.clear_placeholder)
        self.text_box.bind("<Button-1>", self.clear_placeholder)
        self.text_box.bind("<FocusIn>", self.clear_placeholder)
        self.text_box.bind("<FocusOut>", self.show_placeholder)

        self.table_frame = ctk.CTkFrame(self.content_frame)
        self.table_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        self.treeview = ttk.Treeview(self.table_frame, columns=("Character", "Count", "Frequency"), show="headings")
        self.treeview.pack(fill="both", expand=True)

        self.treeview.heading("Character", text="Character")
        self.treeview.heading("Count", text="Count")
        self.treeview.heading("Frequency", text="Frequency")

        self.apply_dark_treeview()

        self.data = None

        self.about_label = ctk.CTkLabel(self.content_frame, text="Frequency Table App\n\n"
                                                                "Version: 1.032\n\n"
                                                                "Created by: Vitalii Kovtun\n\n"
                                                                "This app analyzes the frequency of characters in text files.",
                                       font=("Arial", 14), anchor="center")
        self.about_label.pack(padx=20, pady=20)

        self.close_about_button = ctk.CTkButton(self.content_frame, text="Back to App", command=self.switch_to_text_analysis)
        self.close_about_button.pack(pady=10)

        self.switch_to_text_analysis()

    def apply_dark_treeview(self):
        style = ttk.Style(self)
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

        self.treeview.tag_configure("evenrow", background="#2e2e2e", foreground="white")
        self.treeview.tag_configure("oddrow", background="#1e1e1e", foreground="white")

        self.treeview.column("Character", width=150, anchor="center", minwidth=150)
        self.treeview.column("Count", width=100, anchor="center", minwidth=100)
        self.treeview.column("Frequency", width=150, anchor="center", minwidth=150)

    def show_placeholder(self, event=None):
        if not self.text_box.get("1.0", "end-1c").strip():
            self.text_box.insert("1.0", self.placeholder_text)

    def clear_placeholder(self, event=None):
        if self.text_box.get("1.0", "end-1c").strip() == self.placeholder_text:
            self.text_box.delete("1.0", "end")

    def toggle_menu(self):
        if self.side_menu.winfo_ismapped():
            self.side_menu.pack_forget()
        else:
            self.side_menu.pack(side="left", fill="x", padx=10, anchor="nw")

    def switch_to_text_analysis(self):
        self.about_label.pack_forget()
        self.close_about_button.pack_forget()

        self.input_frame.pack(fill="x", pady=10)
        self.text_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        self.table_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

    def switch_to_other_program(self):
        self.input_label.config(text="Other Program:")
        self.text_box.delete("1.0", "end")
        self.about_frame.pack_forget()

    def show_about(self):
        self.input_frame.pack_forget()
        self.text_frame.pack_forget()
        self.table_frame.pack_forget()

        self.about_label.pack(padx=20, pady=20)
        self.close_about_button.pack(pady=10)

    def load_text_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_box.delete("1.0", "end")
                    self.text_box.insert("1.0", content)
            except Exception as e:
                pass

    def analyze_text(self):
        content = self.text_box.get("1.0", "end").strip()
        if not content:
            return

        content = ''.join(c.lower() for c in content if c.isalpha())

        char_counts = Counter(content)
        total_chars = sum(char_counts.values())

        frequency_data = pd.DataFrame(
            [(char, count, count / total_chars) for char, count in char_counts.items()],
            columns=["Character", "Count", "Frequency"]
        )

        frequency_data.sort_values(by="Frequency", ascending=False, inplace=True)

        self.treeview.delete(*self.treeview.get_children())

        for index, row in frequency_data.iterrows():
            if index % 2 == 0:
                tag = "evenrow"
            else:
                tag = "oddrow"
            self.treeview.insert("", "end", values=(row["Character"], row["Count"], f"{row['Frequency'] * 100:.2f}%"),
                                 tags=(tag,))

        self.data = frequency_data

    def save_data(self):
        if self.data is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                try:
                    self.data.to_csv(file_path, index=False)
                except Exception as e:
                    pass
        else:
            pass


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = FrequencyTableApp()
    app.mainloop()
