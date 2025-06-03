import subprocess
import sys

def check_service_status(service_name):
    try:
        result = subprocess.run(
            ["sc", "query", service_name],
            capture_output=True,
            text=True
        )
        if "RUNNING" in result.stdout:
            return True
        else:
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def main():
    service = sys.argv[1] if len(sys.argv) > 1 else "wuauserv"  # Windows Update service
    if check_service_status(service):
        print(f"Service {service} is running")
    else:
        print(f"Service {service} is not running or invalid")

if __name__ == "__main__":
    main()
