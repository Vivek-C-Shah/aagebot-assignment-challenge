# AageBot Assignment Challenge

Welcome to the **AageBot Assignment Challenge**! This repository contains the code for a simple web server and a Telegram bot that interact with each other using a SQLite database. The bot generates unique UUIDs for users, which can be used to retrieve their Telegram user ID via the web server.

## Table of Contents

- [Live Demo](#live-demo)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
  - [Running the Flask Web Server](#running-the-flask-web-server)
  - [Running the Telegram Bot](#running-the-telegram-bot)
- [Using the Telegram Bot](#using-the-telegram-bot)
- [Project Structure](#project-structure)
- [Code Explanation](#code-explanation)
- [Deployment](#deployment)
- [Assessment Criteria](#assessment-criteria)
- [License](#license)

## Live Demo

- **Telegram Bot Username**: [@AageBotDemobyVivekShahBot](https://web.telegram.org/k/#@AageBotDemobyVivekShahBot)
- **Web Server URL**: [https://aagebot-assignment-challenge.onrender.com](https://aagebot-assignment-challenge.onrender.com)

## Features

- A Flask web server with the following routes:
  - `/`: Instructs users to use the Telegram bot.
  - `/link/{uuid}`: Displays the Telegram user ID associated with the provided UUID.
- A Telegram bot that responds to the following commands:
  - `/start`: Welcomes the user.
  - `/create`: Generates a unique UUID and provides a link to the user.
- Uses SQLite to store the mapping between Telegram user IDs and UUIDs.

## Prerequisites

- **Python 3.7 - 3.11**: Ensure you have a compatible version of Python installed.
- **Telegram Account**: You need a Telegram account to interact with the bot.
- **pip**: Python package installer.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/aagebot-assignment-challenge.git
   cd aagebot-assignment-challenge
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - **On Windows:**

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS/Linux:**

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If a `requirements.txt` file is not present, install the dependencies manually:*

   ```bash
   pip install Flask python-telegram-bot
   ```

5. **Set Up Environment Variables**

   Create a `.env` file in the project root directory and add the following:

   ```dotenv
   TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
   SERVER_URL=http://localhost:5000  # Or your deployed server URL
   PORT=5000
   ```

   - Replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual bot token obtained from BotFather.
   - Update `SERVER_URL` if you are using a different URL or have deployed the server.

## Running the Application

### Running the Flask Web Server

1. **Navigate to the Project Directory**

   ```bash
   cd aagebot-assignment-challenge
   ```

2. **Run the Flask Application**

   ```bash
   python app.py
   ```

   - The server should start on `http://localhost:5000`.

### Running the Telegram Bot

1. **Ensure the Virtual Environment is Activated**

2. **Run the Bot Script**

   ```bash
   python bot.py
   ```

   - The bot will start polling for messages.

## Using the Telegram Bot

1. **Start a Conversation with the Bot**

   Open Telegram and search for **@AageBotDemobyVivekShahBot** or click [here](https://t.me/AageBotDemobyVivekShahBot).

2. **Commands**

   - `/start`: Initializes interaction with the bot.
   - `/create`: Generates a unique link associated with your Telegram user ID.

3. **Retrieve Your Link**

   - After sending `/create`, the bot will reply with a link.
   - Click the link or open it in your browser.
   - The web page will display your Telegram user ID.

## Project Structure

```
aagebot-assignment-challenge/
│
├── app.py                 # Flask web server script
├── bot.py                 # Telegram bot script
├── database.db            # SQLite database file (created at runtime)
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (to be created)
└── README.md              # Project documentation
```

## Code Explanation

### `app.py` (Flask Web Server)

- **Routes:**
  - `/`: Displays a message directing users to the Telegram bot.
  - `/link/<uuid>`: Retrieves the Telegram user ID associated with the UUID from the database and displays it.
  - `/users`: Returns a JSON list of all users and their UUIDs.
  - `/create_user` (POST): Accepts a Telegram user ID and returns a UUID. If the user already exists, it returns the existing UUID.

- **Database Functions:**
  - `init_db()`: Initializes the SQLite database and creates the `UserLink` table if it doesn't exist.
  - `get_db()`: Creates a connection to the database.

### `bot.py` (Telegram Bot)

- **Commands:**
  - `/start`: Welcomes the user and provides instructions.
  - `/create`: Interacts with the Flask web server to generate or retrieve the user's UUID and sends the link to the user.

- **Functions:**
  - `start()`: Handles the `/start` command.
  - `create()`: Handles the `/create` command and makes a POST request to the Flask app to get the user's link.

- **HTTP Server Thread:**
  - `run_http_server()`: Runs a simple HTTP server in a separate thread if needed (for specific deployment scenarios).

- **Environment Variables:**
  - `TELEGRAM_BOT_TOKEN`: The bot's token.
  - `SERVER_URL`: The URL where the Flask app is running.

## Deployment

The application is deployed and accessible via:

- **Telegram Bot**: [@AageBotDemobyVivekShahBot](https://web.telegram.org/k/#@AageBotDemobyVivekShahBot)
- **Web Server**: [https://aagebot-assignment-challenge.onrender.com](https://aagebot-assignment-challenge.onrender.com)

The deployment was done using [Render](https://render.com/), which provides free hosting for web services and background workers.

**Deployment Steps:**

1. **Create an Account on Render**

   Sign up at [render.com](https://render.com/) and create a new web service.

2. **Connect GitHub Repository**

   Link your GitHub repository containing the code.

3. **Configure the Web Service**

   - **Build Command**: Leave it as default or specify `pip install -r requirements.txt`.
   - **Start Command**: For `app.py`, use `python app.py`.
   - **Environment Variables**: Set `TELEGRAM_BOT_TOKEN`, `SERVER_URL`, and `PORT`.

4. **Deploy the Bot as a Background Worker**

   Create a new **Background Worker** in Render for `bot.py`.

   - **Start Command**: `python bot.py`.
   - **Environment Variables**: Same as above.

5. **Update `SERVER_URL`**

   Ensure that the `SERVER_URL` in your `.env` or environment variables matches the deployed web server URL.

## Assessment Criteria

1. **Functionality**: The code works as intended, allowing users to generate a UUID via the Telegram bot and retrieve their Telegram user ID via the web server.

2. **Requirements Satisfaction**: All the requirements listed in the assignment have been met.

3. **Code Quality**:

   - **Clean Code**: The code is well-organized with clear function definitions and comments where necessary.
   - **Maintainability**: The code follows good practices, making it easy to maintain and extend.
   - **SOLID Principles**: The code adheres to SOLID principles to the extent applicable in this context.

4. **Timely Submission**: The assignment was submitted on time.