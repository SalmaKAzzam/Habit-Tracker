from functools import reduce
from datetime import datetime

def get_all_habits(habits_list):
    """Just returns the list of habits."""
    return list(habits_list)

def filter_by_periodicity(habits_list, periodicity):
    """Filters the habit list by Daily or Weekly using a lambda."""
    return list(filter(lambda habit: habit.periodicity.lower() == periodicity.lower(), habits_list))

def calculate_longest_streak(events_list, periodicity):
    """Calculates the longest streak. Uses functional reduce to go through the dates and count consecutive ones"""
    if not events_list:
        return 0

    """Converts string timestamps from the objects into datetime objects"""
    dates = list(map(lambda e: datetime.strptime(e.completion_timestamp, "%Y-%m-%d %H:%M:%S"), events_list))

    if periodicity.lower() == 'daily':
        distinct_dates = sorted(list(set(map(lambda d: d.date(), dates))))

        def daily_reducer(acc, current_date):
            max_streak, current_streak, prev_date = acc
            if prev_date and (current_date - prev_date).days == 1:
                current_streak += 1
            else:
                current_streak = 1
            return (max(max_streak, current_streak), current_streak, current_date)

        return reduce(daily_reducer, distinct_dates, (0, 0, None))[0]

    elif periodicity.lower() == 'weekly':
        distinct_weeks = sorted(list(set(map(lambda d: d.isocalendar()[:2], dates))))

        def weekly_reducer(acc, current_week_tuple):
            max_streak, current_streak, prev_week = acc
            if prev_week:
                prev_y, prev_w = prev_week
                curr_y, curr_w = current_week_tuple
                
                is_consecutive = (curr_y == prev_y and curr_w == prev_w + 1) or \
                                 (curr_y == prev_y + 1 and curr_w == 1 and prev_w >= 52)
                
                if is_consecutive:
                    current_streak += 1
                else:
                    current_streak = 1
            else:
                current_streak = 1
                
            return (max(max_streak, current_streak), current_streak, current_week_tuple)

        return reduce(weekly_reducer, distinct_weeks, (0, 0, None))[0]
    
    return 0

def calculate_longest_streak_of_all(habits_list, all_events_list):
    """
    Calculates the longest streak across all defined habits.
    Uses functional map to calculate streaks for each habit, and reduce to find the maximum.
    """
    if not habits_list or not all_events_list:
        return 0, "None"

    def get_habit_streak(habit):
        habit_events = list(filter(lambda e: e.habit_id == habit.id, all_events_list))
        streak = calculate_longest_streak(habit_events, habit.periodicity)
        return (streak, habit.name)

    # Map each habit to a tuple of (streak, habit_name)
    streaks = list(map(get_habit_streak, habits_list))

    # Reduce to find the one with the maximum streak
    longest = reduce(lambda acc, curr: curr if curr[0] > acc[0] else acc, streaks, (0, "None"))
    return longest