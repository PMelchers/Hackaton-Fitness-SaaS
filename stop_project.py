import sys
from pathlib import Path

try:
    import psutil
except ImportError:
    print("psutil is niet geinstalleerd. Run eerst 'python3 start_project.py' (installeert requirements.txt), of 'pip install psutil'.")
    sys.exit(1)

BASE_DIR = Path(__file__).resolve().parent


def is_our_server(proc):
    cmdline = proc.info.get("cmdline") or []
    if "runserver" not in cmdline:
        return False
    if not any(Path(part).name == "manage.py" for part in cmdline):
        return False
    try:
        cwd = Path(proc.cwd()).resolve()
    except (psutil.Error, OSError):
        return False
    return cwd == BASE_DIR or BASE_DIR in cwd.parents


def find_server_pids():
    pids = []
    for proc in psutil.process_iter(["pid", "cmdline"]):
        if is_our_server(proc):
            pids.append(proc.info["pid"])
    return pids


def main():
    pids = find_server_pids()
    if not pids:
        print("Geen draaiende dev server gevonden voor dit project.")
        return

    procs = []
    for pid in pids:
        try:
            proc = psutil.Process(pid)
            print(f"Stoppen pid {pid}: {' '.join(proc.cmdline())}")
            proc.terminate()
            procs.append(proc)
        except psutil.NoSuchProcess:
            pass

    _, alive = psutil.wait_procs(procs, timeout=5)
    for proc in alive:
        print(f"pid {proc.pid} stopte niet op tijd, force kill")
        proc.kill()

    print("done")


if __name__ == "__main__":
    main()
