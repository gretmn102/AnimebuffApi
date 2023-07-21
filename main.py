import asyncio
import aiohttp
import lxml.html
import time
from lxml.etree import _Element


async def get_html(client, urls):
    async with client.get(urls) as resp:
        print("Обрабатываю ", urls)
        return await resp.text()


async def get_links(client, page):
    html = await get_html(client, page)
    doc = lxml.html.fromstring(html)
    linkAnime = []
    imgAnime = []
    links = doc.xpath("//a[@class='anime-item']/@href")
    imgs = doc.xpath("//img[@class='anime-item__image']/@src")
    for link, img in zip(links, imgs):
        link = "https://animebuff.ru" + link
        img = "https://animebuff.ru" + img

        linkAnime.append(link)
        imgAnime.append(img)
    return linkAnime, imgAnime


async def get_data(client, urls):
    data = await get_links(client, urls)
    for link, img in zip(data[0], data[1]):
        print(link)
        async with client.get(link) as resp:
            html = await resp.text()
            doc = lxml.html.fromstring(html)
            pattern = "//h1"
            nodes: list[_Element] = doc.xpath(pattern)
            if len(nodes) == 0:
                print(f"not found {pattern}")
            else:
                header: _Element = nodes[0]
                print(header.text)


async def main():
    t1 = time.time()
    async with aiohttp.ClientSession() as client:
        tasks = []
        for page in range(1, 2):
            url = f"https://animebuff.ru/anime?page={page}"
            task = asyncio.create_task(get_data(client, url))
            tasks.append(task)

        await asyncio.gather(*tasks)
    print(time.time() - t1)


if __name__ == "__main__":
    asyncio.run(main())
