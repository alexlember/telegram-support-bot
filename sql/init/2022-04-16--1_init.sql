CREATE SCHEMA if not exists raw_telegram_bot;
CREATE SEQUENCE if not exists raw_telegram_bot.user_actions_id_seq;
CREATE SEQUENCE if not exists raw_telegram_bot.logging_events_id_seq;

-- Table: raw_telegram_bot.user_id_to_chat_id

-- DROP TABLE IF EXISTS raw_telegram_bot.user_id_to_chat_id;

CREATE TABLE IF NOT EXISTS raw_telegram_bot.user_id_to_chat_id
(
    user_id bigint NOT NULL,
    chat_id bigint NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT user_id_to_chat_id_pkey PRIMARY KEY (user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS raw_telegram_bot.user_id_to_chat_id
    OWNER to postgres;


-- Table: raw_telegram_bot.user_actions

-- DROP TABLE IF EXISTS raw_telegram_bot.user_actions;

CREATE TABLE IF NOT EXISTS raw_telegram_bot.user_actions
(
    id bigint NOT NULL DEFAULT nextval('raw_telegram_bot.user_actions_id_seq'::regclass),
    user_id bigint NOT NULL,
    action character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    chat_id bigint,
    CONSTRAINT user_actions_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS raw_telegram_bot.user_actions
    OWNER to postgres;


-- Table: raw_telegram_bot.active_chats

-- DROP TABLE IF EXISTS raw_telegram_bot.active_chats;

CREATE TABLE IF NOT EXISTS raw_telegram_bot.active_chats
(
    chat_id bigint NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    CONSTRAINT active_chats_pkey PRIMARY KEY (chat_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS raw_telegram_bot.active_chats
    OWNER to postgres;

-- Table: raw_telegram_bot.logging_events

-- DROP TABLE IF EXISTS raw_telegram_bot.logging_events;

CREATE TABLE IF NOT EXISTS raw_telegram_bot.logging_events
(
    id bigint NOT NULL DEFAULT nextval('raw_telegram_bot.logging_events_id_seq'::regclass),
    level character varying COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone NOT NULL DEFAULT now(),
    user_id bigint,
    chat_id bigint,
    description text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT logging_events_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS raw_telegram_bot.logging_events
    OWNER to postgres;