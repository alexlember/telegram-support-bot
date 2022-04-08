import abc
from abc import ABC

from telegram.ext import Filters, MessageFilter

from settings import SUPPORT_CHAT_ID


class SupportStorageInterface(abc.ABC):
    @abc.abstractmethod
    def get_chat_filter(self) -> MessageFilter:
        """Extracts group chat filter based on chat ids. TODO fills from db on start"""
        pass

    @abc.abstractmethod
    def get_active_chats(self) -> set:
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
    def find_chat_id(self, user_id: int) -> int:
        """Returns an active support chat id by user_id or None if not linked."""
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

    def get_active_chats(self) -> set:
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
        self.active_chats.remove(chat_id)
        return True

    def link_user2chat(self, user_id: int, chat_id: int):
        self.user_id_2_chat_id_dict[user_id] = chat_id

    def next_chat_id(self, user_id: int) -> int:
        chat_id = self.find_chat_id(user_id)
        if chat_id is not None:
            return self.__link_to_provided_or_default_chat(user_id, chat_id)
        else:
            return self.__link_to_provided_or_default_chat(user_id, self.__pick_random_chat())

    def find_chat_id(self, user_id: int) -> int:
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