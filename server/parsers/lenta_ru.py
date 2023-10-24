"""
Модуль для парсинга новостей с сайта https://lenta.ru/
https://lenta.ru/rubrics/economics/companies/ - компании
https://lenta.ru/rubrics/economics/investments/ - инвестиции
https://lenta.ru/rubrics/economics/economy/ - гос экономика
Лента добра - выкл, тогда подгружаются все новости

"""

# Импорт библиотек
from datetime import datetime, timedelta
import datetime
import requests
from bs4 import BeautifulSoup as bs
from . import consts


def get_data():
    """
    Функция получает html страницы и парсит по тегам:
     - заголовок статьи
     - текст статьи
     - время создания статьи
     -
    :return:
    """
    articles = []
    current_date = datetime.datetime.now()
    date_start = current_date - datetime.timedelta(days=60)

    resource = 'https://lenta.ru/'
    link = f'https://lenta.ru/rubrics/economics/companies/'

    r = requests.get(url=link, headers=consts.HEADERS)

    # Получаем html разметку страницы
    soup = bs(r.content, 'html.parser')

    while soup is not None:
        for article in soup.find_all("li", class_='rubric-page__item _news'):
            # Получим заголовок
            header = article.find('h3', class_='card-full-news__title').get_text()
            # Получим ссылку на полный текст новости
            full_text_href = resource + article.find('a', class_='card-full-news _subrubric')['href']
            # Получим контент по ссылке полного текста новости
            article_soup = requests.get(full_text_href).content
            # Заберём оттуда дату
            article_date = \
                bs(article_soup, 'html.parser').find('a',
                                                     class_='topic-header__item topic-header__time').get_text().split(
                    ',')[1].strip()
            day, month, year = article_date.split(' ')
            article_date = f'{day}.{consts.MONTHS[month.lower()]}.{year}'
            create_time = datetime.datetime.strptime(article_date, '%d.%m.%Y')
            # Заберём полный текст новостной статьи
            text = ''
            for text_piece in bs(article_soup, 'html.parser').find_all('p', class_='topic-body__content-text'):
                text += ' ' + text_piece.get_text()
            # Создадим структуру статьи
            article_object = {
                'Header': header,
                'Text': text,
                'CreateTime': create_time,
                'IsProcessed': False,
                'SourceId': 1,
            }

            articles.append(article_object)

        next_page_tag = None  # soup.find("li", class_="rubric-page__item _more")

        if not next_page_tag:
            soup = None
        else:
            href_tag = next_page_tag.find('a', class_='loadmore js-loadmore')
            # print(next_page_tag)
            soup = bs(requests.get(
                url=resource + href_tag['href'], headers=consts.HEADERS).content, "html.parser") if href_tag else None

    return articles


def lenta_parser():
    """

    :return:
    """
    filter = None
    searchUrl = None

    articles = []
    return articles
