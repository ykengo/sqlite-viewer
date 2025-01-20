# SQLite Viewer

A modern SQLite database viewer built with PyQt5 and Fluent Design System. View database tables and execute SQL queries with a clean, intuitive interface.

## Features

- 🎨 Modern Fluent Design interface
- 📁 Easy database file selection
- 📊 View table structures and headers
- 💻 Execute custom SQL queries
- 📋 Results displayed in a readable format
- 🌗 Dark theme support

## Dependencies

- Python 3.x
- PyQt5
- qfluentwidgets
- pandas
- sqlite3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ykengo/sqlite-viewer.git
cd sqlite-viewer
```

2. Install dependencies:
  ```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. Launch the application
2. Click "Set the directory" to select your SQLite database file
3. Use the navigation panel to:
  - View table structures
  - Write and execute SQL queries
  - View query results

## Application Structure

- Backend: Handles database operations
  - view_table(): Lists tables and their headers
  - eval_query(): Executes SQL queries
- CustomMessageBox: Directory input dialog
- Demo: Main application window and UI logic

## Screenshots

![image](https://github.com/user-attachments/assets/bfd232db-3d34-4b44-bee4-9d6be6aec8b3)
![image](https://github.com/user-attachments/assets/3e040877-a191-4422-8f87-8b7d20d0cecc)
![image](https://github.com/user-attachments/assets/bb90b7b0-c4ca-45ae-ad38-1a0eb3dbda9c)
![image](https://github.com/user-attachments/assets/b52bb1e6-9b7a-4bb6-8335-b2e9e6a13903)



