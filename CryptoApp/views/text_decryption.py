import customtkinter as ctk
from tkinter import filedialog
from collections import Counter


class TextDecryptView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(self, text="Text Decryption", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)

        self.load_button = ctk.CTkButton(button_frame, text="Load File", command=self.load_file, width=100)
        self.load_button.pack(side="left", padx=5)

        self.load_mapping_button = ctk.CTkButton(button_frame, text="Load Mapping", command=self.load_mapping, width=100)
        self.load_mapping_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(button_frame, text="Save", command=self.save_file, width=100)
        self.save_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_all, width=100)
        self.clear_button.pack(side="left", padx=5)

        labels_frame = ctk.CTkFrame(self)
        labels_frame.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(labels_frame, text="Encrypted Text:", font=("Helvetica", 14)).pack(side="left", padx=10)
        ctk.CTkLabel(labels_frame, text="Decrypted Text:", font=("Helvetica", 14)).pack(side="right", padx=10)

        text_areas_frame = ctk.CTkFrame(self)
        text_areas_frame.pack(fill="both", expand=True, padx=20, pady=5)

        self.encrypted_text = ctk.CTkTextbox(text_areas_frame, height=200, width=400)
        self.encrypted_text.pack(side="left", fill="both", expand=True, padx=5)

        self.decrypted_text = ctk.CTkTextbox(text_areas_frame, height=200, width=400)
        self.decrypted_text.pack(side="right", fill="both", expand=True, padx=5)

        action_frame = ctk.CTkFrame(self)
        action_frame.pack(fill="x", padx=20, pady=10)

        self.analyze_button = ctk.CTkButton(action_frame, text="Analyze", width=100,
                                          command=self.analyze_text)
        self.analyze_button.pack(side="left", padx=5)

        self.decrypt_button = ctk.CTkButton(action_frame, text="Decrypt", width=100,
                                          command=self.decrypt_text)
        self.decrypt_button.pack(side="left", padx=5)

        freq_frame = ctk.CTkFrame(self)
        freq_frame.pack(fill="both", expand=True, padx=20, pady=10)

        freq_labels_frame = ctk.CTkFrame(freq_frame)
        freq_labels_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(freq_labels_frame, text="Frequency", font=("Helvetica", 14)).pack(side="left", padx=10)
        ctk.CTkLabel(freq_labels_frame, text="From", font=("Helvetica", 14)).pack(side="left", padx=10)
        ctk.CTkLabel(freq_labels_frame, text="To", font=("Helvetica", 14)).pack(side="left", padx=10)

        freq_text_frame = ctk.CTkFrame(freq_frame)
        freq_text_frame.pack(fill="both", expand=True, pady=5)

        self.frequency_text = ctk.CTkTextbox(freq_text_frame, height=150, width=200)
        self.frequency_text.pack(side="left", fill="both", expand=True, padx=5)

        self.from_text = ctk.CTkTextbox(freq_text_frame, height=150, width=100)
        self.from_text.pack(side="left", fill="both", expand=True, padx=5)

        self.to_text = ctk.CTkTextbox(freq_text_frame, height=150, width=100)
        self.to_text.pack(side="left", fill="both", expand=True, padx=5)

    def analyze_frequency(self, text):
        count = Counter(text)
        length = len(text)

        if length == 0:
            return {"freq_list": "No inserted text", "from_chars": "", "to_chars": ""}

        frequency = {char: round(count[char] / length, 4) for char in count}
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

        freq_list = "\n".join([f"{freq}" for _, freq in sorted_freq])
        from_chars = "\n".join([char for char, _ in sorted_freq])

        english_freq_order = "etaoinshrdlucmfwypvbgkjqxz"
        to_chars = "\n".join(list(english_freq_order[:len(sorted_freq)]))

        return {"freq_list": freq_list, "from_chars": from_chars, "to_chars": to_chars}

    def perform_decryption(self, text, from_chars, to_chars):
        decrypted_text = ""
        char_map = dict(zip(from_chars, to_chars))

        for char in text:
            decrypted_text += char_map.get(char, char)

        return decrypted_text

    def analyze_text(self):
        text = self.encrypted_text.get("1.0", "end").strip()
        frequency_data = self.analyze_frequency(text)

        self.frequency_text.delete("1.0", "end")
        self.frequency_text.insert("end", frequency_data["freq_list"])

        self.from_text.delete("1.0", "end")
        self.from_text.insert("end", frequency_data["from_chars"])

        self.to_text.delete("1.0", "end")
        self.to_text.insert("end", frequency_data["to_chars"])

        self.decrypt_text()

    def decrypt_text(self):
        text = self.encrypted_text.get("1.0", "end").strip()
        from_text = self.from_text.get("1.0", "end").strip().split("\n")
        to_text = self.to_text.get("1.0", "end").strip().split("\n")
        
        if not text or not from_text or not to_text:
            return

        decrypted_text = self.perform_decryption(text, from_text, to_text)
        self.decrypted_text.delete("1.0", "end")
        self.decrypted_text.insert("end", decrypted_text)

    def save_file(self):
        decrypted_text = self.decrypted_text.get("1.0", "end").strip()
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(decrypted_text)

    def load_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    text = file.read()
                    self.encrypted_text.delete("1.0", "end")
                    self.encrypted_text.insert("1.0", text)
            except Exception as e:
                self.decrypted_text.delete("1.0", "end")
                self.decrypted_text.insert("1.0", f"Error loading file: {str(e)}")

    def load_mapping(self):
        """Load character mapping from a file."""
        file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    from_chars = []
                    to_chars = []
                    
                    for line in file:
                        line = line.strip()
                        if line and "->" in line:
                            parts = [part.strip() for part in line.split("->")]
                            if len(parts) == 2:
                                from_chars.append(parts[0])
                                to_chars.append(parts[1])

                    self.from_text.delete("1.0", "end")
                    self.from_text.insert("1.0", "\n".join(from_chars))
                    
                    self.to_text.delete("1.0", "end")
                    self.to_text.insert("1.0", "\n".join(to_chars))

                    if self.encrypted_text.get("1.0", "end").strip():
                        self.decrypt_text()
                        
            except Exception as e:
                self.decrypted_text.delete("1.0", "end")
                self.decrypted_text.insert("1.0", f"Error loading mapping file: {str(e)}")

    def clear_all(self):
        """Clear all text areas in the window."""
        self.encrypted_text.delete("1.0", "end")
        self.decrypted_text.delete("1.0", "end")
        self.frequency_text.delete("1.0", "end")
        self.from_text.delete("1.0", "end")
        self.to_text.delete("1.0", "end")
