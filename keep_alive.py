
from flask import Flask
from threading import Thread
import logging

app = Flask('')
logging.basicConfig(level=logging.INFO)

@app.route('/')
def home():
    return "Prediction Bot is alive!", 200

def run():
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logging.error(f"Keep alive server error: {e}")

def keep_alive():
    logging.info("Starting keep alive server...")
    t = Thread(target=run)
    t.daemon = True  # This ensures the thread will stop when the main program stops
    t.start()
    logging.info("Keep alive server started")
