from pprint import pprint
from unittest import TestCase
from bot import Bot
from unittest.mock import patch, Mock, ANY
from vk_api.bot_longpoll import VkBotMessageEvent
from datetime import datetime, timedelta, time
from data import SCENARIOS, FLIGHTS
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

    INPUTS = [
        '/ticket',
        'Москва',
        'Сыктывкар',
        '30-01-2021',
        '1',
        '1',
        'БАБАБУЙ',
        'Да',
        '89043679578'
    ]
    steps = SCENARIOS['ticket']['steps']

    PHONE_NUMBER = {'phone_number': '89043679578'}

    EXPECTED_OUTPUTS = [
        steps['step1']['text'],
        steps['step2']['text'],
        steps['step3']['text'],
        steps['step4']['text'],
        steps['step5']['text'],
        steps['step6']['text'],
        steps['step7']['text'],
        steps['step8']['text'],
        steps['step9']['text'].format(**PHONE_NUMBER)

    ]

    def test_normal(self):
        events = []
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = Mock(return_value=events)

        send_mock = Mock()
        user_id = RAW['object']['message']['from_id']
        for text in self.INPUTS:
            raw_cpy = deepcopy(RAW)
            raw_cpy['object']['message']['text'] = text
            event = VkBotMessageEvent(raw=raw_cpy)
            events.append(event)

        with patch('bot.vk_api.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                self.context = {}
                bot.send_msg = send_mock
                for event in bot.long_poll.listen():
                    try:
                        bot.on_event(event)
                        self.context.update(bot.user_states[user_id].context)
                    except Exception as exc:
                        print(exc)

        expected_outputs_formatted = []

        for st in self.EXPECTED_OUTPUTS:
            expected_outputs_formatted.append(st.format(**self.context))
        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['msg'])
        assert real_outputs == expected_outputs_formatted


class TestNonlinear(TestCase):
    INPUTS = [
        '/ticket',
        'Москва',
        'Казань',
        'Бабабуй',
        '/ticket',
        'Москва',
        'Сыктывкар',
        '30-01-2021',
        '1',
        '1',
        'БАБАБУЙ',
        'Нет',
        'Да'
    ]
    steps = SCENARIOS['ticket']['steps']
    EXPECTED_OUTPUTS = [
        steps['step1']['text'],
        steps['step2']['text'],
        'Нет сообщения между городами',
        steps['step1']['text'],
        steps['step2']['text'],
        steps['step3']['text'],
        steps['step4']['text'],
        steps['step5']['text'],
        steps['step6']['text'],

    ]