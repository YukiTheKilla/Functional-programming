import asyncio
from tkinter import ttk, Scrollbar, Text
import tkinter as tk

class client:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8888
        self.reader = None
        self.writer = None
        self.designer = None

    async def start_client(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("Подключено к серверу")

        await self.receive_message()
        self.writer.close()

    async def send_message(self, message):
        if message == "":
            await self.error("Неверные входные данные")
            return
        self.writer.write(message.encode())
        await self.writer.drain()
        if message == "exit":
            return

    async def receive_message(self):
        while True:
            message = await self.reader.read(1024)
            print(f"{message.decode().strip()}")
            await self.designer.receive_message(message.decode().strip())
            if "Клиент отключен от сервера" in message.decode().strip():
                return

    async def send_message_to_server(self, writer, message):
        writer.write(message.encode())
        await writer.drain()
        if message == "exit":
            return


    async def error(self, message):
        print(f"Ошибка: {message}")

class designer:
    def __init__(self, client):
        self.client = client
        self.message_queue = asyncio.Queue()

        self.root = tk.Tk()
        self.root.title("Клиент")
        self.root.geometry('400x600')
        self.root['background'] = "white"
        self.root.resizable(True, True)

        self.style_frame = ttk.Style()
        self.style_frame.configure("TFrame", background="white")

        self.style_label = ttk.Style()
        self.style_label.configure("TLabel", font=("Arial", 14), padding=10, foreground="white", background="gray")

        self.style_label_message = ttk.Style()
        self.style_label_message.configure("TLabelMessage", font=("Arial", 14))

        self.output_frame = ttk.Frame(self.root, style="TFrame")

        self.message_text = Text(self.output_frame, wrap="word", state="disabled", font=("Arial", 14), height=20)
        self.message_text.pack(fill=tk.BOTH, expand=True)
        
        self.style_input = ttk.Style()
        self.style_input.configure("TEntry", font=("Arial", 14), padding=10, foreground="black", background="gray")
        
        self.input_frame = ttk.Frame(self.root, style="TFrame")
        
        scrollbar = tk.Scrollbar(self.root, command=self.message_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_text.config(yscrollcommand=scrollbar.set)

        self.send_Entry = ttk.Entry(self.input_frame, style="TEntry", width=78, justify="left")
        self.send_Entry.grid(row=0, column=0, sticky="ew")
        self.send_Entry.bind('<Return>', lambda event: asyncio.create_task(self.send_message()))

        self.history = list()

        self.output_frame.pack(fill=tk.BOTH, expand=True) 

        self.input_frame.pack(fill=tk.X, anchor="s")

    def click(self):
        asyncio.create_task(self.send_message())

    async def send_message(self):
        message = self.send_Entry.get()
        await self.message_queue.put(message)
        self.send_Entry.delete(0, "end")

    async def receive_message(self, message):
        self.message_text.config(state="normal")
        self.message_text.insert(tk.END, message + "\n")
        self.message_text.see(tk.END)
        self.message_text.config(state="disabled")
        self.send_Entry.delete(0, "end")

    async def process_messages(self):
        while True:
            message = await self.message_queue.get()
            await self.client.send_message(message)

    async def update(self, interval=0.05):
        while True:
            self.root.update()
            await asyncio.sleep(interval)
            
    

async def main():
    my_client = client()
    my_des = designer(my_client)
    my_client.designer = my_des

    tasks = [
        asyncio.create_task(my_client.start_client()),
        asyncio.create_task(my_des.update()),
        asyncio.create_task(my_des.process_messages()),
    ]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
