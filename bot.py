import vk_api
import logging

from pony.orm import db_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from settings import INTENTS, SCENARIOS, DEFAULT_ANSWER, HELP_ANSWER
import handlers
from models import UserState
import requests
import json
from image_maker import ImageMaker

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

    def send_msg(self, user_id, msg):
        self.api.messages.send(
            random_id=get_random_id(),
            message=msg,
            user_id=user_id
        )

    def get_photo_and_name(self, user_id, context):
        response = self.api.users.get(user_ids=user_id, fields=['photo_100'])
        context['first_name'] = response[0]['first_name']
        context['last_name'] = response[0]['last_name']
        context['photo_url'] = response[0]['photo_100']

    def send_img(self, user_id, image):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        response = requests.post(url=upload_url, files={"photo": ('template.png', image, 'image/png')})

        content = json.loads(response.content)
        photo_data = self.api.photos.saveMessagesPhoto(server=content['server'],
                                                       photo=content['photo'], hash=content['hash'])
        attach = f"photo{photo_data[0]['owner_id']}_{photo_data[0]['id']}"
        self.api.messages.send(
            random_id=get_random_id(),
            attachment=attach,
            user_id=user_id
        )

    @db_session
    def on_event(self, event):
        """
        Обработка события
        :param event: VkBotMessageEvent
        """

        if event.type != VkBotEventType.MESSAGE_NEW:
            # log.debug(f"Не умею обрабатывать данный тип события {event.type}")
            return
        text_to_send = DEFAULT_ANSWER
        user_id = event.message.from_id
        text = event.message.text
        state = UserState.get(user_id=str(user_id))
        if text == '/ticket':
            if state is not None:
                state.delete()
            text_to_send = self.start_scenario(user_id, "ticket")
            self.send_msg(user_id=user_id, msg=text_to_send)
            return
        if text == '/help':
            self.send_msg(user_id=user_id, msg=HELP_ANSWER)
            if state is not None:
                state.delete()
            return
        if state is not None:
            text_to_send = self.continue_scenario(state=state, text=text)
        else:
            for intent in INTENTS:
                if text in intent["tokens"]:
                    if intent["scenario"]:
                        text_to_send = self.start_scenario(user_id, intent["scenario"])
                    else:
                        text_to_send = intent["answer"]
        step = SCENARIOS[state.scenario_name]['steps'][state.step_name]
        if "image" in step:
            im = ImageMaker('external_data/template.png')
            self.get_photo_and_name(user_id, state.context)
            postcard = im.draw_postcard(state.context)
            self.send_img(user_id=user_id, image=postcard)
        self.send_msg(user_id=event.message.from_id, msg=text_to_send)

    def start_scenario(self, user_id, scenario_name):
        first_step_name = SCENARIOS[scenario_name]["first_step"]
        text_to_send = SCENARIOS[scenario_name]["steps"][first_step_name]['text']
        UserState(user_id=str(user_id), scenario_name=scenario_name, step_name=first_step_name, context={})
        return text_to_send

    def continue_scenario(self, state, text):
        steps = SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        next_step = steps[step['next_step']]
        text_to_send = next_step['text']
        correct_input, msg = handler(text=text, context=state.context)
        if correct_input:
            state.step_name = step['next_step']
            if not next_step['next_step']:
                state.delete()
        else:
            if not msg:
                text_to_send = step['failure_text']
            elif msg == 'Нет сообщения между этими городами':
                text_to_send = msg
                state.delete()
            elif msg == 'Неверные данные':
                text_to_send = steps["start_again"]['text']
                state.step_name = "start_again"
            elif msg == 'Не начинать заново':
                state.delete()
                text_to_send = 'Одобрено'
            else:
                text_to_send = msg
        return text_to_send.format(**state.context)


if __name__ == '__main__':
    config_logging()
    bot = Bot(TOKEN, GROUP_ID)
    bot.run()
