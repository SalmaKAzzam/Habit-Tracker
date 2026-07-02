from db_connector import DatabaseConnector
from models import Habit
from datetime import datetime
from analytics import get_all_habits, filter_by_periodicity, calculate_longest_streak, calculate_longest_streak_of_all
from models import TrackingEvent

class HabitTracker:
    """Main app controller linking the DB and the CLI"""
    def __init__(self):
        self.db = DatabaseConnector()
        self.db.connect()

    def run_cli_menu(self):
        """Runs the main interactive loop"""
        while True:
            print("\n--- Habit Tracker Menu ---")
            print("1. View Habits")
            print("2. Add Habit")
            print("3. Edit Habit")
            print("4. Delete Habit")
            print("5. Check-off Habit")
            print("6. Analytics")
            print("7. Exit")
            
            choice = input("\nSelect an option (1-7): ").strip()
            
            if choice == '1':
                print("\n--- Your Current Habits ---")
                habits_data = self.db.fetch_all_habits()
                
                if not habits_data:
                    print("No habits found! Try adding some.")
                else:
                    for data in habits_data:
                        habit = Habit(id=data[0], name=data[1], periodicity=data[2], creation_date=data[3])
                        print(habit)
                        
            elif choice == '2':
                print("\n--- Add a New Habit ---")
                name = input("Enter the habit name (e.g., Meditate): ")
                periodicity = input("Enter periodicity (Daily/Weekly): ")
                creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                self.db.insert_habit(name, periodicity, creation_date)
                print(f"\nSuccess! '{name}' has been added to your habits.")
                
            elif choice == '3':
                print("\n--- Edit a Habit ---")
                habits_data = self.db.fetch_all_habits()
                
                if not habits_data:
                    print("No habits found! Try adding some first.")
                    continue
                
                for data in habits_data:
                    habit = Habit(id=data[0], name=data[1], periodicity=data[2], creation_date=data[3])
                    print(habit)
                    
                try:
                    habit_id = int(input("\nEnter the ID of the habit you want to edit: ").strip())
                    valid_ids = [data[0] for data in habits_data]
                    
                    if habit_id in valid_ids:
                        new_name = input("Enter the new habit name: ").strip()
                        new_periodicity = input("Enter new periodicity (Daily/Weekly): ").strip()
                        
                        self.db.edit_habit(habit_id, new_name, new_periodicity)
                        print(f"\nSuccess! Habit ID {habit_id} has been updated.")
                    else:
                        print(f"\nError: Habit with ID {habit_id} does not exist.")
                        
                except ValueError:
                    print("\nInvalid input. Please enter a valid numerical ID.")
                    
            elif choice == '4':
                print("\n--- Delete a Habit ---")
                habits_data = self.db.fetch_all_habits()
                
                if not habits_data:
                    print("No habits found! Try adding some first.")
                    continue
                
                for data in habits_data:
                    habit = Habit(id=data[0], name=data[1], periodicity=data[2], creation_date=data[3])
                    print(habit)
                    
                try:
                    habit_id = int(input("\nEnter the ID of the habit you want to delete: ").strip())
                    valid_ids = [data[0] for data in habits_data]
                    
                    if habit_id in valid_ids:
                        confirm = input(f"Are you sure you want to delete Habit ID {habit_id}? This deletes all its history too. (y/n): ").strip().lower()
                        if confirm == 'y':
                            self.db.delete_habit(habit_id)
                            print(f"\nSuccess! Habit ID {habit_id} has been completely deleted.")
                        else:
                            print("\nDeletion cancelled.")
                    else:
                        print(f"\nError: Habit with ID {habit_id} does not exist.")
                        
                except ValueError:
                    print("\nInvalid input. Please enter a valid numerical ID.")

            elif choice == '5':
                print("\n--- Check-off a Habit ---")
                habits_data = self.db.fetch_all_habits()
                
                if not habits_data:
                    print("No habits found! Try adding some first.")
                    continue
                
                for data in habits_data:
                    habit = Habit(id=data[0], name=data[1], periodicity=data[2], creation_date=data[3])
                    print(habit)
                    
                try:
                    habit_id_input = input("\nEnter the ID of the habit you want to check off: ").strip()
                    habit_id = int(habit_id_input)
                    
                    valid_ids = [data[0] for data in habits_data]
                    
                    if habit_id in valid_ids:
                        completion_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.db.insert_tracking_event(habit_id, completion_timestamp)
                        
                        habit_name = next(data[1] for data in habits_data if data[0] == habit_id)
                        print(f"\nAwesome! You just checked off '{habit_name}' at {completion_timestamp}.")
                    else:
                        print(f"\nError: Habit with ID {habit_id} does not exist. Please try again.")
                        
                except ValueError:
                    print("\nInvalid input. Please enter a valid numerical ID.")
                
            elif choice == '6':
                print("\n--- Analytics Menu ---")
                print("A. View all currently tracked habits")
                print("B. View habits by periodicity")
                print("C. View longest run streak of all habits")
                print("D. View longest run streak for a given habit")
                
                analytic_choice = input("\nSelect an analytic (A-D): ").strip().upper()
                
                habits_data = self.db.fetch_all_habits()
                all_habits = [Habit(id=data[0], name=data[1], periodicity=data[2], creation_date=data[3]) for data in habits_data]
                
                if analytic_choice == 'A':
                    print("\n--- All Tracked Habits ---")
                    tracked = get_all_habits(all_habits)
                    for h in tracked:
                        print(h)
                        
                elif analytic_choice == 'B':
                    period = input("Enter periodicity to filter by (Daily/Weekly): ").strip()
                    print(f"\n--- {period.capitalize()} Habits ---")
                    filtered_habits = filter_by_periodicity(all_habits, period)
                    
                    if not filtered_habits:
                        print(f"No {period} habits found.")
                    else:
                        for h in filtered_habits:
                            print(h)
                            
                elif analytic_choice == 'C':
                    print("\n--- Longest Streak Across All Habits ---")
                    events_data = self.db.fetch_all_events()
                    all_events = [TrackingEvent(id=e[0], habit_id=e[1], completion_timestamp=e[2]) for e in events_data]
                    
                    streak, best_habit_name = calculate_longest_streak_of_all(all_habits, all_events)
                    print(f"Your longest streak ever is {streak} consecutive completions on the habit '{best_habit_name}'!")

                elif analytic_choice == 'D':
                    print("\n--- Longest Streak for a Specific Habit ---")
                    for h in all_habits:
                        print(h)
                        
                    try:
                        habit_id = int(input("\nEnter the ID of the habit to analyze: ").strip())
                        selected_habit = next((h for h in all_habits if h.id == habit_id), None)
                        
                        if selected_habit:
                            events_data = self.db.fetch_events_for_habit(habit_id)
                            events = [TrackingEvent(id=e[0], habit_id=e[1], completion_timestamp=e[2]) for e in events_data]
                            
                            streak = calculate_longest_streak(events, selected_habit.periodicity)
                            print(f"\nYour longest streak for '{selected_habit.name}' is {streak} consecutive completions!")
                        else:
                            print("Habit ID not found.")
                            
                    except ValueError:
                        print("Invalid input. Please enter a numerical ID.")
                else:
                    print("\nInvalid choice.")
                
            elif choice == '7':
                print("\nExiting Habit Tracker. Goodbye!")
                break
                
            else:
                print("\nInvalid choice. Please enter a number from 1 to 7.")

if __name__ == "__main__":
    app = HabitTracker()
    app.run_cli_menu()