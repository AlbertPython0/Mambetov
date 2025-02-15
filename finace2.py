import subprocess
import sys
import tkinter as tk
from tkinter import ttk

# Список необходимых библиотек
required_packages = [
    'numpy',
    'pandas',
    'openpyxl',
    'tkinter',  # tkinter обычно предустановлен, но можно добавить для уверенности
]

def is_package_installed(package):
    """Проверяет, установлена ли библиотека."""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def install(package, progress_var, output_text):
    """Устанавливает пакет и обновляет прогресс."""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        output_text.insert(tk.END, f'Успешно установлена библиотека: {package}\n')
    except Exception as e:
        output_text.insert(tk.END, f'Не удалось установить библиотеку {package}: {e}\n')
    finally:
        progress_var.set(progress_var.get() + (100 / len(required_packages)))

def start_installation(progress_var, output_text):
    """Запускает установку всех пакетов."""
    for package in required_packages:
        if not is_package_installed(package):
            install(package, progress_var, output_text)
        else:
            output_text.insert(tk.END, f'Библиотека уже установлена: {package}\n')
            progress_var.set(progress_var.get() + (100 / len(required_packages)))

def main():
    # Создаем главное окно
    root = tk.Tk()
    root.title("Установка библиотек")
    root.geometry("400x300")

    # Создаем переменную для прогресса
    progress_var = tk.DoubleVar()

    # Создаем виджет прогресс бара
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
    progress_bar.pack(pady=20, fill=tk.X, padx=20)

    # Создаем текстовое поле для вывода
    output_text = tk.Text(root, height=10, width=50)
    output_text.pack(pady=10, padx=10)

    # Создаем кнопку для начала установки
    start_button = tk.Button(root, text="Начать установку", command=lambda: start_installation(progress_var, output_text))
    start_button.pack(pady=10)

    # Запускаем главный цикл
    root.mainloop()

if __name__ == "__main__":
    main()





import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime
from tkinter import messagebox
import openpyxl
from tkinter import filedialog

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('finance.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS finance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT,
                costs TEXT,
                total REAL,
                date TEXT
            )
        ''')
        self.conn.commit()

    def insert_data(self, description, costs, total, date):
        self.c.execute('''
            INSERT INTO finance(description, costs, total, date) VALUES (?, ?, ?, ?)
        ''', (description, costs, total, date))
        self.conn.commit()

    def update_data(self, id, description, costs, total):
        self.c.execute('''UPDATE finance SET description=?, costs=?, total=? WHERE id=?''',
                       (description, costs, total, id))
        self.conn.commit()

    def delete_data(self, id):
        self.c.execute('DELETE FROM finance WHERE id=?', (id,))
        self.conn.commit()

    def fetch_all(self):
        self.c.execute('SELECT * FROM finance')
        return self.c.fetchall()

    def fetch_totals(self):
        self.c.execute('SELECT SUM(total) FROM finance')
        total_all = self.c.fetchone()[0] or 0
        self.c.execute('SELECT SUM(total) FROM finance WHERE date >= date("now", "start of month")')
        total_month = self.c.fetchone()[0] or 0
        self.c.execute('SELECT SUM(total) FROM finance WHERE date >= date("now", "start of year")')
        total_year = self.c.fetchone()[0] or 0
        return total_all, total_month, total_year


class Child(tk.Toplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить расходы/доходы')
        self.geometry('400x300')
        self.resizable(False, False)
        self.configure(bg='#f0f0f0')

        label_description = tk.Label(self, text='Наименование:', bg='#f0f0f0', font=('Arial', 10))
        label_description.place(x=50, y=50)
        label_selection = tk.Label(self, text='Статья дохода/расхода:', bg='#f0f0f0', font=('Arial', 10))
        label_selection.place(x=50, y=80)
        label_sum = tk.Label(self, text='Сумма:', bg='#f0f0f0', font=('Arial', 12))
        label_sum.place(x=50, y=110)
        label_date = tk.Label(self, text='Дата (ДД.ММ.ГГГГ):', bg='#f0f0f0', font=('Arial', 10))
        label_date.place(x=50, y=140)

        self.entry_description = ttk.Entry(self, font=('Arial', 10))
        self.entry_description.place(x=200, y=50)

        self.entry_money = ttk.Entry(self, font=('Arial', 10))
        self.entry_money.place(x=200, y=110)

        self.combobox = ttk.Combobox(self, values=[u'Доход', u'Расход'], font=('Arial', 10))
        self.combobox.current(0)
        self.combobox.place(x=200, y=80)

        self.entry_date = ttk.Entry(self, font=('Arial', 10))
        self.entry_date.place(x=200, y=140)
        self.entry_date.bind("<KeyRelease>", self.format_date)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=240)

        self.btn_ok = ttk.Button(self, text='Добавить', command=self.on_add)
        self.btn_ok.place(x=220, y=240)

        self.grab_set()
        self.focus_set()

    def format_date(self, event):
        date_str = self.entry_date.get().replace('.', '')
        if len(date_str) >= 2:
            date_str = date_str[:2] + '.' + date_str[2:]
        if len(date_str) >= 5:
            date_str = date_str[:5] + '.' + date_str[5:]
        self.entry_date.delete(0, tk.END)
        self.entry_date.insert(0, date_str)

    def on_add(self):
        description = self.entry_description.get().strip()
        costs = self.combobox.get().strip()
        total_value = self.entry_money.get().strip()
        date = self.entry_date.get().strip() if self.entry_date.get() else datetime.now().strftime('%d.%m.%Y')

        if not description or not costs or not total_value:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля.")
            return

        try:
            total_value = float(total_value)
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом.")
            return

        self.view.records(description, costs, total_value, date)
        self.destroy()


class Update(Child):
    def __init__(self, app, record):
        super().__init__(app)
        self.view = app
        self.record = record
        self.init_edit()
        self.fill_fields()

    def fill_fields(self):
        self.entry_description.insert(0, self.record[1])
        self.combobox.set(self.record[2])
        self.entry_money.insert(0, self.record[3])
        self.entry_date.insert(0, self.record[4])

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать', command=self.on_edit)
        btn_edit.place(x=205, y=170)
        self.btn_ok.destroy()

    def on_edit(self):
        id = self.record[0]
        total_value = float(self.entry_money.get()) if self.entry_money.get() else 0
        self.view.update_records(id, self.entry_description.get(), self.combobox.get(), total_value)
        self.destroy()


class Main(tk.Frame):
    def __init__(self, root, db):
        super().__init__(root)
        self.root = root
        self.db = db
        self.init_main()
        self.view_records()
        self.update_totals()

    def init_main(self):
        self.configure(bg='#f0f0f0')

        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Добавить позицию', command=self.open_dialog, bg='#4CAF50', fg='white', bd=0, font=('Arial', 12))
        btn_open_dialog.pack(side=tk.LEFT, padx=5, pady=5)

        btn_edit_dialog = tk.Button(toolbar, text='Редактировать', bg='#2196F3', fg='white', bd=0, command=self.open_update_dialog, font=('Arial', 12))
        btn_edit_dialog.pack(side='left', padx=5, pady=5)

        btn_delete_dialog = tk.Button(toolbar, text='Удалить позицию', bg='#F44336', fg='white', bd=0, command=self.delete_record, font=('Arial', 12))
        btn_delete_dialog.pack(side='left', padx=5, pady=5)

        btn_export = tk.Button(toolbar, text='Экспорт в Excel', command=self.export_to_excel, bg='#FFC107', fg='white', bd=0, font=('Arial', 12))
        btn_export.pack(side='left', padx=5, pady=5)

        self.search_entry = ttk.Entry(toolbar, font=('Arial', 10))
        self.search_entry.pack(side=tk.LEFT, padx=5, pady=5)

        btn_search = tk.Button(toolbar, text='Поиск', command=self.search_records)
        btn_search.pack(side=tk.LEFT, padx=5, pady=5)

        self.tree = ttk.Treeview(self, columns=('id', 'description', 'costs', 'total', 'date'), height=15, show='headings')

        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.column('description', width=265, anchor=tk.CENTER)
        self.tree.column('costs', width=150, anchor=tk.CENTER)
        self.tree.column('total', width=100, anchor=tk.CENTER)
        self.tree.column('date', width=100, anchor=tk.CENTER)

        self.tree.heading('id', text='ID')
        self.tree.heading('description', text='Наименование')
        self.tree.heading('costs', text='Статья дохода/расхода')
        self.tree.heading('total', text='Сумма')
        self.tree.heading('date', text='Дата')

        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        self.label_month_total = tk.Label(self, text='Итоги за месяц: 0', bg='#f0f0f0', font=('Arial', 12))
        self.label_month_total.pack(side=tk.BOTTOM, anchor='w', padx=10)

        self.label_year_total = tk.Label(self, text='Итоги за год: 0', bg='#f0f0f0', font=('Arial', 12))
        self.label_year_total.pack(side=tk.BOTTOM, anchor='w', padx=10)

        self.label_total_all = tk.Label(self, text='Итоги за все время: 0', bg='#f0f0f0', font=('Arial', 12))
        self.label_total_all.pack(side=tk.BOTTOM, anchor='w', padx=10)

    def records(self, description, costs, total, date):
        self.db.insert_data(description, costs, total, date)
        self.view_records()
        self.update_totals()

    def update_records(self, id, description, costs, total):
        self.db.update_data(id, description, costs, total)
        self.view_records()
        self.update_totals()

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record = self.tree.item(selected_item)['values']
            if messagebox.askquestion('Внимание!', 'Вы точно хотите удалить позицию?') == 'yes':
                self.db.delete_data(record[0])
                self.view_records()
                self.update_totals()

    def export_to_excel(self):
        # Открываем диалог для выбора папки
        folder_selected = filedialog.askdirectory()
        if not folder_selected:  # Проверяем, выбрана ли папка
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите папку для экспорта.")
            return

        # Формируем полный путь к файлу
        file_path = f"{folder_selected}/finance.xlsx"

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Finance Data'

        # Заголовки столбцов
        headers = ['ID', 'Наименование', 'Статья дохода/расхода', 'Сумма', 'Дата']
        sheet.append(headers)

        # Заполнение данными
        for row in self.db.fetch_all():
            sheet.append(row)

        # Сохранение файла
        workbook.save(file_path)
        messagebox.showinfo("Экспорт", f"Данные успешно экспортированы в {file_path}")

    def view_records(self):
        records = self.db.fetch_all()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in records]

    def open_dialog(self):
        Child(self)

    def open_update_dialog(self):
        selected_item = self.tree.selection()
        if selected_item:
            record = self.tree.item(selected_item)['values']
            Update(self, record)

    def update_totals(self):
        total_all, total_month, total_year = self.db.fetch_totals()
        self.label_month_total.config(text=f'Итоги за месяц: {total_month}')
        self.label_year_total.config(text=f'Итоги за год: {total_year}')
        self.label_total_all.config(text=f'Итоги за все время: {total_all}')

    def search_records(self):
        search_query = self.search_entry.get().strip()
        if not search_query:
            messagebox.showinfo("Поиск", "Пожалуйста, введите текст для поиска.")
            return

        self.db.c.execute("SELECT * FROM finance WHERE description LIKE ?", ('%' + search_query + '%',))
        records = self.db.c.fetchall()

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in records]


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root, db)
    app.pack(fill=tk.BOTH, expand=True)
    root.title("Household Finance")
    root.geometry("800x600")  # Увеличенный размер окна
    root.resizable(True, True)  # Возможность изменения размера окна
    root.mainloop()