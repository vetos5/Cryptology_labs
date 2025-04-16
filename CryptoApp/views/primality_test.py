import customtkinter as ctk
from utils.text_utils import (
    create_enhanced_textbox,
    show_error,
    show_message
)
from utils.number_theory import (
    jacobi_symbol,
    solovay_strassen_test,
    analyze_number
)
import random


class PrimalityTestView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        title_label = ctk.CTkLabel(self, text="Primality Test", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        left_panel = ctk.CTkFrame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        right_panel = ctk.CTkFrame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.number_label = ctk.CTkLabel(left_panel, text="Number to Test:", font=("Arial", 14))
        self.number_label.pack(anchor="w", padx=5, pady=5)
        
        self.number_entry = ctk.CTkEntry(left_panel, width=300, font=("Arial", 12))
        self.number_entry.pack(fill="x", padx=5, pady=5)

        random_frame = ctk.CTkFrame(left_panel)
        random_frame.pack(fill="x", padx=5, pady=5)
        
        self.random_digit_label = ctk.CTkLabel(random_frame, text="Random number digits:", font=("Arial", 12))
        self.random_digit_label.pack(side="left", padx=5)
        
        self.random_digit_entry = ctk.CTkEntry(random_frame, width=60)
        self.random_digit_entry.pack(side="left", padx=5)
        self.random_digit_entry.insert(0, "10")
        
        self.generate_random_button = ctk.CTkButton(
            random_frame, 
            text="Generate", 
            command=self.generate_random, 
            corner_radius=8, 
            fg_color="#f39c12"
        )
        self.generate_random_button.pack(side="left", padx=5)

        self.iterations_label = ctk.CTkLabel(left_panel, text="Solovay-Strassen Test Iterations:", font=("Arial", 12))
        self.iterations_label.pack(anchor="w", padx=5, pady=5)
        
        self.iterations_slider = ctk.CTkSlider(
            left_panel, 
            from_=1,
            to=50, 
            number_of_steps=45,
            command=self.update_iterations_label
        )
        self.iterations_slider.pack(fill="x", padx=5, pady=5)
        self.iterations_slider.set(20)
        
        self.iterations_value_label = ctk.CTkLabel(left_panel, text="20 iterations", font=("Arial", 12))
        self.iterations_value_label.pack(anchor="w", padx=5, pady=2)

        button_frame = ctk.CTkFrame(left_panel)
        button_frame.pack(fill="x", padx=5, pady=10)
        
        self.test_button = ctk.CTkButton(
            button_frame, 
            text="Test Primality", 
            command=self.test_primality, 
            corner_radius=8, 
            fg_color="#3498db"
        )
        self.test_button.pack(side="left", padx=5)
        
        self.jacobi_button = ctk.CTkButton(
            button_frame, 
            text="Calculate Jacobi Symbol", 
            command=self.show_jacobi_dialog, 
            corner_radius=8, 
            fg_color="#2ecc71"
        )
        self.jacobi_button.pack(side="left", padx=5)
        
        self.clear_button = ctk.CTkButton(
            button_frame, 
            text="Clear", 
            command=self.clear_fields, 
            corner_radius=8
        )
        self.clear_button.pack(side="left", padx=5)


        self.results_label = ctk.CTkLabel(right_panel, text="Results:", font=("Arial", 14))
        self.results_label.pack(anchor="w", padx=5, pady=5)
        
        self.results_text = create_enhanced_textbox(right_panel, height=300)
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)

        self.show_initial_message()
        
    def show_initial_message(self):
        message = """Welcome to the Primality Test module.

Enter a number to test whether it's prime using:
- Deterministic primality test (for smaller numbers)
- Solovay-Strassen probabilistic primality test

You can also calculate the Jacobi symbol for a pair of numbers.

To get started, enter a number and click "Test Primality"."""
        
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", message)
        
    def update_iterations_label(self, value):
        iterations = int(value)
        self.iterations_value_label.configure(text=f"{iterations} iterations")
        
    def generate_random(self):
        try:
            digits = int(self.random_digit_entry.get())
            if digits <= 0:
                show_error(self.results_text, "Number of digits must be positive")
                return
                
            if digits > 1000:
                show_error(self.results_text, "Number of digits must be less than or equal to 1000")
                return

            min_val = 10**(digits-1)
            max_val = 10**digits - 1

            random_number = random.randint(min_val, max_val)
            if random_number > 2 and random_number % 2 == 0:
                random_number += 1
                
            self.number_entry.delete(0, "end")
            self.number_entry.insert(0, str(random_number))
            
        except ValueError:
            show_error(self.results_text, "Please enter a valid number of digits")
            
    def test_primality(self):
        try:
            number_text = self.number_entry.get().strip()
            if not number_text:
                show_error(self.results_text, "Please enter a number to test")
                return
                
            number = int(number_text)
            iterations = int(self.iterations_slider.get())
            
            results = analyze_number(number, iterations)
            
            if results["error"]:
                show_error(self.results_text, results["error"])
                return

            output = f"Analysis of number: {number}\n\n"
            
            if results["deterministic_possible"]:
                output += f"Deterministic check: {results['deterministic_check'].upper()}\n"
            else:
                output += f"Deterministic check: {results['deterministic_check']}\n"
                
            output += f"Solovay-Strassen test: {results['solovay_strassen_result'].upper()}\n"
            output += f"Confidence level: {1 - 0.5**iterations:.10f}\n\n"
            
            output += "Solovay-Strassen test details:\n"
            
            if isinstance(results["solovay_strassen_details"], list) and not all(isinstance(d, dict) for d in results["solovay_strassen_details"]):

                for msg in results["solovay_strassen_details"]:
                    output += f"• {msg}\n"
            else:
                for detail in results["solovay_strassen_details"]:
                    iteration = detail["iteration"]
                    a = detail["a"]
                    jacobi = detail["jacobi"]
                    mod_exp = detail["mod_exp"]
                    congruent = "PASS" if detail["congruent"] else "FAIL"
                    
                    output += f"Test {iteration}: a={a}, Jacobi({a}/{number})={jacobi}, "
                    output += f"a^((n-1)/2) mod n={mod_exp}, Test: {congruent}\n"
                    
                    if not detail["congruent"]:
                        output += f"  → Found a witness that {number} is composite!\n"
                        break
            
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", output)
            
        except ValueError as e:
            show_error(self.results_text, f"Invalid input: {str(e)}")
        except Exception as e:
            show_error(self.results_text, f"An error occurred: {str(e)}")
            
    def show_jacobi_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Jacobi Symbol Calculator")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()

        num_frame = ctk.CTkFrame(dialog)
        num_frame.pack(fill="x", padx=20, pady=10)
        
        num_label = ctk.CTkLabel(num_frame, text="Numerator (a):", font=("Arial", 12))
        num_label.pack(side="left", padx=5)
        
        num_entry = ctk.CTkEntry(num_frame, width=200)
        num_entry.pack(side="left", padx=5)

        den_frame = ctk.CTkFrame(dialog)
        den_frame.pack(fill="x", padx=20, pady=10)
        
        den_label = ctk.CTkLabel(den_frame, text="Denominator (n):", font=("Arial", 12))
        den_label.pack(side="left", padx=5)
        
        den_entry = ctk.CTkEntry(den_frame, width=200)
        den_entry.pack(side="left", padx=5)

        result_frame = ctk.CTkFrame(dialog)
        result_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        result_text = create_enhanced_textbox(result_frame)
        result_text.pack(fill="both", expand=True, padx=5, pady=5)
        result_text.insert("1.0", "Enter values and click 'Calculate'")

        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        def calculate_jacobi():
            try:
                a = int(num_entry.get())
                n = int(den_entry.get())
                
                if n <= 0 or n % 2 == 0:
                    result_text.delete("1.0", "end")
                    result_text.insert("1.0", "Error: Denominator (n) must be an odd positive integer")
                    return
                
                result = jacobi_symbol(a, n)
                
                output = f"Jacobi Symbol ({a}/{n}) = {result}\n\n"
                output += f"This means that {a} is "
                
                if result == 1:
                    output += "a quadratic residue modulo " if n % 4 == 1 else "either a quadratic residue or non-residue modulo "
                    output += f"{n}."
                elif result == -1:
                    output += "a quadratic non-residue modulo " if n % 4 == 1 else "either a quadratic residue or non-residue modulo "
                    output += f"{n}."
                else:  # result == 0
                    output += f"not coprime to {n}."
                
                result_text.delete("1.0", "end")
                result_text.insert("1.0", output)
                
            except ValueError:
                result_text.delete("1.0", "end")
                result_text.insert("1.0", "Error: Please enter valid integers")
            except Exception as e:
                result_text.delete("1.0", "end")
                result_text.insert("1.0", f"Error: {str(e)}")
        
        calc_button = ctk.CTkButton(
            button_frame, 
            text="Calculate", 
            command=calculate_jacobi, 
            corner_radius=8, 
            fg_color="#3498db"
        )
        calc_button.pack(side="left", padx=5)
        
        close_button = ctk.CTkButton(
            button_frame, 
            text="Close", 
            command=dialog.destroy, 
            corner_radius=8
        )
        close_button.pack(side="right", padx=5)
        
    def clear_fields(self):
        self.number_entry.delete(0, "end")
        self.random_digit_entry.delete(0, "end")
        self.random_digit_entry.insert(0, "10")
        self.iterations_slider.set(20)
        self.update_iterations_label(20)
        self.show_initial_message() 