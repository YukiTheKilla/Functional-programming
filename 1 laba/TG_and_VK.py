import tkinter as tk
from tkinter import ttk
import csv
from telethon.sync import TelegramClient
import requests
import time
import os
import config
import threading

# Определение функции get_comments перед использованием
def get_comments(post_id):
    comments = []
    response = requests.get("https://api.vk.com/method/wall.getComments",
        params={
            "access_token": config.VK_token,
            "v": config.API_version,
            "owner_id": config.domain,
            "post_id": post_id,
            "count": 100
        }
    )
    comments_data = response.json().get("response", {}).get("items", [])
    for comment in comments_data:
        text = comment.get("text", "")
        comments.append(text)
    return comments

# Создаем главное окно приложения
root = tk.Tk()
root.title("Social Media Logger")

# Создаем вкладку для Telegram
telegram_tab = ttk.Frame(root)
telegram_tab.grid(row=0, column=0, padx=10, pady=10)
notebook = ttk.Notebook(telegram_tab)
notebook.grid(row=0, column=0, padx=10, pady=10)

# Создаем вкладку для логирования чата в Telegram
def log_telegram_chats(chat_usernames):
    for chat_username in chat_usernames:
        with TelegramClient(config.phone_number, config.API_id, config.API_hash) as client:
            csv_file_path = os.path.join(r'C:\Users\Acer\Desktop\study\functional programming\1 laba\log', f'TG_{chat_username}.csv')
            tick = 0

            with open(csv_file_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Message"])

                for message in client.iter_messages(chat_username):
                    try:
                        chat_message = message.text

                        # Лог csv
                        csv_writer = csv.writer(csvfile)
                        csv_writer.writerow([chat_message])

                    except Exception as e:
                        pass

                    # Политика ТГ
                    tick += 1
                    if tick >= config.message_cap:
                        break
                    time.sleep(1 / 30)
        print(f"DONE for {chat_username}..........................................................................................................")

telegram_chat_tab = ttk.Frame(notebook)
notebook.add(telegram_chat_tab, text="Логирование чата в Telegram")

# Создаем кнопку для логирования чата в Telegram
log_button_telegram = tk.Button(telegram_chat_tab, text="Начать логирование", command=lambda: log_telegram_chats(config.chat_username))
log_button_telegram.pack()

# Создаем вкладку для сбора постов из VK
def log_vk_posts(domains):
    def process_domain(domain):
        VK_all_posts = []
        offset = config.VK_offset_start
        time.sleep(1) 
        while offset < config.VK_offset_finish:
            response = requests.get("https://api.vk.com/method/wall.get",
                params={
                    "access_token": config.VK_token,
                    "v": config.API_version,
                    "domain": domain,
                    "count": config.number_of_statements_in_VK,
                    "offset": offset
                }
            )
            data = response.json().get("response", {}).get("items", [])
            time.sleep(0.1)
            offset += config.number_of_statements_in_VK
            VK_all_posts.extend(data)

        output_dir = "C:\\Users\\Acer\\Desktop\\study\\functional programming\\1 laba\\log"
        output_file = os.path.join(output_dir, f"VK_{domain}.csv")

        # Открываем файл в режиме "a" (append), если файл уже существует
        mode = "a" if os.path.exists(output_file) else "w"
        with open(output_file, mode, newline='') as file:
            csv_writer = csv.writer(file)

            # Если файл только что создан, записываем заголовок
            if mode == "w":
                csv_writer.writerow(["post_text", "comments"])

            for post in VK_all_posts:
                try:
                    post_text = post.get("text", "")
                    post_id = post.get("id", 0)
                    comments = get_comments(post_id)
                    csv_writer.writerow([post_text, "\n".join(comments)])
                except:
                    pass

        print(f"DONE for {domain}..........................................................................................................")

    threads = []
    for domain in domains:
        thread = threading.Thread(target=process_domain, args=(domain,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

vk_posts_tab = ttk.Frame(notebook)
notebook.add(vk_posts_tab, text="Логирование постов из VK")

# Создаем кнопку для логирования постов из VK
log_button_vk = tk.Button(vk_posts_tab, text="Начать логирование", command=lambda: log_vk_posts(config.domain))
log_button_vk.pack()

# Запускаем главный цикл приложения
root.mainloop()
