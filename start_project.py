import subprocess, sys, os
from pathlib import Path

BASE_DIR = Path(__file__).parent
MANAGE_LOCATION = BASE_DIR / "SAAS" / "manage.py"
VENV_DIR = BASE_DIR / "venv"
VENV_PYTHON_WINDOWS = VENV_DIR / "Script" / "python.exe"
VENV_PYTHON_LINUX = VENV_DIR / "bin" / "python"
REQS_LOCATION = VENV_DIR / "lib" / "python3.14" / "site-packages"
NPM_DIR = MANAGE_LOCATION.parent / "theme" / "static_src" / "node_modules"

if not VENV_DIR.exists():
    print("venv not found")
    subprocess.run([sys.executable, "-m", "venv", "venv"])
    print("created venv")

requirements = open("requirements.txt").read().split('\n')
presentRequirements = [res.stem for res in REQS_LOCATION.iterdir() if res.is_dir()]
sel_venv = None

if VENV_PYTHON_WINDOWS.exists(): 
    print("windows detected")
    sel_venv = VENV_PYTHON_WINDOWS
elif VENV_PYTHON_LINUX.exists():
    print("linux detected")
    sel_venv = VENV_PYTHON_LINUX
else:
    print("error in os selection")
    sys.exit()

if not set(requirements).issubset(presentRequirements):
    print(f"requirements not satisfied")

    if sel_venv is not None:
        pip_loc = sel_venv.parent / "pip"
        subprocess.run([sel_venv, pip_loc, "install", "-r", "requirements.txt"])
        print("done installing requirements")

if sel_venv is not None:
    if not NPM_DIR.exists():
        print("installing tailwind requirements")
        subprocess.run([sel_venv, MANAGE_LOCATION, "tailwind", "install"])
        print("done")
        
    print("running makemigrations")
    subprocess.run([sel_venv, MANAGE_LOCATION, "makemigrations"])
    print("done")

    print("running migrations")
    subprocess.run([sel_venv, MANAGE_LOCATION, "migrate"])
    print("done")

    print("starting server")
    os.execv(sel_venv, [sel_venv, MANAGE_LOCATION, "runserver"])