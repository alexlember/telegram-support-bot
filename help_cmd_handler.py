from telegram import Update
from telegram.ext import CallbackContext

from need_help import create_need_help_reply_markup, NEED_HELP_INFORMATION_WHERE_TO_SEARCH, \
    NEED_HELP_INFORMATION_REFUGEE_STATUS, NEED_HELP_INFORMATION_LIFE_IN_SWEDEN, NEED_HELP_INFORMATION_MEET_PEOPLE, \
    NEED_HELP_INFORMATION_FIND_ACCOMMODATION, NEED_HELP_INFORMATION_LANGUAGE, NEED_HELP_INFORMATION_FREE_OPTIONS, \
    NEED_HELP_INFORMATION_EDUCATION_INTEGRATION
from ready_to_help import create_ready_to_help_reply_markup, READY_TO_HELP_DONATE_INFORMATION, \
    READY_TO_HELP_PHYSICALLY_INFORMATION, READY_TO_HELP_SOCIALLY_INFORMATION


def handle_cmd_choice(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'need_help_where_to_search':
        query.message.reply_text(
            text='Ресурсы о том, где переселенцам можно найти информацию о помощи: '
                 + NEED_HELP_INFORMATION_WHERE_TO_SEARCH,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'need_help_refugee_status':
        query.message.reply_text(
            text='О статусе украинских переселенцев: ' + NEED_HELP_INFORMATION_REFUGEE_STATUS,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'need_help_life_in_swe':
        query.message.reply_text(
            text='Информация о жизни в Швеции: ' + NEED_HELP_INFORMATION_LIFE_IN_SWEDEN,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'need_help_meet_people':
        query.message.reply_text(
            text='Встречи для беженцев c Украины: ' + NEED_HELP_INFORMATION_MEET_PEOPLE,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'need_help_language':
        query.message.reply_text(
            text='Языковые Курсы: ' + NEED_HELP_INFORMATION_LANGUAGE,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'need_help_find_accommodation':
        query.message.reply_text(
            text='Найти Жилье: ' + NEED_HELP_INFORMATION_FIND_ACCOMMODATION,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'need_help_integration_education':
        query.message.reply_text(
            text='Бесплатные курсы и возможности для интеграции: ' + NEED_HELP_INFORMATION_EDUCATION_INTEGRATION,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'need_help_free_options':
        query.message.reply_text(
            text='Другие бесплатные возможности: ' + NEED_HELP_INFORMATION_FREE_OPTIONS,
            reply_markup=create_need_help_reply_markup()
        )
    elif query.data == 'ready_to_help_donate':
        query.message.reply_text(
            text='Варианты пожертвований: ' + READY_TO_HELP_DONATE_INFORMATION,
            reply_markup=create_ready_to_help_reply_markup()
        )
    elif query.data == 'ready_to_help_physically':
        query.message.reply_text(
            text='Варианты физической помощи: ' + READY_TO_HELP_PHYSICALLY_INFORMATION,
            reply_markup=create_ready_to_help_reply_markup()
        )
    elif query.data == 'ready_to_help_socially':
        query.message.reply_text(
            text='Варианты социальной помощи: ' + READY_TO_HELP_SOCIALLY_INFORMATION,
            reply_markup=create_ready_to_help_reply_markup()
        )
