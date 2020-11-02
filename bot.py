import vk_api
import logging
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from data import INTENTS, SCENARIOS, DEFAULT_ANSWER
import handlers
try:
    from settings import TOKEN, GROUP_ID
except ImportError:
    exit("You forgot to set token and group id\n DO cp settings.py.default settings.py and set parameters")

log = logging.getLogger('bot')


def config_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler("logging.log", mode='a', encoding='utf8')
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    log.addHandler(file_handler)
    file_handler.setLevel(logging.DEBUG)

    log.setLevel(logging.DEBUG)


class UserState:
    def __init__(self, scenario, step, context):
        self.scenario_name = scenario
        self.step_name = step
        self.context = context


class Bot:
    """
    echo bot для vk.com

    Use Python 3.7
    """
    def __init__(self, token, group_id):
        """

        :param token: секретный api токен
        :param group_id: id группы вконтакте
        """
        self.vk_session = vk_api.VkApi(token=token)
        self.api = self.vk_session.get_api()
        self.long_poll = VkBotLongPoll(self.vk_session, group_id)
        self.user_states = {}

    def run(self):
        """
        Запуск бота
        """
        for event in self.long_poll.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception("Поймано исключение при обработке события")

    def _send_msg(self, user_id, msg):
        self.api.messages.send(
            random_id=get_random_id(),
            message=msg,
            user_id=user_id
        )

    def on_event(self, event):
        """
        Обработка события
        :param event: VkBotMessageEvent
        """

        if event.type != VkBotEventType.MESSAGE_NEW:
            log.debug(f"Не умею обрабатывать данный тип события {event.type}")
            return
        text_to_send = DEFAULT_ANSWER
        user_id = event.message.from_id
        text = event.message.text
        if user_id in self.user_states:
            log.debug(f"User {user_id} is in scenario")
            text_to_send = self.continue_scenario(user_id=user_id, text=text)
        else:
            log.debug("Intents branch")
            for intent in INTENTS:
                if text in intent["tokens"]:
                    if intent["scenario"]:
                        log.debug("Init new scenario")
                        scenario_name = intent["scenario"]
                        first_step_name = SCENARIOS[scenario_name]["first_step"]
                        text_to_send = SCENARIOS[scenario_name]["steps"][first_step_name]['text']
                        self.user_states[user_id] = UserState(scenario_name, first_step_name, context={})
                    else:
                        log.debug("Just answer")
                        text_to_send = intent["answer"]
        self._send_msg(user_id=event.message.from_id, msg=text_to_send)

    def continue_scenario(self, user_id, text):
        state = self.user_states[user_id]
        steps = SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        next_step = steps[step['next_step']]
        text_to_send = next_step['text']
        if handler(text=text, context=state.context):
            if next_step['next_step']:
                state.step_name = step['next_step']
            else:
                self.user_states.pop(user_id)
        else:
            text_to_send = step['failure_text']
        return text_to_send


if __name__ == '__main__':
    config_logging()
    bot = Bot(TOKEN, GROUP_ID)
    bot.run()
