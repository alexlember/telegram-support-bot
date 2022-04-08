# telegram-support-bot

Repository for TG support bot


### Run bot locally
___

First, you need to install all dependencies:

    pip install -r requirements.txt

Then you can run the bot. Don't forget to create .env file in the root folder with all required params (read above).

    python bot.py

### Bot API description

    start - Начать
    needhelp - Мне нужна помощь
    readytohelp - Я хочу помочь
    connect_with_operators - Связаться

### How to use bot.

    1) There are 2 env variables: TELEGRAM_TOKEN and SUPPORT_CHAT_ID
    TELEGRAM_TOKEN - take from @botfather
    SUPPORT_CHAT_ID - default support chat (can't delete).

    2) There is an option to extend number of groups.
    Just create any group in telegram and add there our bot.
    Then you may send a command to this chat: /oncall@bot_name
    And this chat will be included to the support.

    3) There is an option to remove the chat from the on-call.
    In order to do that you need to send a command 
    to this chat: /offcall@bot_name
    And this chat will be excluded to the support.

    4) When some person (who wants to get help) writes the message to
    the bot this message is routed to the one of the support chats. 
    The choice of the support chat is made in order, one by one. There
    will always be at least 1 chat (default, provided with env var - SUPPORT_CHAT_ID)

    5) If the person was once routed to any support chat, his/her messages 
    would always be sent to that chat from that time. If that chat was removed
    from the on-call, the person's message would be sent to a different chat.
    So, it is important to make sure that the person's case is handled finally 
    before closing the chat, because right now it is not possible 
    to get the message history from the other support chat. 
    The only way is only to forward them manually but this is not convenient.
    
    
