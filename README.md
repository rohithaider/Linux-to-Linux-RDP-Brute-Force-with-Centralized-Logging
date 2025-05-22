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

