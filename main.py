import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Файл для хранения данных
DATA_FILE = 'training_data.json'

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        
        # Создаем интерфейс
        self.create_input_frame()
        self.create_table()
        self.create_filters()
        # Загружаем существующие данные
        self.load_data()

    def create_input_frame(self):
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        # Поле для даты
        ttk.Label(frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0)
        self.date_entry = ttk.Entry(frame)
        self.date_entry.grid(row=0, column=1, padx=5)

        # Тип тренировки
        ttk.Label(frame, text="Тип тренировки:").grid(row=0, column=2)
        self.type_combo = ttk.Combobox(frame, values=["Кардио", "Силовая", "Йога", "Пилатес"])
        self.type_combo.grid(row=0, column=3, padx=5)

        # Длительность
        ttk.Label(frame, text="Длительность (мин):").grid(row=0, column=4)
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=0, column=5, padx=5)

        # Кнопка добавления
        ttk.Button(frame, text="Добавить тренировку", command=self.add_training).grid(row=0, column=6, padx=10)

    def create_table(self):
        self.tree = ttk.Treeview(self, columns=("Дата", "Тип", "Длительность"), show='headings')
        self.tree.heading('Дата', text='Дата')
        self.tree.heading('Тип', text='Тип тренировки')
        self.tree.heading('Длительность', text='Длительность')
        self.tree.pack(pady=10)

    def create_filters(self):
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0)
        self.filter_type = ttk.Combobox(filter_frame, values=["Все", "Кардио", "Силовая", "Йога", "Пилатес"])
        self.filter_type.current(0)
        self.filter_type.grid(row=0, column=1)
        self.filter_type.bind("<<ComboboxSelected>>", lambda e: self.apply_filters())

        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=2, padx=5)
        self.filter_date_entry = ttk.Entry(filter_frame)
        self.filter_date_entry.grid(row=0, column=3, padx=5)
        ttk.Button(filter_frame, text="Применить", command=self.apply_filters).grid(row=0, column=4, padx=5)
        ttk.Button(filter_frame, text="Сбросить", command=self.load_data).grid(row=0, column=5, padx=5)

    def validate_date(self, date_text):
        """
        Проверяет правильность формата даты.
        """
        try:
            datetime.strptime(date_text, '%d.%m.%Y')
            return True
        except ValueError:
            return False

    def add_training(self):
        date = self.date_entry.get()
        t_type = self.type_combo.get()
        duration = self.duration_entry.get()

        # Валидация
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ДД.ММ.ГГГГ.")
            return
        if not duration.isdigit() or int(duration) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return
        if not t_type:
            messagebox.showerror("Ошибка", "Выберите тип тренировки.")
            return

        # Добавляем запись в таблицу
        self.tree.insert('', 'end', values=(date, t_type, duration))
        # Обновляем JSON
        self.save_data()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_combo.set('')
        self.duration_entry.delete(0, tk.END)

    def save_data(self):
        data = []
        for item in self.tree.get_children():
            data.append(self.tree.item(item)['values'])
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Загрузка из файла
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for row in data:
                    self.tree.insert('', 'end', values=row)
        # Обновление фильтров
        self.filter_type.current(0)
        self.filter_date_entry.delete(0, tk.END)

    def apply_filters(self):
        # Перезагружаем все данные
        self.load_data()
        selected_type = self.filter_type.get()
        date_filter = self.filter_date_entry.get()

        # Фильтрация по типу
        if selected_type != "Все":
            for item in self.tree.get_children():
                if self.tree.set(item, 'Тип') != selected_type:
                    self.tree.delete(item)
        # Фильтр по дате
        if date_filter:
            for item in self.tree.get_children():
                if self.tree.set(item, 'Дата') != date_filter:
                    self.tree.delete(item)

if __name__ == '__main__':
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()