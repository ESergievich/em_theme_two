import asyncio
import os

import aiofiles
from bs4 import BeautifulSoup

from config import DIRECTORY, PAGE_URL, SELECTOR_LINKS, SELECTOR_DATES


async def fetch_html(session, url):
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def download_file(session, url, filename):
    os.makedirs(DIRECTORY, exist_ok=True)
    filepath = os.path.join(DIRECTORY, filename)

    async with session.get(url) as response:
        response.raise_for_status()
        async with aiofiles.open(filepath, 'wb') as f:
            content = await response.read()
            await f.write(content)


def get_last_page_url(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination_items = soup.select('.bx-pagination ul li')

    if len(pagination_items) >= 2:
        last_page_li = pagination_items[-2]
        href = last_page_li.find('a').get('href')
        if href:
            return int(href.split('-')[-1])

    return 1


async def process_pages(session):
    # html = await fetch_html(session, f"{PAGE_URL}1")
    # last_page = get_last_page_url(html) # 391
    last_page = 391

    tasks = [
        fetch_html(session, f"{PAGE_URL}{page_num}")
        for page_num in range(1, last_page + 1)
    ]
    pages_html = await asyncio.gather(*tasks)

    download_tasks = []
    for html in pages_html:
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select(SELECTOR_LINKS)
        dates = soup.select(SELECTOR_DATES)

        for link, date in zip(links, dates):
            href = link.get('href')
            year = date.get_text().split('.')[2]

            if href and int(year) < 2023:
                return download_tasks

            filename = href.split('/')[-1].split('?')[0]
            download_tasks.append(download_file(session, href, filename))

    return download_tasks
