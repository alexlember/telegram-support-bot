select chat_id, created_at
from raw_telegram_bot.active_chats
order by random()
limit 1;
