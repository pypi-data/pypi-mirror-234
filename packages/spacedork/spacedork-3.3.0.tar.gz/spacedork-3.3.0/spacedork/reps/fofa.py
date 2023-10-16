import asyncio
import base64
import httpx

from spacedork.reps.base import SearchBase


def format_fofa(item):
    new_item = {
        "url": f'{item[0]}://{item[1]}:{item[2]}',
        "ip": item[1],
        "port": item[2],
    }
    return new_item


class Fofa(SearchBase):
    def __init__(self, token=None, email=None, thread=2, **kwargs):
        super().__init__(**kwargs)
        self.url = 'https://fofa.info'
        self.token = token
        self.email = email
        self.resources = None
        self.plan = None
        self.client = httpx.AsyncClient()
        self.client.headers = {'User-Agent': 'Python spacedork Client 3.0'}
        self.semaphore = asyncio.Semaphore(thread)
        self.total = -1

    async def query(self, dork: str, page: int):
        async with self.semaphore:
            if 0 < self.total < (page - 1) * 20:
                return
            url = f'{self.url}/api/v1/search/all'
            try:
                resp = await self.client.get(url, timeout=60,
                                             params={"qbase64": base64.b64encode(dork.encode()).decode(),
                                                     "page": page, "key": self.token,
                                                     "email": self.email,
                                                     "fields": "protocol,ip,port"})
            except Exception as e:
                print(f"Req Error:{e}")
                return
            if resp and resp.status_code == 200:
                content = resp.json()
                total = content['size']
                self.total = total
                for match in content['results']:
                    item = format_fofa(match)
                    self.echo(item)
            else:
                print(f"req Error:{resp}")

    async def search(self, dork, start_page=1, end_page=1, resource='host') -> (list, int):
        tasks = []
        items = []
        total = 0
        for page in range(start_page, end_page + 1):
            tasks.append(asyncio.create_task(self.query(dork, page)))
        await asyncio.gather(*tasks)
        return items, total


if __name__ == "__main__":
    zoomeye = Fofa("", email="")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(zoomeye.search("weblogic"))
