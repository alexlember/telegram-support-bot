from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def ready_to_help_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Как вы хотите помочь?', reply_markup=create_ready_to_help_reply_markup())


def create_ready_to_help_reply_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Пожертвовать", callback_data='ready_to_help_donate')
        ],
        [
            InlineKeyboardButton("Помочь физически", callback_data='ready_to_help_physically')
        ],
        [
            InlineKeyboardButton("Поддержать морально", callback_data='ready_to_help_socially')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


READY_TO_HELP_DONATE_INFORMATION = """
1) Отправить донат гуманитарным организациям, работающим в Украине.
https://nuforum.se/Donation/donation/

2) Сбор гуманитарной помощи для отправки в Украину.
Адрес: Sveavägen 162 
Понедельник - суббота 9.00-12.00.
https://www.facebook.com/uavhub.stockholm/

3) Паляниця, гуманитарный склад для беженцев.
- Принести вещи
Адрес: Selmedalsvägen 28, Stockholm
Будні 12:00 -17:00; Сб-Вскр 10:00 -17:00
https://www.facebook.com/groups/palyanytsya
Список необходимого:
https://docs.google.com/document/u/1/d/e/2PACX-1vTaYZcK_t10q0vFZMatEqZRPbDHpC8BOCSeOO9zDuCDMufhzEfYCASRVVE9fare5NVqgfEdFG16v3eH/pub

4) Помощь в переезде.
- поддержка товарами первой необходимости 
- гуманитарная помощь (склады)

Локации:
- у Миграционных центров в Sundbyberg, Märsta 
- в порту Nynäshamn 
- у временных резиденций для беженцев в регионе Stor Stockholm
https://www.facebook.com/groups/530929821690119

Вступайте в группу в фейсбуке и пишите координаторам, они есть в шапке профиля группы.
небольшой видео-влог про один волонтерский день: 
https://youtu.be/edV1PG_Rr3k 
"""

READY_TO_HELP_PHYSICALLY_INFORMATION = """
1) Гуманитарный склад в Marsta для беженцев.
Три локации: на входе, на складе и в миграционке.

Адрес: Marsta Migrationsverket, Maskingatan 9, 195 60 Arlandastad, Sweden
Понедельник - суббота 9.00-12.00.
Тина - координатор. https://www.facebook.com/tinatriv

Инструкция для волонтеров MARSTA:
https://drive.google.com/drive/folders/1Gj8w3wGIGIvnaXzY85pz-Ozwec4y9YlQ?usp=sharing

2) Паляниця, гуманитарный склад для беженцев.
Адрес: Selmedalsvägen 28, Stockholm
Будні 12:00 -17:00; Сб-Вскр 10:00 -17:00
https://www.facebook.com/groups/palyanytsya

3) Помощь в переезде (склады)

Локации:
- в порту Nynäshamn 
https://www.facebook.com/groups/530929821690119

Вступайте в группу в фейсбуке и пишите координаторам, они есть в шапке профиля группы.
небольшой видео-влог про один волонтерский день: 
https://youtu.be/edV1PG_Rr3k 
"""

READY_TO_HELP_SOCIALLY_INFORMATION = """
1) Встречи с украинцами в Стокгольме.
Информационная и моральная поддержка семьям из Украины.
Адрес: Dianavägen 10, Hjorthagskyrkan
Вторник - Среда, 13:00 - 16:00
https://www.facebook.com/groups/ukrainehjorthagen/

2) Помощь в переезде.
- информационная поддержка 
- социализация 

Локации:
- у Миграционных центров в Sundbyberg, Märsta 
- у временных резиденций для беженцев в регионе Stor Stockholm
https://www.facebook.com/groups/530929821690119

Вступайте в группу в фейсбуке и пишите координаторам, они есть в шапке профиля группы.
небольшой видео-влог про один волонтерский день: 
https://youtu.be/edV1PG_Rr3k 

3) Rädda Barnen & Stadsmissionen. Быть контактным лицом для беженцев.
https://www.tryggstartisverige.se/volontr

4) Поддержка ЛГБТ - беженцев из Украины.
https://docs.google.com/forms/d/e/1FAIpQLSdkJH2nbzkcSzmImn6nMjTtBwQ-WrcVC1jn_aTZhCn0EXJgjQ/viewform	
"""
