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
    
### How to deploy bot in Heroku

    1) heroku login
    2) heroku config - see env variables
    3) heroku config:set REFUGEE_TELEGRAM_TOKEN=..... set env variables
    (REFUGEE_TELEGRAM_TOKEN, LOGGING_CHAT_ID, SUPPORT_CHAT_ID, HEROKU_APP_NAME)
    4) push to heroku/main to trigger app deploy


### How to deploy bot in AWS

    1) docker, docker-compose, git should be installed in AWS.
    2) choose the right branch in git
    3) make sure you have proper settings in 
    postgres_env_vars.env and telegram_env_vars files
    4) ./docker-compose build
    5) ./docker-compose up -d
    ---
    What should happen?
    1st time run:
    - pretty long duration of ./docker-compose build (need to fetch required images ~2GB),
    this would take time.
    - 2 containers should be running (postgres and telegram bot)
    
    If you do update of the telegram bot, build will take several seconds only.
    The postgres container won't even be re-created it would keep running.
    ---

### How to use the bot if you are a support team member


- All messages from users who applied with a question via bot are appearing in the support chat. 
You reply to this message via "Reply", then the user receives your answer ANONYMOUSLY 
in his chat with the bot (on behalf of the bot). If the user has permission in the telegram settings 
(Settings/Privacy and Security/Who can add a link to my account when forwarding my messages?), 
then a link to the user's profile will be available in the support chat. 
In case this setting is disabled for a user, you will only be able to see his name.

- You can create as many support chats as you like. 
To do this, you need to create a group (New group), then add a bot there and send 
a command in the message: /oncall. Then this group will be added to the list of 
active bot groups where questions from users will come. Any of the coordinators 
can be added to this group (who has more competence on issues), 
any of the group can answer users' questions.

- In order for messages to stop coming to your group, 
you must send the following command in the message: /offcall. 
There is a pre-created default support group that cannot be disabled 
from messages with the /offcall command.

- Messages from users will arrive randomly in one of the chats from the active list 
(default chat + all chats added by the /oncall command). 
At the same time, if the user sent messages and got into one of the chats, 
he would already be "glued" to it, and all his subsequent messages would only come there.

- If at some point the chat is turned off with the /offcall command, 
then the next message from the user will go to the next random chat 
and the previous correspondence with this user will be lost. 
This is a shortcoming of the current solution. For the time being, 
it is proposed to give this to the coordinator, i.e. 
they will need to try not to close their chats if they have open questions. 
In the future, this shortcoming will be improved.

- The default chat will be the largest load, 
it is suggested to start with only this chat for now, 
perhaps this will be enough. If there are too many messages, then additional chats can be created.