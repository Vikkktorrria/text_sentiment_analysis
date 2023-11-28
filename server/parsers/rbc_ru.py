"""

https://www.rbc.ru/business/
"""
import datetime
import requests

from bs4 import BeautifulSoup as bs

from . import consts

# TODO: возможно, здесь лучше каждый раз получать только первую страницу новостей при последующем запуске парсера

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
    link = f'https://www.rbc.ru/business/' # https://www.rbc.ru/v10/ajax/get-news-by-filters/?category=business&offset=32&limit=12

    r = requests.get(url=link, headers=consts.HEADERS)

    # Получаем html разметку страницы
    soup = bs(r.content, 'html.parser')
    # print(soup)
    while soup is not None:
        for article in soup.find_all("div", class_='item'):
            header = article.find('span', class_='item__title').get_text().strip()

            full_text_href = article.find('a', class_='item__link')['href']

            article_soup = requests.get(full_text_href).content
            article_date = bs(article_soup, 'html.parser').find('time', class_='article__header__date')['content'].split('T')[0]

            # day, month, year = article_date.split(' ')
            # article_date = f'{day}.{consts.MONTHS[month.lower()]}.{year}'
            create_time = datetime.datetime.strptime(article_date, '%Y-%m-%d')

            # Полный текст новостной статьи
            text = ''
            for text_piece in bs(article_soup, 'html.parser').find_all('p'):
                text += text_piece.get_text()

            article_object = {
                'Header': header,
                'Text': text,
                'CreateTime': create_time,
                'IsProcessed': False,
                'SourceId': 1,
            }
            print(article_object)

            articles.append(article_object)

        next_page_tag = soup.find(
            "li", class_="rubric-page__item _more")

        if not next_page_tag:
            soup = None
        else:
            href_tag = next_page_tag.find('a', class_='loadmore js-loadmore')
            print(next_page_tag)
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