from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def init_db():
    """Initialize the database and create the UserLink table."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserLink (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER,
            uuid TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    return 'Please go to the Telegram bot and send /create to get your link.'

@app.route('/link/<uuid>')
def link(uuid):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT telegram_user_id FROM UserLink WHERE uuid = ?', (uuid,))
    result = cursor.fetchone()
    conn.close()
    if result:
        telegram_user_id = result[0]
        return f'The Telegram user ID associated with this link is: {telegram_user_id}'
    else:
        return 'Invalid link or no user associated with this link.'

@app.route('/users')
def get_users():
    """Retrieve all users and their UUIDs."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT telegram_user_id, uuid FROM UserLink')
    users = cursor.fetchall()
    conn.close()
    users_list = [{'telegram_user_id': user[0], 'uuid': user[1]} for user in users]
    return jsonify(users_list)

@app.route('/add_user', methods=['POST'])
def add_user():
    """Add a new user to the database."""
    data = request.json
    telegram_user_id = data.get('telegram_user_id')
    uuid = data.get('uuid')
    
    if not telegram_user_id or not uuid:
        return jsonify({'error': 'Invalid data'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO UserLink (telegram_user_id, uuid) VALUES (?, ?)', (telegram_user_id, uuid))
        conn.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        conn.close()
    
    return jsonify({'success': True}), 201

print(f'Starting the server on port 5000...')
if __name__ == '__main__':
    try:
        print(f'Starting the server on port 5000...')
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f'Error: {e}')
        raise e