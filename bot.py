import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3
import uuid
import os
from dotenv import load_dotenv
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

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
        # User does not exist, create a new UUID and insert it
        new_uuid = str(uuid.uuid4())
        try:
            cursor.execute('INSERT INTO UserLink (telegram_user_id, uuid) VALUES (?, ?)', (user_id, new_uuid))
            conn.commit()
            link = f'{SERVER_URL}/link/{new_uuid}'
            await update.message.reply_text(f'{first_name}, your link is: {link}')
        except Exception as e:
            print(e)
    
    conn.close()

# def run_http_server():
#     port = int(os.getenv('PORT', 8080))
#     server_address = ('', port)
#     httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
#     print(f"Starting HTTP server on port {port}")
#     httpd.serve_forever()

async def main():
    init_db()
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('create', create))

    # Initialize the application
    await application.initialize()

    # Set webhook
    await application.bot.set_webhook(f'{SERVER_URL}/webhook/{TOKEN}')

    # Start the application
    await application.start()
    await application.updater.start_webhook(
        listen='0.0.0.0',
        port=int(os.getenv('PORT', 8080)),
        url_path=f'/webhook/{TOKEN}',
        webhook_url=f'{SERVER_URL}/webhook/{TOKEN}'
    )

    await application.idle()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())