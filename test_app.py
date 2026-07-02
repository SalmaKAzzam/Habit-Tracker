import pytest
from datetime import datetime, timedelta
from models import Habit, TrackingEvent
from db_connector import DatabaseConnector
from analytics import get_all_habits, filter_by_periodicity, calculate_longest_streak, calculate_longest_streak_of_all

# --- 1. CORE OOP MODEL TESTS ---

def test_habit_model_creation():
    """Verify that the Habit class correctly stores metadata."""
    h = Habit(id=1, name="Read 10 Pages", periodicity="Daily", creation_date="2026-06-01 10:00:00")
    assert h.name == "Read 10 Pages"
    assert h.periodicity == "Daily"
    assert h.id == 1

# --- 2. DATABASE CRUD TESTS ---

@pytest.fixture
def temp_db():
    """Creates an isolated in-memory database specifically for testing."""
    db = DatabaseConnector(db_name=":memory:")
    db.connect()
    db.create_tables()
    yield db
    db.connection.close()

def test_database_insert_and_fetch_habit(temp_db):
    """Test creating and retrieving a habit."""
    temp_db.insert_habit("Meditate", "Daily", "2026-06-01 10:00:00")
    habits = temp_db.fetch_all_habits()
    
    assert len(habits) == 1
    assert habits[0][1] == "Meditate"

def test_database_edit_habit(temp_db):
    """Test editing an existing habit's name and periodicity."""
    temp_db.insert_habit("Run", "Daily", "2026-06-01 10:00:00")
    habits = temp_db.fetch_all_habits()
    habit_id = habits[0][0]
    
    # Edit the habit
    temp_db.edit_habit(habit_id, "Sprint", "Weekly")
    updated_habits = temp_db.fetch_all_habits()
    
    assert updated_habits[0][1] == "Sprint"
    assert updated_habits[0][2] == "Weekly"

def test_database_delete_habit(temp_db):
    """Test deleting a habit and ensuring it's removed from the database."""
    temp_db.insert_habit("Read", "Daily", "2026-06-01 10:00:00")
    habits_before = temp_db.fetch_all_habits()
    assert len(habits_before) == 1
    
    habit_id = habits_before[0][0]
    temp_db.delete_habit(habit_id)
    
    habits_after = temp_db.fetch_all_habits()
    assert len(habits_after) == 0

# --- 3. ANALYTICS MODULE TESTS ---

@pytest.fixture
def mock_habits():
    """Provides a predefined list of Habit objects for functional testing."""
    return [
        Habit(1, "Read", "Daily", "2026-06-01 10:00:00"),
        Habit(2, "Walk", "Daily", "2026-06-01 10:00:00"),
        Habit(3, "Clean", "Weekly", "2026-06-01 10:00:00")
    ]

def test_get_all_habits(mock_habits):
    """Test Analytics Function 1: Return all habits."""
    result = get_all_habits(mock_habits)
    assert len(result) == 3

def test_filter_by_periodicity(mock_habits):
    """Test Analytics Function 2: Filter by periodicity."""
    daily_habits = filter_by_periodicity(mock_habits, "Daily")
    weekly_habits = filter_by_periodicity(mock_habits, "Weekly")
    
    assert len(daily_habits) == 2
    assert len(weekly_habits) == 1
    assert weekly_habits[0].name == "Clean"

def test_calculate_longest_streak_daily():
    """Test Analytics Function 3: Longest streak for a specific habit (Daily)."""
    events = [
        TrackingEvent(1, 1, "2026-06-01 10:00:00"),
        TrackingEvent(2, 1, "2026-06-02 10:00:00"),
        TrackingEvent(3, 1, "2026-06-03 10:00:00")
    ]
    streak = calculate_longest_streak(events, "Daily")
    assert streak == 3

def test_calculate_longest_streak_weekly():
    """Test Analytics Function 3: Longest streak for a specific habit (Weekly)."""
    # 2026-06-01 is Week 23, 2026-06-08 is Week 24.
    events = [
        TrackingEvent(1, 3, "2026-06-01 10:00:00"), 
        TrackingEvent(2, 3, "2026-06-08 10:00:00")  
    ]
    streak = calculate_longest_streak(events, "Weekly")
    assert streak == 2

def test_calculate_longest_streak_of_all(mock_habits):
    """Test Analytics Function 4: Longest streak across all habits."""
    events = [
        # Habit 1 (Read) has a streak of 2
        TrackingEvent(1, 1, "2026-06-01 10:00:00"),
        TrackingEvent(2, 1, "2026-06-02 10:00:00"),
        # Habit 2 (Walk) has a streak of 3
        TrackingEvent(3, 2, "2026-06-01 10:00:00"),
        TrackingEvent(4, 2, "2026-06-02 10:00:00"),
        TrackingEvent(5, 2, "2026-06-03 10:00:00")
    ]
    
    streak, best_habit = calculate_longest_streak_of_all(mock_habits, events)
    assert streak == 3
    assert best_habit == "Walk"

# --- 4. 4-WEEK HISTORICAL DATA TEST ---

def test_4_weeks_historical_streak():
    """Verify streak calculations using 4 weeks (28 days) of time-series data."""
    base_date = datetime(2026, 5, 1) # Start May 1st
    events = []
    
    # We will simulate 28 consecutive days of checking off a daily habit
    for i in range(28):
        current_date = base_date + timedelta(days=i)
        timestamp = current_date.strftime("%Y-%m-%d 10:00:00")
        events.append(TrackingEvent(i+1, 1, timestamp))
        
    streak = calculate_longest_streak(events, "Daily")
    
    # The streak should perfectly equal 28
    assert streak == 28
    
    # Now simulate a break in the streak on day 15
    events.pop(14) 
    broken_streak = calculate_longest_streak(events, "Daily")
    
    # The longest streak should now be 14 (days 1-14) or 13 (days 16-28)
    assert broken_streak == 14