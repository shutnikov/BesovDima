import tkinter as tk
from tkinter import messagebox
import random
import json
import os

# Предопределённые цитаты
quotes = [
    {"text": "Жизнь - это 10% того, что с тобой происходит, и 90% того, как ты реагируешь на это.", "author": "Чарльз Свиндолл", "topic": "жизнь"},
    {"text": "Лучше сделать и пожалеть, чем пожалеть, что не сделал.", "author": "Роберт Кийосаки", "topic": "мотивация"},
    {"text": "Успех — это способность идти от неудачи к неудаче без потери энтузиазма.", "author": "Винстон Черчилль", "topic": "успех"},
    {"text": "Только тот, кто рискнул пойти далеко, узнает, насколько он далеко может зайти.", "author": "Томас Джефферсон", "topic": "риски"},
    # Можно добавить ещё цитат
]

history = []
HISTORY_FILE = 'history.json'

def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []

def save_history():
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

# Создаем окно
root = tk.Tk()
root.title("Random Quote Generator")

# Обработчик закрытия для сохранения
def on_closing():
    save_history()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Фильтры
filter_frame = tk.Frame(root)
filter_frame.pack(pady=5)

tk.Label(filter_frame, text="Фильтр по автору:").grid(row=0, column=0, padx=5)
author_filter_var = tk.StringVar()
author_filter_entry = tk.Entry(filter_frame, textvariable=author_filter_var, width=20)
author_filter_entry.grid(row=0, column=1, padx=5)

tk.Label(filter_frame, text="Фильтр по теме:").grid(row=0, column=2, padx=5)
topic_filter_var = tk.StringVar()
topic_filter_entry = tk.Entry(filter_frame, textvariable=topic_filter_var, width=20)
topic_filter_entry.grid(row=0, column=3, padx=5)

# Функция фильтрации
def get_filtered_quotes():
    author_f = author_filter_var.get().lower()
    topic_f = topic_filter_var.get().lower()
    return [q for q in quotes if
            (author_f in q['author'].lower()) and
            (topic_f in q['topic'].lower())]

# Отображение цитаты
quote_frame = tk.Frame(root)
quote_frame.pack(pady=10)

quote_text = tk.Text(quote_frame, wrap='word', width=70, height=5, font=("Arial", 12))
quote_text.pack()

def display_quote(quote):
    quote_text.delete(1.0, tk.END)
    text = f"\"{quote['text']}\"\n\n— {quote['author']} ({quote['topic']})"
    quote_text.insert(tk.END, text)

# Генерация случайной цитаты
def generate_quote():
    filtered_quotes = get_filtered_quotes()
    if not filtered_quotes:
        messagebox.showinfo("Нет цитат", "Нет цитат, соответствующих фильтру.")
        return
    quote = random.choice(filtered_quotes)
    display_quote(quote)
    # Добавим в историю
    history.append(quote)
    update_history_list()

# Область истории
history_frame = tk.Frame(root)
history_frame.pack(pady=10)

tk.Label(history_frame, text="История:").pack()

history_listbox = tk.Listbox(history_frame, width=80, height=10)
history_listbox.pack()

def update_history_list():
    history_listbox.delete(0, tk.END)
    for h in reversed(history):
        display_str = f"\"{h['text']}\" — {h['author']} ({h['topic']})"
        history_listbox.insert(tk.END, display_str)

# Кнопка генерировать
generate_button = tk.Button(root, text="Сгенерировать цитату", command=generate_quote)
generate_button.pack(pady=5)

# Поля для добавления новой цитаты
add_frame = tk.LabelFrame(root, text="Добавить новую цитату")
add_frame.pack(pady=10, fill='x', padx=10)

tk.Label(add_frame, text="Текст:").grid(row=0, column=0, sticky='e')
new_text_entry = tk.Entry(add_frame, width=50)
new_text_entry.grid(row=0, column=1, padx=5, pady=2)

tk.Label(add_frame, text="Автор:").grid(row=1, column=0, sticky='e')
new_author_entry = tk.Entry(add_frame, width=50)
new_author_entry.grid(row=1, column=1, padx=5, pady=2)

tk.Label(add_frame, text="Тема:").grid(row=2, column=0, sticky='e')
new_topic_entry = tk.Entry(add_frame, width=50)
new_topic_entry.grid(row=2, column=1, padx=5, pady=2)

def add_new_quote():
    text = new_text_entry.get().strip()
    author = new_author_entry.get().strip()
    topic = new_topic_entry.get().strip()
    if not text or not author or not topic:
        messagebox.showwarning("Ошибка", "Все поля обязательно заполнить.")
        return
    new_q = {'text': text, 'author': author, 'topic': topic}
    quotes.append(new_q)
    messagebox.showinfo("Успех", "Цитата добавлена.")
    # Очистить поля
    new_text_entry.delete(0, tk.END)
    new_author_entry.delete(0, tk.END)
    new_topic_entry.delete(0, tk.END)

add_button = tk.Button(add_frame, text="Добавить цитату", command=add_new_quote)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

# Кнопка применить фильтры
filter_button = tk.Button(root, text="Применить фильтры", command=update_history_list)
filter_button.pack(pady=5)

# Загрузка истории при запуске
load_history()
update_history_list()

root.mainloop()