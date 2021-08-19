import datetime


def create_url(start: datetime):
    urls = []
    date = start
    now = datetime.datetime.now()

    while (date < now):
        url = f'https://lenta.ru/{date.year}/{date.month:02}/{date.day:02})'
        print(url)
        urls.append(url)
        date += + datetime.timedelta(days=1)

    return urls


# date = datetime.datetime(year=2011, month=1, day=1)
# urls = create_url(date)
# print(urls)
# import json
# f = open('russianews/result/link.jl', 'r', encoding="utf-8")
#
# # returns JSON object as
# # a dictionary
# data = json.load(f)


import pandas as pd
jsonObj = pd.read_json(path_or_buf="./russianews/result/link.jl", lines=True)
print()