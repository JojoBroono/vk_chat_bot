from datetime import time

ROUTES = {
    'Москва': {
        'Сыктывкар': ['AB11', 'DC34', 'AC22'],
        'Казань': ['CD90', 'BA12', 'BA19'],
        'Киров': ['GH56', 'GH48']
    },
    'Сыктывкар': {
        'Москва': [],
        'Казань': [],
        'Киров': []
    },
    'Казань': {
        'Москва': [],
        'Сыктывкар': [],
        'Киров': []
    },
    'Киров': {
        'Москва': [],
        'Сыктывкар': [],
        'Казань': []
    }
}

FLIGHTS = {
    'AB11': {
        'period': 'week',
        'days': (0, 3),
        'time': time(15, 30)
    },
    'DC34': {
        'period': 'month',
        'days': (10, 20),
        'time': time(12, 00)
    },
    'AC22': {
        'period': 'day',
        'days': [0],
        'time': time(10, 15)
    },
    'CD90': {
        'period': 'month',
        'days': [4, 12, 20, 28],
        'time': time(15, 30)
    },
    'BA12': {
        'period': 'month',
        'days': [5, 10, 15, 20],
        'time': time(2, 00)
    },
    'BA19': {
        'period': 'week',
        'days': [6],
        'time': time(6, 00)
    },
    'GH56': {
        'period': 'day',
        'days': [0],
        'time': time(11, 20)
    },
    'GH48': {
        'period': 'week',
        'days': [2],
        'time': time(15, 00)
    },
}

SCENARIOS = {
    "ticket": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Введите город отправления",
                "failure_text": "Город введен неправильно. Попробуйте ещё раз",
                "handler": "from_city_handler",
                "next_step": "step2"
            },
            "step2": {
                "text": "Введите город прибытия",
                "failure_text": "Город введен неправильно. Попробуйте ещё раз",
                "handler": "to_city_handler",
                "next_step": "step3"
            },
            "step3": {
                "text": "Введите дату в формате dd-mm-yyyy",
                "failure_text": "Неверный формат. Попробуйте еще раз",
                "handler": "date_handler",
                "next_step": "step4"
            },
            "step4": {
                "text": "Вот список ближайших рейсов: {flights_output}\n"
                        "Введите пожалуйста номер подходящего рейса",
                "failure_text": "Такого номера нет. Введите число от 1 до 5",
                "handler": "flight_handler", #TODO add
                "next_step": "step5"
            },
            "step5": {
                "text": "Какое количество мест необходимо? Введите число от 1 до 5",
                "failure_text": "Введите число от 1 до 5",
                "handler": "places_handler",
                "next_step": "step7"
            },
            # TODO комментарий
            # "step6": {
            #     "text": "Спасибо! Данные записаны",
            #     "failure_text": None,
            #     "handler": None,
            #     "next_step": None
            # },
            "step7": {
                "text": "Итак, вы ввели следующие данные:\n"
                        "Город отправления: {from_city}\n"
                        "Город назначения: {to_city}\n"
                        "Дата: {date}\n"
                        "Номер рейса: {flight_number}, отправляется в {flight_time}\n"
                        "Количество мест: {amount_of_places}\n"
                        "Данные верны? Введите Да/Нет",
                "failure_text": "Не понятно. Пожалуйста, введите Да или Нет",
                "handler": "right_data_handler",
                "next_step": "step8"
            },
            "step8": {
                "text": "Введите номер телефона",
                "failure_text": "Номер введен неверно. Попробуйте ещё раз",
                "handler": "phone_number_handler",# TODO handler
                "next_step": "step9"
            },
            "step9": {
                "text": "Спасибо! С вами свяжутся по номеру {phone_number}",# TODO format
                "failure_text": None,
                "handler": None,
                "next_step": None
            },
            # "step_incorrect_data": {
            #     "text": "Хотите ввести данные заново?",
            #     "failure_text": None,
            #     "handler": None,
            #     "next_step": None
            # }
        }
    }
}

DEFAULT_ANSWER = "Не понимаю вас."

HELP_ANSWER = "HELP"

INTENTS = [
    {
        "name": "greeting",
        "tokens": ["привет"],
        "scenario": None,
        "answer": "Приветствую, сапиенс. Чего желаете?"
    },
    {
        "name": "ticket",
        "tokens": ["/ticket"],
        "scenario": "ticket",
        "answer": None
    },
    {
        "name": "help",
        "tokens": ["/help"],
        "scenario": None,
        "answer": HELP_ANSWER
    }
]