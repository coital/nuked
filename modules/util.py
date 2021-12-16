from modules import package
from typing import Dict, List
import os, datetime, ast, sys, subprocess, json, time, ctypes

try:
    import fade, random, discord, requests
    import cursor
    from colorama import Fore
    from rich import color
    from rich.console import Console
    from pypresence import Presence
    from modules import init
    console = Console(color_system="auto")
except ImportError as e:
    if "discord" in e.name:
        package.install_module(module="discord.py-self")
    else:
        package.install_module(module=e.name)
        print(f"Installed missing module {e.name}, restarting..")
    package.restart()

version = "v6.0"
version_float = 6.0
global rpc

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def set_title(title: str):
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f"{title}")
    elif os.name == "posix":
        print(f"\x1b]2;{title}\x07")


def get_time():
    return datetime.datetime.now().strftime("%H:%M, %m/%d/%y")

def get_config():
    with open("./config.json") as f:
        return json.load(f)

def get_color():
    with open("./config.json") as f:
        config = json.load(f)
    match str(config["Theme"]).lower():
        case "default":
            return discord.Color(0xFAFAFA)
        case "light pink":
            return discord.Color(0xFFC0CB)
        case "light blue":
            return discord.Color(0xADD8E6)
        case _:
            return discord.Color(0xFAFAFA)
        
def toast_message(message: str):
    if os.name == "nt":
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
                    "Nuked",
                    f"{message}",
                    duration=5,
                    threaded=True)
    else:
        pass

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

def signal_handler(signal, frame):
    cursor.show()
    clear()
    console.print("Logging out of Nuked", justify="center")
    time.sleep(1)
    clear()
    exit(0)

def check_token(token: str):
    headers = {"Content-Type": "application/json", "authorization": token}
    r = requests.get(
        "https://discordapp.com/api/v9/users/@me/library", headers=headers)
    if r.status_code == 200:
        return
    else:
        os.remove(f'{os.getcwd()}/config.json')
        clear()
        error('Invalid token.')
        init.init()

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

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
    for file in os.listdir("./events/"):
        if file.endswith(".py"):
            commands_dict.append(f"events.{file[:-3]}")
    return commands_dict

def enable_light_mode() -> Dict:
    light_mode_commands = []
    for command in load_commands():
        if "light" not in command and "event" not in command:
            light_mode_commands.append(command)
    return light_mode_commands

def presplash():
    console = Console()
    for letter in "Welcome":
        console.print(letter, justify="center")
        time.sleep(0.1)
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
    console.print(f"[reset][bold]{version}[/bold][/reset]", justify="center")
    

def error(content: str):
    console.print(f"\n[reset][red][bright][{get_time()}][/bright][/red] {content}[/reset]")


def log(content: str):
    console.print(f"\n[reset][cyan][bright][{get_time()}][/bright][/cyan] {content}[/reset]")

def setup_rich_presence() -> bool:
    global rpc
    try:
        rpc = Presence(client_id="916855918552023081")
        rpc.connect()
        rpc.update(details=f"Connected | {version}",
                large_image="avatar", start=time.time(),
                join="Join")
    except Exception as e:
        error(f"RPC Failed to initialize: [bold]{e}[/bold].")
        time.sleep(2.5)

def enable_rich_presence() -> bool:
    return setup_rich_presence()

async def disable_rich_presence() -> bool:
    global rpc
    await rpc.clear()
    return True