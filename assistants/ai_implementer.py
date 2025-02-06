import tkinter as tk
from tkinter import scrolledtext
import subprocess
import os
from datetime import datetime
import re
from PIL import ImageGrab

class AIImplementer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AI Implementation Assistant")
        self.setup_gui()
        self.screenshot_folder = "implementation_logs"
        self.ensure_folders()
        
    def setup_gui(self):
        self.root.geometry('900x700')
        self.root.configure(bg='#2D2D2D')
        
        # Instructions input
        self.instruction_label = tk.Label(
            self.root,
            text="Paste AI Instructions Here:",
            bg='#2D2D2D',
            fg='white'
        )
        self.instruction_label.pack(pady=5)
        
        self.instruction_text = scrolledtext.ScrolledText(
            self.root,
            height=10,
            bg='#3D3D3D',
            fg='white'
        )
        self.instruction_text.pack(pady=5, padx=10, fill=tk.X)
        
        # Execute button
        self.execute_button = tk.Button(
            self.root,
            text="Execute Instructions",
            command=self.process_instructions,
            bg='#4D4D4D',
            fg='white'
        )
        self.execute_button.pack(pady=5)
        
        # Status output
        self.status_label = tk.Label(
            self.root,
            text="Execution Log:",
            bg='#2D2D2D',
            fg='white'
        )
        self.status_label.pack(pady=5)
        
        self.status_text = scrolledtext.ScrolledText(
            self.root,
            height=20,
            bg='#3D3D3D',
            fg='white'
        )
        self.status_text.pack(pady=5, padx=10, fill=tk.X)
    
    def ensure_folders(self):
        if not os.path.exists(self.screenshot_folder):
            os.makedirs(self.screenshot_folder)
    
    def take_screenshot(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_folder}/{name}_{timestamp}.png"
        screenshot = ImageGrab.grab()
        screenshot.save(filename)
        return filename
    
    def log_action(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.status_text.see(tk.END)
    
    def execute_terminal_command(self, command):
        try:
            self.log_action(f"Executing command: {command}")
            # Run command and capture output
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Get output in real-time
            while True:
                output = process.stdout.readline()
                if output:
                    self.log_action(f"Output: {output.strip()}")
                error = process.stderr.readline()
                if error:
                    self.log_action(f"Error: {error.strip()}")
                if output == '' and error == '' and process.poll() is not None:
                    break
            
            screenshot = self.take_screenshot("terminal_output")
            self.log_action(f"Screenshot saved: {screenshot}")
            return True
        except Exception as e:
            self.log_action(f"Error executing command: {str(e)}")
            return False
    
    def create_file(self, filename, content):
        try:
            self.log_action(f"Creating file: {filename}")
            with open(filename, 'w') as f:
                f.write(content)
            self.log_action(f"File created successfully")
            screenshot = self.take_screenshot("file_created")
            self.log_action(f"Screenshot saved: {screenshot}")
            return True
        except Exception as e:
            self.log_action(f"Error creating file: {str(e)}")
            return False
    
    def process_instructions(self):
        instructions = self.instruction_text.get("1.0", tk.END).strip()
        self.log_action("Processing new instructions")
        
        # Check for terminal command prefix
        if instructions.startswith('Execute terminal command:'):
            command = instructions.replace('Execute terminal command:', '').strip()
            self.execute_terminal_command(command)
        
        # Look for other terminal commands
        elif instructions.startswith('python ') or instructions.startswith('pip ') or instructions.startswith('gh '):
            self.execute_terminal_command(instructions.strip())
        
        # Look for code file creation
        elif "code " in instructions:
            match = re.search(r"code\s+(\S+)", instructions)
            if match:
                filename = match.group(1)
                # Extract code block
                code_block = instructions.split(filename, 1)[1].strip()
                self.create_file(filename, code_block)
        
        self.log_action("Finished processing instructions")
        screenshot = self.take_screenshot("final_state")
        self.log_action(f"Final state screenshot saved: {screenshot}")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    implementer = AIImplementer()
    implementer.run()