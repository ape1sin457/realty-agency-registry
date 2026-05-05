import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- Логіка бази даних ---
def init_db():
    conn = sqlite3.connect('real_estate.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS apartments 
                      (id INTEGER PRIMARY KEY, address TEXT, rooms INTEGER, price REAL)''')
    conn.commit()
    conn.close()

def add_to_db(address, rooms, price):
    conn = sqlite3.connect('real_estate.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO apartments (address, rooms, price) VALUES (?, ?, ?)", (address, rooms, price))
    conn.commit()
    conn.close()

# --- Інтерфейс ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Реєстр нерухомості")
        self.geometry("600x500")

        # Поля введення
        tk.Label(self, text="Адреса:").pack(pady=5)
        self.addr_entry = tk.Entry(self, width=50)
        self.addr_entry.pack()

        tk.Label(self, text="Кількість кімнат:").pack(pady=5)
        self.rooms_entry = tk.Entry(self, width=20)
        self.rooms_entry.pack()

        tk.Label(self, text="Ціна ($):").pack(pady=5)
        self.price_entry = tk.Entry(self, width=20)
        self.price_entry.pack()

        # Кнопки
        tk.Button(self, text="Додати квартиру", command=self.save_data, bg="#e1e1e1").pack(pady=15)
        
        # Таблиця
        columns = ("ID", "Адреса", "Кімнати", "Ціна")
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.refresh_table()

    def save_data(self):
        addr = self.addr_entry.get()
        rooms = self.rooms_entry.get()
        price = self.price_entry.get()
        
        if addr and rooms and price:
            try:
                add_to_db(addr, int(rooms), float(price))
                self.addr_entry.delete(0, tk.END)
                self.rooms_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                self.refresh_table()
                messagebox.showinfo("Успіх", "Дані збережено!")
            except ValueError:
                messagebox.showerror("Помилка", "Ціна та кількість кімнат мають бути числами!")
        else:
            messagebox.showwarning("Помилка", "Заповніть всі поля")

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apartments")
        for row in cursor.fetchall():
            self.tree.insert("", tk.END, values=row)
        conn.close()

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
