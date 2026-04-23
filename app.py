import sqlite3
import os
import anthropic
from datetime import date

# connect to database (creates file if it doesn't exist)
def get_connection():
    conn = sqlite3.connect("machine_logs.db")
    return conn

# create the table if it doesn't already exist
def setup_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_name TEXT,
            issue TEXT,
            duration_mins INTEGER,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()

# add a new downtime event to the database
def log_event():
    machine_name = input("Machine name: ")
    issue = input("What was the issue: ")
    duration_mins = input("How long was the downtime (in minutes): ")
    today = str(date.today())

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO events (machine_name, issue, duration_mins, date) VALUES (?, ?, ?, ?)",
        (machine_name, issue, duration_mins, today)
    )
    conn.commit()
    conn.close()
    print("Event logged!")

# get all events from db and print them
def view_events():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    conn.close()

    if len(rows) == 0:
        print("No events logged yet.")
        return

    print("\n--- All Machine Events ---")
    for row in rows:
        print(f"ID: {row[0]} | Machine: {row[1]} | Issue: {row[2]} | Duration: {row[3]} mins | Date: {row[4]}")
    print()

# pull all events and format them into a string for the AI
def get_events_as_text():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM events")
    rows = cur.fetchall()
    conn.close()

    if len(rows) == 0:
        return None

    # build a readable string from all the rows
    text = ""
    for row in rows:
        text += f"- Machine: {row[1]}, Issue: {row[2]}, Downtime: {row[3]} minutes, Date: {row[4]}\n"

    return text

# send the data to claude and get a report back
def generate_report():
    data = get_events_as_text()

    if data is None:
        print("No events to report on.")
        return

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY environment variable not set.")
        return

    print("Generating report with AI...")

    client = anthropic.Anthropic(api_key=api_key)

    # send the machine data to claude and ask for a plain english summary
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Here is a log of machine downtime events:\n\n{data}\n\nPlease summarize this in plain English. Highlight which machines had the most issues, total downtime, and any patterns you notice. Keep it simple and easy to understand."
            }
        ]
    )

    report = message.content[0].text

    # save report to a text file
    with open("report.txt", "w") as f:
        f.write(f"Machine Downtime Report - {date.today()}\n")
        f.write("=" * 40 + "\n\n")
        f.write(report)

    print("Report saved to report.txt!")
    print("\nPreview:")
    print(report[:300] + "..." if len(report) > 300 else report)

# main loop - keeps showing the menu until user exits
def main():
    setup_db()

    while True:
        print("\n--- Machine Log Menu ---")
        print("1. Log Event")
        print("2. View Events")
        print("3. Generate AI Report")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            log_event()
        elif choice == "2":
            view_events()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Invalid option, try again.")

main()
