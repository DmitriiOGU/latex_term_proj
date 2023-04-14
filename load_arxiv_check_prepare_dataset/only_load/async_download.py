import aiohttp, asyncio
URL = 'https://catfact.ninja/'
class Api:
    def __init__(self, url: str):
        self.url = url
    def run_case(func, path, times):
        start_timestamp = time.time()
        
        asyncio.run(func(path, times))
    
        task_time = round(time.time() - start_timestamp, 2)
        rps = round(times / task_time, 1)
        print(
            f"| Requests: {times}; Total time: {task_time} s; RPS: {rps}. |\n"
        )
    async def async_http_get(self, path: str, times: int):
        async with aiohttp.ClientSession() as session:
            content = []
            for _ in tqdm(range(times), desc='Async fetching data...', colour='GREEN'):
                response = await session.get(url=self.url + path)
                content.append(await response.text(encoding='UTF-8'))
            return content
if __name__ == '__main__':
    N=50	
    URL = 'https://export.arxiv.org/e-print/0906.4082'
    api = Api(URL)
    run_case(api.async_http_get, path='fact/', times=N)