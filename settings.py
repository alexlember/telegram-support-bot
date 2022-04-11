import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv("REFUGEE_TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    raise Exception("Please setup the .env variable REFUGEE_TELEGRAM_TOKEN.")

SUPPORT_CHAT_ID = int(os.getenv("SUPPORT_CHAT_ID"))
if SUPPORT_CHAT_ID is None:
    raise Exception("Please setup the .env variable SUPPORT_CHAT_ID.")

PORT = int(os.environ.get('PORT', '8443'))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME")

CONNECT_WITH_OPERATORS_ENABLED = False

HELLO_GENERAL_MESSAGE = """
Вы приехали в Швецию или только собираетесь сюда? Вам нужна помощь? Вы хотите сами помочь, 
но не знаете как? 
Здесь вы сможете легко найти полезную информацию, упорядоченную по разделам.
Изучайте их, нажимая на нужные кнопки. 
Скоро появится функция прямой связи с волонтерами. 
"""

HELLO_CONNECT_MESSAGE = """
Связаться с нами и задать вопрос можно будет через кнопку “Связаться с координаторами”, несколько волонтеров будут время от времени проверять, 
поступили ли новые сообщения, и реагировать на них.
"""

REPLY_TO_THIS_MESSAGE_TXT = "Reply на это сообщение"
WRONG_REPLY_TXT = "Ошибка при Reply (не то сообщение)"

READY_TO_HELP_BTN_TXT = "Хочу помочь"
NEED_HELP_BTN_TXT = "Мне нужна помощь"
CONNECT_TO_VOLUNTEER_BTN_TXT = "Связаться с координаторами"

CONNECT_TO_VOLUNTEER_INFORMATION = """
Нас очень мало, но мы стараемся помогать всем по возможности.
Убедительная просьба для начала изучить разделы "Хочу помочь" или "Мне нужна помощь",
возможно там уже будет ответ на ваш вопрос. 
"""


def get_logging_chat_id():
    return os.getenv("LOGGING_CHAT_ID")
