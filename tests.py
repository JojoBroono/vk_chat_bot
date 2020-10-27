from unittest import TestCase
from bot import Bot
from unittest.mock import patch, Mock


class Test1(TestCase):
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
