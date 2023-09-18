from modules import package
import os, datetime, ast, sys, json, time, ctypes, asyncio

try:
    import fade, random, discord, requests, cursor
    from git import Repo    
    from rich.console import Console
    from pypresence import Presence
    from modules import init
    from colorama import deinit, init as cinit
except ImportError as e:
    if "discord" in e.name:
        package.install_module(module="discord.py-self")
    else:
        package.install_module(module=e.name)
        print(f"Installed missing module {e.name}, restarting..")
    package.restart()

if os.name == "nt":
    console = Console(
            color_system="auto", 
            legacy_windows=True,
        )
else:
    console = Console(color_system="auto")
utd_api = f"https://discord.com/api/v10"
version = 6.05
global rpc

def clear():
    sys.stdout.flush()
    os.system("clear" if os.name != "nt" else "cls")

def check_for_update():
    try:
        with open("./config.json") as f:
            config = json.load(f)
    except FileNotFoundError:
        return
    if config["Automatically Check for Updates"]:
        r = requests.get(url="https://raw.githubusercontent.com/coital/nuked/main/version?v=1")
        ver = float(r.text)
        if ver > version:
            if config["Auto Update"]:
                auto_update()
            else:
                clear()
                console.bell()
                log(f"[blink][link=https://github.com/coital/nuked]Update for Nuked is available[/link]![/blink] New version: v{ver}, current version: v{version}")
                log("You can update by replacing the core files with the ones at https://github.com/coital/nuked")
                input()
         

def auto_update():
    r = requests.get("https://raw.githubusercontent.com/coital/nuked/main/version")
    try:
        os.mkdir(f"./{r.text}")
    except:
        return
    repo = Repo.clone_from("git://github.com/coital/nuked.git", f"./{r.text}")
    repo.close()
    log(f"New Nuked version is in ./{r.text}.")

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
    """
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
    // rip embeds :(
    """
    return 0xfafafa
    
        
def toast_message(message: str):
    if os.name == "nt":
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
                    "Nuked",
                    f"{message}",
                    duration=5,
                    threaded=True)

def get_token(email: str, password: str):
    r = requests.post(f"{utd_api}/auth/login", json={"login":email,"password":password,"undelete":False,"captcha_key":None,"login_source":None,"gift_code_sku_id":None}, headers={"content-type": "application/json"})
    try:
        token = r.json()["token"]
    except:
        return None
    else:
        return token

def signal_handler(signal, frame):
    cursor.show()
    clear()
    console.print("Logging out of Nuked", justify="center")
    time.sleep(1)
    clear()
    check_for_update()
    exit(0)

def check_token(token: str):
    headers = {"Content-Type": "application/json", "authorization": token}
    r = requests.get(
        f"{utd_api}/users/@me/library", headers=headers)
    if r.status_code == 200:
        return
    else:
        os.remove(f'{os.getcwd()}/config.json')
        clear()
        log('Invalid token.', error=True)
        time.sleep(1)
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

def load_commands() -> dict:
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

def enable_light_mode() -> dict:
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
    cinit(convert=True)
    clear()
    with open("./config.json") as f:
        config = json.load(f)
    functions = [fade.purpleblue]
    if config["Random Splash Color"]:
        functions = [fade.fire, fade.greenblue, fade.water, fade.pinkred]
    splash = random.choice(functions)("""                      
                 ███╗   ██╗██╗   ██╗██╗  ██╗███████╗██████╗
                 ████╗  ██║██║   ██║██║ ██╔╝██╔════╝██╔══██╗
                 ██╔██╗ ██║██║   ██║█████╔╝ █████╗  ██║  ██║
                 ██║╚██╗██║██║   ██║██╔═██╗ ██╔══╝  ██║  ██║
                 ██║ ╚████║╚██████╔╝██║  ██╗███████╗██████╔╝
                 ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ 
    """)
    console.print(splash, justify="center", end="")
    console.print(f"{version}\n", justify="center", style="reset")
    r = requests.get("https://raw.githubusercontent.com/coital/nuked/main/motd")
    if r.status_code in (200, 204):
        console.print(f"MOTD: [bold]{r.text}[/]\n", justify="center")
    deinit()
def log(content: str, color="cyan", error=False):
    console.print(f"\n[reset][{'red' if error else color}][bright][{get_time()}][/bright][/{'red' if error else color}] {content}[/reset]")

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
        log(f"RPC Failed to initialize: [bold]{e}[/bold].", error=True)
        time.sleep(2.5)
    return False

def disable_rich_presence() -> bool:
    global rpc
    rpc.close()
    return True

def embed_to_str(embed: discord.Embed) -> str:
    str = f"""{embed.title if embed.title else ""}\n{embed.description if embed.description else ""}\n"""
    embeds = embed.fields
    for em in embeds:
        str +=  f"""\n{em.name} : {em.value}\n"""

    str += f"""{embed.footer.text if embed.footer else ""}\n{embed.image.url if embed.image else ""}\n{embed.thumbnail.url if embed.thumbnail else ""}\n"""
    return str
