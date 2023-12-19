# Finance Tracker
This is a simple finance tracker app using Python's Tkinter library for graphical user interface and Postgresql for storing the expenses.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Overview
This application allows you to keep record of your expenses and visualize your expenses over the current month in a pie-chart or the whole year till the current month in a bar graph.

## Features
- Interactive GUI interface built with tkinter.
- Add a expense along with the date, amount, category and remaks.
- Delete an added expense i.e. Undo fucntionality. 
- Get the list of your recent expenses.
- Visualize your monthly and yearly expenses.

## Requirements
- Python 3.x
- Tkinter (usually included in Python installations)
- Postgres (psycopg2)
- Tkcalendar
- Matplotlib (to visualize expenses)
- Pillow (to save and access the charts)

## Installation
1. Create a directory:
   ```bash
   mkdir <directory_name>
   ```

2. Create a virtual environment:
   ```bash
   cd <directory_name>
   python -m venv env
   ```

3. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

4. Create a database:
  - Install PostgreSQL: If you haven't already, install PostgreSQL on your local machine.

  - Access PostgreSQL: Use the command line or a GUI like pgAdmin to access PostgreSQL.

  - Create a Database: Run the following SQL command to create a new database (replace <database_name> with your desired name):
    - open psql shell:
    ```bash
    psql -U <usernamne>
    ```
    - Create a database
    ```bash
   CREATE DATABASE <database_name>;```

    


## Usage
1. Open a terminal or command prompt.
2. Navigate to the directory where the app files are located.
3. Activate the virtual environment: `source env/bin/activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run the command `cd FINANCE_TRACKER`.
6. Navigate to the set_database.py and set the database.
7. Run the command: `python project.py`.
8. The gui window will appear. Add your expenses and visualize.
9. Have fun

## Contributing
Contributions are welcome! Feel free to open issues or pull requests for any improvements or bug fixes.

## License
This project is licensed under the [MIT License](LICENSE).
