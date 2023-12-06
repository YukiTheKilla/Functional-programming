import tkinter as tk

# Function to save parameters to the config.py file
def save_parameters():
    config_path = "C:/Users/Acer/Desktop/study/functional programming/1 laba with interface/config.py"
    with open(config_path, "w") as file:
        file.write(f'VK_token = "{vk_token_entry.get()}"\n')
        file.write(f'API_version = {float(api_version_entry.get())}\n')
        file.write(f'domain = "{domain_entry.get()}"\n')
        file.write(f'number_of_statements_in_VK = {int(statements_in_vk_entry.get())}\n')
        file.write(f'VK_offset_start = {int(offset_start_entry.get())}\n')
        file.write(f'VK_offset_finish = {int(offset_finish_entry.get())}\n')
        file.write(f'API_id = "{api_id_entry.get()}"\n')
        file.write(f'API_hash = "{api_hash_entry.get()}"\n')
        file.write(f'phone_number = "{phone_number_entry.get()}"\n')
        file.write(f'chat_username = "{chat_username_entry.get()}"\n')
        file.write(f'message_cap = {int(message_cap_entry.get())}\n')
    print("Parameters saved to 'config.py' file.")

# Create the window
window = tk.Tk()
window.title("Configurator")

# Create a label and an input field for each parameter
vk_token_label = tk.Label(window, text="VK Token:")
vk_token_label.pack()
vk_token_entry = tk.Entry(window)
vk_token_entry.pack()

api_version_label = tk.Label(window, text="API Version:")
api_version_label.pack()
api_version_entry = tk.Entry(window)
api_version_entry.pack()

domain_label = tk.Label(window, text="VK Group Name:")
domain_label.pack()
domain_entry = tk.Entry(window)
domain_entry.pack()

statements_in_vk_label = tk.Label(window, text="Statements in VK:")
statements_in_vk_label.pack()
statements_in_vk_entry = tk.Entry(window)
statements_in_vk_entry.pack()

offset_start_label = tk.Label(window, text="Offset Start:")
offset_start_label.pack()
offset_start_entry = tk.Entry(window)
offset_start_entry.pack()

offset_finish_label = tk.Label(window, text="Offset Finish:")
offset_finish_label.pack()
offset_finish_entry = tk.Entry(window)
offset_finish_entry.pack()

api_id_label = tk.Label(window, text="Telegram API ID:")
api_id_label.pack()
api_id_entry = tk.Entry(window)
api_id_entry.pack()

api_hash_label = tk.Label(window, text="Telegram API Hash:")
api_hash_label.pack()
api_hash_entry = tk.Entry(window)
api_hash_entry.pack()

phone_number_label = tk.Label(window, text="Phone Number:")
phone_number_label.pack()
phone_number_entry = tk.Entry(window)
phone_number_entry.pack()

chat_username_label = tk.Label(window, text="Chat Username:")
chat_username_label.pack()
chat_username_entry = tk.Entry(window)
chat_username_entry.pack()

message_cap_label = tk.Label(window, text="Message Cap:")
message_cap_label.pack()
message_cap_entry = tk.Entry(window)
message_cap_entry.pack()

save_button = tk.Button(window, text="Save Parameters", command=save_parameters)
save_button.pack()

window.mainloop()
