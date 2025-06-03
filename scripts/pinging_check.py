import subprocess
import platform
import sys

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
    if ping(host):
        print(f"{host} is reachable")
    else:
        print(f"{host} is not reachable")

if __name__ == "__main__":
    main()
