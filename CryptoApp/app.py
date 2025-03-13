import customtkinter as ctk
from views.text_analysis import TextAnalysisView
from views.about import AboutView
from views.cypher import CypherView
from utils.themes import apply_dark_treeview


class FrequencyTableApp(ctk.CTk):
    def __init__(self):
        """Initialize the Frequency Table Application."""
        super().__init__()

        self.title("Frequency Table App")
        self.geometry("800x600")

        self.language = 'en'
        self.current_view = None

        self.menu_frame = ctk.CTkFrame(self, height=40)
        self.menu_frame.pack(fill="x", side="top")

        self.hamburger_button = ctk.CTkButton(self.menu_frame, text="☰", width=40, command=self.toggle_menu)
        self.hamburger_button.pack(side="left", padx=10)

        self.side_menu = ctk.CTkFrame(self.menu_frame, height=40, fg_color="#2e2e2e")
        self.side_menu.pack(side="left", fill="x", padx=10, anchor="nw")

        self.text_analysis_button = ctk.CTkButton(self.side_menu, text="Text Analysis", width=100,
                                                  command=self.switch_to_text_analysis)
        self.text_analysis_button.pack(side="left", padx=10)

        self.other_program_button = ctk.CTkButton(self.side_menu, text="Cypher", width=100,
                                                  command=self.switch_to_other_program)
        self.other_program_button.pack(side="left", padx=10)

        self.about_button = ctk.CTkButton(self.side_menu, text="About", width=100,
                                           command=self.switch_to_about)
        self.about_button.pack(side="left", padx=10)

        self.text_analysis_view = TextAnalysisView(self)
        self.about_view = AboutView(self)
        self.cypher_view = CypherView(self)

        self.switch_to_text_analysis()

    def toggle_menu(self):
        """Toggle the visibility of the side menu."""
        if self.side_menu.winfo_ismapped():
            self.side_menu.pack_forget()
        else:
            self.side_menu.pack(side="left", fill="x", padx=10, anchor="nw")

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


if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")

    app = FrequencyTableApp()
    app.mainloop()
