from db_connector import DatabaseConnector
from datetime import datetime, timedelta
import random

def seed_database():
    print("Connecting to database...")
    db = DatabaseConnector()
    db.connect()
    
    habits = db.fetch_all_habits()
    
    if not habits:
        print("No habits found! Please run db_connector.py first to create the tables and predefined habits.")
        return

    today = datetime.now()
    events_added = 0
    
    print("Generating 4 weeks of historical tracking data...")
    
    for habit in habits:
        habit_id = habit[0]
        habit_name = habit[1]
        periodicity = habit[2]
        
        if periodicity.lower() == 'daily':
            for i in range(28):
                if random.random() > 0.15:  # 85% chance
                    past_date = today - timedelta(days=27 - i)
                    timestamp = past_date.strftime("%Y-%m-%d 10:00:00")
                    db.insert_tracking_event(habit_id, timestamp)
                    events_added += 1
                    
        elif periodicity.lower() == 'weekly':
            for i in range(4):
                past_date = today - timedelta(weeks=3 - i)
                timestamp = past_date.strftime("%Y-%m-%d 10:00:00")
                db.insert_tracking_event(habit_id, timestamp)
                events_added += 1

    print(f"Success! Inserted {events_added} tracking events across your predefined habits.")

if __name__ == "__main__":
    seed_database()