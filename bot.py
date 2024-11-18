from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
import uuid
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve the token and server URL from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SERVER_URL = os.getenv('SERVER_URL')
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name
    await update.message.reply_text(f'Welcome, {first_name}! Send /create to get your link.')

async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name
    print("user info", update.effective_user)
    user_id = update.effective_user.id
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if the user already exists
    cursor.execute('SELECT uuid FROM UserLink WHERE telegram_user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result:
        # User already exists, retrieve the existing UUID
        existing_uuid = result[0]
        link = f'{SERVER_URL}/link/{existing_uuid}'
        await update.message.reply_text(f'{first_name}, your account is already connected. Your link is: {link}')
    else:
        # User does not exist, create a new UUID and send a request to add it
        new_uuid = str(uuid.uuid4())
        try:
            response = requests.post(f'{SERVER_URL}/add_user', json={'telegram_user_id': user_id, 'uuid': new_uuid})
            if response.status_code == 201:
                link = f'{SERVER_URL}/link/{new_uuid}'
                await update.message.reply_text(f'{first_name}, your link is: {link}')
            else:
                await update.message.reply_text(f'Error: {response.json().get("error", "Unknown error")}')
        except Exception as e:
            print(e)
    
    conn.close()

def run_http_server():
    port = int(os.getenv('PORT', 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

def main():
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('create', create))
    
    # Start the HTTP server in a separate thread
    threading.Thread(target=run_http_server, daemon=True).start()
    
    application.run_polling()

if __name__ == '__main__':
    main()