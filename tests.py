from unittest import TestCase
from bot import Bot
from unittest.mock import patch, Mock, ANY
from vk_api.bot_longpoll import VkBotMessageEvent
from datetime import datetime, timedelta
from data import SCENARIOS
from copy import deepcopy

RAW = {'type': 'message_new', 'object': {
    'message': {'date': 1603838534, 'from_id': 423771201, 'id': 160, 'out': 0, 'peer_id': 423771201, 'text': 'Привет',
                'conversation_message_id': 159, 'fwd_messages': [], 'important': False, 'random_id': 0,
                'attachments': [], 'is_hidden': False},
    'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'open_photo', 'callback'],
                    'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}, 'group_id': 199485380,
       'event_id': '1874d0405988d6ebdfcf1950f01e9d1c2221e902'}


class TestNormal(TestCase):

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

    # def test_on_event(self):
    #     event = VkBotMessageEvent(raw=self.RAW)
    #
    #     send_mock = Mock()
    #
    #     with patch('bot.vk_api.VkApi'):
    #         with patch('bot.VkBotLongPoll'):
    #             bot = Bot('', '')
    #             bot.api.messages.send = send_mock
    #
    #             bot.on_event(event)
    #
    #     send_mock.assert_called_once_with(
    #         random_id=ANY,
    #         message=self.RAW['object']['message']['text'],
    #         user_id=self.RAW['object']['message']['from_id']
    #     )

    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%d-%m-%Y')
    INPUTS = [
        '/ticket',
        'Москва',
        'Сыктывкар',
        tomorrow_str,
        '1',
        '1',
        'БАБАБУЙ',
        'Да',
        '89043679578'
    ]
    steps = SCENARIOS['ticket']['steps']
    EXPECTED_OUTPUTS = [
        steps['step1']['text'],
        steps['step2']['text'],
        steps['step3']['text'],
        ANY,
        steps['step5']['text'],
        steps['step6']['text'],
        ANY,
        steps['step8']['text'],
        ANY

    ]

    def test_normal(self):
        events = []
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = Mock(return_value=events)

        send_mock = Mock()

        for text in self.INPUTS:
            raw_cpy = deepcopy(RAW)
            raw_cpy['object']['message']['text'] = text
            event = VkBotMessageEvent(raw=raw_cpy)
            events.append(event)

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.send_msg = send_mock
                bot.run()

        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['msg'])
        print(real_outputs)
        print(self.EXPECTED_OUTPUTS)
        assert real_outputs == self.EXPECTED_OUTPUTS

