# 💤 Auto Sleep

A simple Python script to automatically put your PC to sleep after a period of inactivity. Designed for people whose computers refuse to sleep properly due to background processes or unknown quirks.

## ✅ Features
- Automatically sleeps your PC after a set idle time
- Lightweight and runs silently in the background
- Easy to customize (sleep timer, checks, notifications)

## 💡 Why?
Some systems simply won't enter sleep mode on their own — Auto Sleep fixes that by enforcing sleep after you've been inactive for a while.

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/420jk420/AutoSleep.git
cd auto-sleep

Install dependencies
pip install -r requirements.txt

Run the script
python auto_sleep.py

Configuration (sleep.py)
IDLE_TIME_LIMIT = 5400 # Time limit for inactivity (in seconds)
NOTIFICATION_TIMEOUT = 60  # Time limit for user to respond to notification (in seconds)

Contributions Welcome
Feel free to submit issues or pull requests! If your PC is stubborn like mine, this might save you some energy costs too.
