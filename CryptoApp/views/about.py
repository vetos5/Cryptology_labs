# views/about.py
import customtkinter as ctk
from PIL import Image, ImageTk


class AboutView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.about_label = ctk.CTkLabel(
            self,
            text="Cryptology App\n\nVersion: 1.33\n\nCreated by: Vitalii Kovtun",
            font=("Arial", 14),
        )
        self.about_label.pack(padx=20, pady=10)

        self.display_about_image()

        # Back button
        self.back_button = ctk.CTkButton(self, text="Back", command=self.parent.switch_to_text_analysis)
        self.back_button.pack(pady=10)

    def display_about_image(self):
        """Load and display an image in the about section."""
        try:
            image = Image.open("resources/images/DSC01212.jpg")
            image = image.resize((300, 240), Image.Resampling.LANCZOS)
            image = image.rotate(-90, expand=True)

            self.about_image = ImageTk.PhotoImage(image)

            self.about_image_label = ctk.CTkLabel(self, image=self.about_image, text="")
            self.about_image_label.configure(image=self.about_image)
            self.about_image_label.image = self.about_image
            self.about_image_label.pack(pady=10)

        except Exception as e:
            print(f"Error loading image: {e}")
