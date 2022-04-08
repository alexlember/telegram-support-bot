import unittest

from settings import SUPPORT_CHAT_ID
from storage import InMemSupportStorage


class TestInMemSupportStorage(unittest.TestCase):

    def test_init(self):
        storage = InMemSupportStorage()

        """Default state check after init"""
        self.assertEqual({SUPPORT_CHAT_ID}, storage.get_active_chats())
        self.assertEqual('Filters.chat(' + str(SUPPORT_CHAT_ID) + ')', storage.get_chat_filter().name)
        self.assertIsNone(storage.find_chat_id(1111))

        """Can't remove default chat id"""
        self.assertFalse(storage.remove_chat(SUPPORT_CHAT_ID))

        """Nothing is changed if try to add a default chat id"""
        storage.add_chat(SUPPORT_CHAT_ID)
        self.assertEqual({SUPPORT_CHAT_ID}, storage.get_active_chats())
        self.assertEqual('Filters.chat(' + str(SUPPORT_CHAT_ID) + ')', storage.get_chat_filter().name)

        """Result of adding chat id differs from default"""
        storage.add_chat(-44444)
        self.assertEqual({SUPPORT_CHAT_ID, -44444}, storage.get_active_chats())
        self.assertEqual('Filters.chat(-44444, ' + str(SUPPORT_CHAT_ID) + ')', storage.get_chat_filter().name)

        """Result of removing chat id differs from default"""
        storage.remove_chat(-44444)
        self.assertEqual({SUPPORT_CHAT_ID}, storage.get_active_chats())
        self.assertEqual('Filters.chat(' + str(SUPPORT_CHAT_ID) + ')', storage.get_chat_filter().name)

        """Result of linking user id to chat id"""
        storage.link_user2chat(1111, -44444)
        self.assertEqual(-44444, storage.find_chat_id(1111))

        """user id is linked to the non-active chat. He is forwarded to the default chat"""
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(1111))

        """several requests returns the same result (user is linked)"""
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(1111))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(1111))

        """adding another chat and balancing clients"""
        storage.add_chat(-5555)
        self.assertEqual({SUPPORT_CHAT_ID, -5555}, storage.get_active_chats())
        self.assertEqual('Filters.chat(-5555, ' + str(SUPPORT_CHAT_ID) + ')', storage.get_chat_filter().name)
        self.assertEqual(-5555, storage.next_chat_id(2222))
        self.assertEqual(-5555, storage.next_chat_id(2222))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(3333))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(3333))
        self.assertEqual(-5555, storage.next_chat_id(4444))
        self.assertEqual(-5555, storage.next_chat_id(4444))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(5555))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(5555))
        self.assertEqual(-5555, storage.next_chat_id(6666))
        self.assertEqual(-5555, storage.next_chat_id(6666))

        """adding another chat and continue balancing clients"""
        storage.add_chat(-6666)
        self.assertEqual({SUPPORT_CHAT_ID, -5555, -6666}, storage.get_active_chats())
        self.assertEqual('Filters.chat(-5555, ' + str(SUPPORT_CHAT_ID) + ', -6666)', storage.get_chat_filter().name)
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(7777))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(7777))
        self.assertEqual(-6666, storage.next_chat_id(8888))
        self.assertEqual(-6666, storage.next_chat_id(8888))
        self.assertEqual(-5555, storage.next_chat_id(9999))
        self.assertEqual(-5555, storage.next_chat_id(9999))
        self.assertEqual(-5555, storage.next_chat_id(2222))
        self.assertEqual(-5555, storage.next_chat_id(2222))
        self.assertEqual(-5555, storage.next_chat_id(4444))
        self.assertEqual(-5555, storage.next_chat_id(4444))
        self.assertEqual(-5555, storage.next_chat_id(6666))
        self.assertEqual(-5555, storage.next_chat_id(6666))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(3333))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(3333))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(5555))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(5555))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(7777))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(7777))
        self.assertEqual(-6666, storage.next_chat_id(8888))
        self.assertEqual(-6666, storage.next_chat_id(8888))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(10000))
        self.assertEqual(SUPPORT_CHAT_ID, storage.next_chat_id(10000))
        self.assertEqual(-6666, storage.next_chat_id(20000))
        self.assertEqual(-6666, storage.next_chat_id(20000))


if __name__ == '__main__':
    unittest.main()
