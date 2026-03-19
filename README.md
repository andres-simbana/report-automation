# report-automation

Playwright automation to query monthly reports on a slow-loading internal system.

## Problem

The report system takes a long time to process each query and the Preview button is only clickable once the system is ready. Running this manually for 3 months of data was time-consuming and unreliable.

## Solution

Script that:
- Automatically selects date ranges for the last 1, 2, and 3 months
- Retries every 30 seconds until the Preview button becomes clickable
- Runs in a loop every 30 minutes to keep data refreshed

## Setup

```bash
pip install -r requirements.txt
playwright install msedge
```

## Usage

```bash
python MasterReport.py
```

1. The browser opens and navigates to the report URL
2. Log in manually with your corporate account
3. Press ENTER once the report page is loaded
4. The script takes over from there

## Notes

- Login is manual since the system uses corporate SSO (Microsoft)
- Update `url_reporte` in `MasterReport.py` with your actual report URL
