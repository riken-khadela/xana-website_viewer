import sqlite3

# Specify the path to your database file
db_file = 'db.db'

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

        # Create a trigger to automatically insert or update data in "attached_table" when a row is inserted into "main_table" with view set to true
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS insert_or_update_attached_table
            AFTER INSERT ON main_table
            WHEN NEW.view = 1
            BEGIN
                -- Check if a record with the same date already exists
                DECLARE existing_count INTEGER;
                SELECT COUNT(*) INTO existing_count FROM attached_table WHERE date = NEW.date;

                -- If a record exists, increment the number column; otherwise, insert a new record
                IF existing_count > 0 THEN
                    UPDATE attached_table SET number = number + 1 WHERE date = NEW.date;
                ELSE
                    INSERT INTO attached_table (date, number) VALUES (NEW.date, 1);
                END IF;
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

# create_db_ifnot()

# add_data_with_view("14/03/2024", True)
# add_data_with_view("14/03/2024", False) # Adding a view for a different date

# views_per_day = get_views_per_day()
# for date, count in views_per_day.items():
#     print(f"Date: {date}, Total Views: {count}")
print(get_views_per_day())