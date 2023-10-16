import aiohttp

class FortmesAPIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_data(self, endpoint):
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    async def push_data(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                return await response.json()
