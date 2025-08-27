"""
Fitness Coach CLI - Pure Python (built-in libraries only)

This beginner-friendly command-line app lets coaches and clients
register/login, schedule fitness sessions, and generate Jitsi Meet links.
Data is stored in simple text files (CSV-style).

Files created in the same folder as this script:
- users.txt
- sessions.txt
- readme.md
"""
import os
import csv
import random
import string
from datetime import datetime

# -------------------------------
# Constants & File Paths
# -------------------------------

# Resolve files relative to this script so the app works no matter the CWD.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(SCRIPT_DIR, "users.txt")
SESSIONS_FILE = os.path.join(SCRIPT_DIR, "sessions.txt")

JITSI_BASE_URL = "https://meet.jit.si/"
ROOM_PREFIX = "FitnessSession_"
# -------------------------------
# Helper: ensure data files exist
# -------------------------------

def bootstrap_files():
    """Create empty data files if they don't exist yet."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as f:
            pass
    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "w", newline="", encoding="utf-8") as f:
            pass

# -------------------------------
# File I/O helpers
# -------------------------------

def load_from_file(filepath):
    """
    Read CSV-like rows from a text file and return a list of lists (rows).
    Empty lines are skipped.
    """
    rows = []
    if not os.path.exists(filepath):
        return rows
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            rows.append(row)
    return rows

def save_to_file(filepath, rows):
    """
    Write a list of lists to a CSV-like text file, overwriting existing content.
    Each inner list is written as one line.
    """
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

# -------------------------------
# Authentication
# -------------------------------

def register_user():
    """
    Create a new user. Role must be 'coach' or 'client'.
    Duplicate usernames are not allowed.
    """
    print("\n=== Register New User ===")
    users = load_from_file(USERS_FILE)
    existing_usernames = {u[0] for u in users}  # u = [username,password,role,email]

    while True:
        username = input("Choose a username: ").strip()
        if not username:
            print("Username cannot be empty.")
            continue
        if "," in username:
            print("Commas are not allowed in username.")
            continue
        if username in existing_usernames:
            print("That username is already taken. Try another.")
            continue
        break

    while True:
        password = input("Choose a password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue
        break

    while True:
        role = input("Choose role ('coach' or 'client'): ").strip().lower()
        if role not in ("coach", "client"):
            print("Role must be 'coach' or 'client'.")
            continue
        break

    while True:
        email = input("Enter your email: ").strip()
        if not email:
            print("Email cannot be empty.")
            continue
        if "," in email:
            print("Commas are not allowed in email.")
            continue
        break

    users.append([username, password, role, email])
    save_to_file(USERS_FILE, users)
    print(f"User '{username}' registered successfully as {role}!\n")

def login_user():
    """
    Prompt for username/password. Return a dict with the user record on success:
    {"username": ..., "role": ..., "email": ...}
    Return None on failure.
    """
    print("\n=== Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    users = load_from_file(USERS_FILE)
    for row in users:
        if len(row) != 4:
            continue  # skip malformed rows
        if row[0] == username and row[1] == password:
            print(f"Welcome, {username}! You are logged in as {row[2]}.\n")
            return {"username": row[0], "role": row[2], "email": row[3]}
    print("Invalid username or password.\n")
    return None

# -------------------------------
# Jitsi helpers
# -------------------------------

def generate_unique_id():
    """Create a unique ID using current datetime and random characters."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{timestamp}{rand}"

def generate_jitsi_link():
    """Create a unique Jitsi Meet room URL string."""
    unique = generate_unique_id()
    room_name = f"{ROOM_PREFIX}{unique}"
    return JITSI_BASE_URL + room_name

# -------------------------------
# Session management
# -------------------------------

def schedule_session(coach_username):
    """Create a new session for a coach."""
    print("\n=== Schedule New Session ===")
    users = load_from_file(USERS_FILE)
    valid_clients = {u[0] for u in users if len(u) >= 3 and u[2] == "client"}
    if not valid_clients:
        print("No clients found. Ask someone to register as a client first.\n")
        return

    print("Known clients:", ", ".join(sorted(valid_clients)))
    while True:
        client = input("Client username: ").strip()
        if client not in valid_clients:
            print("Unknown client. Please enter one of the listed client usernames.")
            continue
        break

    while True:
        date_str = input("Session date (YYYY-MM-DD): ").strip()
        time_str = input("Session time (HH:MM, 24-hour): ").strip()
        try:
            scheduled_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            if scheduled_dt < datetime.now():
                print("That time is in the past. Please choose a future time.")
                continue
            break
        except ValueError:
            print("Invalid date or time format. Please try again.")
            continue

    session_id = generate_unique_id()
    jitsi_link = generate_jitsi_link()
    status = "scheduled"
    notes = ""

    sessions = load_from_file(SESSIONS_FILE)
    sessions.append([session_id, coach_username, client, date_str, time_str, jitsi_link, status, notes])
    save_to_file(SESSIONS_FILE, sessions)

    print("\nSession created!")
    print(f"Session ID: {session_id}")
    print(f"Coach:      {coach_username}")
    print(f"Client:     {client}")
    print(f"When:       {date_str} {time_str}")
    print(f"Jitsi Link: {jitsi_link}\n")

def view_sessions(current_user):
    """Display sessions for the logged-in user (coach or client)."""
    print("\n=== My Sessions ===")
    sessions = load_from_file(SESSIONS_FILE)
    count = 0
    for row in sessions:
        if len(row) < 8:
            continue
        is_mine = (row[1] == current_user["username"]) or (row[2] == current_user["username"])
        if is_mine:
            count += 1
            print("-" * 60)
            print(f"ID: {row[0]}")
            print(f"Coach: {row[1]} | Client: {row[2]}")
            print(f"When: {row[3]} {row[4]} | Status: {row[6]}")
            print(f"Jitsi: {row[5]}")
            if row[7]:
                print(f"Notes: {row[7]}")
    if count == 0:
        print("No sessions found.")
    print("")

def find_session_by_id(session_id):
    """Return (index, row) for a session id, or (None, None) if not found."""
    sessions = load_from_file(SESSIONS_FILE)
    for idx, row in enumerate(sessions):
        if len(row) >= 1 and row[0] == session_id:
            return idx, row
    return None, None

def edit_session(coach_username):
    """Allow a coach to change date/time or client for one of their sessions."""
    print("\n=== Edit Session ===")
    target_id = input("Enter Session ID to edit: ").strip()
    idx, row = find_session_by_id(target_id)
    if idx is None:
        print("Session not found.\n")
        return
    if row[1] != coach_username:
        print("You can only edit your own sessions.\n")
        return
    if row[6] == "canceled":
        print("This session has been canceled.\n")
        return

    print("Leave blank to keep unchanged.")
    new_date = input(f"New date (YYYY-MM-DD) [current: {row[3]}]: ").strip()
    new_time = input(f"New time (HH:MM) [current: {row[4]}]: ").strip()
    new_client = input(f"New client username [current: {row[2]}]: ").strip()

    if new_client:
        users = load_from_file(USERS_FILE)
        valid_clients = {u[0] for u in users if len(u) >= 3 and u[2] == "client"}
        if new_client not in valid_clients:
            print("Unknown client. Edit canceled.\n")
            return
        row[2] = new_client

    if new_date or new_time:
        date_str = new_date if new_date else row[3]
        time_str = new_time if new_time else row[4]
        try:
            _ = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
            row[3] = date_str
            row[4] = time_str
        except ValueError:
            print("Invalid date/time. Edit canceled.\n")
            return

    sessions = load_from_file(SESSIONS_FILE)
    sessions[idx] = row
    save_to_file(SESSIONS_FILE, sessions)
    print("Session updated.\n")

def cancel_session(coach_username):
    """Allow a coach to cancel a session."""
    print("\n=== Cancel Session ===")
    target_id = input("Enter Session ID to cancel: ").strip()
    idx, row = find_session_by_id(target_id)
    if idx is None:
        print("Session not found.\n")
        return
    if row[1] != coach_username:
        print("You can only cancel your own sessions.\n")
        return
    if row[6] == "canceled":
        print("Session already canceled.\n")
        return
    row[6] = "canceled"
    sessions = load_from_file(SESSIONS_FILE)
    sessions[idx] = row
    save_to_file(SESSIONS_FILE, sessions)
    print("Session canceled.\n")

def regenerate_link(coach_username):
    """Allow a coach to generate a fresh Jitsi link for a session."""
    print("\n=== Generate/Refresh Session Link ===")
    target_id = input("Enter Session ID: ").strip()
    idx, row = find_session_by_id(target_id)
    if idx is None:
        print("Session not found.\n")
        return
    if row[1] != coach_username:
        print("You can only modify your own sessions.\n")
        return
    if row[6] == "canceled":
        print("This session is canceled.\n")
        return
    new_link = generate_jitsi_link()
    row[5] = new_link
    sessions = load_from_file(SESSIONS_FILE)
    sessions[idx] = row
    save_to_file(SESSIONS_FILE, sessions)
    print(f"New Jitsi link: {new_link}\n")

def add_session_notes(coach_username):
    """Allow a coach to append notes to a session."""
    print("\n=== Add Session Notes ===")
    target_id = input("Enter Session ID: ").strip()
    idx, row = find_session_by_id(target_id)
    if idx is None:
        print("Session not found.\n")
        return
    if row[1] != coach_username:
        print("You can only modify your own sessions.\n")
        return
    if row[6] == "canceled":
        print("This session is canceled.\n")
        return
    existing = row[7] if len(row) >= 8 else ""
    print(f"Current notes: {existing!r}")
    note = input("Add note: ").strip()
    row[7] = (existing + " | " if existing else "") + note if note else existing
    sessions = load_from_file(SESSIONS_FILE)
    sessions[idx] = row
    save_to_file(SESSIONS_FILE, sessions)
    print("Notes updated.\n")

def client_get_link(client_username):
    """For clients: get Jitsi link for a given session."""
    print("\n=== Join Session ===")
    target_id = input("Enter your Session ID: ").strip()
    idx, row = find_session_by_id(target_id)
    if idx is None:
        print("Session not found.\n")
        return
    if row[2] != client_username:
        print("This session does not belong to you.\n")
        return
    if row[6] == "canceled":
        print("This session has been canceled.\n")
        return
    print(f"Jitsi link: {row[5]}\n")

# -------------------------------
# Menus
# -------------------------------

def coach_menu(current_user):
    """Menu loop shown to coaches."""
    while True:
        print("=== Coach Menu ===")
        print("1. Schedule New Session")
        print("2. View My Sessions")
        print("3. Generate/Refresh Session Link")
        print("4. Edit Session")
        print("5. Cancel Session")
        print("6. Add Session Notes")
        print("7. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            schedule_session(current_user["username"])
        elif choice == "2":
            view_sessions(current_user)
        elif choice == "3":
            regenerate_link(current_user["username"])
        elif choice == "4":
            edit_session(current_user["username"])
        elif choice == "5":
            cancel_session(current_user["username"])
        elif choice == "6":
            add_session_notes(current_user["username"])
        elif choice == "7":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.\n")

def client_menu(current_user):
    """Menu loop shown to clients."""
    while True:
        print("=== Client Menu ===")
        print("1. View My Sessions")
        print("2. Join Session (get Jitsi link)")
        print("3. Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_sessions(current_user)
        elif choice == "2":
            client_get_link(current_user["username"])
        elif choice == "3":
            print("Logging out...\n")
            break
        else:
            print("Invalid choice. Try again.\n")

# -------------------------------
# Main loop
# -------------------------------

def main():
    bootstrap_files()
    while True:
        print("=== Fitness Coach Manager ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            user = login_user()
            if user:
                if user["role"] == "coach":
                    coach_menu(user)
                else:
                    client_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()


