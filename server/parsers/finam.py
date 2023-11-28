"""
Модуль для парсинга новостей с сайта https://www.finam.ru/

https://www.finam.ru/publications/section/companies/
"""

import datetime
import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from . import consts


def get_data():
    """

    :return:
    """

    articles = []
    current_date = datetime.datetime.now()
    date_start = current_date - datetime.timedelta(days=60)

    resource = 'https://www.finam.ru/'
    link = f'https://www.finam.ru/publications/section/companies/date/' \
           f'{date_start.strftime("%Y-%m-%d")}/{current_date.strftime("%Y-%m-%d")}/ '
    print(link)

    # Чтобы не открывать браузер, а запускать только процесс
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Firefox(options=options)
    driver.get(link)
    html = driver.page_source

    soup = bs(html, 'html.parser')
    driver.quit()

    for article in soup.find_all("a", class_='publication-list-item'):
        header = article.find('div', class_='font-l bold').get_text().strip()
        full_text_href = resource + article['href']

        driver = webdriver.Firefox(options=options)
        driver.get(full_text_href)
        article_soup = driver.page_source
        driver.quit()

        article_date = bs(article_soup, 'html.parser') \
            .find('div', class_='mr1x cl-grey').get_text().split(' ')[1].strip()

        create_time = datetime.datetime.strptime(article_date, '%d.%m.%y')
        # Полный текст новостной статьи
        text = ''
        for text_piece in bs(article_soup, 'html.parser').find('div', class_='clearfix mb2x').find_all('p'):
            text += text_piece.get_text()

        # Создадим структуру статьи
        article_object = {
            'Header': header,
            'Text': text,
            'CreateTime': create_time,
            'IsProcessed': False,
            'SourceId': 3,
        }

        print(article_object)

        articles.append(article_object)

    return articles
