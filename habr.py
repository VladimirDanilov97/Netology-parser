from bs4 import BeautifulSoup
from pprint import pprint
import asyncio
import aiohttp
import logging
import time
import requests
from fake_useragent import UserAgent
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
logging.disable(logging.CRITICAL)



def scrap_main_page(User_Agent):
    headers = {
    'User-Agent': User_Agent
    }
    url = 'https://habr.com/ru/all/'
    response = requests.get(url=url, headers=headers) 
    with open('index.html', 'w') as f:
        f.write(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    times = soup.find_all('time')
    titles = soup.find_all('a', class_='tm-article-snippet__title-link')
    all_keywords = soup.find_all(class_='tm-article-snippet__hubs')
    zipped = list(zip(titles, all_keywords, times))

    return zipped

async def scrap_content_page(link):
    async with aiohttp.ClientSession() as session:   
        async with session.get(url=link) as resp:
                title_soup = BeautifulSoup(await resp.text(), 'html.parser')
                text = title_soup.find(id='post-content-body').text.lower()
                return text
         

async def filter_func(tuple, KEYWORDS):
    link ='https://habr.com' + tuple[0]['href']
    text = await scrap_content_page(link)
    title = tuple[0].text
    keywords = tuple[1].text 
    time = tuple[2]['datetime']
    logging.debug(f'{title}')  
    if (
    set(text.lower().split()) & set(KEYWORDS) != set()) or (
    set(title.lower().split()) & set(KEYWORDS) != set()) or (
    set(keywords.lower().split()) & set(KEYWORDS) != set()):
        return(time, title, link)

async def main():

    KEYWORDS = ['дизайн', 'фото', 'web', 'python', ]
    ua = UserAgent()
    zipped = scrap_main_page(User_Agent=ua.google)
    tasks = [filter_func(tup, KEYWORDS) for tup in zipped]
    l = await asyncio.gather(*tasks)
    result = list(filter(lambda x: x != None, l))
    return result
     


if __name__ == '__main__':
    res = asyncio.run(main())
    pprint(res)