insert into raw_telegram_bot.user_id_to_chat_id (user_id, chat_id)
values (%s, %s)
on conflict (user_id) do nothing;