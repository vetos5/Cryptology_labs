from tkinter import filedialog
import base64

def load_text_file(text_widget):
    """Load text from a file into a text widget."""
    file_path = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()
                text_widget.delete("1.0", "end")
                text_widget.insert("1.0", text)
            return True
        except Exception as e:
            return f"Error loading file: {str(e)}"
    return False

def save_text_file(text_widget):
    """Save text from a text widget to a file."""
    text = text_widget.get("1.0", "end").strip()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
            return True
        except Exception as e:
            return f"Error saving file: {str(e)}"
    return False

def load_binary_file(output_widget=None):
    """Load binary data from a file."""
    file_path = filedialog.askopenfilename(
        defaultextension=".key",
        filetypes=[("Key files", "*.key"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, "rb") as file:
                data = file.read()
            if output_widget:
                output_widget.delete("1.0", "end")
                output_widget.insert("1.0", f"File loaded successfully from {file_path}")
            return data
        except Exception as e:
            if output_widget:
                output_widget.delete("1.0", "end")
                output_widget.insert("1.0", f"Error loading file: {str(e)}")
            return None
    return None

def save_binary_file(data, output_widget=None):
    """Save binary data to a file."""
    if not data:
        if output_widget:
            output_widget.delete("1.0", "end")
            output_widget.insert("1.0", "Error: No data available to save.")
        return False
        
    file_path = filedialog.asksaveasfilename(
        defaultextension=".key",
        filetypes=[("Key files", "*.key"), ("All files", "*.*")]
    )
    
    if file_path:
        try:
            with open(file_path, "wb") as file:
                file.write(data)
            if output_widget:
                output_widget.delete("1.0", "end")
                output_widget.insert("1.0", f"Data saved successfully to {file_path}")
            return True
        except Exception as e:
            if output_widget:
                output_widget.delete("1.0", "end")
                output_widget.insert("1.0", f"Error saving file: {str(e)}")
            return False
    return False

def create_enhanced_textbox(parent, **kwargs):
    """Create a text box with enhanced configuration for better copy-paste support."""
    from customtkinter import CTkTextbox
    
    # Default settings for better text handling
    default_settings = {
        "wrap": "word",
        "height": 100,
        "font": ("Arial", 12),
        "activate_scrollbars": True,
        "undo": True,
        "autoseparators": True,
        "maxundo": -1
    }
    
    # Override defaults with any provided settings
    settings = {**default_settings, **kwargs}
    
    # Create and return the text box
    return CTkTextbox(parent, **settings)

def show_error(output_widget, message):
    """Display an error message in the output widget."""
    output_widget.delete("1.0", "end")
    output_widget.insert("1.0", f"Error: {message}")
    
def show_message(output_widget, message):
    """Display a message in the output widget."""
    output_widget.delete("1.0", "end")
    output_widget.insert("1.0", message) 