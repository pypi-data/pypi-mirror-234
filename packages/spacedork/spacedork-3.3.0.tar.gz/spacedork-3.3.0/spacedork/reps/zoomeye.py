import asyncio
import logging
import time

import httpx

from spacedork.reps.base import SearchBase


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


class ZoomEye(SearchBase):
    def __init__(self, token,thread=2, **kwargs):
        super().__init__(**kwargs)
        self.url = 'https://api.zoomeye.org'
        self.token = token
        self.resources = None
        self.plan = None
        self.client = httpx.AsyncClient()
        self.client.headers = {'User-Agent': 'Python Zoomeye Client 3.0', 'API-KEY': token}
        self.semaphore = asyncio.Semaphore(thread)
        self.total = -1


    async def query(self, dork: str, page: int, resource='host'):
        async with self.semaphore:
            if 0 < self.total < (page - 1) * 20:
                return
            url = f'{self.url}/{resource}/search'
            try:
                resp = await self.client.get(url, timeout=60, params={"query": dork, "page": page})
            except Exception as e:
                print(f"Req Error:{e}")
                return
            if resp and resp.status_code == 200 and 'matches' in resp.text:
                content = resp.json()
                total = content['total']
                self.total = total
                for match in content['matches']:
                    item = format_zoomeye(match)
                    print(item['url'])
            else:
                print(f"req Error:{resp}")

    async def search(self, dork, start_page=1, end_page=1, resource='host') -> (list, int):
        tasks = []
        items = []
        total = 0
        for page in range(start_page, end_page + 1):
            tasks.append(asyncio.create_task(self.query(dork, page, resource=resource)))
        await asyncio.gather(*tasks)
        return items, total


if __name__ == "__main__":
    zoomeye = ZoomEye("")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(zoomeye.search("weblogic"))
