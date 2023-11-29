import os
import shutil
import subprocess
import tkinter as tk
import sqlite3

# Підключення до бази даних SQLite
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Створення таблиці користувачів (якщо не існує)
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (username TEXT, password TEXT, role TEXT)''')

# Функція реєстрації нового користувача
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    role = role_entry.get()
    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    message_label.config(text="Користувач зареєстрований!")

# Функція авторизації
def authenticate_user():
    username = username_entry.get()
    password = password_entry.get()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        role = user[2]
        # Тут можна додати логіку для різних ролей користувачів
        message_label.config(text=f"Успішно авторизовано! Роль: {role}")
    else:
        message_label.config(text="Невірне ім'я користувача або пароль!")

# Створення графічного інтерфейсу за допомогою Tkinter
root = tk.Tk()
root.title("Авторизація")

username_label = tk.Label(root, text="Ім'я користувача:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Пароль:")
password_label.pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

role_label = tk.Label(root, text="Роль:")
role_label.pack()
role_entry = tk.Entry(root)
role_entry.pack()

register_button = tk.Button(root, text="Реєстрація", command=register_user)
register_button.pack()

authenticate_button = tk.Button(root, text="Авторизація", command=authenticate_user)
authenticate_button.pack()

message_label = tk.Label(root, text="")
message_label.pack()

root.mainloop()


