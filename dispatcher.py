import collections
from calendar import monthrange
from pprint import pprint

from settings import ROUTES, FLIGHTS
from datetime import timedelta, date
DAY, WEEK = timedelta(days=1), timedelta(weeks=1)


def get_week_schedule(from_city, to_city, start_date):
    # return dict { date0(datetime.date object): [flight1, flight2, flight3], date1: [...], ...}
    result = collections.defaultdict(list)
    flights = ROUTES[from_city][to_city]
    for key, val in FLIGHTS.items():
        if key not in flights:
            continue
        if val['period'] == 'week':
            for day_number in val['days']:
                _date = next_week_day(start_date, day_number)
                result[_date].append(key)
        elif val['period'] == 'month':
            for day_number in val['days']:
                _date = next_month_day(start_date, day_number)
                if _date < start_date + WEEK:
                    result[_date].append(key)
        elif val['period'] == 'day':
            for i in range(7):
                _date = start_date + i * DAY
                result[_date].append(key)
    return result


def next_week_day(start_date, day_number):
    delta = (day_number - start_date.weekday()) % 7
    return start_date + timedelta(days=delta)


def next_month_day(start_date, day_number):
    delta = (day_number - start_date.day) % monthrange(start_date.year, start_date.month)[1]
    return start_date + timedelta(days=delta)


def dispatcher(from_city, to_city, departure_date):
    flights = []
    _date = departure_date
    while True:
        schedule = get_week_schedule(from_city, to_city, _date)
        for i in range(7):
            for flight in schedule[_date]:
                flights.append((flight, date.strftime(_date, "%d-%m-%Y")))
                if len(flights) == 5:
                    return flights
            _date += DAY
        if _date - departure_date == timedelta(days=365):
            return flights


if __name__ == '__main__':
    pprint(dispatcher('Москва', 'Сыктывкар', date.today()))