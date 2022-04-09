import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, \
    MessageHandler, Filters

from help_cmd_handler import handle_cmd_choice
from need_help import need_help_menu
from ready_to_help import ready_to_help_menu
from settings import TELEGRAM_TOKEN, HELLO_GENERAL_MESSAGE, READY_TO_HELP_BTN_TXT, NEED_HELP_BTN_TXT, \
    CONNECT_TO_VOLUNTEER_INFORMATION, CONNECT_TO_VOLUNTEER_BTN_TXT, \
    REPLY_TO_THIS_MESSAGE_TXT, WRONG_REPLY_TXT, CONNECT_WITH_OPERATORS_ENABLED, HELLO_CONNECT_MESSAGE
from storage import InMemSupportStorage

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

storage = InMemSupportStorage()


def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message with default buttons"""
    keyboard = [
        [
            KeyboardButton(READY_TO_HELP_BTN_TXT),
            KeyboardButton(NEED_HELP_BTN_TXT)
        ]
    ]

    if CONNECT_WITH_OPERATORS_ENABLED:
        keyboard.append([
                KeyboardButton(CONNECT_TO_VOLUNTEER_BTN_TXT)
            ]
        )

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=False,
                                       resize_keyboard=True)

    msg = HELLO_GENERAL_MESSAGE + HELLO_CONNECT_MESSAGE if CONNECT_WITH_OPERATORS_ENABLED else HELLO_GENERAL_MESSAGE
    update.message.reply_text(msg, reply_markup=reply_markup)

    logger.info(f'/start is called. user_id: {update.message.from_user.id}')


def on_call(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    storage.add_chat(chat_id)
    update.message.reply_text(f'the chat is on-call. Active chats: {storage.get_active_chats()}')
    logger.info(f'/oncall is called. chat_id: {chat_id}')


def off_call(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    was_removed = storage.remove_chat(chat_id)
    msg = 'The chat is off-call.'
    if was_removed:
        msg = "The chat is default and can't be removed from on-call."
    update.message.reply_text(msg + f" Active chats: {storage.get_active_chats()}")
    logger.info(f'/offcall is called. chat_id: {chat_id}')


def connect_with_operators(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(CONNECT_TO_VOLUNTEER_INFORMATION)
    user_id = update.message.from_user.id
    chat_id = storage.next_chat_id(user_id)
    user_info = update.message.from_user.to_dict()
    context.bot.send_message(
        chat_id=chat_id,
        text=f"""
📞 Connected {user_info}.
        """,
    )
    logger.info(f'/connect with operators is called. chat_id: {chat_id}, user_info: {user_info}')


def forward_to_support_chat(update, context):
    user_id = update.message.from_user.id
    chat_id = storage.next_chat_id(user_id)

    forwarded = update.message.forward(chat_id=chat_id)
    if not forwarded.forward_from:
        context.bot.send_message(
            chat_id=chat_id,
            reply_to_message_id=forwarded.message_id,
            text=f"{update.message.from_user.id}\n{REPLY_TO_THIS_MESSAGE_TXT}"
        )
        logger.info(f'/forward_to_support_chat is called (forbidden forward). chat_id: {chat_id}, user_id: {user_id}')
    else:
        logger.info(f'/forward_to_support_chat is called. chat_id: {chat_id}, user_id: {user_id}')


def forward_from_support_to_user(update, context):
    chat_id = update.message.chat_id
    user_id = None
    if update.message.reply_to_message.forward_from:
        user_id = update.message.reply_to_message.forward_from.id
    elif REPLY_TO_THIS_MESSAGE_TXT in update.message.reply_to_message.text:
        try:
            user_id = int(update.message.reply_to_message.text.split('\n')[0])
        except ValueError:
            user_id = None
    if user_id:
        context.bot.copy_message(
            message_id=update.message.message_id,
            chat_id=user_id,
            from_chat_id=update.message.chat_id
        )
        logger.info(f'/forward_from_support_to_user is called. chat_id: {chat_id}, user_id: {user_id}')
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=WRONG_REPLY_TXT
        )
        logger.warning(f"/forward_from_support_to_user is called. Can't find user_id for chat_id: {chat_id}")


updater = Updater(TELEGRAM_TOKEN)


updater.dispatcher.add_handler(CallbackQueryHandler(handle_cmd_choice))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + NEED_HELP_BTN_TXT + ')$'), need_help_menu))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + READY_TO_HELP_BTN_TXT + ')$'), ready_to_help_menu))

if CONNECT_WITH_OPERATORS_ENABLED:
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + CONNECT_TO_VOLUNTEER_BTN_TXT + ')$'),
                                                  connect_with_operators))
    updater.dispatcher.add_handler(CommandHandler('oncall', on_call))
    updater.dispatcher.add_handler(CommandHandler('offcall', off_call))

    updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.private, forward_to_support_chat))
    updater.dispatcher.add_handler(MessageHandler(storage.get_chat_filter() & Filters.reply,
                                                  forward_from_support_to_user))


updater.start_polling()
updater.idle()
