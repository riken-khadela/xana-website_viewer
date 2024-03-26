import sqlite3
from datetime import datetime, timedelta
from maill import SendErrorMail
from etc.variable import *



def create_db_ifnot():
    try:
        # Connect to the SQLite database. If the database file doesn't exist, it will be created automatically.
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Create the first table "main_table" if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS main_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                view BOOLEAN NOT NULL
            )
        ''')

        # Create the second table "attached_table" if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attached_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                number INTEGER NOT NULL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sent_emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sent_at TIMESTAMP NOT NULL
            )
        ''')

        # Create a trigger to automatically insert or update data in "attached_table" when a row is inserted into "main_table" with view set to true
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS insert_or_update_attached_table
            AFTER INSERT ON main_table
            WHEN NEW.view = 1
            BEGIN
                -- Update the number column in attached_table if a record with the same date exists
                UPDATE attached_table 
                SET number = number + 1 
                WHERE date = NEW.date;

                -- Insert a new record into attached_table if no record with the same date exists
                INSERT INTO attached_table (date, number) 
                SELECT NEW.date, 1 
                WHERE (SELECT changes() = 0);
            END;
        ''')

        # Commit changes and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)

def add_data_with_view(date, view):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Insert data into main_table
        # cursor.execute("INSERT INTO main_table (date, view) VALUES (?, ?)", (date, view))

        # If view is True, insert data into attached_table as well
        if view:
            cursor.execute("INSERT INTO attached_table (date, number) VALUES (?, ?)", (date, 1))

        # Commit changes and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)

def get_views_per_day():
    views_per_day = {}
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Execute SQL query to get the total count of views per day
        cursor.execute('''
            SELECT date, COUNT(*) AS total_views
            FROM attached_table
            GROUP BY date
        ''')

        # Fetch all rows and create a dictionary
        for row in cursor.fetchall():
            views_per_day[row[0]] = row[1]

        # Close the connection
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)

    return views_per_day


def has_sent_email_within_last_15_minutes():
    try:
        # Check if the current time is after 6pm today
        if datetime.now().hour < 18:
            return False

        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Calculate the start of today at 6pm
        start_of_today_at_6pm = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=18)

        # Execute SQL query to check if an email has been sent after 6pm today
        cursor.execute('''
            SELECT COUNT(*)
            FROM sent_emails
            WHERE sent_at >= ?
        ''', (start_of_today_at_6pm,))

        # Fetch the result
        result = cursor.fetchone()[0]

        # Close the connection
        conn.close()

        return result > 0
    except sqlite3.Error as e:
        print("SQLite error:", e)
        return False

def mark_email_as_sent():
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Insert the current timestamp into the "sent_emails" table
        cursor.execute("INSERT INTO sent_emails (sent_at) VALUES (?)", (datetime.now(),))

        # Commit changes and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)

# add_data_with_view("14/03/2024", True)

def send_final_mail():
    return
    # Check if an email has been sent within the last 15 minutes
    if has_sent_email_within_last_15_minutes() or True:
        views_per_day = get_views_per_day()
        body = ''
        for date, count in views_per_day.items():
            print(f"Date: {date}, Total Views: {count}")
            body += f"Date: {date}, Total Views: {count}\n"
        sm = SendErrorMail()
        sm.send_email(system_no=SYSTEM_NO,subject="Unique view on xana.net",body=body)
        print("Sending email...")
        mark_email_as_sent()

