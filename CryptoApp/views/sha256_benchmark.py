import customtkinter as ctk
import hashlib
import time
import threading
from typing import Optional

class SHA256BenchmarkView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = ctk.CTkLabel(self, text="SHA256 Decryption Time Benchmark", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=20)
        
        # Input frame
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=20, pady=10)
        
        # Input field for text to hash
        self.input_label = ctk.CTkLabel(input_frame, text="Enter text to hash:")
        self.input_label.pack(side="left", padx=5)
        
        self.input_text = ctk.CTkTextbox(input_frame, height=100, width=400)
        self.input_text.pack(side="left", padx=5)
        
        # Button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        # Start button
        self.start_button = ctk.CTkButton(button_frame, text="Start Benchmark", command=self.start_benchmark)
        self.start_button.pack(side="left", padx=5)
        
        # Stop button
        self.stop_button = ctk.CTkButton(button_frame, text="Stop", command=self.stop_benchmark, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        
        # Results frame
        results_frame = ctk.CTkFrame(self)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Results text
        self.results_text = ctk.CTkTextbox(results_frame, height=200, width=400)
        self.results_text.pack(fill="both", expand=True)
        
        # Status label
        self.status_label = ctk.CTkLabel(self, text="Ready")
        self.status_label.pack(pady=10)
        
        self.is_running = False
        self.benchmark_thread: Optional[threading.Thread] = None
        
    def start_benchmark(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            self.status_label.configure(text="Running benchmark...")
            
            # Get input text
            input_text = self.input_text.get("1.0", "end-1c")
            if not input_text:
                self.results_text.insert("end", "Please enter some text to hash.\n")
                self.stop_benchmark()
                return
                
            # Start benchmark in a separate thread
            self.benchmark_thread = threading.Thread(target=self.run_benchmark, args=(input_text,))
            self.benchmark_thread.start()
            
    def stop_benchmark(self):
        if self.is_running:
            self.is_running = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.status_label.configure(text="Benchmark stopped")
            
    def run_benchmark(self, input_text: str):
        iterations = 0
        total_time = 0
        
        while self.is_running:
            start_time = time.time()
            
            # Perform SHA256 hash
            hashlib.sha256(input_text.encode()).hexdigest()
            
            end_time = time.time()
            iteration_time = end_time - start_time
            
            total_time += iteration_time
            iterations += 1
            
            # Update results every 100 iterations
            if iterations % 100 == 0:
                avg_time = total_time / iterations
                self.results_text.insert("end", f"Iteration {iterations}: Average time = {avg_time:.6f} seconds\n")
                self.results_text.see("end")
                
        # Final results
        if iterations > 0:
            avg_time = total_time / iterations
            self.results_text.insert("end", f"\nFinal Results:\n")
            self.results_text.insert("end", f"Total iterations: {iterations}\n")
            self.results_text.insert("end", f"Average time: {avg_time:.6f} seconds\n")
            self.results_text.insert("end", f"Operations per second: {1/avg_time:.2f}\n")
            self.results_text.see("end") 