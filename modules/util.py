from modules import package
from typing import Dict, List
import os, datetime, ast, sys, subprocess, json, time, ctypes, asyncio

try:
    import colorama
    import fade, random, discord, requests, pystyle
    import cursor
    from colorama import Fore
    import rich
    from rich.console import Console
    from pypresence import Presence
    from modules import init
except ImportError as e:
    if "discord" in e.name:
        package.install_module(module="discord.py-self")
    else:
        package.install_module(module=e.name)
        print(f"Installed missing module {e.name}, restarting..")
    package.restart()

console = Console(
        color_system="auto", 
        legacy_windows=True,
        #soft_wrap=True
    )
version = 6.01
global rpc

def clear():
    os.system("clear" if os.name != "nt" else "cls")

def set_title(title: str):
    if os.name == "nt":
        ctypes.windll.kernel32.SetConsoleTitleW(f"{title}")
    elif os.name == "posix":
        print(f"\x1b]2;{title}\x07")


def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S, %m/%d/%y")

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

def check_for_update():
    with open("./config.json") as f:
        config = json.load(f)
    if config["Automatically Check for Updates"]:
        r = requests.get(url="https://raw.githubusercontent.com/coital/nuked/main/version")
        ver = float(r.text)
        if ver > version:
            clear()
            console.bell()
            log(f"[blink][link=https://github.com/coital/nuked]Update for Nuked is available[/link]![/blink] New version: v{ver}, current version: v{version}")
            log("You can update by replacing the core files with the ones at https://github.com/coital/nuked")
            input()

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
    for letter in "Welcome":
        console.print(letter, justify="center")
        time.sleep(0.1)
    clear()

def splash():
    colorama.init(strip=True, convert=True, autoreset=True)
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
    console.print(splash, justify="center", end="")
    colorama.deinit()
    console.print(f"{version}\n", justify="center", style="reset")
    r = requests.get("https://raw.githubusercontent.com/coital/nuked/main/motd")
    if r.status_code in (200, 204):
        console.print(f"MOTD: [bold]{r.text}[/]", justify="center")
    

def error(content: str):
    console.print(f"\n[reset][red][bright][{get_time()}][/bright][/red] {content}[/reset]", end="")

def log(content: str):
    console.print(f"\n[reset][cyan][bright][{get_time()}][/bright][/cyan] {content}[/reset]", end="")

def setup_rich_presence() -> bool:
    global rpc
    try:
        rpc = Presence(client_id="916855918552023081")
        rpc.connect()
        rpc.update(details=f"Connected | {version}",
                large_image="avatar", start=time.time(),
                join="Join")
        return True
    except Exception as e:
        error(f"RPC Failed to initialize: [bold]{e}[/bold].")
        time.sleep(2.5)
    return False
def enable_rich_presence() -> bool:
    return setup_rich_presence()

def disable_rich_presence() -> bool:
    global rpc
    rpc.close()
    return True