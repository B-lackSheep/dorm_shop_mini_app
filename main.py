import uvicorn
import logging
from telegram_bot import start_bot_polling
import threading


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_bot():
    try:
        start_bot_polling()
    except Exception as e:
        logger.error(f"Bot failed with exception: {e}")
        threading.Timer(5.0, run_bot).start()


def run_web():
    uvicorn.run(
        "web:app",
        host="0.0.0.0",
        port=8000
    )


if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    run_web()