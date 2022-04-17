select chat_id
from raw_telegram_bot.user_id_to_chat_id
where user_id = (%s);
