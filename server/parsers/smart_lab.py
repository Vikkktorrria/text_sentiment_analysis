"""
Модуль для парсинга новостей с сайта https://smart-lab.ru/
https://smart-lab.ru/news/ - Новости компаний и новости по акциям

"""

# Импорт библиотек
from datetime import timedelta
import datetime

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

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
    # date_start = current_date - datetime.timedelta(days=60)

    resource = 'https://smart-lab.ru'
    # link = f'https://smart-lab.ru/news/'

    # Чтобы не открывать браузер, а запускать только процесс
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get('https://smart-lab.ru/news/')
    html = driver.page_source

    soup = bs(html, 'html.parser')
    driver.quit()

    for news_header in soup.find_all('h3', class_='title'):
        driver = webdriver.Firefox(options=options)
        # driver.get('https://smart-lab.ru/news/')
        link = resource + news_header.find('a')['href']

        driver.get(link)
        news_soup = bs(driver.page_source, 'html.parser')

        header = news_soup.find('h1', class_='title').find('span').get_text()
        text = news_soup.find('div', {'id': 'content_box'}).find('div', class_='content').get_text()
        article_date, article_time = news_soup.find('li', class_='date').get_text().split(',')
        day, month, year = article_date.split(' ')
        article_date = f'{day}.{consts.MONTHS[month.lower()]}.{year}'
        create_time = datetime.datetime.strptime(article_date, '%d.%m.%Y')

        driver.quit()

        # Создадим структуру статьи
        article_object = {
            'Header': header,
            'Text': text,
            'CreateTime': create_time,
            'IsProcessed': False,
            'SourceId': 4,
        }

        articles.append(article_object)

    return articles

def lenta_parser():
    """

    :return:
    """
    filter = None
    searchUrl = None

    articles = []
    return articles