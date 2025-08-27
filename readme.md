# Fitness Coach CLI

This is my first Python project! 🎉  
It’s a simple command-line app where coaches and clients can log in, manage fitness sessions, and get Jitsi links for online workouts.  

I built it only with *pure Python* (no extra libraries). Everything is stored in text files, so it’s really easy to run and understand.

---

## Project Files

Here’s what the folder looks like:

CL Fitness App Projects/ ├── main.py       # the main Python program ├── users.txt     # stores users (username, password, role, email) ├── sessions.txt  # stores sessions (coach, client, time, link, etc.) └── README.md     # this file :)

---

## How to Run

1. Install Python 3 if you don’t already have it.  
2. Open a terminal in this project’s folder.  
3. Run:

```bash
python main.py

(if that doesn’t work, try python3 main.py)


---

Test Accounts

I already added some sample users:

Coach: huda/123

Client: smith/49s

Client: john/456



---

How Data is Stored

users.txt → saves accounts like this:

john,456,client,john@gmail.com

sessions.txt → saves sessions like this:

20250826110956JF8FQY,1,john,2025-08-27,23:23,https://meet.jit.si/FitnessSession_20250826111414A9XCHS,canceled,

---

What You Can Do

When you run the program:

Coaches can schedule sessions, see their sessions, cancel or edit them, and get Jitsi links.

Clients can see their sessions and join them using the Jitsi links.



---

Why I Made This

I wanted to practice:

Reading/writing text files

Basic login system (register + login)

Menus and program flow

Working with dates and random strings



---

Next Steps

Some ideas I might try later:

Hide passwords instead of plain text

Add reminders for sessions

Maybe turn it into a small web app one day
_______

Thanks for checking this out! 🙌