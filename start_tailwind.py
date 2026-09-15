import os, sys

from pathlib import Path

BASE_DIR = Path(__file__).parent
MANAGE_LOCATION = BASE_DIR / "SAAS" / "manage.py"
VENV_DIR = BASE_DIR / "venv"
VENV_PYTHON_WINDOWS = VENV_DIR / "Scripts" / "python.exe"
VENV_PYTHON_LINUX = VENV_DIR / "bin" / "python"
REQS_LOCATION = VENV_DIR / "lib" / "python3.14" / "site-packages"
NPM_DIR = MANAGE_LOCATION.parent / "theme" / "static_src" / "node_modules"

if not NPM_DIR.exists():
    print("req not found run start_project first")
    sys.exit()

selOS = VENV_PYTHON_LINUX

if not VENV_PYTHON_LINUX.exists():
    selOS = VENV_PYTHON_WINDOWS

os.execv(selOS, [selOS, MANAGE_LOCATION, "tailwind", "start"])