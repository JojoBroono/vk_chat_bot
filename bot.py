import vk_api
import logging
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
try:
    from settings import TOKEN, GROUP_ID
except ImportError:
    exit("You forgot to set token and group id")

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
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info("Отправляем сообщение назад")
            msg = event.object.message['text']
            self.api.messages.send(
                random_id=get_random_id(),
                message=msg,
                user_id=event.object.message['from_id']
            )
        else:
            log.debug(f"Не умею обрабатывать данный тип события {event.type}")


if __name__ == '__main__':
    config_logging()
    bot = Bot(TOKEN, GROUP_ID)
    bot.run()
