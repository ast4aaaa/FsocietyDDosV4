# FSOCIETY DDoS V4

> ⚠️ **Disclaimer**  
This tool is created strictly for **educational** and **authorized security testing** purposes. Do **NOT** use this tool against servers, websites, or networks without explicit permission. Misuse of this software is illegal and unethical.

---

## 📌 Overview

**FSOCIETY DDoS V4** is a GUI-based HTTP flood tool designed to simulate DDoS attacks for stress-testing and educational demonstrations.

It provides a simple and intuitive interface that allows users to:

- Launch HTTP-based attack simulations
- Choose from multiple HTTP methods (HEAD, GET, POST)
- Configure thread count and duration
- Perform basic DNS tools (like DNS lookup)

> ⚠️ **Note:** UDP, TCP, or Layer 4 attacks are not supported.

---

## 🖥️ Interface & Features

### Attack Settings

- **Target URL** – Input the web address of the system you're stress-testing.
- **Attack Method** – Choose one of:
  - `GET`
  - `POST`
  - `HEAD`
- **Thread Count** – Set the number of concurrent threads.
- **Duration** – Specify the duration of the attack in seconds.

### DNS Tools

- **DNS Lookup** – Perform DNS lookups for the target domain.

---

## 💾 Download

You can download the precompiled Windows executable here:

**🔗 [Download FsocietyV4.exe](https://files.fm/f/cdgh8map8h)**

---

## ⚙️ Usage

### Using the Executable

1. Download the `.exe` file from the link above.
2. Run the executable.
3. Input the target URL, select the attack method, set the thread count, and specify the duration.
4. Click "Start" to initiate the attack simulation.

### Using the Python Script

1. Clone the repository:

   ```bash
   git clone https://github.com/ast4aaaa/FsocietyDDosV4.git
   cd FsocietyDDosV4 && python FsocietyV4.py
