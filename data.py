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