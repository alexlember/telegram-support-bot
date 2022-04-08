from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, \
    MessageHandler, Filters
from settings import TELEGRAM_TOKEN, HELLO_MESSAGE, READY_TO_HELP_BTN_TXT, NEED_HELP_BTN_TXT, NEED_HELP_INFORMATION, \
    READY_TO_HELP_INFORMATION, CONNECT_TO_VOLUNTEER_INFORMATION, CONNECT_TO_VOLUNTEER_BTN_TXT, \
    REPLY_TO_THIS_MESSAGE_TXT, WRONG_REPLY_TXT
from storage import InMemSupportStorage


storage = InMemSupportStorage()


def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message with default buttons"""
    keyboard = [
        [
            KeyboardButton(READY_TO_HELP_BTN_TXT),
            KeyboardButton(NEED_HELP_BTN_TXT)
        ],
        [
            KeyboardButton(CONNECT_TO_VOLUNTEER_BTN_TXT)
        ]
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=False,
                                       resize_keyboard=True)

    update.message.reply_text(HELLO_MESSAGE, reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text=f"Selected option: {query.data}")


def on_call(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    storage.add_chat(chat_id)
    update.message.reply_text(f'the chat is on-call. Active chats: {storage.get_active_chats()}')


def off_call(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    was_removed = storage.remove_chat(chat_id)
    msg = 'The chat is off-call.'
    if was_removed:
        msg = "The chat is default and can't be removed from on-call."
    update.message.reply_text(msg + f" Active chats: {storage.get_active_chats()}")


def need_help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(NEED_HELP_INFORMATION)


def ready_to_help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(READY_TO_HELP_INFORMATION)


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
    else:
        context.bot.send_message(
            chat_id=chat_id,
            text=WRONG_REPLY_TXT
        )


updater = Updater(TELEGRAM_TOKEN)


updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + NEED_HELP_BTN_TXT + ')$'), need_help))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + READY_TO_HELP_BTN_TXT + ')$'), ready_to_help))
updater.dispatcher.add_handler(MessageHandler(Filters.regex('^(' + CONNECT_TO_VOLUNTEER_BTN_TXT + ')$'),
                                              connect_with_operators))
updater.dispatcher.add_handler(CommandHandler('oncall', on_call))
updater.dispatcher.add_handler(CommandHandler('offcall', off_call))
updater.dispatcher.add_handler(CommandHandler('readytohelp', ready_to_help))
updater.dispatcher.add_handler(CommandHandler('needhelp', need_help))

updater.dispatcher.add_handler(MessageHandler(Filters.chat_type.private, forward_to_support_chat))
updater.dispatcher.add_handler(MessageHandler(storage.get_chat_filter() & Filters.reply,
                                              forward_from_support_to_user))


updater.start_polling()
updater.idle()
