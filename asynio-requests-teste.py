import asyncio
import time
from aiohttp import ClientSession 


async def getData(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    firstTime = time.time()

    async with ClientSession() as session:
        tasks = []
        for _ in range(1000):
            res = getData(session, 'https://pokeapi.co/api/v2/ability/?limit=20&offset=20')
            tasks.append(res)
        results = await asyncio.gather(*tasks)
         
    endTime = time.time()

    print("Tempo de execução:", round(endTime - firstTime, 2), "segundos")
    print(len(results))

if __name__ == '__main__':
    asyncio.run(main())
