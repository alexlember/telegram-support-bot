import logging

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, \
    MessageHandler, Filters

import settings
from help_cmd_handler import handle_cmd_choice
from need_help import need_help_menu
from ready_to_help import ready_to_help_menu
from settings import TELEGRAM_TOKEN, HELLO_GENERAL_MESSAGE, READY_TO_HELP_BTN_TXT, NEED_HELP_BTN_TXT, \
    CONNECT_TO_VOLUNTEER_INFORMATION, CONNECT_TO_VOLUNTEER_BTN_TXT, \
    REPLY_TO_THIS_MESSAGE_TXT, WRONG_REPLY_TXT, CONNECT_WITH_OPERATORS_ENABLED, HELLO_CONNECT_MESSAGE, \
    get_logging_chat_id, SUPPORT_CHAT_ID, get_passphrase
from storage import InMemSupportStorage, PostgresSupportStorage

AUTH_CMD_PREFIX_LENGTH = 5
AUTH_CMD_REGEXP = r'^(auth [^\s-]+)$'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

storage = PostgresSupportStorage()


def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message with default buttons"""
    keyboard = [
        [
            KeyboardButton(READY_TO_HELP_BTN_TXT),
            KeyboardButton(NEED_HELP_BTN_TXT)
        ]
    ]

    if CONNECT_WITH_OPERATORS_ENABLED:
        keyboard.append(
            [
                KeyboardButton(CONNECT_TO_VOLUNTEER_BTN_TXT)
            ]
        )

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=False,
                                       resize_keyboard=True)

    msg = HELLO_GENERAL_MESSAGE + HELLO_CONNECT_MESSAGE if CONNECT_WITH_OPERATORS_ENABLED else HELLO_GENERAL_MESSAGE
    update.message.reply_text(msg, reply_markup=reply_markup)

    user_id = update.message.from_user.id
    storage.insert_user_action(user_id, None, "/start")
    __log_info(f'/start is called. user_id: {user_id}', user_id, None, context)


def authorize(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    msg = update.message.text

    passphrase = get_passphrase()

    if passphrase is None:
        __log_info(f"/authorize is called. passphrase is not set, can't authorize",
                   user_id, None, context)
        update.message.reply_text("Permission denied")
    elif passphrase == msg[AUTH_CMD_PREFIX_LENGTH:]:
        __log_info(f"/authorize is called. passphrase matched, authorizing",
                   user_id, None, context)
        storage.insert_authorized_user(user_id)
        update.message.reply_text(f'you are authorized now!')
    else:
        __log_info(f"/authorize is called. passphrase not matched, can't authorize",
                   user_id, None, context)
        update.message.reply_text(f'you are not authorized')


def on_call(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    if not storage.is_user_authorized(user_id):
        __log_info(f'/oncall is called (unauthorized). chat_id: {chat_id}', user_id, chat_id, context)
        update.message.reply_text("Permission denied")
    else:
        storage.add_chat(chat_id)
        storage.insert_user_action(user_id, chat_id, "/on-call")
        update.message.reply_text(f'the chat is on-call. Active chats: {storage.get_active_chats()}')
        __log_info(f'/oncall is called. chat_id: {chat_id}', user_id, chat_id, context)


def off_call(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if not storage.is_user_authorized(user_id):
        __log_info(f'/offcall is called (unauthorized). chat_id: {chat_id}', user_id, chat_id, context)
        update.message.reply_text("Permission denied")
    else:
        was_removed = storage.remove_chat(chat_id)
        msg = 'The chat is off-call.'
        if not was_removed:
            msg = "The chat is default and can't be removed from on-call."
        storage.insert_user_action(user_id, chat_id, "/off-call")
        update.message.reply_text(msg + f" Active chats: {storage.get_active_chats()}")
        __log_info(f'/offcall is called. chat_id: {chat_id}', user_id, chat_id, context)


def off_call_all(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if user_id not in settings.get_superusers():
        __log_info(f'/offcalla is called (unauthorized). chat_id: {chat_id}', user_id, chat_id, context)
        update.message.reply_text("Permission denied")
    else:
        storage.remove_all_active_except_default(chat_id)
        storage.insert_user_action(user_id, chat_id, "/offcalla")
        update.message.reply_text("All chats except default are removed from on-call Active chats: "
                                  f"{storage.get_active_chats()}")
        __log_info(f'/offcalla is called. chat_id: {chat_id}', user_id, chat_id, context)


def unauth_all(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id

    if user_id not in settings.get_superusers():
        __log_info(f'/unautha is called (unauthorized). chat_id: {chat_id}', user_id, chat_id, context)
        update.message.reply_text("Permission denied")
    else:
        storage.unauthorize_all()
        storage.insert_user_action(user_id, chat_id, "/unautha")
        update.message.reply_text("All users are unauthorised. Please auth again")
        __log_info(f'/unautha is called. chat_id: {chat_id}', user_id, chat_id, context)


def connect_with_operators(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(CONNECT_TO_VOLUNTEER_INFORMATION)
    user_id = update.message.from_user.id
    chat_id = storage.next_chat_id(user_id)
    user_info = update.message.from_user.to_dict()
    storage.insert_user_action(user_id, chat_id, "/connect with operators")
    __log_info(f'/connect with operators is called. chat_id: {chat_id}, user_info: {user_info}',
               user_id, chat_id, context)
    context.bot.send_message(
        chat_id=chat_id,
        text=f"""
📞 Connected {user_info}.
        """,
    )


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
        storage.insert_user_action(user_id, chat_id, "/forward_to_support_chat (forbidden forward)")
        __log_info(f'/forward_to_support_chat is called (forbidden forward). chat_id: {chat_id}, user_id: {user_id}',
                   user_id, chat_id, context)
    else:
        storage.insert_user_action(user_id, chat_id, "/forward_to_support_chat")
        __log_info(f'/forward_to_support_chat is called. chat_id: {chat_id}, user_id: {user_id}',
                   user_id, chat_id, context)


def forward_from_support_to_user(update, context):
    chat_id = update.message.chat_id
    user_id = None
    from_user = update.message.from_user.id
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
        storage.insert_user_action(from_user, chat_id, f"/forward_from_support_to_user to user_id: {user_id}")
        __log_info(f'/forward_from_support_to_user is called. chat_id: {chat_id}, from user: {from_user} '
                   f'to user_id: {user_id}', from_user, chat_id, context)
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=WRONG_REPLY_TXT
        )
        storage.insert_user_action(from_user, chat_id, f"/forward_from_support_to_user (user find error) to user_id: {user_id}")
        __log_warn(f"/forward_from_support_to_user is called. From user: {from_user}. Can't find user_id {from_user} for chat_id: {chat_id}",
                   from_user, chat_id, context)


def __log_info(msg, user_id, chat_id, context):
    logger.info(msg)
    storage.insert_logging_event("info", user_id, chat_id, msg)
    __log_to_chat(msg, context)


def __log_warn(msg, user_id, chat_id, context):
    logger.warning(msg)
    storage.insert_logging_event("warn", user_id, chat_id, msg)
    __log_to_chat(msg, context)


def __log_to_chat(msg, context):
    logging_chat = get_logging_chat_id()
    if logging_chat is not None:
        context.bot.send_message(
            chat_id=logging_chat,
            text=msg
        )


updater = Updater(TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CallbackQueryHandler(handle_cmd_choice))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex(AUTH_CMD_REGEXP), authorize))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + NEED_HELP_BTN_TXT + ')$'), need_help_menu))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + READY_TO_HELP_BTN_TXT + ')$'), ready_to_help_menu))

if CONNECT_WITH_OPERATORS_ENABLED:
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + CONNECT_TO_VOLUNTEER_BTN_TXT + ')$'),
                                                  connect_with_operators))
    updater.dispatcher.add_handler(CommandHandler('oncall', on_call))
    updater.dispatcher.add_handler(CommandHandler('offcall', off_call))
    updater.dispatcher.add_handler(CommandHandler('offcalla', off_call_all))
    updater.dispatcher.add_handler(CommandHandler('unautha', unauth_all))

    updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.private, forward_to_support_chat))
    updater.dispatcher.add_handler(MessageHandler(storage.get_chat_filter() & Filters.reply,
                                                  forward_from_support_to_user))


storage.init_db()
storage.add_chat(SUPPORT_CHAT_ID)

# Run bot
# if HEROKU_APP_NAME is None:  # pooling mode

logger.info("Can't detect 'HEROKU_APP_NAME' env. Running bot in pooling mode.")
updater.start_polling()

# else:  # webhook mode
#     logger.info("Running bot in webhook mode. Make sure that this url is correct: "
#                 f"https://{HEROKU_APP_NAME}.herokuapp.com/")
#     updater.start_webhook(
#         listen="0.0.0.0",
#         port=PORT,
#         url_path=TELEGRAM_TOKEN,
#         webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}"
#     )

updater.idle()
