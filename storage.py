import abc
import logging
import os
from abc import ABC

import psycopg2
from telegram.ext import Filters, MessageFilter

from settings import SUPPORT_CHAT_ID, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class SupportStorageInterface(abc.ABC):
    @abc.abstractmethod
    def get_chat_filter(self) -> MessageFilter:
        """Extracts group chat filter based on chat ids."""
        pass

    @abc.abstractmethod
    def get_active_chats(self) -> iter:
        """Extracts all active support chats (except default)"""
        pass

    @abc.abstractmethod
    def add_chat(self, chat_id: int):
        """Add a new support chat to on-call (idempotent)"""
        pass

    @abc.abstractmethod
    def remove_chat(self, chat_id: int) -> bool:
        """Remove a support chat from on-call (idempotent).
        True - the chat was successfully removed.
        False - the chat can't be removed.
        """
        pass

    @abc.abstractmethod
    def link_user2chat(self, user_id: int, chat_id: int):
        """Make association between the user id and the chat id (idempotent)"""
        pass

    @abc.abstractmethod
    def next_chat_id(self, user_id: int) -> int:
        """Returns an active support chat id by user_id.
        If this is the first message made by user {user_id}, returns a next chat (for balancing).
        If this is not the first user {user_id} message, then all further messages
        should go to the same chat"""
        pass

    @abc.abstractmethod
    def find_chat_id(self, user_id: int) -> int or None:
        """Returns an active support chat id by user_id or None if not linked."""
        pass

    @abc.abstractmethod
    def init_db(self):
        """Perform some actions to init the app"""
        pass

    @abc.abstractmethod
    def insert_logging_event(self, level: str, user_id: int or None, chat_id: int or None, description: str):
        """Insert logging action to the storage"""
        pass

    @abc.abstractmethod
    def insert_user_action(self, user_id: int, chat_id: int or None, action: str):
        """Insert user business action to the storage"""
        pass

    @abc.abstractmethod
    def insert_authorized_user(self, user_id: int):
        """Insert user to the authorized table"""
        pass

    @abc.abstractmethod
    def is_user_authorized(self, user_id: int) -> bool:
        """Checks if the user is authorized"""
        pass


class InMemSupportStorage(SupportStorageInterface, ABC):
    def __init__(self):
        self.user_id_2_chat_id_dict = {}
        self.active_chats = set()
        self.active_chats.add(SUPPORT_CHAT_ID)
        self.current_chat = -1
        self.group_filter = Filters.chat(SUPPORT_CHAT_ID)

    def get_chat_filter(self) -> MessageFilter:
        return self.group_filter

    def get_active_chats(self) -> iter:
        return self.active_chats

    def add_chat(self, chat_id: int):
        if chat_id == SUPPORT_CHAT_ID:
            pass
        self.group_filter.add_chat_ids(chat_id)
        self.active_chats.add(chat_id)

    def remove_chat(self, chat_id: int) -> bool:
        if chat_id == SUPPORT_CHAT_ID:
            return False
        self.group_filter.remove_chat_ids(chat_id)
        self.active_chats.discard(chat_id)
        return True

    def link_user2chat(self, user_id: int, chat_id: int):
        self.user_id_2_chat_id_dict[user_id] = chat_id

    def next_chat_id(self, user_id: int) -> int:
        chat_id = self.find_chat_id(user_id)
        if chat_id is not None:
            return self.__link_to_provided_or_default_chat(user_id, chat_id)
        else:
            return self.__link_to_provided_or_default_chat(user_id, self.__pick_random_chat())

    def find_chat_id(self, user_id: int) -> int or None:
        return self.user_id_2_chat_id_dict.get(user_id, None)

    def __link_to_provided_or_default_chat(self, user_id, chat_id) -> int:
        if chat_id in self.active_chats:
            self.link_user2chat(user_id, chat_id)
            return chat_id
        else:
            return self.__link_to_default(user_id)

    def __link_to_default(self, user_id) -> int:
        self.link_user2chat(user_id, SUPPORT_CHAT_ID)
        return SUPPORT_CHAT_ID

    def __pick_random_chat(self) -> int:
        self.current_chat = self.current_chat + 1
        if self.current_chat >= len(self.active_chats):
            self.current_chat = 0

        return list(self.active_chats)[self.current_chat]

    def init_db(self):
        pass

    def insert_logging_event(self, level: str, user_id: int or None, chat_id: int or None, description: str):
        pass

    def insert_user_action(self, user_id: int, chat_id: int or None, action: str):
        pass

    def insert_authorized_user(self, user_id: int):
        pass

    def is_user_authorized(self, user_id: int) -> bool:
        return True
###


def insert_active_chat(chat_id: int):
    logger.info(f'insert to active_chats. chat_id: {chat_id}')
    transaction("insert_active_chat.sql", [chat_id])


def insert_logging_event(level: str, user_id: int or None, chat_id: int or None, description: str):
    logger.info(f'insert to logging_events. level: {level}, user_id: {user_id}, chat_id: {chat_id}, '
                f'description: {description}')
    transaction("insert_logging_event.sql", [level, user_id, chat_id, description])


def insert_user_action(user_id: int, chat_id: int or None, action: str):
    logger.info(f'insert to user_actions. user_id: {user_id}, chat_id: {chat_id}, action: {action}')
    transaction("insert_user_action.sql", [user_id, chat_id, action])


def insert_user_id_to_chat_id_mapping(user_id: int, chat_id: int):
    logger.info(f'insert to user_id_to_chat_id. user_id: {user_id}, chat_id: {chat_id}')
    transaction("insert_user_id_to_chat_id.sql", [user_id, chat_id])


def insert_authorized_user(user_id: int):
    logger.info(f'insert_authorized_user. user_id: {user_id}')
    transaction("insert_authorized_user.sql", [user_id])


def remove_active_chat(chat_id: int):
    logger.info(f'delete from active_chats. id: {chat_id}')
    transaction("remove_active_chat_by_id.sql", [chat_id])


def remove_all_active_chats(exception_chat_id: int):
    logger.info(f'remove_all_active_chats. exception id: {exception_chat_id}')
    transaction("remove_all_active_chats_except_id.sql", [exception_chat_id])


def remove_all_auth_users():
    logger.info('remove_all_auth_users')
    transaction("remove_all_auth_users.sql")


def is_chat_active(chat_id: int) -> bool:
    logger.info(f'get_active_chat. id: {chat_id}')
    active_chat = select_single("get_active_chat_by_id.sql", [chat_id])
    logger.info(f"active_chat: {active_chat}")
    return active_chat is not None


def is_user_authorized(user_id: int) -> bool:
    logger.info(f'is_user_authorized. id: {user_id}')
    user = select_single("get_authorized_user_by_id.sql", [user_id])
    logger.info(f"authorized user: {user}")
    return user is not None


def get_active_chat_randomly() -> int:
    logger.info('get_active_chat_randomly')
    rnd_active_chat = select_single("get_rnd_active_chat.sql")
    logger.info(f"Random chat: {rnd_active_chat}")
    return rnd_active_chat[0]


def get_chat_id_by_user_id_mapping(user_id: int) -> int or None:
    logger.info(f'get_chat_id_by_user_id. user_id: {user_id}')
    chat = select_single("get_chat_id_by_user_id.sql", [user_id])
    logger.info(f"Chat {chat} by user_id: {user_id}")
    return chat[0] if chat is not None else None


def get_all_active_chats() -> iter:
    logger.info('get_all_active_chats')
    active_chats = select_many("get_all_active_chats.sql")
    for row in active_chats:
        logger.info(f"Id = {row[0]}")
        logger.info(f"Created_at = {row[1]}\n")

    return list(map(lambda x: x[0], active_chats))


def print_all_user_actions():
    logger.info('get_all_user_actions')
    user_actions = select_many("get_all_user_actions.sql")
    for row in user_actions:
        logger.info(f"Id = {row[0]}")
        logger.info(f"UserId = {row[1]}")
        logger.info(f"ChatId = {row[2]}")
        logger.info(f"Action = {row[3]}")
        logger.info(f"Created_at = {row[4]}\n")


def print_all_chat_id_to_user_id_mappings():
    logger.info('get_all_chat_id_to_user_id_mappings')
    user_id_to_chat_id = select_many("get_all_user_2_chat_mappings.sql")
    for row in user_id_to_chat_id:
        logger.info(f"UserId = {row[0]}")
        logger.info(f"ChatId = {row[1]}")
        logger.info(f"Created_at = {row[2]}\n")


def print_all_logging_events():
    logger.info('get_all_logging_events')
    logging_events = select_many("get_all_logging_events.sql")
    for row in logging_events:
        logger.info(f"Id = {row[0]}")
        logger.info(f"Level = {row[1]}")
        logger.info(f"Created_at = {row[2]}\n")
        logger.info(f"UserId = {row[3]}")
        logger.info(f"ChatId = {row[4]}")
        logger.info(f"Description = {row[5]}\n")


def transaction(sql_file_path, varargs=None):
    conn = connect()
    with conn.cursor() as cursor:
        with open("sql/" + sql_file_path, "r") as sql_file:
            cursor.execute(sql_file.read(), varargs)
    conn.commit()
    conn.close()


def select_many(sql_file_path, varargs=None):
    return select(sql_file_path, lambda curs: curs.fetchall(), varargs)


def select_single(sql_file_path, varargs=None):
    return select(sql_file_path, lambda curs: curs.fetchone(), varargs)


def select(sql_file_path, cursor_function, varargs=None):
    conn = connect()
    with conn.cursor() as cursor:
        with open("sql/" + sql_file_path, "r") as sql_file:
            cursor.execute(sql_file.read(), varargs)
            result = cursor_function(cursor)
    conn.commit()
    conn.close()
    return result


def connect():
    return psycopg2.connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )


def try_log_to_db(msg: str, e: Exception, user_id: int or None, chat_id: int or None):
    try:
        logger.error(msg, e)
        insert_logging_event("error", user_id, chat_id, msg + str(e))
    except Exception as e_inner:
        logger.error("insert_logging_event error", e_inner)


class PostgresSupportStorage(SupportStorageInterface, ABC):
    def __init__(self):
        self.group_filter = Filters.chat(SUPPORT_CHAT_ID)

    def get_chat_filter(self) -> MessageFilter:
        return self.group_filter

    def get_active_chats(self) -> iter:
        try:
            return get_all_active_chats()
        except Exception as e:
            try_log_to_db("get_active_chats error", e, None, None)
            return set()

    def add_chat(self, chat_id: int):
        try:
            if chat_id == SUPPORT_CHAT_ID:
                pass
            self.group_filter.add_chat_ids(chat_id)
            insert_active_chat(chat_id)
        except Exception as e:
            try_log_to_db("add_chat error", e, None, chat_id)

    def remove_chat(self, chat_id: int) -> bool:
        try:
            if chat_id == SUPPORT_CHAT_ID:
                return False
            self.group_filter.remove_chat_ids(chat_id)
            remove_active_chat(chat_id)
            return True
        except Exception as e:
            try_log_to_db("remove_chat error", e, None, chat_id)
            return False

    def remove_all_active_except_default(self, chat_id: int):
        try:
            active_chats_to_drop = list(set(get_all_active_chats()) - set([SUPPORT_CHAT_ID]))
            remove_all_active_chats(SUPPORT_CHAT_ID)
            self.group_filter.remove_chat_ids(active_chats_to_drop)
        except Exception as e:
            try_log_to_db("remove_all_active_except_default error", e, None, chat_id)

    @staticmethod
    def unauthorize_all():
        try:
            remove_all_auth_users()
        except Exception as e:
            try_log_to_db("unauthorize_all error", e, None, None)

    def link_user2chat(self, user_id: int, chat_id: int):
        try:
            insert_user_id_to_chat_id_mapping(user_id, chat_id)
        except Exception as e:
            try_log_to_db("link_user2chat error", e, user_id, chat_id)

    def next_chat_id(self, user_id: int) -> int:
        chat_id = self.find_chat_id(user_id)
        if chat_id is not None:
            return self.__link_to_provided_or_default_chat(user_id, chat_id)
        else:
            return self.__link_to_provided_or_default_chat(user_id, get_active_chat_randomly())

    def find_chat_id(self, user_id: int) -> int or None:
        try:
            return get_chat_id_by_user_id_mapping(user_id)
        except Exception as e:
            try_log_to_db("find_chat_id error", e, user_id, None)
            return None

    @staticmethod
    def __link_to_provided_or_default_chat(user_id, chat_id) -> int:
        try:
            if is_chat_active(chat_id):
                insert_user_id_to_chat_id_mapping(user_id, chat_id)
                return chat_id
            else:
                rnd_chat = get_active_chat_randomly()
                insert_user_id_to_chat_id_mapping(user_id, rnd_chat)
                return rnd_chat
        except Exception as e:
            try_log_to_db("__link_to_provided_or_default_chat error", e, user_id, chat_id)
            return SUPPORT_CHAT_ID

    def init_db(self):
        logger.info('starting init_db...')

        list_of_sql_init_files = sorted(filter(lambda x: os.path.isfile(os.path.join("sql/init", x)),
                                               os.listdir("sql/init")))

        conn = connect()
        with conn.cursor() as cursor:
            for sql_file_name in list_of_sql_init_files:
                with open(f"sql/init/{sql_file_name}", "r") as sql_file:
                    logger.info(f"applying {sql_file_name} on db")
                    cursor.execute(sql_file.read())

        conn.commit()
        conn.close()
        self.group_filter.add_chat_ids(get_all_active_chats())
        logger.info("init_db completed")

    def insert_logging_event(self, level: str, user_id: int or None, chat_id: int or None, description: str):
        try:
            insert_logging_event(level, user_id, chat_id, description)
        except Exception as e:
            logger.error("insert_logging_event error", e)

    def insert_user_action(self, user_id: int, chat_id: int or None, action: str):
        try:
            insert_user_action(user_id, chat_id, action)
        except Exception as e:
            err_msg = f"error during insert_user_action. user_id: {user_id}, action: {action}"
            try_log_to_db(err_msg, e, user_id, chat_id)

    def insert_authorized_user(self, user_id: int):
        try:
            insert_authorized_user(user_id)
        except Exception as e:
            err_msg = f"error during insert_authorized_user. user_id: {user_id}"
            try_log_to_db(err_msg, e, user_id, None)
        pass

    def is_user_authorized(self, user_id: int) -> bool:
        try:
            return is_user_authorized(user_id)
        except Exception as e:
            err_msg = f"error during is_user_authorized. user_id: {user_id}"
            try_log_to_db(err_msg, e, user_id, None)
            return False
