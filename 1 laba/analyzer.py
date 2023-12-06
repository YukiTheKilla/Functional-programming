import tkinter as tk
from tkinter import filedialog
import csv
import config
import os
import nltk
import concurrent.futures

nltk.download("punkt")
nltk.download("stopwords")

csv_file_paths = [
    r'C:\Users\Acer\Desktop\study\functional programming\1 laba\TG_log\chat_log.csv',
    rf'C:\Users\Acer\Desktop\study\functional programming\1 laba\VK_log\{config.domain}.csv'
]

# Путь для сохранения результатов
results_path = r'C:\Users\Acer\Desktop\study\functional programming\1 laba\results'

from nltk.corpus import stopwords
# Дополнительные слова для списка стоп-слов
additional_stop_words = [
    'Word', 'Count', 'Total', 'Words', '-', '=', 'ты', 'да', 'the', 'у', '`', 'and',
    'все', 'ну', 'a', 'of', 'to', 'for', 'так', 'меня', 'но', 'там', 'i', 'echo',
    '<<', 'мне', 'если', 'щас', 'ок', 'нет', 'тебе', 'есть', 'или', 'тебя', '>>',
    'можно', 'привет', 'через', 'сегодня', '%temp%\\temp.vbs', 'in', 'завтра', 'надо',
    '{', '1', 'го', 'потом', 'хорошо', 'чё', '?', '}', 'уже', 'только', 'может', 'ещё',
    'ща', 'могу', 'до', 'it', 'буду', 'is', 'int', 'can', 'reg', '\/v', '\/d',
    'add', '<', 'же', '2', '10', 'минут', '5', '\/f', 'просто', 'когда', 'cloud-based', 'as', 'data', '3', 'из',
    'блять', 'this', 'мин', 'после', 'if', '%', '\/t', 'еще', 'знаю', 'будет', 'be', '{`', 'тут', 'time',
]

# Объединим список стоп-слов из NLTK и дополнительные стоп-слова
stop_words = set(stopwords.words("russian") + additional_stop_words)

def analyze_csv_file(file_path):
    try:
        word_count = {}
        total_words = 0  # Добавляем счетчик общего количества слов
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                for word in row:
                    # Разбить строку на слова (просто разделите по пробелам)
                    words = word.split()
                    total_words += len(words)  # Обновляем счетчик общего количества слов
                    for w in words:
                        w = w.strip().lower()  # Преобразовать в нижний регистр и убрать пробелы
                        if w and w not in stop_words:  # Исключить стоп-слова
                            word_count[w] = word_count.get(w, 0) + 1
        
        # Список кортежей (слово, количество) из словаря
        word_count_list = [(word, count) for word, count in word_count.items()]
        
        # Сортируем список по количеству слов в убывающем порядке
        sorted_word_count = sorted(word_count_list, key=lambda x: x[1], reverse=True)
        
        # Создайте CSV файл и сохраните в него результаты в папке results
        output_file = os.path.join(results_path, f'result_{os.path.basename(file_path)}')
        with open(output_file, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Word', 'Count'])  # Запись заголовка
            csv_writer.writerow(['Total Words', total_words])  # Записываем общее количество слов
            csv_writer.writerows(sorted_word_count)  # Запись данных
        
        print(f'Results saved to {output_file}')
    except FileNotFoundError as e:
        print(f"Файл '{file_path}' не найден: {e}")
    except Exception as e:
        print(f"Произошла ошибка при анализе файла {file_path}: {str(e)}")

def analyze_files():
    file_paths_text = file_paths_entry.get("1.0", "end-1c")
    file_paths = [path.strip() for path in file_paths_text.split('\n') if path.strip()]

    if not file_paths:
        result_label.config(text="Пожалуйста, введите пути к файлам.")
        return

    def analyze_single_file(file_path):
        analyze_csv_file(file_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(file_paths)) as executor:
        for file_path in file_paths:
            executor.submit(analyze_single_file, file_path)

    result_label.config(text="Анализ завершен. Результаты сохранены.")
    
def browse_files():
    file_paths = filedialog.askopenfilenames(title="Выберите файлы", filetypes=[("CSV files", "*.csv")])
    file_paths_entry.delete(1.0, tk.END)  # Очистка текстовго поля
    for file_path in file_paths:
        file_paths_entry.insert(tk.END, file_path + '\n')

root = tk.Tk()
root.title("Анализ CSV файлов")

#Компоненты интерфейса
file_paths_label = tk.Label(root, text="Пути к файлам (каждый путь с новой строки):")
file_paths_label.pack()
file_paths_entry = tk.Text(root, width=50, height=10)
file_paths_entry.pack()

browse_button = tk.Button(root, text="Обзор файлов", command=browse_files)
browse_button.pack()

analyze_button = tk.Button(root, text="Анализировать файлы", command=analyze_files)
analyze_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
