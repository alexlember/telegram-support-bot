import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_logging_chat_id() -> int or None:
    val = os.getenv("LOGGING_CHAT_ID")
    return int(val) if val is not None else None


def get_passphrase() -> str or None:
    return os.getenv("PASSPHRASE")

def get_superusers() -> list:
    return list(map(lambda x: int(x), os.getenv("SUPERUSERS").split()))

TELEGRAM_TOKEN = os.getenv("REFUGEE_TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    raise Exception("Please setup the .env variable REFUGEE_TELEGRAM_TOKEN.")

SUPPORT_CHAT_ID = int(os.getenv("SUPPORT_CHAT_ID"))
if SUPPORT_CHAT_ID is None:
    raise Exception("Please setup the .env variable SUPPORT_CHAT_ID.")

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
if POSTGRES_PASSWORD is None:
    raise Exception("Please setup the .env variable POSTGRES_PASSWORD.")

POSTGRES_USER = os.getenv("POSTGRES_USER")
if POSTGRES_USER is None:
    raise Exception("Please setup the .env variable POSTGRES_USER.")

POSTGRES_DB = os.getenv("POSTGRES_DB")
if POSTGRES_DB is None:
    raise Exception("Please setup the .env variable POSTGRES_DB.")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

CONNECT_WITH_OPERATORS_ENABLED = bool(os.getenv("CONNECT_WITH_OPERATORS_ENABLED", "True"))

HELLO_GENERAL_MESSAGE = """
Добро пожаловать в Швецию!
Полезная информация для собирающихся или приехавших в Швецию из Украины, а также для тех, кто хотел бы помочь. 
Информация упорядочена по разделам. Изучайте, нажимая на нужные кнопки.
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
Добрый день! К сожалению, нас очень мало, но мы очень постараемся вам помочь.
Убедительная просьба для начала изучить разделы "Мне нужна помощь" и "Хочу помочь",
возможно там уже есть ответ на ваш вопрос. Если ответа там нет, тогда опишите ваш вопрос 
как можно подробнее, чтобы наши координаторы смогли сразу ответить. 
К вопросу можете приложить фотографии и другие файлы.
"""
