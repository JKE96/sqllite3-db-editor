# SQLite3 DB Editor

Contributors:
- GitHub Copilot
- Jarod England

## Overview

This project is a web-based SQLite3 database editor built using Flask and jQuery. It allows users to view, edit, add, and delete rows in any table within a given SQLite3 database. The tables are editable by allowing the user to double-click on a table cell and directly update the database. Dropdowns are provided for columns associated with other tables.

## Features

- View tables in an SQLite3 database
- Edit table cells by double-clicking
- Add new rows to tables
- Delete selected rows
- Dropdowns for columns associated with other tables

## Setup Instructions

### Prerequisites

- Python 3.x
- Flask
- jQuery
- Bootstrap

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/sqllite3_db_editing.git
    cd sqllite3_db_editing
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install flask
    ```

4. Initialize the SQLite3 database with sample data:
    ```sh
    python init_db.py
    ```

5. Run the Flask application:
    ```sh
    python app.py
    ```

6. Open your web browser and navigate to `http://127.0.0.1:5000/` to access the SQLite3 DB Editor.

### Dependencies

- [Flask](https://flask.palletsprojects.com/)
- [jQuery](https://jquery.com/)
- [Bootstrap](https://getbootstrap.com/)

## Usage

- Click on a table name to view its contents.
- Double-click on a table cell to edit its value.
- Use the "Add New Row" button to add a new row to the table.
- Use the "Allow Deleting Rows" button to enable row selection for deletion.
- Use the "Delete Selected Rows" button to delete the selected rows.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to all contributors for their efforts in making this project possible.