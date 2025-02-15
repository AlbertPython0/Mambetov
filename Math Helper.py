import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import math
from math import pi, sin, cos, tan, sqrt

class MathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Математический помощник 9-10 класс")
        self.root.geometry("1000x700")
        self.root.configure(bg='#F0F0F0')
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#F0F0F0')
        self.style.configure('TButton', font=('Arial', 12), padding=10, background='#4CAF50', foreground='white')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), background='#F0F0F0')
        self.style.configure('TLabel', font=('Arial', 12), background='#F0F0F0')
        self.style.configure('TEntry', font=('Arial', 12), padding=5)
        self.style.map('TButton', background=[('active', '#45a049')])
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.create_main_menu()
        
        self.frames = {}
        self.create_quadratic_frame()
        self.create_biquadratic_frame()
        self.create_linear_system_frame()
        self.create_geometry_frame()
        self.create_pythagoras_frame()
        self.create_percentage_frame()
        self.create_volume_frame()
        self.create_trigonometry_frame()
        self.create_arithmetic_prog_frame()
        self.create_geometric_prog_frame()

    def create_main_menu(self):
        ttk.Label(self.main_frame, text="Добро пожаловать в математический помощник!", 
                 style='Title.TLabel').pack(pady=20)
        
        topics = [
            ("Биквадратные уравнения", self.show_biquadratic),
            ("Квадратные уравнения", self.show_quadratic),
            ("Системы линейных уравнений", self.show_linear_system),
            ("Площадь фигур", self.show_geometry),
            ("Теорема Пифагора", self.show_pythagoras),
            ("Проценты", self.show_percentage),
            ("Объем тел", self.show_volume),
            ("Тригонометрия", self.show_trigonometry),
            ("Арифметическая прогрессия", self.show_arithmetic_prog),
            ("Геометрическая прогрессия", self.show_geometric_prog)
        ]
        
        for text, command in topics:
            btn = ttk.Button(self.main_frame, text=text, command=command)
            btn.pack(pady=5, fill='x', ipady=5)

    def create_frame(self, name, title):
        frame = ttk.Frame(self.root)
        self.frames[name] = frame
        
        ttk.Label(frame, text=title, style='Title.TLabel').pack(pady=20)
        back_btn = ttk.Button(frame, text="Назад", command=self.show_main)
        back_btn.pack(side='bottom', pady=20)
        return frame

    def show_main(self):
        for frame in self.frames.values():
            frame.pack_forget()
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Квадратные уравнения
    def create_quadratic_frame(self):
        frame = self.create_frame("quadratic", "Решение квадратных уравнений")
        
        inputs = ttk.Frame(frame)
        inputs.pack(pady=10)
        
        ttk.Label(inputs, text="a:").grid(row=0, column=0, padx=5)
        self.a_entry = ttk.Entry(inputs)
        self.a_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(inputs, text="b:").grid(row=1, column=0, padx=5)
        self.b_entry = ttk.Entry(inputs)
        self.b_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(inputs, text="c:").grid(row=2, column=0, padx=5)
        self.c_entry = ttk.Entry(inputs)
        self.c_entry.grid(row=2, column=1, padx=5)
        
        solve_btn = ttk.Button(frame, text="Решить", command=self.solve_quadratic)
        solve_btn.pack(pady=10)
        
        self.result_quadratic = ttk.Label(frame, text="")
        self.result_quadratic.pack()

    def solve_quadratic(self):
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            c = float(self.c_entry.get())
            
            D = b**2 - 4*a*c
            if D < 0:
                result = "Нет действительных корней"
            elif D == 0:
                x = -b / (2*a)
                result = f"Один корень: x = {x:.2f}"
            else:
                x1 = (-b + math.sqrt(D)) / (2*a)
                x2 = (-b - math.sqrt(D)) / (2*a)
                result = f"Два корня: x1 = {x1:.2f}, x2 = {x2:.2f}"
            
            self.result_quadratic.config(text=result)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")

    # Биквадратные уравнения
    def create_biquadratic_frame(self):
        frame = self.create_frame("biquadratic", "Решение биквадратных уравнений")
        
        inputs = ttk.Frame(frame)
        inputs.pack(pady=10)
        
        ttk.Label(inputs, text="a:").grid(row=0, column=0, padx=5)
        self.a_biquad_entry = ttk.Entry(inputs)
        self.a_biquad_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(inputs, text="b:").grid(row=1, column=0, padx=5)
        self.b_biquad_entry = ttk.Entry(inputs)
        self.b_biquad_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(inputs, text="c:").grid(row=2, column=0, padx=5)
        self.c_biquad_entry = ttk.Entry(inputs)
        self.c_biquad_entry.grid(row=2, column=1, padx=5)
        
        solve_btn = ttk.Button(frame, text="Решить", command=self.solve_biquadratic)
        solve_btn.pack(pady=10)
        
        self.result_biquadratic = ttk.Label(frame, text="")
        self.result_biquadratic.pack()

    def solve_biquadratic(self):
        try:
            a = float(self.a_biquad_entry.get())
            b = float(self.b_biquad_entry.get())
            c = float(self.c_biquad_entry.get())
            
            D = b**2 - 4*a*c
            if D < 0:
                result = "Нет действительных корней"
            else:
                y1 = (-b + math.sqrt(D)) / (2*a)
                y2 = (-b - math.sqrt(D)) / (2*a)
                
                roots = []
                if y1 >= 0:
                    roots.extend([math.sqrt(y1), -math.sqrt(y1)])
                if y2 >= 0:
                    roots.extend([math.sqrt(y2), -math.sqrt(y2)])
                
                if not roots:
                    result = "Нет действительных корней"
                else:
                    result = "Корни: " + ", ".join(f"{x:.2f}" for x in roots)
            
            self.result_biquadratic.config(text=result)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")

    # Системы линейных уравнений
    def create_linear_system_frame(self):
        frame = self.create_frame("linear_system", "Решение систем линейных уравнений")
        
        ttk.Label(frame, text="Формат: a1x + b1y = c1\na2x + b2y = c2").pack()
        
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        self.entries_linear = []
        for i in range(6):
            entry = ttk.Entry(input_frame, width=8)
            entry.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.entries_linear.append(entry)
        
        solve_btn = ttk.Button(frame, text="Решить", command=self.solve_linear_system)
        solve_btn.pack(pady=10)
        
        self.result_linear = ttk.Label(frame, text="")
        self.result_linear.pack()

    def solve_linear_system(self):
        try:
            a1 = float(self.entries_linear[0].get())
            b1 = float(self.entries_linear[1].get())
            c1 = float(self.entries_linear[2].get())
            a2 = float(self.entries_linear[3].get())
            b2 = float(self.entries_linear[4].get())
            c2 = float(self.entries_linear[5].get())
            
            det = a1*b2 - a2*b1
            if det == 0:
                self.result_linear.config(text="Система не имеет единственного решения")
            else:
                x = (b2*c1 - b1*c2) / det
                y = (a1*c2 - a2*c1) / det
                self.result_linear.config(text=f"Решение: x = {x:.2f}, y = {y:.2f}")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные коэффициенты")

    # Площадь фигур
    def create_geometry_frame(self):
        frame = self.create_frame("geometry", "Площадь фигур")
        
        self.shape_var = tk.StringVar()
        shapes = ["Круг", "Треугольник", "Прямоугольник"]
        shape_menu = ttk.Combobox(frame, textvariable=self.shape_var, values=shapes, state="readonly")
        shape_menu.pack(pady=10)
        
        ttk.Button(frame, text="Рассчитать", command=self.calculate_area).pack(pady=10)
        self.result_geom = ttk.Label(frame, text="")
        self.result_geom.pack()

    def calculate_area(self):
        shape = self.shape_var.get()
        try:
            if shape == "Круг":
                r = float(simpledialog.askstring("Ввод", "Введите радиус:"))
                area = pi * r**2
            elif shape == "Треугольник":
                a = float(simpledialog.askstring("Ввод", "Основание:"))
                h = float(simpledialog.askstring("Ввод", "Высота:"))
                area = 0.5 * a * h
            elif shape == "Прямоугольник":
                a = float(simpledialog.askstring("Ввод", "Длина:"))
                b = float(simpledialog.askstring("Ввод", "Ширина:"))
                area = a * b
            else:
                area = None
                
            self.result_geom.config(text=f"Площадь: {area:.2f}" if area else "Ошибка выбора")
        except:
            messagebox.showerror("Ошибка", "Некорректный ввод")

    # Теорема Пифагора
    def create_pythagoras_frame(self):
        frame = self.create_frame("pythagoras", "Теорема Пифагора")
        
        self.side_var = tk.StringVar(value="c")
        ttk.Radiobutton(frame, text="Гипотенузу (c)", variable=self.side_var, value="c").pack()
        ttk.Radiobutton(frame, text="Катет (a)", variable=self.side_var, value="a").pack()
        
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Сторона 1:").grid(row=0, column=0)
        self.pyth_a = ttk.Entry(input_frame)
        self.pyth_a.grid(row=0, column=1)
        
        ttk.Label(input_frame, text="Сторона 2:").grid(row=1, column=0)
        self.pyth_b = ttk.Entry(input_frame)
        self.pyth_b.grid(row=1, column=1)
        
        ttk.Button(frame, text="Вычислить", command=self.calculate_pythagoras).pack()
        self.result_pyth = ttk.Label(frame, text="")
        self.result_pyth.pack()

    def calculate_pythagoras(self):
        try:
            a = float(self.pyth_a.get())
            b = float(self.pyth_b.get())
            side = self.side_var.get()
            
            if side == "c":
                c = sqrt(a**2 + b**2)
                self.result_pyth.config(text=f"Гипотенуза: {c:.2f}")
            else:
                if max(a, b) <= min(a, b):
                    raise ValueError
                c = sqrt(abs(a**2 - b**2))
                self.result_pyth.config(text=f"Катет: {c:.2f}")
        except:
            messagebox.showerror("Ошибка", "Некорректные значения")

    # Проценты
    def create_percentage_frame(self):
        frame = self.create_frame("percentage", "Работа с процентами")
        
        self.percent_var = tk.IntVar()
        types = [
            ("Сколько % от числа", 0),
            ("Найти число по %", 1),
            ("Процентное соотношение", 2)
        ]
        for text, val in types:
            ttk.Radiobutton(frame, text=text, variable=self.percent_var, value=val).pack()
            
        input_frame = ttk.Frame(frame)
        input_frame.pack(pady=10)
        
        self.percent_entry1 = ttk.Entry(input_frame)
        self.percent_entry1.grid(row=0, column=1, padx=5)
        self.percent_entry2 = ttk.Entry(input_frame)
        self.percent_entry2.grid(row=1, column=1, padx=5)
        
        ttk.Label(input_frame, text="Число 1:").grid(row=0, column=0)
        ttk.Label(input_frame, text="Число 2:").grid(row=1, column=0)
        
        ttk.Button(frame, text="Вычислить", command=self.calculate_percentage).pack()
        self.result_percent = ttk.Label(frame, text="")
        self.result_percent.pack()

    def calculate_percentage(self):
        try:
            mode = self.percent_var.get()
            x = float(self.percent_entry1.get())
            y = float(self.percent_entry2.get())
            
            if mode == 0:
                result = (y / x) * 100
                text = f"{y} это {result:.1f}% от {x}"
            elif mode == 1:
                result = (x * y) / 100
                text = f"{y}% от {x} = {result:.2f}"
            elif mode == 2:
                result = (x / y) * 100
                text = f"{x} составляет {result:.1f}% от {y}"
                
            self.result_percent.config(text=text)
        except:
            messagebox.showerror("Ошибка", "Проверьте введенные значения")

    # Объем тел
    def create_volume_frame(self):
        frame = self.create_frame("volume", "Объем геометрических тел")
        
        self.volume_shape_var = tk.StringVar()
        shapes = ["Куб", "Сфера", "Цилиндр", "Конус"]
        shape_menu = ttk.Combobox(frame, textvariable=self.volume_shape_var, values=shapes, state="readonly")
        shape_menu.pack(pady=10)
        
        ttk.Button(frame, text="Рассчитать", command=self.calculate_volume).pack(pady=10)
        self.result_volume = ttk.Label(frame, text="")
        self.result_volume.pack()

    def calculate_volume(self):
        shape = self.volume_shape_var.get()
        try:
            if shape == "Куб":
                a = float(simpledialog.askstring("Ввод", "Длина ребра куба:"))
                volume = a**3
            elif shape == "Сфера":
                r = float(simpledialog.askstring("Ввод", "Радиус сферы:"))
                volume = (4/3) * pi * r**3
            elif shape == "Цилиндр":
                r = float(simpledialog.askstring("Ввод", "Радиус основания:"))
                h = float(simpledialog.askstring("Ввод", "Высота цилиндра:"))
                volume = pi * r**2 * h
            elif shape == "Конус":
                r = float(simpledialog.askstring("Ввод", "Радиус основания:"))
                h = float(simpledialog.askstring("Ввод", "Высота конуса:"))
                volume = (1/3) * pi * r**2 * h
            else:
                volume = None
                
            self.result_volume.config(text=f"Объем: {volume:.2f}" if volume else "Ошибка выбора")
        except:
            messagebox.showerror("Ошибка", "Некорректный ввод")

    # Тригонометрия
    def create_trigonometry_frame(self):
        frame = self.create_frame("trigonometry", "Тригонометрия")
        
        self.trig_func_var = tk.StringVar()
        functions = ["sin(x)", "cos(x)", "tan(x)"]
        func_menu = ttk.Combobox(frame, textvariable=self.trig_func_var, values=functions, state="readonly")
        func_menu.pack(pady=10)
        
        ttk.Label(frame, text="Угол (градусы):").pack()
        self.angle_entry = ttk.Entry(frame)
        self.angle_entry.pack()
        
        ttk.Button(frame, text="Вычислить", command=self.calculate_trig).pack(pady=10)
        self.result_trig = ttk.Label(frame, text="")
        self.result_trig.pack()

    def calculate_trig(self):
        try:
            func = self.trig_func_var.get()
            angle = float(self.angle_entry.get())
            radians = math.radians(angle)
            
            if func == "sin(x)":
                result = sin(radians)
            elif func == "cos(x)":
                result = cos(radians)
            elif func == "tan(x)":
                result = tan(radians)
            else:
                result = None
                
            self.result_trig.config(text=f"{func} = {result:.4f}" if result else "Ошибка выбора")
        except:
            messagebox.showerror("Ошибка", "Некорректный ввод")

    # Арифметическая прогрессия
    def create_arithmetic_prog_frame(self):
        frame = self.create_frame("arithmetic_prog", "Арифметическая прогрессия")
        
        ttk.Label(frame, text="Первый член (a1):").pack()
        self.a1_entry = ttk.Entry(frame)
        self.a1_entry.pack()
        
        ttk.Label(frame, text="Разность (d):").pack()
        self.d_entry = ttk.Entry(frame)
        self.d_entry.pack()
        
        ttk.Label(frame, text="Номер члена (n):").pack()
        self.n_entry = ttk.Entry(frame)
        self.n_entry.pack()
        
        ttk.Button(frame, text="Вычислить", command=self.calculate_arithmetic_prog).pack(pady=10)
        self.result_arithmetic = ttk.Label(frame, text="")
        self.result_arithmetic.pack()

    def calculate_arithmetic_prog(self):
        try:
            a1 = float(self.a1_entry.get())
            d = float(self.d_entry.get())
            n = int(self.n_entry.get())
            
            an = a1 + (n - 1) * d
            self.result_arithmetic.config(text=f"{n}-й член: {an:.2f}")
        except:
            messagebox.showerror("Ошибка", "Некорректный ввод")

    # Геометрическая прогрессия
    def create_geometric_prog_frame(self):
        frame = self.create_frame("geometric_prog", "Геометрическая прогрессия")
        
        ttk.Label(frame, text="Первый член (b1):").pack()
        self.b1_entry = ttk.Entry(frame)
        self.b1_entry.pack()
        
        ttk.Label(frame, text="Знаменатель (q):").pack()
        self.q_entry = ttk.Entry(frame)
        self.q_entry.pack()
        
        ttk.Label(frame, text="Номер члена (n):").pack()
        self.n_geom_entry = ttk.Entry(frame)
        self.n_geom_entry.pack()
        
        ttk.Button(frame, text="Вычислить", command=self.calculate_geometric_prog).pack(pady=10)
        self.result_geometric = ttk.Label(frame, text="")
        self.result_geometric.pack()

    def calculate_geometric_prog(self):
        try:
            b1 = float(self.b1_entry.get())
            q = float(self.q_entry.get())
            n = int(self.n_geom_entry.get())
            
            bn = b1 * (q ** (n - 1))
            self.result_geometric.config(text=f"{n}-й член: {bn:.2f}")
        except:
            messagebox.showerror("Ошибка", "Некорректный ввод")

    # Методы для отображения фреймов
    def show_quadratic(self): self._show_frame('quadratic')
    def show_biquadratic(self): self._show_frame('biquadratic')
    def show_linear_system(self): self._show_frame('linear_system')
    def show_geometry(self): self._show_frame('geometry')
    def show_pythagoras(self): self._show_frame('pythagoras')
    def show_percentage(self): self._show_frame('percentage')
    def show_volume(self): self._show_frame('volume')
    def show_trigonometry(self): self._show_frame('trigonometry')
    def show_arithmetic_prog(self): self._show_frame('arithmetic_prog')
    def show_geometric_prog(self): self._show_frame('geometric_prog')
    
    def _show_frame(self, name):
        self.main_frame.pack_forget()
        self.frames[name].pack(expand=True, fill='both', padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = MathApp(root)
    root.mainloop()
