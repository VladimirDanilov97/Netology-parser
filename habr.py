import requests
from bs4 import BeautifulSoup
from pprint import pprint
import asyncio
import aiohttp


KEYWORDS = ['дизайн', 'фото', 'web', 'python']
url = 'https://habr.com/ru/all/'

response = requests.get(url=url)
soup = BeautifulSoup(response.text, 'html.parser')

titles = soup.find_all('a', class_='tm-article-snippet__title-link')
articles = list(zip(
    [time['datetime'] for time in soup.find_all('time')],
    [title.text if set(KEYWORDS)&set(title.text.split())!=set() else None for title in titles ],
    [title['href'] if set(KEYWORDS)&set(title.text.split())!=set() else None for title in titles]
))
articles = list(filter(lambda article: article[2] != None and article[1] != None , articles))
pprint(articles)