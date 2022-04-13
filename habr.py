from bs4 import BeautifulSoup
from pprint import pprint
import asyncio
import aiohttp
import logging
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
# logging.disable(logging.DEBUG)

KEYWORDS = ['дизайн', 'фото', 'web', 'python', ]
url = 'https://habr.com/ru/all/'

async def scrap_content_page(link):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=link) as resp:
                    title_soup = BeautifulSoup(await resp.text(), 'html.parser')
                    text = title_soup.find(id='post-content-body').text.lower()
    return text

    
async def get_data():
    result = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, 'html.parser')
            times = soup.find_all('time')
            titles = soup.find_all('a', class_='tm-article-snippet__title-link')
            all_keywords = soup.find_all('div', class_='tm-article-snippet__hubs')
            zipped = list(zip(titles, all_keywords, times))
            for title, keyword, time in zipped:
                logging.debug(f'{title.text}')
                link = 'https://habr.com'+title['href']
                text = await scrap_content_page(link)
                logging.debug(f'2 = {title.text}')
                if (
                set(keyword) & set(KEYWORDS) != set()) or (
                set(text.split()) & set(KEYWORDS) != set()) or (
                set(title.text.split()) & set(KEYWORDS) != set()):
                    result.append([
                        time['datetime'],
                        title.text,
                        link])
    logging.info(f'{result}')

async def main():
    await get_data()


if __name__ == '__main__':
    asyncio.run(main())