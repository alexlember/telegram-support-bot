select user_id, created_at
from raw_telegram_bot.authorized_users
where user_id = (%s);
