# report-automation

Playwright automation script that handles a **slow-loading internal report system**. It automates date selection and report generation for the last 3 months, running in an infinite loop every 30 minutes. Built to handle SSO (single sign-on) login manually and retry aggressively when the report system is unresponsive.

---

## 🛠️ Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-2EAD33?style=flat-square&logo=playwright&logoColor=white)
![Microsoft Edge](https://img.shields.io/badge/Microsoft_Edge-0078D7?style=flat-square&logo=microsoft-edge&logoColor=white)

---

## 💡 What it does

1. Opens **Microsoft Edge** and navigates to the report system URL
2. Waits for you to **log in manually** via SSO (corporate account)
3. Enters a loop that every **30 minutes** runs queries for the **last 3 months**
4. For each month, selects date ranges and clicks the Preview button
5. If the system is slow or unresponsive, **retries up to 20 times** (30s between retries)

---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/andres-simbana/report-automation.git
cd report-automation
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Playwright browsers
```bash
playwright install msedge
```

---

## ▶️ Running

Set the report system URL as an environment variable:

```bash
# Linux/Mac
export REPORT_URL="https://your-internal-report-system.com/report"

# Windows (PowerShell)
$env:REPORT_URL = "https://your-internal-report-system.com/report"
```

Then run:
```bash
python MasterReport.py
```

The browser will open. **Log in manually with your corporate account**, then press **ENTER** in the terminal to start the automation.

---

## ⚠️ Notes

- Requires **Microsoft Edge** installed on the machine
- Designed for internal systems with SSO — login is always manual
- Runs indefinitely until stopped with `Ctrl+C`
