import asyncio
from datetime import datetime

class server:
    def __init__(self):
        self.clients_rooms = dict()
        self.clents = set()
        
    async def message_for_server(self, client, room, message):
        print(f"Клиент {client[2]}, из комнаты {room}, {message}")
        
    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        await self.to_server(writer, "Введите имя")
        name_new_client = await reader.read(1024)
        name_new_client = name_new_client.decode().strip()
        new_client = (writer, reader, name_new_client)
        await self.message_for_server(client=new_client, room="Нет комнаты", message="Подключился к серверу")
        await self.to_server(writer, f"Теперь вы:{name_new_client}")

        while True:
            action = await new_client[1].read(1024)
            action = action.decode().strip()
            await self.message_for_server(new_client, "Нет комнаты", f"Выполнил команду {action}")
            if action == "help":
                await self.to_server(new_client[0],"")
                await self.to_server(new_client[0],"-c:create room")
                await self.to_server(new_client[0],"-e:enter room")
                await self.to_server(new_client[0],"-s:start chating")
                await self.to_server(new_client[0],"exit:exit room")
                continue
            if action == "-c":
                await self.create_room(new_client)
                users_room = await self.enter_room(new_client)
            elif action == "-e":
                self.clents.add((new_client, "Такой комнаты не существует"))
                users_room = await self.enter_room(new_client)
            elif action == "exit":
                await self.exit(new_client, "Такой комнаты не существует")
            else:
                await self.to_server(new_client[0], "Неизвестная команда")
                continue
            break
        
        await self.receive_message(new_client, users_room)
        
    async def to_server(self, writer, response):
        writer.write(f"{response}\n".encode())
        await writer.drain()
    async def receive_message(self, client, name_room):
        tasks = []
        while True:
            message = await client[1].read(1024)
            message = message.decode().strip()
            tasks.append(asyncio.create_task(self.message_for_server(client, name_room, f"Отправил сообщение: {message}")))
            
            if message == "exit":
                await self.exit(client, name_room)
                await tasks[0]
                return
            
            tasks.append(asyncio.create_task(self.sends_message(client, message, name_room)))
            await asyncio.gather(*tasks)
            tasks.clear()
            
    async def sends_message(self, send_client, message, name_room):
        tasks = []
        time_now = datetime.now()
        time_now = str(time_now)
        time_now = time_now[:time_now.rfind(":")]
        for client in self.clients_rooms[name_room]:
            if send_client == client:                
                client[0].write(f"Вы, {time_now}: {message}".encode())
            else:
                client[0].write(f"{send_client[2]}, {time_now}: {message}".encode())
            tasks.append(asyncio.create_task(client[0].drain()))
        await asyncio.gather(*tasks)
            
    async def create_room(self, client):
        await self.to_server(client[0], "Введите название комнаты")
        while True:
            name_room = await client[1].read(1024)
            name_room = name_room.decode().strip()
            if name_room in self.clients_rooms.keys():
                await self.to_server(client[0], "Комната с таким названием уже существует")
            else:
                self.clients_rooms[name_room] = [client]
                self.clents.add((client, name_room))
                await self.message_for_server(client, "Нет комнаты", f"Создал комнату {name_room}")
                break
        
    async def enter_room(self, client)->str:
        if (client, "Такой комнаты не существует") in self.clents:
            all_rooms = ""
            for line in self.clients_rooms.keys():
                all_rooms = all_rooms + line + "\n"
            await self.to_server(client[0], f"Введите название комнаты, для выполнения входа:\n{all_rooms}")
            while True:
                name_room = await client[1].read(1024)
                name_room = name_room.decode().strip()
                if name_room in self.clients_rooms.keys():
                    break
                await self.to_server(client[0], "Такой комнаты не существует")
            self.clients_rooms[name_room].append(client)
        else:
            for name_key, peoples_room in self.clients_rooms.items():
                if client in peoples_room:
                    name_room = name_key
        tasks = [           
        asyncio.create_task(self.to_server(client[0], f"Вы вошли в комнату {name_room}")),
        asyncio.create_task(self.message_for_server(client, "Нет комнаты", f"Вошел в комнату {name_room}"))
        ]
        
        while True:
            action = await client[1].read(1024)
            if action.decode().strip() == "-s":
                tasks.append(asyncio.create_task(self.to_server(client[0], "Вход выполнен успешно")))
                break
            else:
               await self.to_server(client[0], "неизвестаня команда") 
               
        tasks.append(asyncio.create_task(self.message_for_server(client, name_room, f"выполнил команду: start")))
        tasks.append(asyncio.create_task(self.sends_message(client, "вошел в комнату", name_room)))    
        
        asyncio.gather(*tasks)
        return name_room
    
    async def exit(self, client, users_room):
        await self.to_server(client[0], "Вы отключены от сервера")
        if users_room != "Такой комнаты не существует":
            self.clients_rooms[users_room].remove(client)
            await self.message_for_server(client, users_room, f"выполнил команду: exit") 
        client[0].close()

    async def start_server(self):
        server = await asyncio.start_server(
            self.handle_client, '127.0.0.1', 8888)
        addr = server.sockets[0].getsockname()
        print(f"сервер запущен на {addr}")

        async with server:
            await server.serve_forever()
if __name__ == "__main__":
    my_server = server()
    asyncio.run(my_server.start_server())
