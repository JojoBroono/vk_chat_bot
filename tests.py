from unittest import TestCase
from bot import Bot
from unittest.mock import patch, Mock, ANY
from vk_api.bot_longpoll import VkBotMessageEvent


class Test1(TestCase):
    RAW = {'type': 'message_new', 'object': {'message': {'date': 1603838534, 'from_id': 423771201, 'id': 160, 'out': 0, 'peer_id': 423771201, 'text': 'Привет', 'conversation_message_id': 159, 'fwd_messages': [], 'important': False, 'random_id': 0, 'attachments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'open_photo', 'callback'], 'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}, 'group_id': 199485380, 'event_id': '1874d0405988d6ebdfcf1950f01e9d1c2221e902'}

    def test_run(self):
        call_count = 5
        events = [{} for i in range(call_count)]
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = Mock(return_value=events)

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call({})
                assert bot.on_event.call_count == call_count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW)

        send_mock = Mock()

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api.messages.send = send_mock

                bot.on_event(event)

        send_mock.assert_called_once_with(
            random_id=ANY,
            message=self.RAW['object']['message']['text'],
            user_id=self.RAW['object']['message']['from_id']
        )
