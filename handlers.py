import re
import datetime
from settings import FLIGHTS, ROUTES
from dispatcher import dispatcher

phone_number_re = re.compile(r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$')


def normalize_city(text):
    if re.match(r'москв', text.lower()):
        return 'Москва'
    elif re.match(r'сыктывкар', text.lower()):
        return 'Сыктывкар'
    elif re.match(r'киров', text.lower()):
        return 'Киров'
    elif re.match(r'казан', text.lower()):
        return 'Казань'
    else:
        return ''


def from_city_handler(text, context):
    city = normalize_city(text)
    if not city:
        return False, ''
    context['from_city'] = city
    return True, ''


def to_city_handler(text, context):
    city = normalize_city(text)
    if not city:
        return False, ''
    if not ROUTES[context['from_city']][city]:
        return False, 'Нет сообщения между городами',
    context['to_city'] = city
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
        context['flights_output'] = '\n'
        for i, flight in enumerate(flights):
            num = flight[0]
            date = flight[1]
            flight_time = FLIGHTS[num]['time']
            flight_time_str = datetime.time.strftime(flight_time, '%H:%M')
            context['flights_output'] += f"{i + 1}) {num} : {date} {flight_time_str}\n"
        return True, ''
    except ValueError:
        return False, 'Неверный формат даты'


def flight_handler(text, context):
    if '1' <= text <= '5':
        number = int(text) - 1
        context['flight_number'] = context['flights'][number][0]
        context['date'] = context['flights'][number][1]
        flight_time = FLIGHTS[context['flight_number']]['time']
        context['flight_time'] = datetime.time.strftime(flight_time, '%H:%M')
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


def start_again_handler(text, context):
    if text.lower() == 'да':
        return True, ''
    elif text.lower() == 'нет':
        return False, 'Не начинать заново'
    else:
        return False, ''


def comment_handler(text, context):
    context['comment'] = text
    return True, ''


if __name__ == '__main__':
    print(flight_handler('2', {}))
    print(flight_handler('8', {}))
    print(flight_handler('0', {}))
    print(flight_handler('5', {}))
