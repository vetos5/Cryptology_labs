import customtkinter as ctk
from views.text_analysis import TextAnalysisView
from views.about import AboutView
from views.cypher import CypherView
from views.text_decryption import TextDecryptView
from views.sha256_benchmark import SHA256BenchmarkView
from views.vigenere import VigenereView
from views.one_time_pad import OneTimePadView
from views.primality_test import PrimalityTestView
from utils.themes import apply_dark_treeview


class FrequencyTableApp(ctk.CTk):
    def __init__(self):
        """Initialize the Frequency Table Application."""
        super().__init__()

        self.title("Frequency Table App")
        self.geometry("800x600")

        self.language = 'en'
        self.current_view = None

        # Define view mappings (excluding About)
        self.views = {
            "Text Analysis": (TextAnalysisView, self.switch_to_text_analysis),
            "Cypher": (CypherView, self.switch_to_other_program),
            "Text Decrypt": (TextDecryptView, self.switch_to_text_decrypt),
            "SHA256 Benchmark": (SHA256BenchmarkView, self.switch_to_sha256_benchmark),
            "Vigenère": (VigenereView, self.switch_to_vigenere),
            "One-Time Pad": (OneTimePadView, self.switch_to_one_time_pad),
            "Primality Test": (PrimalityTestView, self.switch_to_primality_test)
        }

        self.menu_frame = ctk.CTkFrame(self, height=40)
        self.menu_frame.pack(fill="x", side="top")

        # Create the option menu
        self.view_selector = ctk.CTkOptionMenu(
            self.menu_frame,
            values=list(self.views.keys()),
            command=self.switch_view,
            width=200,
            height=32,
            font=("Arial", 12),
            fg_color="#2e2e2e",
            button_color="#1e1e1e",
            button_hover_color="#3e3e3e"
        )
        self.view_selector.pack(side="left", padx=20, pady=5)
        self.view_selector.set("Text Analysis")  # Set default value

        # Create About button
        self.about_button = ctk.CTkButton(
            self.menu_frame,
            text="About",
            command=self.switch_to_about,
            width=100,
            height=32,
            font=("Arial", 12),
            fg_color="#2e2e2e",
            hover_color="#3e3e3e"
        )
        self.about_button.pack(side="right", padx=20, pady=5)

        # Initialize all views
        self.text_analysis_view = TextAnalysisView(self)
        self.about_view = AboutView(self)
        self.cypher_view = CypherView(self)
        self.text_decrypt_view = TextDecryptView(self)
        self.sha256_benchmark_view = SHA256BenchmarkView(self)
        self.vigenere_view = VigenereView(self)
        self.one_time_pad_view = OneTimePadView(self)
        self.primality_test_view = PrimalityTestView(self)

        # Show default view
        self.switch_to_text_analysis()

    def switch_view(self, view_name):
        """Generic view switching method called by the option menu."""
        if view_name in self.views:
            _, switch_method = self.views[view_name]
            switch_method()

    def switch_to_text_analysis(self):
        """Switch to the text analysis view."""
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.text_analysis_view
        self.current_view.pack(fill="both", expand=True)

    def switch_to_about(self):
        """Switch to the about view."""
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.about_view
        self.current_view.pack(fill="both", expand=True)

    def switch_to_other_program(self):
        """Switch to the other program view."""
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.cypher_view
        self.current_view.pack(fill="both", expand=True)

    def switch_to_text_decrypt(self):
        """Switch to the text decrypt view."""
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.text_decrypt_view  
        self.current_view.pack(fill="both", expand=True)

    def switch_to_sha256_benchmark(self):
        """Switch to the SHA256 benchmark view."""
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.sha256_benchmark_view
        self.current_view.pack(fill="both", expand=True)

    def switch_to_vigenere(self):
        """Switch to the Vigenère cipher view."""
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.vigenere_view
        self.current_view.pack(fill="both", expand=True)

    def switch_to_one_time_pad(self):
        """Switch to the One-Time Pad cipher view."""
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.one_time_pad_view
        self.current_view.pack(fill="both", expand=True)

    def switch_to_primality_test(self):
        if self.current_view:
            self.current_view.pack_forget()
        self.current_view = self.primality_test_view
        self.current_view.pack(fill="both", expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = FrequencyTableApp()
    app.mainloop()
