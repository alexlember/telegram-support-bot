from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


def need_help_menu(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Какая помощь вам необходима?', reply_markup=create_need_help_reply_markup())


def create_need_help_reply_markup() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("Где искать помощь?", callback_data='need_help_where_to_search')
        ],
        [
            InlineKeyboardButton("Статус переселенца", callback_data='need_help_refugee_status')
        ],
        [
            InlineKeyboardButton("Жизнь в Швеции", callback_data='need_help_life_in_swe')
        ],
        [
            InlineKeyboardButton("Встретиться с людьми", callback_data='need_help_meet_people')
        ],
        [
            InlineKeyboardButton("Язык", callback_data='need_help_language')
        ],
        [
            InlineKeyboardButton("Найти жилье", callback_data='need_help_find_accommodation')
        ],
        [
            InlineKeyboardButton("Интеграция, обучение", callback_data='need_help_integration_education')
        ],
        [
            InlineKeyboardButton("Бесплатные возможности", callback_data='need_help_free_options')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


NEED_HELP_INFORMATION_WHERE_TO_SEARCH = """
“Помощь украинцам в Швеции” - тг канал и форум (можно попросить помощь или совет)
https://t.me/refugeesinSweden
https://forum.dopomoga.se/

Nordic Ukraine Forum - запросы почти любого профиля. Некоммерческая организация для украинцев. 
https://nuforum.se/

Допомога 🇺🇦 біженцям в Швеції / Stöd till ukrainska flyktingar i Sverige
https://www.facebook.com/groups/262714735902652/

Допомога біженцям в Швеціїя. Вся необхідна інформація - Телеграм канал
https://t.me/dopomogavshvecii

SwedenUA - спільнота українців У Швеції / community of Ukrainians in Sweden
https://www.facebook.com/groups/252153281796964/

Помощь беженцам в Гетеборге
https://www.helpukrainegbg.se/	
https://www.facebook.com/groups/helpukraineingbg/permalink/363700915754779/
"""


NEED_HELP_INFORMATION_REFUGEE_STATUS = """
Памятка, которую раздают у миграционного агентства
https://docs.google.com/document/d/1NoKq7FPVTGlosZ5VWCZCZrDWXb0KGMeyZKazbv-2pqU/edit 

Официальная информация от Migrationsverket о подаче на статус беженца 
https://www.migrationsverket.se/Other-languages/Russkij/Zasita-na-osnovanii-Direktivy-o-vremennoj-zasite-v-slucae-massovogo-pritoka-peremesennyh-lic.html

Видео юриста о регистрации украинских беженцев онлайн на сайте миграционки 
https://www.youtube.com/watch?v=NXunT_vo-xQ
"""


NEED_HELP_INFORMATION_LIFE_IN_SWEDEN = """
Различные памятки на украинском языке о разных аспектах жизни в Швеции
https://docs.google.com/document/d/1-t33xzfduo-m1FKDMLEtPnRsb1RAdfehQrWCFLkgh6E/edit?usp=sharing

SwedenUA - спільнота українців У Швеції / community of Ukrainians in Sweden
https://www.facebook.com/groups/252153281796964/

Nуstart i Sverige för Ukrainare - Новий старт для українців в Швеції
https://www.facebook.com/groups/nystartsverige/

Группа для украинских мам в Швеции
https://www.facebook.com/groups/739071442806022

Много разной информации о Швеции (на русском языке)
https://www.informationsverige.se/ru/

Русскоговорящее Женское Общество Швеции
https://www.facebook.com/groups/330019677391358
"""

NEED_HELP_INFORMATION_MEET_PEOPLE = """
Mötesplats på Frälsningsarmén

- Местро встречи для беженцев с Украины. Здесь можно пообедать, получить продукты, информационную помощь. Понедельник и вторник с 13 по 16. 
Östermalmsgatan 69 i Stockholm

- Мрия - встречи для детей и взрослых
https://www.facebook.com/groups/3080911452150836/
📍 Patricia boat - Söder Mälarstrand, Kajplats 19 
🕑 Every Wednesday 11:00-19:00 
☕️🍩11:00-12:00 – «Fika»: coffee, tea, snacks 
🍲12:00-18:00 – Lunch/Early dinner 
🕺🏼12:00-19:00 – Various activities for children and adults

- Центр для украинских беженцев
https://www.facebook.com/ukrainianinsweden/
Södra Hamnvägen 9, 15 минут от станции Slussen на автобусе. Туда можно прийти в понедельник - четверг с 10 до 13 
и получить информационную поддержку от волонтеров, попить кофе и чай. Также можно организовывать там свои мероприятия.

- Встречи для переселенцев из Украины в Стокгольме (общение, информация, поиск работы)
https://www.facebook.com/groups/ukrainehjorthagen/

- Занятия для детишек в центре Dream Space
https://www.facebook.com/groups/708231696978599/
метро Norsborg
"""

NEED_HELP_INFORMATION_FIND_ACCOMMODATION = """
В этих группах можно найти место пожить и переночевать у местных. 
Будьте осторожны и бдительны, есть люди, которые могут воспользоваться положением беженцев в свои целях.
- Ukrainian refugees in Sweden- Accommodation, Help & Shelter - поиск жилья в Швеции
https://www.facebook.com/groups/682101599891991/

- Öppna din dörr för Ukraina
https://www.facebook.com/groups/343051644412157/ 

- Living Room for Displaced People - HUS: Help Ukraine Stockholm
https://www.facebook.com/CenterForDisplacedUkrainians/

- Hjälp Ukrainas flyktingar
https://www.facebook.com/groups/1123608588415187/

- Найти временное жилье в Швеции
https://www.tryggstartisverige.se/
"""

NEED_HELP_INFORMATION_LANGUAGE = """
- Folkuniversitet
https://www.folkuniversitetet.se/in-english/swedish-courses/swedish-for-asylum-seekers/
Бесплатные курсы по изучению шведского

- ABF Stockholm
https://abfstockholm.se/svenska-for-asylsokande/
Бесплатные курсы по изучению шведского, на курсах - информация о шведском обществе и шведском рынке труда, 
разные экскурсии и посещения разных организаций и мест в Стокгольме.

- Studiefrämjandet Vuxenskola
Olga Biba 
olga.biba@sv.se
070-7634414
Шведский язык

- Курсы шведского для беженцев с персональным номером (начало 29 марта!) 
https://www.facebook.com/events/410034800927820/?ref=newsfeed 

"""


NEED_HELP_INFORMATION_FREE_OPTIONS = """

- Бесплатный вход в Скансен для всех с украинским паспортом 
https://www.skansen.se/sv/open-entrance-ukrainian

- Бесплатные мероприятия в Стокгольме для всех!
https://kompissverige.se/stockholm/#aktiviteter
Все от кино до боулинга, театра, лекции и концерта. Цель - находить новые знакомства. 
Эти мероприятия в основном посещают те, кто недавно в Стокгольме, но также есть и местные. 
Бронировать желательно заранее место, так как большой интерес к этим мероприятиям!

- Бесплатный вход в Технический музей в Стокгольме до 4 марта 2023 года! 
Карта LMA от Шведского миграционного управления или действительный украинский паспорт, 
могут использоваться в качестве входного билета. 
Adress: Museivägen 7, 115 27 Stockholm

- Бесплатный вход (по пятницам) в бассейны Medley для детей и подростков и сопровождающих родителей, 
при наличии украинского паспорта.
https://www.medley.se/vara-anlaggningar

* Medley Nacka simhall 
Адрес: Griffelvägen 11, 131 40 Nacka 
* Medley Tyresö Aquarena 
Адрес: Simvägen 2, 135 39 Tyresö 
* Medley Näckenbadet 
Адрес: Neglingevägen 2, 133 34 Saltsjöbaden 
* Medley Järfällabadet 
Адрес: Mjölnarvägen 1B, 177 41 Järfälla 
* Medley Sollentuna sim- och sporthall 
Адрес: Stubbhagsvägen 2, 192 51 Sollentuna 
* Medley Tibblebadey 
Адрес: Attundavägen 5-7, 183 36 Täby
"""

NEED_HELP_INFORMATION_EDUCATION_INTEGRATION = """
- Курсы по редактированию видео
https://framtidstaget.se/se/medialab
Говорят по-русски и английски

- Курс по ремонту мобильных телефонов
https://framtidstaget.se/en/smartphone-repair
Язык курса - английский и шведский

- Бесплатные мероприятия и встречи для беженцев и всех желающих: "языковые кафе", спорт, йога, танцы.
https://www.hejframling.se/stockholm
Расписание мероприятий

- Найти себе "друга" среди местных
https://www.midsommargarden.se/medvan
https://kompissverige.se/bli-kompis/
Организация "Друг в Швеции". Эта организация "соединяет" новоприбывших в Стокгольм и тех, кто уже давно живет в Швеции.
Люди проводят несколько встреч и потом решают, продолжать ли им контакт. Есть возможность также бесплатно участвовать в 
различных мероприятиях вместе с другом, например, бесплатные походы в музеи Стокгольма.

- Бесплатный курс по плаванию для беженцев
https://stockholmswimmingclub.se/free-swimming-courses-for-asylum-seekers/
Курсы для тех, кто не умеет плавать и те, кто учится плавать. Курс длится два месяца, встречи два раза в неделю.

- Бесплатное плаванье для девушек до 30 лет
stockholm@tamam.se
Группа для девушек, кто недавно приехал в Швецию. Каждую неделю они ходят плавать бесплатно с инструктором. 
Также организовываются и другие встречи, игра в боулинг, бильярд, и т.д. 
Если им написать, они добавят в вотсап группу девушек.

- Бесплатные занятия по танцам, музыке искусству для молодежи до 25 лет, метро Telefonplan
https://www.midsommargarden.se/studioung
Разное расписание в зависимости от недели

- Волонтерить на футбольных матчах известной шведской команды
Aylin Wallin
0739500361
Предлагают возможность поволонтерить для беженцев, оставят потом рекомендательное письмо. 
Желательно говорить по-английски хотя бы на базовом уровне.
"""
