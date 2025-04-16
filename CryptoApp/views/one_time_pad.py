import customtkinter as ctk
import base64
from utils.text_utils import (
    load_text_file, 
    save_text_file, 
    load_binary_file,
    save_binary_file, 
    create_enhanced_textbox,
    show_error,
    show_message
)
from utils.cipher_utils import one_time_pad_encrypt, one_time_pad_decrypt


class OneTimePadView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        title_label = ctk.CTkLabel(self, text="One-Time Pad Cipher", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)

        self.load_button = ctk.CTkButton(button_frame, text="Load File", command=self.load_file, width=100)
        self.load_button.pack(side="left", padx=5)

        self.save_button = ctk.CTkButton(button_frame, text="Save", command=self.save_file, width=100)
        self.save_button.pack(side="left", padx=5)
        
        self.save_key_button = ctk.CTkButton(button_frame, text="Save Key", command=self.save_key, width=100)
        self.save_key_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(button_frame, text="Clear", command=self.clear_fields, width=100)
        self.clear_button.pack(side="left", padx=5)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.input_label = ctk.CTkLabel(input_frame, text="Input Text:", font=("Arial", 14))
        self.input_label.pack(anchor="nw", padx=5, pady=5)

        self.input_text_box = create_enhanced_textbox(input_frame)
        self.input_text_box.pack(fill="both", expand=True, padx=5)
        
        key_frame = ctk.CTkFrame(self)
        key_frame.pack(fill="x", padx=20, pady=10)
        
        self.key_label = ctk.CTkLabel(key_frame, text="Key:", font=("Arial", 14))
        self.key_label.pack(side="left", padx=5)
        
        self.key_load_button = ctk.CTkButton(key_frame, text="Load Key", command=self.load_key, width=100)
        self.key_load_button.pack(side="left", padx=5)

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
        
        self.key = bytes()

    def load_file(self):
        result = load_text_file(self.input_text_box)
        if isinstance(result, str):
            show_error(self.output_text_box, result)

    def save_file(self):
        result = save_text_file(self.output_text_box)
        if isinstance(result, str):
            show_error(self.output_text_box, result)

    def save_key(self):
        if not self.key:
            show_error(self.output_text_box, "No key available to save.")
            return
        
        save_binary_file(self.key, self.output_text_box)

    def load_key(self):
        self.key = load_binary_file(self.output_text_box) or bytes()

    def generate_key(self):
        text = self.input_text_box.get("1.0", "end").strip()
        
        if not text:
            show_error(self.output_text_box, "Please provide input text before generating a key.")
            return

        _, self.key = one_time_pad_encrypt(text)
        
        show_message(self.output_text_box, 
                    f"Random key generated for the input text.\n" +
                    f"Key length: {len(self.key)} bytes\n" +
                    "Use 'Save Key' to save it for later decryption.")

    def encrypt_text(self):
        text = self.input_text_box.get("1.0", "end").strip()
        
        if not text:
            show_error(self.output_text_box, "Please provide input text.")
            return

        if not self.key:
            encrypted_text, self.key = one_time_pad_encrypt(text)
            if encrypted_text:
                self.output_text_box.delete("1.0", "end")
                self.output_text_box.insert("1.0", encrypted_text)
            else:
                show_error(self.output_text_box, "Encryption failed")
            return

        text_bytes = text.encode('utf-8')
        if len(self.key) < len(text_bytes):
            show_error(self.output_text_box, "Key is too short for the input text. Generating new key.")
            encrypted_text, self.key = one_time_pad_encrypt(text)
            if encrypted_text:
                self.output_text_box.delete("1.0", "end")
                self.output_text_box.insert("1.0", encrypted_text)
            return
            
        # Use existing key
        encrypted_bytes = bytes(a ^ b for a, b in zip(text_bytes, self.key))
        encrypted_text = base64.b64encode(encrypted_bytes).decode('utf-8')
            
        self.output_text_box.delete("1.0", "end")
        self.output_text_box.insert("1.0", encrypted_text)

    def decrypt_text(self):
        encrypted_text = self.input_text_box.get("1.0", "end").strip()
        
        if not encrypted_text:
            show_error(self.output_text_box, "Please provide encrypted text.")
            return
            
        if not self.key:
            show_error(self.output_text_box, "No key available. Please load a key first.")
            return
            
        decrypted_text = one_time_pad_decrypt(encrypted_text, self.key)
        if decrypted_text:
            self.output_text_box.delete("1.0", "end")
            self.output_text_box.insert("1.0", decrypted_text)
        else:
            show_error(self.output_text_box, "Decryption failed. Make sure you have the correct key.")

    def clear_fields(self):
        self.input_text_box.delete("1.0", "end")
        self.output_text_box.delete("1.0", "end")
        self.key = bytes()
