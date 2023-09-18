import os, subprocess, sys, time

# thank you reuben for helping me realize things
def install_module(module):
    if "git" in module:
        os.system(f"{sys.executable} -m pip install gitpython")
        print("You are missing the git cli. You can download it at https://git-scm.com/downloads.")
        restart()
    elif "cryptodome" in module:
        os.system(f"{sys.executable} -m pip install pycryptodome")
        restart()
    elif "not found" in subprocess.getoutput(f"{sys.executable} -m pip show {module}"):
        os.system(f"{sys.executable} -m pip install {module}")
        print(f"Installed {module}.")
    return

def restart():
    time.sleep(1)
    os.execv(sys.executable, ['python', sys.argv[0]])

if os.name == "nt":
    install_module("win10toast")