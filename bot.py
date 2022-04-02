from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from settings import TELEGRAM_TOKEN


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello {update.effective_user.first_name}')


def on_call(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.effective_user.first_name}, you are on-call')


def off_call(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.effective_user.first_name}, you are off-call')


def need_help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.effective_user.first_name}, here are some useful links if you need help')


def ready_to_help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'{update.effective_user.first_name}, here are some useful links if you want to help')


updater = Updater(TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(CommandHandler('oncall', on_call))
updater.dispatcher.add_handler(CommandHandler('offcall', off_call))
updater.dispatcher.add_handler(CommandHandler('readytohelp', ready_to_help))
updater.dispatcher.add_handler(CommandHandler('needhelp', need_help))

updater.start_polling()
updater.idle()
