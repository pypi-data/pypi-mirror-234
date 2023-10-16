import asyncio
import logging
import time

import httpx


def format_zoomeye(item):
    new_item = {}
    if isinstance(item["ip"], list):
        if item["ip"]:
            new_item["ip"] = item["ip"][0]
        else:
            new_item["ip"] = ""
    else:
        new_item["ip"] = item['ip']
    port = str(item['portinfo']['port'])
    if "site" in item and item["site"]:
        new_item["url"] = "http://{}".format(item["site"])
    else:
        if "443" in port:
            new_item["url"] = f"https://{item['ip']}:{port}"
        else:
            new_item["url"] = f"http://{item['ip']}:{port}"
    if "country_name_CN" in item:
        new_item["country"] = item.pop("country_name_CN")
    if "subdivisions_name_CN" in item:
        new_item["city"] = item.pop("subdivisions_name_CN")
    return new_item


class ZoomEye(object):
    def __init__(self, token):
        self.url = 'https://api.zoomeye.org'
        self.token = token
        self.resources = None
        self.plan = None
        self.client = httpx.AsyncClient()
        self.client.headers = {'User-Agent': 'Python Zoomeye Client 3.0', 'API-KEY': token}
        self.semaphore = asyncio.Semaphore(10)
        self.total = -1

    async def query(self, dork: str, page: int, resource='host'):
        async with self.semaphore:
            if 0 < self.total < (page - 1) * 20:
                return
            url = f'{self.url}/{resource}/search'
            resp = await self.client.get(url, timeout=60, params={"query": dork, "page": page})
            if resp and resp.status_code == 200 and 'matches' in resp.text:
                content = resp.json()
                total = content['total']
                self.total = total
                for match in content['matches']:
                    item = format_zoomeye(match)
                    print(item['url'])

    async def search(self, dork, start_page=1, end_page=1, resource='host') -> (list, int):
        tasks = []
        items = []
        total = 0
        for page in range(start_page, end_page + 1):
            tasks.append(asyncio.create_task(self.query(dork, page, resource=resource)))
        await asyncio.gather(*tasks)
        return items, total


if __name__ == "__main__":
    zoomeye = ZoomEye("61D71206-3e56-65342-37f3-72b1743ba50")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(zoomeye.search("weblogic"))
