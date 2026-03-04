<p align="center">
  <h1><strong>Automation is not about replacing people - it’s about empowering them to do more meaningful work.</strong></h1>
</p>

# 🛰️ SSH Service Check & Outlook Report Automation
=================================================

This README provides a **fully detailed, professional, emoji‑enhanced** documentation for the SSH automation script you created. It covers architecture, setup, configuration, HTML formatting, performance, security, troubleshooting, roadmap, and more.

---

# 📚 Table of Contents
1. 🚀 Overview
2. ✨ Features
3. 🖥️ System Requirements
4. 📦 Python Dependencies
5. ⚙️ Installation
6. 🔧 Configuration
7. 📁 Command Matrix Structure (`commands_data`)
8. 🔐 Credential Management
9. ▶️ Usage
10. 🎨 HTML Output & Styling
11. 🧾 Logging
12. 🛡️ Error Handling
13. 🔒 Security Best Practices
14. ⚡ Performance & Scalability
15. 🌐 External Config (JSON/YAML)
16. 🧪 Testing Strategy
17. 🧯 Troubleshooting
18. ⏰ Scheduling (Windows Task Scheduler)
19. 📁 Project Structure
20. 🔖 Version Pinning
21. 🗺️ Roadmap / Improvements
22. 📝 License

---

# 🚀 1. Overview
This automation script connects to multiple servers via **SSH**, executes commands, checks whether specific expected output substrings are present, and generates a **color‑coded HTML email** through Microsoft Outlook.

It is built using:
- **Paramiko** → For SSH communication
- **pywin32** → Outlook COM automation (`win32com.client`)
- **HTML formatting** → For a readable, color-coded status email

---

# ✨ 2. Features
- 🔐 Secure SSH connection via Paramiko
- 📬 Automatic HTML email generation in Outlook
- 🧩 Config‑driven command execution (easy to extend)
- 🖥️ Supports multiple servers and multiple commands per server
- 🧾 Paramiko logging for debugging SSH issues
- 🛡 Robust exception handling for:
  - Authentication errors
  - Hostname/DNS errors
  - SSH protocol failures
  - Unexpected runtime exceptions
- 🎨 Clean and color-coded HTML report

---

# 🖥️ 3. System Requirements
- Windows 10/11 (mandatory due to Outlook COM)
- Python 3.9+
- Microsoft Outlook (installed & configured)
- Administrator or network access to SSH port **22**

---

# 📦 4. Python Dependencies
Your `requirements.txt` should contain only:
```
paramiko
pywin32
pandas
```
Because:
- `win32com.client` → from pywin32
- `datetime`, `socket` → Python built‑ins

---

# ⚙️ 5. Installation
### 1️⃣ Create virtual environment
```
python -m venv .venv
. .venv/Scripts/activate
```

### 2️⃣ Upgrade pip
```
pip install --upgrade pip
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

---

# 🔧 6. Configuration
All server execution logic is stored in the Python dictionary `commands_data`. Each server can have multiple commands, each with expected substrings.

---

# 📁 7. Command Matrix Structure (`commands_data`)
Example:
```
commands_data = {
  "SERVER_1": [
    {
      "command": "systemctl is-active sshd",
      "present": ["active"]
    }
  ],
  "SERVER_2": [
    {
      "command": "ps -ef | grep nginx",
      "present": ["nginx"]
    }
  ]
}
```

### ✔️ Rules:
- `command`: The command executed on the server
- `present`: List of strings to verify in command output

---

# 🔐 8. Credential Management
Avoid hardcoding credentials.
Use **environment variables**:
```
setx SSH_USERNAME "myuser"
setx SSH_PASSWORD "mypassword"
```
Then in code:
```
import os
username = os.getenv("SSH_USERNAME")
password = os.getenv("SSH_PASSWORD")
```

Or use **SSH key-based authentication**.

---

# ▶️ 9. Usage
Run the script:
```
python your_script.py
```
It will automatically open a **composed Outlook email window**, allowing you to review before sending.

---

# 🎨 10. HTML Output & Styling
The script generates HTML with:
- 🔵 Blue: Connection messages
- 🟢 Green: Keyword found
- 🔴 Red: Keyword not found

You must use **actual HTML tags** like `<span>` instead of escaped `&lt;span&gt;`.

Example:
```
<span style='color:green;'>postgres is running</span>
```

---

# 🧾 11. Logging
Paramiko logs go to:
```
paramiko.log
```
Useful for debugging:
- SSH handshake errors
- Key issues
- Timeout diagnostics

---

# 🛡️ 12. Error Handling
The script handles:
- `paramiko.AuthenticationException`
- `socket.gaierror` (DNS resolution error)
- `paramiko.SSHException`
- Generic `Exception`

All errors are added to the HTML email.

---

# 🔒 13. Security Best Practices
- ❌ Do NOT store passwords in code
- ✔️ Use key-based authentication
- ✔️ Use environment variables or Windows Credential Manager
- ❌ Avoid `AutoAddPolicy` in production
- ✔️ Harden SSH configurations

---

# ⚡ 14. Performance & Scalability
To optimize:
- Use **ThreadPoolExecutor** for parallel SSH execution
- Add **timeouts** for:
  - SSH connect
  - Command execution
- Add retries for unreliable hosts

---

# 🌐 15. External Configuration (JSON/YAML)
Example JSON:
```
{
  "hosts": {
    "server1": [{"command": "uptime", "present": ["load"]}],
    "server2": [{"command": "df -h", "present": ["/dev"]}]
  }
}
```
This allows changing servers without editing script.

---

# 🧪 16. Testing Strategy
### Recommended Tests:
- ✔️ Unit test SSH command execution using mocks
- ✔️ Mock Outlook COM objects
- ✔️ Validate HTML formatting
- ✔️ Validate error formatting logic

---

# 🧯 17. Troubleshooting
| Issue | Cause | Fix |
|------|-------|------|
| HTML showing `<span>` | Used `&lt;span&gt;` | Use `<span>` |
| Outlook not opening | Outlook not installed | Install or open Outlook manually |
| SSH timeout | Slow server | Increase timeout |
| DNS error | Bad hostname | Use IP or fix DNS |

---

# ⏰ 18. Scheduling (Windows Task Scheduler)
Use a wrapper batch file:
```
@echo off
call .venv\Scripts ctivate
python your_script.py
```
Add it as a scheduled task.

---

# 📁 19. Project Structure
```
project/
│ README.txt
│ requirements.txt
│ proczen.py
│ run.bat
```

---

# 🔖 20. Version Pinning
```
paramiko==3.4.0
pywin32==306
pandas==2.2.0
```

---

# 🗺️ 21. Roadmap / Enhancements
- 📊 HTML table with colored badges
- 📎 CSV attachment summary
- 🔑 Strict SSH host key checking
- 🌍 SMTP email (Linux compatible)
- 🔁 Automatic retries

---

# 📝 22. License
```
© 2026 Internal Automation Script. All rights reserved.
```

---
