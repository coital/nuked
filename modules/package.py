import os, subprocess, sys
from typing import List



def install_module(module: str=None, modules: List[str]=None):
    if not module and not modules:
        return
    elif modules:
        for module in modules:
            if "not found" in subprocess.getoutput(f"{sys.executable} -m pip show {module}"):
                os.system(f"{sys.executable} -m pip install {module}")
                print(f"Installed {module}")
            else:
                print(f"{module} already installed, continuing")
        print("Restarting.")
        restart()
    elif module:
        if "not found" in subprocess.getoutput(f"{sys.executable} -m pip show {module}"):
            os.system(f"{sys.executable} -m pip install {module}")
            print(f"Installed {module}")
    return

def restart():
    os.execv(sys.executable, ['python'] + [sys.argv[0]])