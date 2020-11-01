import vk_api
import logging
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from data import INTENTS, SCENARIOS, DEFAULT_ANSWER
try:
    from settings import TOKEN, GROUP_ID
except ImportError:
    exit("You forgot to set token and group id\n DO cp settings.py.default settings.py and set parameters")

log = logging.getLogger('bot')


def config_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    stream_handler.setLevel(logging.INFO)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler("logging.log", mode='a', encoding='utf8')
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    log.addHandler(file_handler)
    file_handler.setLevel(logging.DEBUG)

    log.setLevel(logging.DEBUG)


class UserState:
    def __init__(self, scenario, step, context):
        self.scenario = scenario
        self.step = step
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

    def on_event(self, event):
        """
        Обработка события
        :param event: VkBotMessageEvent
        """

        if event.type != VkBotEventType.MESSAGE_NEW:
            log.debug(f"Не умею обрабатывать данный тип события {event.type}")
            return
        user_id = event.message.from_id
        if user_id in self.user_states:
            # do scenario
            log.debug(f"User {user_id} is in scenario")
        else:
            text = event.message.text
            # ищем, какой именно intent
            for intent in INTENTS:
                if text in intent["tokens"]:
                    # если сценарий есть - переходим на сценарий
                    if intent["scenario"]:
                        self.user_states[user_id] = UserState(
                            scenario=intent["scenario"],
                            step=SCENARIOS[intent["scenario"]]["first_step"],
                            context={}
                        )
                    # иначе - пишем ответ
                    else:
                        msg = intent["answer"]
                        self.api.messages.send(
                            random_id=get_random_id(),
                            message=msg,
                            user_id=event.message.from_id
                        )

                    return

            self.api.messages.send(
                random_id=get_random_id(),
                message=DEFAULT_ANSWER,
                user_id=event.message.from_id
            )


if __name__ == '__main__':
    config_logging()
    bot = Bot(TOKEN, GROUP_ID)
    bot.run()
