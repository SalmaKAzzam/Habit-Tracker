import sqlite3

class DatabaseConnector:
    """Handles all the SQLite database stuff"""
    def __init__(self, db_name="habits.db"):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def create_tables(self):
        """Creates the tables if they don't exist yet"""
        cursor = self.connection.cursor()
        
        # Table 1: habits
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL,
                creation_date DATETIME NOT NULL
            )
        ''')
        
        # Table 2: tracking_events
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracking_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                completion_timestamp DATETIME NOT NULL,
                FOREIGN KEY (habit_id) REFERENCES habits (id)
            )
        ''')
        
    def fetch_all_habits(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, periodicity, creation_date FROM habits")
        return cursor.fetchall()
    
    def insert_habit(self, name, periodicity, creation_date):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO habits (name, periodicity, creation_date) 
            VALUES (?, ?, ?)
        ''', (name, periodicity, creation_date))
        self.connection.commit()
    
    def insert_tracking_event(self, habit_id, completion_timestamp):
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO tracking_events (habit_id, completion_timestamp) 
            VALUES (?, ?)
        ''', (habit_id, completion_timestamp))
        self.connection.commit()
    
    def fetch_events_for_habit(self, habit_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, habit_id, completion_timestamp FROM tracking_events WHERE habit_id = ?", (habit_id,))
        return cursor.fetchall()

    def fetch_all_events(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, habit_id, completion_timestamp FROM tracking_events")
        return cursor.fetchall()
                
    def edit_habit(self, habit_id, new_name, new_periodicity):
        """Updates the name and periodicity of an existing habit in the database."""
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE habits 
            SET name = ?, periodicity = ? 
            WHERE id = ?
        ''', (new_name, new_periodicity, habit_id))
        self.connection.commit()

    def delete_habit(self, habit_id):
        """Deletes a habit and all of its associated tracking events to prevent orphaned data."""
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM tracking_events WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        self.connection.commit()
        

if __name__ == "__main__":
    db = DatabaseConnector()
    db.connect()
    
    db.create_tables()
    print("Database and tables created successfully!")
    
    cursor = db.connection.cursor()
    
    try:
        habits_data = [
            ('Drink Water', 'Daily', '2026-06-01 10:00:00'),
            ('Read 10 Pages', 'Daily', '2026-06-01 10:00:00'),
            ('Go for a Walk', 'Daily', '2026-06-01 10:00:00'),
            ('Grocery Shopping', 'Weekly', '2026-06-01 10:00:00'),
            ('Clean Apartment', 'Weekly', '2026-06-01 10:00:00')
        ]
        
        cursor.executemany('''
            INSERT INTO habits (name, periodicity, creation_date) 
            VALUES (?, ?, ?)
        ''', habits_data)
        
        db.connection.commit()
        print("5 predefined habits inserted successfully!")
        
    except sqlite3.Error as e:
        print(f"Oops, something went wrong: {e}")
        
    finally:
        db.connection.close()