# Python CLI Habit Tracker

A lightweight, backend-focused Habit Tracking application built with Python. This app allows users to define daily and weekly habits, check them off, and track their longest streaks using an interactive Command Line Interface (CLI). 

This project was developed using Object-Oriented Programming (OOP) for state management and functional programming (map, filter, reduce) for data analytics. Data is securely and locally stored using SQLite3.

## Features
* **Create, Edit, and Delete Habits:** Fully manage your daily or weekly routines.
* **Tracking:** Check off habits as you complete them. 
* **Advanced Analytics:** * View all tracked habits.
  * Filter habits by periodicity (Daily vs. Weekly).
  * Calculate your longest continuous streak for a specific habit.
  * Discover your longest streak across all tracked habits.
* **Persistent Storage:** Zero-configuration SQLite3 database.

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd <your-repo-folder>

```

2. **Install requirements:**
The app uses standard Python libraries, but you will need `pytest` to run the test suite.
```bash
pip install pytest

```


3. **Initialize the Database & Predefined Data:**
Run the database connector to create the tables, and the seed file to generate 4 weeks' worth of test tracking data.
```bash
python db_connector.py
python seed.py

```



---

## Usage

To start the application and open the interactive main menu, run:

```bash
python main.py

```

### Screenshots

d:\Dated\Pictures\Screenshots\Screenshot 2026-07-03 015930.png d:\Dated\Pictures\Screenshots\Screenshot 2026-07-03 015835.png

---

## Running the Unit Tests

This project includes a comprehensive suite of Pytest unit tests covering the OOP models, database CRUD operations, analytics functions, and historical time-series streak validations.

To run the tests, simply execute:

```bash
pytest test_app.py -v

```

```

---