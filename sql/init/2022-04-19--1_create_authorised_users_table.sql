-- Table: raw_telegram_bot.authorized_users

-- DROP TABLE IF EXISTS raw_telegram_bot.authorized_users;

CREATE TABLE IF NOT EXISTS raw_telegram_bot.authorized_users
(
    user_id bigint NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT authorized_users_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS raw_telegram_bot.authorized_users
    OWNER to postgres;
