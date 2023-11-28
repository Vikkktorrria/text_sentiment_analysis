import requests


def get_news(api_key):
    url = "https://newsapi.org/v2/everything?domains=kommersant.ru&language=ru&apiKey=" + api_key
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
