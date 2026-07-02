class Habit:
    """Represents a single habit tracking model."""
    def __init__(self, id, name, periodicity, creation_date):
        self.id = id
        self.name = name
        self.periodicity = periodicity
        self.creation_date = creation_date

    def __str__(self):
        return f"[{self.id}] {self.name} ({self.periodicity}) - Created: {self.creation_date}"

class TrackingEvent:
    """Stores the timestamp for when a habit gets checked off."""
    def __init__(self, id, habit_id, completion_timestamp):
        self.id = id
        self.habit_id = habit_id
        self.completion_timestamp = completion_timestamp