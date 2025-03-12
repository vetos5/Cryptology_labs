import customtkinter as ctk
from tkinter import filedialog
class CypherView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill="x", pady=10)

        self.load_table_button = ctk.CTkButton(
            self.button_frame, text="Load Table", command=self.load_table, corner_radius=8
        )
        self.load_table_button.pack(side="left", padx=5)

        self.decipher_button = ctk.CTkButton(
            self.button_frame, text="Decipher", command=self.decipher_text, corner_radius=8, fg_color="#2ecc71"
        )
        self.decipher_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(
            self.button_frame, text="Clear", command=self.clear_fields, corner_radius=8, fg_color="#e74c3c"
        )
        self.clear_button.pack(side="left", padx=5)

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.input_label = ctk.CTkLabel(self.input_frame, text="Input Text to Decipher:", font=("Arial", 14))
        self.input_label.pack(anchor="nw", padx=5, pady=5)

        self.input_text_box = ctk.CTkTextbox(self.input_frame, wrap="word", height=100, font=("Arial", 12))
        self.input_text_box.pack(fill="both", expand=True, padx=5)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.table_label = ctk.CTkLabel(self.table_frame, text="Cipher Table (e.g., A -> Q):", font=("Arial", 14))
        self.table_label.pack(anchor="nw", padx=5, pady=5)

        self.table_text_box = ctk.CTkTextbox(self.table_frame, wrap="word", height=100, font=("Arial", 12))
        self.table_text_box.pack(fill="both", expand=True, padx=5)

        self.output_frame = ctk.CTkFrame(self)
        self.output_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.output_label = ctk.CTkLabel(self.output_frame, text="Deciphered Output:", font=("Arial", 14))
        self.output_label.pack(anchor="nw", padx=5, pady=5)

        self.output_text_box = ctk.CTkTextbox(self.output_frame, wrap="word", height=100, font=("Arial", 12))
        self.output_text_box.pack(fill="both", expand=True, padx=5)

    def load_table(self):
        """Load a cipher table from a file."""
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    cipher_table = file.read()
                    self.table_text_box.delete("1.0", "end")
                    self.table_text_box.insert("1.0", cipher_table.strip())
            except Exception as e:
                self.output_text_box.delete("1.0", "end")
                self.output_text_box.insert("1.0", f"Error loading file: {e}")

    def decipher_text(self):
        """Decipher the text based on the substitution cipher table."""
        cipher_table = self.table_text_box.get("1.0", "end").strip()
        message = self.input_text_box.get("1.0", "end").strip()

        if not cipher_table or not message:
            self.output_text_box.delete("1.0", "end")
            self.output_text_box.insert("1.0", "Error: Provide a valid cipher table and message.")
            return

        cipher_map = {}
        try:
            for line in cipher_table.splitlines():
                plain, cipher = line.split("->")
                cipher_map[cipher.strip()] = plain.strip()
        except ValueError:
            self.output_text_box.delete("1.0", "end")
            self.output_text_box.insert("1.0", "Error: Invalid cipher table format. Use 'A -> Q' format.")
            return

        deciphered_text = ''.join(cipher_map.get(c.upper(), c) for c in message)

        self.output_text_box.delete("1.0", "end")
        self.output_text_box.insert("1.0", deciphered_text)

    def clear_fields(self):
        """Clear all text fields."""
        self.input_text_box.delete("1.0", "end")
        self.table_text_box.delete("1.0", "end")
        self.output_text_box.delete("1.0", "end")