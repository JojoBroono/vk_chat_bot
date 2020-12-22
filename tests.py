from copy import deepcopy
from datetime import timedelta, date
from unittest import TestCase
from unittest.mock import patch, Mock

from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot
from models import UserState
from settings import SCENARIOS
from image_maker import ImageMaker

RAW = {'type': 'message_new', 'object': {
    'message': {'date': 1603838534, 'from_id': 423771201, 'id': 160, 'out': 0, 'peer_id': 423771201, 'text': 'Привет',
                'conversation_message_id': 159, 'fwd_messages': [], 'important': False, 'random_id': 0,
                'attachments': [], 'is_hidden': False},
    'client_info': {'button_actions': ['text', 'vkpay', 'open_app', 'location', 'open_link', 'open_photo', 'callback'],
                    'keyboard': True, 'inline_keyboard': True, 'carousel': True, 'lang_id': 0}}, 'group_id': 199485380,
       'event_id': '1874d0405988d6ebdfcf1950f01e9d1c2221e902'}


def my_transaction(func):
    def wrapper(*args, **kwargs):
        with db_session:
            func(*args, **kwargs)
        rollback()

    return wrapper


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

    tomorrow = date.strftime(date.today() + timedelta(days=1), '%d-%m-%Y')

    INPUTS = [
        '/ticket',
        'Москва',
        'Сыктывкар',
        tomorrow,
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

    @my_transaction
    def test_normal(self):
        events = []
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = Mock(return_value=events)

        send_mock = Mock()
        send_img_mock = Mock()
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
                bot.send_img = send_img_mock
                bot.get_photo_and_name = Mock()
                for event in bot.long_poll.listen():
                    try:
                        bot.on_event(event)

                        state = UserState.get(user_id=str(user_id))
                        self.context.update(state.context)
                    except Exception as exc:
                        print(exc)

        assert send_mock.call_count == len(self.INPUTS)
        expected_outputs_formatted = []

        for st in self.EXPECTED_OUTPUTS:
            expected_outputs_formatted.append(st.format(**self.context))
        real_outputs = []
        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['msg'])

        assert real_outputs == expected_outputs_formatted


class TestNonlinear(TestCase):
    tomorrow = date.strftime(date.today() + timedelta(days=1), '%d-%m-%Y')
    INPUTS = [
        '/ticket',
        'Казань',
        'Киров',
        '/ticket',
        'Москва',
        'Сыктывкар',
        tomorrow,
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
        steps['step7']['text'],
        steps['start_again']['text'],
        steps['step1']['text']
    ]

    @my_transaction
    def test_nonlinear(self):
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
                        state = UserState.get(user_id=str(user_id))
                        self.context.update(state.context)
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

