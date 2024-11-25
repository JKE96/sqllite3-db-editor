from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('interfaces.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    return render_template('index.html', tables=tables)

@app.route('/table/<table_name>')
def get_table(table_name):
    conn = get_db_connection()
    rows = conn.execute(f'SELECT * FROM {table_name}').fetchall()
    columns = [description[0] for description in conn.execute(f'SELECT * FROM {table_name}').description]
    conn.close()
    return jsonify({'columns': columns, 'rows': [dict(row) for row in rows]})

@app.route('/update', methods=['POST'])
def update_table():
    data = request.json
    if 'table' not in data or 'column' not in data or 'value' not in data or 'id' not in data:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    table_name = data['table']
    column = data['column']
    value = data['value']
    row_id = data['id']
    
    conn = get_db_connection()
    conn.execute(f'UPDATE {table_name} SET {column} = ? WHERE id = ?', (value, row_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/delete', methods=['POST'])
def delete_rows():
    data = request.json
    if 'table' not in data or 'ids' not in data:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    table_name = data['table']
    ids = data['ids']
    
    conn = get_db_connection()
    conn.execute(f'DELETE FROM {table_name} WHERE id IN ({",".join("?" * len(ids))})', ids)
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@app.route('/add', methods=['POST'])
def add_row():
    data = request.json
    if 'table' not in data:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400

    table_name = data['table']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get the columns with NOT NULL constraints
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    not_null_columns = [col['name'] for col in columns_info if col['notnull']]
    
    # Create a dictionary with default values for NOT NULL columns
    default_values = {col: '' for col in not_null_columns}
    columns = ', '.join(default_values.keys())
    placeholders = ', '.join(['?'] * len(default_values))

    all_text_columns = [col['name'] for col in columns_info if col['type'] =='TEXT']
    default_text_values = {col: '' for col in all_text_columns}
    text_columns = ', '.join(default_text_values.keys())
    text_placeholders = ', '.join(['?'] * len(default_text_values))
    
    if(len(placeholders) > 0 ):
        cursor.execute(f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})', list(default_values.values()))
    elif (len(text_placeholders) > 0):
        cursor.execute(f'INSERT INTO {table_name} ({text_columns}) VALUES ({text_placeholders})', list(default_text_values.values()))
    else:
        conn.close()
        #TODO, prevent failing with only integer columns
        return jsonify({'status': 'error', 'message': 'No row with text data for initialization'}), 400
    
    conn.commit()
    row_id = cursor.lastrowid
    conn.close()
    return jsonify({'status': 'success', 'id': row_id})

@app.route('/options/<table_name>/<column_name>')
def get_options(table_name, column_name):
    conn = get_db_connection()
    rows = conn.execute(f'SELECT DISTINCT {column_name} FROM {table_name}').fetchall()
    conn.close()
    return jsonify([row[column_name] for row in rows])

if __name__ == '__main__':
    app.run(debug=True)