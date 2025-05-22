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

