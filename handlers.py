import re
import datetime
from data import FLIGHTS, ROUTES
from dispatcher import dispatcher

city_re = re.compile(r'москв|сыктывкар|киров|казан')
phone_number_re = re.compile(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')


def city_handler(text, context):
    match = re.match(city_re, text.lower())
    if not match:
        return False
    if 'from_city' in context:
        context['to_city'] = text
    else:
        context['from_city'] = text
    return True


def from_city_handler(text, context):
    match = re.match(city_re, text.lower())
    if not match:
        return False, ''
    context['from_city'] = text
    return True, ''


def to_city_handler(text, context):
    match = re.match(city_re, text.lower())
    if not match:
        return False, ''
    if not ROUTES[context['from_city']][text]:
        return False, 'Нет сообщения между городами',
    context['to_city'] = text
    return True, ''


def date_handler(text, context):
    _format = '%d-%m-%Y'
    try:
        d = datetime.datetime.strptime(text, _format)
        today = datetime.datetime.now()
        year = datetime.timedelta(days=365)
        if d < today or d > today + year:
            return False, 'Слишком ранняя или слишком поздняя дата'
        context['date'] = text

        flights = dispatcher(context['from_city'], context['to_city'], d)
        context['flights'] = flights
        return True, ''
    except ValueError:
        return False, 'Неверный формат даты'


def flight_handler(text, context):
    if '1' <= text <= '5':
        context['flight_number'] = text
        return True, ''
    else:
        return False, ''


def places_handler(text, context):
    if '1' <= text <= '5':
        context['amount_of_places'] = text
        return True, ''
    else:
        return False, ''


def right_data_handler(text, context):
    if text.lower() == 'да':
        return True, ''
    elif text.lower() == 'нет':
        return False, 'Неверные данные'
    else:
        return False, ''


def phone_number_handler(text, context):
    match = re.match(phone_number_re, text.lower())
    if not match:
        return False, ''
    context['phone_number'] = text
    return True, ''


if __name__ == '__main__':
    print(flight_handler('2', {}))
    print(flight_handler('8', {}))
    print(flight_handler('0', {}))
    print(flight_handler('5', {}))
