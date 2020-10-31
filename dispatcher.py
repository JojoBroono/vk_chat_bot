import collections
from calendar import monthrange
from pprint import pprint

from flights import ROUTES, FLIGHTS
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
                date = next_week_day(start_date, day_number)
                result[date].append(key)
        elif val['period'] == 'month':
            for day_number in val['days']:
                date = next_month_day(start_date, day_number)
                if date < start_date + WEEK:
                    result[date].append(key)
    return result


def next_week_day(start_date, day_number):
    delta = (day_number - start_date.weekday()) % 7
    return start_date + timedelta(days=delta)


def next_month_day(start_date, day_number):
    delta = (day_number - start_date.day) % monthrange(start_date.year, start_date.month)[1]
    return start_date + timedelta(days=delta)


def dispatcher(from_city, to_city, departure_date):
    flights = []
    date = departure_date
    while True:
        schedule = get_week_schedule(from_city, to_city, date)
        for i in range(7):
            for flight in schedule[date]:
                flights.append((flight, date.isoformat()))
                if len(flights) == 10:
                    return flights
            date += DAY
        if date - departure_date == timedelta(days=365):
            return flights


if __name__ == '__main__':
    pprint(dispatcher('Москва', 'Лондон', date.today()))