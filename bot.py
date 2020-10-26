import vk_api
import logging
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from _token import TOKEN
GROUP_ID = 199485380

log = logging.getLogger('bot')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))

file_handler = logging.FileHandler("logging.log", encoding='utf8')
file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
log.addHandler(file_handler)
log.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)


class Bot:
    def __init__(self, token, group_id):
        self.vk_session = vk_api.VkApi(token=token)
        self.api = self.vk_session.get_api()
        self.long_poll = VkBotLongPoll(self.vk_session, group_id)

    def run(self):
        for event in self.long_poll.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception("Поймано исключение при обработке события")

    def on_event(self, event):
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
            # raise ValueError("Шрек- лучший мультфилм")


if __name__ == '__main__':
    bot = Bot(TOKEN, GROUP_ID)
    bot.run()
