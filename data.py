ROUTES = {
    'Москва': {
        'Лондон': ['AB11', 'DC34', 'AC22']
    }
}

FLIGHTS = {
    'AB11': {
        'period': 'week',
        'days': (0, 3),
    },
    'DC34': {
        'period': 'month',
        'days': (10, 20)
    },
    # 'AC22': {
    #     'period': 'day',
    #     'days': 0
    # }
}

SCENARIOS = {
    "ticket": {
        "first_step": "step1",
        "steps": {
            "step1": {
                "text": "Введите город отправления",
                "failure_text": "Город введен неправильно. Попробуйте ещё раз",
                "handler": "city_handler",
                "next_step": "step2"
            },
            "step2": {
                "text": "Введите город прибытия",
                "failure_text": "Город введен неправильно. Попробуйте ещё раз",
                "handler": "city_handler",
                "next_step": "step3"
            },
            "step3": {
                "text": "Спасибо! Данные записаны",
                "failure_text": None,
                "handler": None,
                "next_step": None
            },
            "step4": {
                "text": "Спасибо! Данные записаны",
                "failure_text": None,
                "handler": None,
                "next_step": None
            },
            "step5": {
                "text": "Спасибо! Данные записаны",
                "failure_text": None,
                "handler": None,
                "next_step": None
            },
            "step6": {
                "text": "Спасибо! Данные записаны",
                "failure_text": None,
                "handler": None,
                "next_step": None
            },
            "step7": {
                "text": "Итак, вы ввели следующие данные:\n"
                        "Город отправления: {from_city}\n"
                        "Город назначения: {to_city}\n"
                        "Дата: {date}\n"
                        "Номер рейса: {flight_number}, отправляется в {flight_time}\n"
                        "Количество мест: {amount_of_places}\n"
                        "",
                "failure_text": None,
                "handler": None,
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
            }
        }
    }
}

DEFAULT_ANSWER = "Не знаю как ответить"

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