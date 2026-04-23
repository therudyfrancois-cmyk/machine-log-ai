import sqlite3  # sqlite3 comes with Python — no install needed
import datetime  # lets us get today's date automatically


# The name of the database file that will be created on your computer
DATABASE_FILE = "machine_log.db"


def get_connection():
    """
    Opens a connection to the SQLite database file.
    Think of this like opening a filing cabinet before you can read or add files.
    """
    connection = sqlite3.connect(DATABASE_FILE)  # creates the file if it doesn't exist yet
    return connection  # hand the open connection back to whoever asked for it


def create_table():
    """
    Creates the 'events' table if it doesn't already exist.
    A table is like a spreadsheet — it has columns and rows.
    Our columns are: id, machine_name, issue_description, duration_minutes, date.
    """
    connection = get_connection()  # open the filing cabinet
    cursor = connection.cursor()  # a cursor is like a pen — it lets you write/read

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            machine_name TEXT NOT NULL,
            issue_description TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    """)
    # INTEGER PRIMARY KEY AUTOINCREMENT = SQLite will auto-number each row (1, 2, 3...)
    # TEXT NOT NULL = this column must have text, it can't be empty
    # INTEGER NOT NULL = this column must have a whole number, it can't be empty

    connection.commit()   # save the changes (like hitting Ctrl+S)
    connection.close()    # close the filing cabinet when done


def log_event(machine_name, issue_description, duration_minutes):
    """
    Adds a new downtime event to the database.
    Takes three pieces of info from the user and saves them as a new row.
    The date is set automatically to today.
    """
    connection = get_connection()  # open the filing cabinet
    cursor = connection.cursor()   # get our writing pen

    today = datetime.date.today().isoformat()  # gets today's date as "YYYY-MM-DD" string
    # Example: "2026-04-23"

    cursor.execute("""
        INSERT INTO events (machine_name, issue_description, duration_minutes, date)
        VALUES (?, ?, ?, ?)
    """, (machine_name, issue_description, duration_minutes, today))
    # The ? marks are placeholders — SQLite fills them in safely from the tuple above
    # Using ? instead of putting values directly in the string prevents "SQL injection" attacks

    connection.commit()  # save the new row
    connection.close()   # close up

    print(f"\n Event logged for '{machine_name}' on {today}.")  # confirm to the user


def get_all_events():
    """
    Retrieves every row from the events table and returns them as a list.
    Each item in the list is a tuple: (id, machine_name, issue, duration, date)
    """
    connection = get_connection()  # open the filing cabinet
    cursor = connection.cursor()   # get our reading pen

    cursor.execute("SELECT * FROM events ORDER BY date DESC")
    # SELECT * means "give me all columns"
    # ORDER BY date DESC means newest events appear first

    events = cursor.fetchall()  # fetchall() grabs every matching row at once
    connection.close()          # close up

    return events  # hand the list of events back to whoever called this function


def format_events_for_ai(events):
    """
    Converts the list of database rows into a plain-English block of text.
    The AI (Claude) understands text, not database rows — so we translate.
    """
    if not events:  # if the list is empty (no events logged yet)
        return "No events have been logged yet."

    lines = []  # start with an empty list of text lines

    for event in events:
        # Unpack the tuple into readable variable names
        event_id, machine, issue, duration, date = event

        # Build a human-readable sentence for each event
        line = f"- [{date}] Machine: {machine} | Issue: {issue} | Downtime: {duration} minutes"
        lines.append(line)  # add this line to our list

    # Join all lines into one big text block, separated by newlines
    return "\n".join(lines)
