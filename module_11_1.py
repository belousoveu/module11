import requests
import matplotlib.pyplot as mpl
import pandas as pd
from threading import Thread
import datetime


class Rates(Thread):
    __base_url = 'https://cbrates.rbc.ru/tsv/cb/'
    rates = {}

    def __init__(self, currency_code):
        self.code = currency_code
        Thread.__init__(self)

    def run(self):
        url = f'{self.__base_url}{self.code}.tsv'
        resp = requests.get(url).text.split('\n')
        dates = [x.split('\t')[0] for x in resp]
        rates_list = [x.split('\t')[2] for x in resp]

        self.rates[self.code] = [dates, rates_list]


if __name__ == '__main__':
    currency = {'USD': '840', 'EUR': '978', 'GBR': '826'}
    # code = currency['USD']
    threads = []
    for code in currency:
        thread = Rates(currency[code])
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
    data = {}
    for key, value in currency.items():
        data[key] = pd.Series(Rates.rates[value][1], index=pd.to_datetime(Rates.rates[value][0], format='%Y%m%d'))

    currency_rates = pd.DataFrame(data)
    rates_last_10 = currency_rates.tail(10)
    print('Курс за последние 10 дней')
    print(rates_last_10)
    rates_today = currency_rates.loc[datetime.date.today().strftime('%Y-%m-%d')]
    print('Курсы валют на сегодня:')
    print(rates_today)
    rateUSD = currency_rates['USD'].loc[datetime.date(2024, 7, 1).strftime('%Y-%m-%d')]
    print('Курс USD на 01.07.2024 года', rateUSD)

    dates = rates_last_10.index.tolist()
    usd = rates_last_10['USD'].tolist()
    eur = rates_last_10['EUR'].tolist()
    gbr = rates_last_10['GBR'].tolist()

    mpl.title('Курсы валют за последние 10 дней', fontsize=20, fontname='Times New Roman')
    mpl.plot(dates, usd, label='USD', color='blue')
    mpl.plot(dates, eur, label='EUR', color='red')
    mpl.plot(dates, gbr, label='GBR', color='green')
    mpl.legend(['USD', 'EUR', 'GBR'], loc='upper left')
    mpl.xticks(rotation=45)

    mpl.show()
