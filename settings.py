import os
from dotenv import load_dotenv, find_dotenv

# Loading .env variables
load_dotenv(find_dotenv())

TELEGRAM_TOKEN = os.getenv("REFUGEE_TELEGRAM_TOKEN")
if TELEGRAM_TOKEN is None:
    raise Exception("Please setup the .env variable REFUGEE_TELEGRAM_TOKEN.")
