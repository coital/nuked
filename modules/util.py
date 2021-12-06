import os, fade, datetime, time, random, json, requests
from typing import Dict
from colorama import Fore
from rich.console import Console
from win10toast import ToastNotifier
from pypresence import Presence
from discord.ext import commands
toaster = ToastNotifier()
console = Console()
version = "v6.0"
version_float = 6.0


def clear():
    os.system("clear" if os.name != "nt" else "cls")

def get_time():
    return datetime.datetime.now().strftime("%H:%M, %m/%d/%y")

def setup_rich_presence():
    try:
        rpc = Presence(client_id="916855918552023081")
        rpc.connect()
        rpc.update(details=f"Connected | {version}",
                large_image="avatar", start=time.time())
    except Exception as e:
        error(f"RPC Failed to initialize, reason: {e}.")
        time.sleep(2.5)
        
def toast_message(message: str):
    toaster.show_toast(
                    "Nuked",
                    f"{message}",
                    duration=5,
                    threaded=True)

def check_for_update():
    with open("./config.json") as f:
        config = json.load(f)
    if config["Automatically Check for Updates"]:
        r = requests.get(url="https://raw.githubusercontent.com/coital/nuked/main/version")
        ver = float(r.text)
        if ver > version_float:
            clear()
            log(f"Update for Nuked is available at https://github.com/coital/nuked. New version: v{ver}, current version: v{version_float}")
            time.sleep(5)

def load_commands() -> Dict:
    commands_dict = []
    for file in os.listdir("./commands/fun/"):
        if file.endswith(".py"):
            commands_dict.append(f"commands.fun.{file[:-3]}")
    for file in os.listdir("./commands/malicious/"):
        if file.endswith(".py"):
            commands_dict.append(f"commands.malicious.{file[:-3]}")
    for file in os.listdir("./commands/nsfw/"):
        if file.endswith(".py"):
            commands_dict.append(f"commands.nsfw.{file[:-3]}")
    for file in os.listdir("./commands/utility/"):
        if file.endswith(".py"):
            commands_dict.append(f"commands.utility.{file[:-3]}")
    for file in os.listdir("./commands/"):
        if file.endswith(".py"):
            commands_dict.append(f"commands.{file[:-3]}")
    return commands_dict

def presplash():
    console = Console()
    for letter in "Welcome":
        console.print(letter, justify="center")
        time.sleep(0.15)
    clear()

def splash():
    with open("./config.json") as f:
        config = json.load(f)
    functions = [fade.purpleblue]
    if config["Random Splash Color"]:
        functions = [fade.brazil, fade.fire, fade.greenblue, fade.purpleblue, fade.random, fade.water]
    splash = random.choice(functions)("""                        
                                      ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗
                                      ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
                                      ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██║  ██║
                                      ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██║  ██║
                                      ██║ ╚████║╚██████╔╝██║  ██╗███████╗██████╔╝
                                      ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ 
    """)
    print(splash)
    console.print(version, justify="center")
    
def error(content: str):
    print(f"\n{Fore.LIGHTRED_EX}[{get_time()}]{Fore.RESET} {content}{Fore.RESET}")


def log(content: str):
    print(f"\n{Fore.CYAN}[{get_time()}]{Fore.RESET} {content}{Fore.RESET}")