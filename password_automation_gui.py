import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import pyautogui
import time
import threading
import sys

class PasswordAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Automation")
        self.root.geometry("600x400")
        
        self.running = False
        self.thread = None
        self.passwords = []
        
        # Стилизация
        self.style = ttk.Style()
        self.style.configure('TButton', padding=6, font=('Arial', 10))
        self.style.configure('TLabel', font=('Arial', 10))
        
        # Создание элементов GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм управления
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10, padx=10, fill=tk.X)
        
        # Кнопки
        self.start_btn = ttk.Button(control_frame, text="Start", command=self.start)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Exit", command=self.exit_app).pack(side=tk.RIGHT, padx=5)
        
        # Выбор файла
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=5, padx=10, fill=tk.X)
        
        ttk.Button(file_frame, text="Select Password File", command=self.load_file).pack(side=tk.LEFT)
        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        # Лог
        log_frame = ttk.Frame(self.root)
        log_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, state='disabled')
        self.log_area.pack(fill=tk.BOTH, expand=True)
        
    def load_file(self):
        file_path = filedialog.askopenfilename(title="Select Password File")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.passwords = file.read().splitlines()
                self.file_label.config(text=file_path)
                self.log("File loaded successfully")
            except Exception as e:
                self.log(f"Error loading file: {str(e)}")
    
    def start(self):
        if not self.passwords:
            self.log("Error: No password file selected!")
            return
            
        self.running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.thread = threading.Thread(target=self.automate_password_entry)
        self.thread.start()
        self.log("Automation started")
        
    def stop(self):
        self.running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.log("Automation stopped")
    
    def exit_app(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        self.root.destroy()
        sys.exit()
        
    def automate_password_entry(self):
        for password in self.passwords:
            if not self.running:
                break
            
            try:
                # Очистка предыдущего пароля
                pyautogui.hotkey('ctrl', 'a')  # Выделить весь текст
                pyautogui.press('backspace')   # Удалить выделенный текст
                
                # Ввод нового пароля
                pyautogui.write(password)
                pyautogui.press('enter')
                self.log(f"Entered password: {password}")
                time.sleep(1)
            except Exception as e:
                self.log(f"Error: {str(e)}")
                self.stop()
                break
    
    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordAutomationApp(root)
    root.mainloop()
