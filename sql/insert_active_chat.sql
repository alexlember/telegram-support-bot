insert into raw_telegram_bot.active_chats (chat_id)
values (%s)
on conflict (chat_id) do nothing;