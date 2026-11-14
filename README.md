# LUXE SCAN-WEB

Single-file Python web vulnerability scanner with colored terminal UI, multi-threaded checks, heuristic confirmation, HTML report, and Telegram delivery.

**Dev:** [LUXE](https://t.me/LU_KT)

Authorized testing only. Use exclusively on systems you own or have written permission to test.

## Features

- LFI, RCE, SQLi (error / boolean / time-based), XSS (canary + executable context)
- SSRF, XXE, SSTI, Open Redirect, CRLF, CSRF markers, CORS credentials, JWT reaction
- Admin and sensitive path discovery
- Subdomain probing with soft-404 filtering
- Technology fingerprinting, email extraction, cookie capture
- File extraction from confirmed LFI
- Optional RCE follow-ups: backdoor attempts and trace cleanup (authorized targets only)
- Baseline comparison and multi-confirm checks to reduce false positives
- Thread-local sessions and automatic retries on network errors
- Built-in `CONFIG` defaults + CLI overrides
- `LUXE.HTML` report and Telegram summary with Dev button

## Requirements

- Python 3.8+ (Windows / Linux / macOS)
- Install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

Edit defaults inside `main.py`:

```python
CONFIG = {
    "target": "",
    "token": "",
    "chat_id": "",
    "workers": 12,
    "timeout": 10,
}
```

## Usage

Interactive:

```bash
python main.py
```

CLI:

```bash
python main.py -u https://target.com -t BOT_TOKEN -c CHAT_ID -w 12
```

Help:

```bash
python main.py -h
```

## CLI flags

| Flag | Description |
|------|-------------|
| `-u, --url` | Target URL |
| `-t, --token` | Token bot Tele |
| `-c, --chat` | id chat Tele |
| `-w, --workers` | Worker threads (default 12) |
| `-h, --help` | Show help |

## Output

- Live terminal findings
- Local report: `LUXE.HTML`
- Telegram message with counts + Dev button, plus HTML document when token/chat are set

## Notes

- Results are heuristic and need manual verification.
- XSS checks confirm unencoded reflection in executable-looking context, not full browser execution.
- Aggressive modules must only be used on authorized systems.

## Contact

Tele Me : [LUXE](https://t.me/LU_KT)
