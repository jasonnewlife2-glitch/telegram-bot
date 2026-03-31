# Telegram Signal Bot

A Python-based Telegram bot built with `aiogram` and `flask` (for keep-alive) that provides game signals (Mines, Aviator, etc.).

## Project Structure
- `main.py`: Main bot logic.
- `keep_alive.py`: Flask server to keep the bot running.
- `attached_assets/`: Media files for the bot.
- `static/`, `templates/`: Web files for the keep-alive server.
- `*.json`: Persistent storage for users and state.

## Setup
1. Set `BOT_TOKEN` and `ADMIN_ID` in Secrets.
2. Run `python main.py`.