import customtkinter as ctk
from utils.text_utils import (
    load_text_file,
    save_text_file,
    create_enhanced_textbox,
    show_error,
    show_message
)
from utils.cipher_utils import vigenere_encrypt, vigenere_decrypt, generate_vigenere_key


class VigenereView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(self, text="Vigenère Cipher", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)

        self.load_button = ctk.CTkButton(button_frame, text="Load File", command=self.load_file, width=100)
        self.load_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(button_frame, text="Save", command=self.save_file, width=100)
        self.save_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_fields, width=100)
        self.clear_button.pack(side="left", padx=5)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.input_label = ctk.CTkLabel(input_frame, text="Input Text:", font=("Arial", 14))
        self.input_label.pack(anchor="nw", padx=5, pady=5)

        self.input_text_box = create_enhanced_textbox(input_frame)
        self.input_text_box.pack(fill="both", expand=True, padx=5)

        key_frame = ctk.CTkFrame(self)
        key_frame.pack(fill="x", padx=20, pady=5)
        
        self.key_label = ctk.CTkLabel(key_frame, text="Key:", font=("Arial", 14))
        self.key_label.pack(side="left", padx=5)
        
        self.key_entry = ctk.CTkEntry(key_frame, width=200)
        self.key_entry.pack(side="left", padx=5)

        self.generate_key_button = ctk.CTkButton(
            key_frame, text="Generate Key", command=self.generate_key, corner_radius=8, fg_color="#f39c12"
        )
        self.generate_key_button.pack(side="left", padx=5)

        action_frame = ctk.CTkFrame(self)
        action_frame.pack(fill="x", padx=20, pady=10)

        self.encrypt_button = ctk.CTkButton(
            action_frame, text="Encrypt", command=self.encrypt_text, corner_radius=8, fg_color="#3498db"
        )
        self.encrypt_button.pack(side="left", padx=5)

        self.decrypt_button = ctk.CTkButton(
            action_frame, text="Decrypt", command=self.decrypt_text, corner_radius=8, fg_color="#2ecc71"
        )
        self.decrypt_button.pack(side="left", padx=5)

        output_frame = ctk.CTkFrame(self)
        output_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.output_label = ctk.CTkLabel(output_frame, text="Output Text:", font=("Arial", 14))
        self.output_label.pack(anchor="nw", padx=5, pady=5)

        self.output_text_box = create_enhanced_textbox(output_frame)
        self.output_text_box.pack(fill="both", expand=True, padx=5)

    def load_file(self):
        result = load_text_file(self.input_text_box)
        if isinstance(result, str):
            show_error(self.output_text_box, result)

    def save_file(self):
        result = save_text_file(self.output_text_box)
        if isinstance(result, str):
            show_error(self.output_text_box, result)

    def generate_key(self):
        key = generate_vigenere_key()
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, key)

    def encrypt_text(self):
        text = self.input_text_box.get("1.0", "end").strip()
        key = self.key_entry.get().strip()
        
        if not text or not key:
            show_error(self.output_text_box, "Please provide both text and key.")
            return

        result = vigenere_encrypt(text, key)
        
        if result is None:
            show_error(self.output_text_box, "Key must contain at least one letter.")
            return
                
        self.output_text_box.delete("1.0", "end")
        self.output_text_box.insert("1.0", result)

    def decrypt_text(self):
        text = self.input_text_box.get("1.0", "end").strip()
        key = self.key_entry.get().strip()
        
        if not text or not key:
            show_error(self.output_text_box, "Please provide both text and key.")
            return

        result = vigenere_decrypt(text, key)
        
        if result is None:
            show_error(self.output_text_box, "Key must contain at least one letter.")
            return
                
        self.output_text_box.delete("1.0", "end")
        self.output_text_box.insert("1.0", result)

    def clear_fields(self):
        self.input_text_box.delete("1.0", "end")
        self.key_entry.delete(0, "end")
        self.output_text_box.delete("1.0", "end") 