import asyncio

import aiohttp

from config import BASE_URL
from db import init_db
from process_excel import process_excel_files
from process_pages import process_pages


async def main():
    async with aiohttp.ClientSession(BASE_URL) as session:
        tasks = await process_pages(session)
        await asyncio.gather(*tasks)
    await init_db()
    await process_excel_files()


if __name__ == "__main__":
    asyncio.run(main())
