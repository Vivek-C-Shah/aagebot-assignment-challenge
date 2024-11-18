from http.server import HTTPServer, SimpleHTTPRequestHandler
import logging
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve the token and server URL from environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SERVER_URL = os.getenv('SERVER_URL')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name
    await update.message.reply_text(f'Welcome, {first_name}! Send /create to get your link.')

async def create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.effective_user.first_name
    user_id = update.effective_user.id
    print("user info", update.effective_user)
    
    # Make a request to the Flask app to create or retrieve the user link
    response = requests.post(f'{SERVER_URL}/create_user', json={'telegram_user_id': user_id})
    data = response.json()
    
    if data['new']:
        await update.message.reply_text(f'{first_name}, your new link is: {SERVER_URL}/link/{data["uuid"]}')
    else:
        await update.message.reply_text(f'{first_name}, your account is already connected. Your link is: {SERVER_URL}/link/{data["uuid"]}')

def run_http_server():
    port = int(os.getenv('PORT', 8080))
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Starting HTTP server on port {port}")
    httpd.serve_forever()

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('create', create))
    
    # Start the HTTP server in a separate thread
    threading.Thread(target=run_http_server, daemon=True).start()
    
    application.run_polling()

if __name__ == '__main__':
    main()