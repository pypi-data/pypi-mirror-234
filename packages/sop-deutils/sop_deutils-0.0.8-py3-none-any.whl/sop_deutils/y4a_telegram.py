import requests
import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def send_message(
    text: str,
    bot_token: str = None,
    chat_id: str = None,
):
    """
    Send a message to a group chat of Telegram

    :param text: the message to send
    :param bot_token: the token of the bot which send the message
    :param chat_id: the chat id where the message is sent
    """

    if not bot_token:
        bot_token = '6318613524:AAG3_JGEsTZbSvcupG5aJk-jZPzghuf3yZ4'
    if not chat_id:
        chat_id = '-868321875'

    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": 'Markdown',
    }
    response = requests.post(telegram_url, json=payload)
    if response.status_code == 200:
        logging.info("Telegram alert sent successfully!")
    else:
        logging.info("Failed to send Telegram alert!")
