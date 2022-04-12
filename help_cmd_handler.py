from telegram import Update
from telegram.ext import CallbackContext

from need_help import create_need_help_reply_markup, NEED_HELP_INFORMATION_WHERE_TO_SEARCH, \
    NEED_HELP_INFORMATION_REFUGEE_STATUS, NEED_HELP_INFORMATION_LIFE_IN_SWEDEN, NEED_HELP_INFORMATION_MEET_PEOPLE, \
    NEED_HELP_INFORMATION_FIND_ACCOMMODATION, NEED_HELP_INFORMATION_LANGUAGE, NEED_HELP_INFORMATION_FREE_OPTIONS, \
    NEED_HELP_INFORMATION_EDUCATION_INTEGRATION, NEED_HELP_INFORMATION_MEDICINE, NEED_HELP_INFORMATION_PSYCHOLOGICAL, \
    NEED_HELP_INFORMATION_TRANSPORT, NEED_HELP_INFORMATION_HOW_TO_GET_TO_SWEDEN, need_help_menu, \
    create_back_to_need_help_reply_markup, send_reply_need_help_menu
from ready_to_help import create_ready_to_help_reply_markup, READY_TO_HELP_DONATE_INFORMATION, \
    READY_TO_HELP_PHYSICALLY_INFORMATION, READY_TO_HELP_SOCIALLY_INFORMATION, ready_to_help_menu, \
    create_back_to_ready_to_help_reply_markup, send_reply_ready_to_help_menu


def handle_cmd_choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'need_help_where_to_search':
        __send_msg_no_preview_need_help(query.message, 'Ресурсы о том, где переселенцам можно найти информацию о помощи: ' + NEED_HELP_INFORMATION_WHERE_TO_SEARCH)
    elif query.data == 'need_help_refugee_status':
        __send_msg_no_preview_need_help(query.message, 'О статусе украинских переселенцев: ' + NEED_HELP_INFORMATION_REFUGEE_STATUS)
    elif query.data == 'need_help_life_in_swe':
        __send_msg_no_preview_need_help(query.message, 'Информация о жизни в Швеции: ' + NEED_HELP_INFORMATION_LIFE_IN_SWEDEN)
    elif query.data == 'need_help_meet_people':
        __send_msg_no_preview_need_help(query.message, 'Встречи для беженцев из Украины: ' + NEED_HELP_INFORMATION_MEET_PEOPLE)
    elif query.data == 'need_help_language':
        __send_msg_no_preview_need_help(query.message, 'Языковые Курсы: ' + NEED_HELP_INFORMATION_LANGUAGE)
    elif query.data == 'need_help_find_accommodation':
        __send_msg_no_preview_need_help(query.message, 'Найти Жилье: ' + NEED_HELP_INFORMATION_FIND_ACCOMMODATION)
    elif query.data == 'need_help_integration_education':
        __send_msg_no_preview_need_help(query.message, 'Бесплатные курсы и возможности для интеграции: ' + NEED_HELP_INFORMATION_EDUCATION_INTEGRATION)
    elif query.data == 'need_help_free_options':
        __send_msg_no_preview_need_help(query.message, 'Досуг/спорт: ' + NEED_HELP_INFORMATION_FREE_OPTIONS)
    elif query.data == 'need_help_medicine':
        __send_msg_no_preview_need_help(query.message, 'Медицина: ' + NEED_HELP_INFORMATION_MEDICINE)
    elif query.data == 'need_help_psychological':
        __send_msg_no_preview_need_help(query.message, 'Психологическая помощь: ' + NEED_HELP_INFORMATION_PSYCHOLOGICAL)
    elif query.data == 'need_help_how_to_get_to_swe':
        __send_msg_no_preview_need_help(query.message, 'Как добраться до Швеции?: ' + NEED_HELP_INFORMATION_HOW_TO_GET_TO_SWEDEN)
    elif query.data == 'need_help_transport':
        __send_msg_no_preview_need_help(query.message, 'Транспорт: ' + NEED_HELP_INFORMATION_TRANSPORT)

    elif query.data == 'ready_to_help_donate':
        __send_msg_no_preview_ready_to_help(query.message, 'Варианты пожертвований: ' + READY_TO_HELP_DONATE_INFORMATION)
    elif query.data == 'ready_to_help_physically':
        __send_msg_no_preview_ready_to_help(query.message, 'Варианты физической помощи: ' + READY_TO_HELP_PHYSICALLY_INFORMATION)
    elif query.data == 'ready_to_help_socially':
        __send_msg_no_preview_ready_to_help(query.message, 'Варианты социальной помощи: ' + READY_TO_HELP_SOCIALLY_INFORMATION)

    elif query.data == 'back_to_need_help':
        send_reply_need_help_menu(query.message)
    elif query.data == 'back_to_ready_to_help':
        send_reply_ready_to_help_menu(query.message)


def __send_msg_no_preview_ready_to_help(query_message, text):
    __send_msg_no_preview(query_message, text, create_back_to_ready_to_help_reply_markup())


def __send_msg_no_preview_need_help(query_message, text):
    __send_msg_no_preview(query_message, text, create_back_to_need_help_reply_markup())


def __send_msg_no_preview(query_message, text, reply_markup):
    query_message.reply_text(
        text=text,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


