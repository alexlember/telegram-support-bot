insert into raw_telegram_bot.authorized_users (user_id)
values (%s)
on conflict (user_id) do nothing;
