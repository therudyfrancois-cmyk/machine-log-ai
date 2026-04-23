# Machine Log & AI Report Generator

A command-line tool I built to log machine downtime events and automatically generate maintenance reports using AI. 

Inspired by 3 years working on CNC and EDM machines at an aerospace manufacturer where we tracked everything manually. Wanted to automate that with code.

## What it does

- Log machine downtime events to a local database
- View all logged events
- Generate a plain-English maintenance report using the Claude AI API
- Saves the report as a .txt file

## Tech Stack

- Python
- SQLite
- Anthropic Claude API
- Prompt Engineering

## How to run it

**1. Clone the repo**
```bash
git clone https://github.com/therudyfrancois-cmyk/machine-log-ai.git
cd machine-log-ai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your API key**

Windows:
```bash
set ANTHROPIC_API_KEY=your_key_here
```

Mac/Linux:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

**4. Run it**
```bash
python app.py
```

## Why I built this

I spent 3 years running Fanuc CNC and EDM machines at Pursuit Aerospace. Every time a machine went down we tracked it manually on paper or in a spreadsheet. At the end of the week someone would write a summary report by hand.

When I started learning Python I wanted to build something real instead of just following tutorials. This solves a problem I actually lived. The database replaces the paper log. The AI report replaces the manual write-up.

Also wanted to connect three things I was learning at the same time — Python, SQL, and API calls — into one project that makes sense as a system.

## What I learned

- SQLite database creation and SQL queries from Python
- Making real API calls and handling responses
- Prompt engineering — how you phrase the instruction determines how useful the output is
- Storing API keys securely with environment variables instead of hardcoding them

## Author

Rudy Francois — CS student at WGU | Ex-aerospace machinist |
