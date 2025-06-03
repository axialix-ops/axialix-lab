#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

# Список серверов (замените на свои IP/домена)
servers = [
    "8.8.8.8",           # Google DNS
    "1.1.1.1",           # Cloudflare DNS
    "axialix.ddns.net",  # твой домен
]

# Файл для логов
log_file = "ping_log.txt"

def ping(host):
    try:
        # Для Linux используем -c 1 (1 попытка)
        result = subprocess.run(
            ["ping", "-c", "1", host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception as e:
        return False

def log_status(host, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"[{now}] {host}: {'OK' if status else 'FAIL'}\n")

def main():
    for server in servers:
        is_up = ping(server)
        log_status(server, is_up)
        print(f"{server}: {'✅ OK' if is_up else '❌ FAIL'}")

if __name__ == "__main__":
    main()
