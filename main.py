import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- Логика базы данных ---
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

# --- Интерфейс ---
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Реєстр нерухомості")
        self.geometry("500x400")

        # Поля ввода
        tk.Label(self, text="Адреса:").pack()
        self.addr_entry = tk.Entry(self, width=40)
        self.addr_entry.pack()

        tk.Label(self, text="Кількість кімнат:").pack()
        self.rooms_entry = tk.Entry(self)
        self.rooms_entry.pack()

        tk.Label(self, text="Ціна ($):").pack()
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()

        # Кнопки
        tk.Button(self, text="Додати квартиру", command=self.save_data).pack(pady=10)
        
        # Таблица
        self.tree = ttk.Treeview(self, columns=("ID", "Адреса", "Кімнати", "Ціна"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Адреса", text="Адреса")
        self.tree.heading("Кімнати", text="Кімнати")
        self.tree.heading("Ціна", text="Ціна")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.refresh_table()

    def save_data(self):
        addr = self.addr_entry.get()
        rooms = self.rooms_entry.get()
        price = self.price_entry.get()
        
        if addr and rooms and price:
            add_to_db(addr, int(rooms), float(price))
            self.refresh_table()
            messagebox.showinfo("Успіх", "Дані збережено!")
        else:
            messagebox.showwarning("Помилка", "Заповніть всі поля")

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        conn = sqlite3.connect('real_estate.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apartments")
        for row in cursor.fetchall():
            self.tree.insert("",```

---

### 3. Що попросити в ІІ для заповнення пояснювальної записки:
Щ tk.END, values=row)
        conn.close()

if __name__ == "__main__":
    init_db()
    app = App()
    app.mainloop()
