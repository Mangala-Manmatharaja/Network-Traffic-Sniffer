import psutil
import socket
import time
from datetime import datetime


def get_active_connections():
    connections = psutil.net_connections(kind="inet")
    active = []

    for conn in connections:
        if conn.status == "ESTABLISHED" and conn.raddr:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}"
            pid = conn.pid
            try:
                proc_name = psutil.Process(pid).name()
            except Exception:
                proc_name = "N/A"
            active.append((laddr, raddr, proc_name, pid))

    return active


def main():
    print("[*] Starting Windows-compatible traffic monitor...")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            conns = get_active_connections()
            if conns:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Active connections:")
                for laddr, raddr, proc_name, pid in conns:
                    print(f"  {laddr} → {raddr} | Process: {proc_name} (PID: {pid})")
                print("-" * 60)
            time.sleep(3)
    except KeyboardInterrupt:
        print("\n[*] Monitoring stopped.")


if __name__ == "__main__":
    main()
