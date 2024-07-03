import time
import threading
from k_amino import Client, SubClient
from rich.console import Console

# Create console and client objects
console = Console()
client = Client()

# Prompt for login credentials
email = "sumeetbangi0@gmail.com"
password = "@Soul2413"
client.login(email=email, password=password)

# Global variables to control chat link updates
ncd_id = None
thread_id = None
ncd_client = None
stop_leaving = False

# Function to update chat link
def update_chat_link():
    global ncd_id, thread_id, ncd_client, stop_leaving
    while True:
        chat_link = client.get_from_link(console.input("[bold cyan]Chat link: "))
        ncd_id = chat_link.comId
        thread_id = chat_link.objectId
        ncd_client = SubClient(comId=ncd_id, client=client)
        stop_leaving = True  # Stop the current leave process
        time.sleep(1)
        stop_leaving = False  # Allow new leave process

# Function to leave chat with a countdown
def leave_chat_repeatedly():
    global stop_leaving
    try:
        while True:
            if ncd_client and thread_id and not stop_leaving:
                # Countdown
                for i in range(3, 0, -1):
                    console.print(f"[bold yellow]{i}", end='\r')
                    time.sleep(1)
                console.print("[bold red]Leaving the chat...", end='\r')
                time.sleep(1)  # Briefly show the leave message before clearing it
                ncd_client.leave_chat(chatId=thread_id)
                console.print("[bold red]Left the chat.", end='\r')
            time.sleep(3)
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}")

# Start the thread for updating chat link
threading.Thread(target=update_chat_link, daemon=True).start()

# Start the leave chat process
leave_chat_repeatedly()

