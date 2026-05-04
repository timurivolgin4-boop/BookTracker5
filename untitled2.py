import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json

API_KEY = "ВАШ_API_КЛЮЧ"  # Замените на свой ключ с exchangerate-api.com
API_URL = "https://v6.exchangerate-api.com/v6/{}/latest/{}"

# Загрузка истории из файла
def load_history():
    try:
        with open('history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Сохранение истории в файл
def save_history(history):
    with open('history.json', 'w') as f:
        json.dump(history, f, indent=2)

# Получение списка валют (можно расширить)
CURRENCIES = ["USD", "EUR", "RUB", "GBP", "JPY", "CNY"]

# Конвертация валюты
def convert():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Введите положительное число!")
        return

    from_curr = from_combo.get()
    to_curr = to_combo.get()

    try:
        response = requests.get(API_URL.format(API_KEY, from_curr))
        data = response.json()
        rate = data['conversion_rates'][to_curr]
        result = amount * rate
        result_label.config(text=f"{to_curr} {result:.2f}")

        # Сохранение в историю
        history = load_history()
        history.append({
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "result": result,
            "rate": rate,
            "date": data['time_last_update_utc']
        })
        save_history(history)
        update_history_table()
    except Exception as e:
        messagebox.showerror("Ошибка", "Не удалось получить данные от API.")

# Обновление таблицы истории
def update_history_table():
    for i in history_table.get_children():
        history_table.delete(i)
    for item in load_history():
        history_table.insert('', 'end', values=(
            item['from'],
            item['to'],
            item['amount'],
            item['result'],
            item['rate'],
            item['date']
        ))

# Создание окна
window = tk.Tk()
window.title("Currency Converter")
window.geometry("600x500")
window.resizable(False, False)

# Виджеты
tk.Label(window, text="Из:").grid(row=0, column=0, padx=10, pady=10)
from_combo = ttk.Combobox(window, values=CURRENCIES, width=5)
from_combo.current(0)
from_combo.grid(row=0, column=1, padx=10, pady=10)

tk.Label(window, text="В:").grid(row=0, column=2, padx=10, pady=10)
to_combo = ttk.Combobox(window, values=CURRENCIES, width=5)
to_combo.current(1)
to_combo.grid(row=0, column=3, padx=10, pady=10)

tk.Label(window, text="Сумма:").grid(row=1, column=0, padx=10, pady=10)
amount_entry = tk.Entry(window, width=15)
amount_entry.grid(row=1, column=1, padx=10, pady=10)

convert_btn = tk.Button(window, text="Конвертировать", command=convert)
convert_btn.grid(row=1, column=3, padx=10, pady=10)

result_label = tk.Label(window, text="", font=("Arial", 14))
result_label.grid(row=2, column=0, columnspan=4, pady=20)

# Таблица истории
history_table = ttk.Treeview(window, columns=("Из", "В", "Сумма", "Результат", "Курс", "Дата"), show='headings')
for col in history_table["columns"]:
    history_table.heading(col, text=col)
history_table.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

update_history_table()

window.mainloop()