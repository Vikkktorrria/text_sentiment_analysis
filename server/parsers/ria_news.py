"""
Модуль для парсинга новостей с сайта https://ria.ru/

"""

import requests
import datetime

from bs4 import BeautifulSoup as bs

from . import consts

RIA_RU = 'https://ria.ru/company/'

RIA_RU_COMPANY = 'https://ria.ru/services/tagsearch/?date_start={date_start}&date={date_end}&tags%5B%5D=company'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.1.932 Yowser/2.5 Safari/537.36',
    'accept': '*/*'
}

def get_data():
    """
    Функция парсит новости за последние 7 дней с сайта Ria.ru
    :return: List - список статей
    """
    articles = []
    current_date = datetime.datetime.now()
    date_start = current_date - datetime.timedelta(days=60)

    resource =  'https://ria.ru/company/' # RIA_RU_COMPANY #
    link = f'https://ria.ru/services/tagsearch/?date_start={date_start.strftime("%Y%m%d")}&date={current_date.strftime("%Y%m%d")}&tags%5B%5D=company'
    print(link)

    r = requests.get(url=link, headers=consts.HEADERS)

    soup = bs(r.content, 'html.parser')
    print(soup)
    while soup is not None:
        for article in soup.find_all("div", class_='list-item'):

            article_header = article.find('a', class_='list-item__title')
            header = article_header.get_text()
            print(article_header['href'])
            article_soup = requests.get(article_header['href']).content
            article_date = bs(article_soup, 'html.parser').find('div', class_='article__info-date').find('a').get_text().split(' ')[-1]
            print(article_date)
            create_time = datetime.datetime.strptime(article_date, '%d.%m.%Y')
            # Полный текст новостной статьи
            text = ''
            for text_piece in bs(article_soup, 'html.parser').find_all('div', class_='article__text'):
                text += text_piece.get_text()

            print(text)

            article_object = {
                'Header': header,
                'Text': text,
                'CreateTime': create_time,
                'IsProcessed': False,
                'SourceId': 2,
            }

            articles.append(article_object)

        nextPageTag = soup.find(
            "div", class_="list-more")
        print(nextPageTag)
        soup = bs(requests.get(
            url=resource + nextPageTag['data-url'].split('/')[-1], headers=consts.HEADERS).content, "html.parser") if nextPageTag else None

    return articles

    # for article in soup.find_all("div", class_="list-item__content"):
    #     articleHeader = article.find('a', class_="list-item__title").get_text()
    #     print(articleHeader)

    # print()

def ria_parser():
    filter = None
    searchUrl = None

    articles = []
    return articles

# get_data()