import re

city_re = re.compile(r'лондон|москв|париж|хельсинк')


def city_handler(text, context):
    match = re.match(city_re, text.lower())
    if not match:
        return False
    if 'from_city' in context:
        context['to_city'] = text
    else:
        context['from_city'] = text
    return True


if __name__ == '__main__':
    print(city_handler("Лондоном", {}))
    print(city_handler("Китай", {}))
    print(city_handler("лондона", {}))
    print(city_handler("масква", {}))