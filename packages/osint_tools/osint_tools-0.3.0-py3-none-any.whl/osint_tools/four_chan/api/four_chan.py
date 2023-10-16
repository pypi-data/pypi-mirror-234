from ..schemas import *
import json
import httpx
import requests
# import urllib.parse
import urllib.request
import asyncio
# import random
from time import sleep
import os.path

def get_catalog(board: Board, as_dict: bool = False) -> list[CatalogThread]:
    url = f'https://a.4cdn.org/{Board[board]}/catalog.json'
    data = requests.get(url).json()

    all_posts: list[CatalogThread] = []
    for page in data:
        for thread in page['threads']:
            '''attach board to thread'''
            assert not isinstance(board, list), 'board should not be list'
            thread['board'] = board
            all_posts.append(CatalogThread(**thread))
    return all_posts



def catalog_image_generator(board: Board):
    # https://github.com/4chan/4chan-API/blob/master/pages/User_images_and_static_content.md
    url = f'https://a.4cdn.org/{Board[board]}/catalog.json'
    r = requests.get(url).json()
    lst = []
    for idx, page in enumerate(r):
        for thread in r[idx]['threads']:
            if 'last_replies' in thread:
                for comment in thread['last_replies']:
                    if 'ext' in comment and 'tim' in comment:
                        url = 'http://i.4cdn.org/{0}/{1}{2}'.format(
                            board, 
                            str(comment['tim']), 
                            str(comment['ext'])
                        )
                        lst.append(url)
    print(lst)
    print(len(lst))
    for i in lst:
        yield i

def iter_img_lst(board, save_dir: str):
    '''
    https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/If-Modified-Since
    If-Modified-Since: <day-name>, <day> <month> <year> <hour>:<minute>:<second> GMT
    e.g.:  Thu, 15 Dec 2022 03:51:47 GMT
    '''
    path = f'{save_dir}/'
    counter = 0
    for img in catalog_image_generator(board):
        file_name = img.split('/')[-1]
        if not os.path.isfile(path + file_name):# if file does not exist; download image.
            sleep(5)
            try:
                filename, headers = urllib.request.urlretrieve(img, path + file_name)
            except Exception as e:
                print(e)
            else:
                counter += 1
                print(f'{counter}: {filename} {headers}')
        else:
            print(f'file exists: {file_name}')
            continue



# req = urllib.request.Request('http://www.example.com/')
# req.add_header('Referer', 'http://www.python.org/')
# # Customize the default User-Agent header value:
# req.add_header('User-Agent', 'urllib-example/0.1 (Contact: . . .)')
# r = urllib.request.urlopen(req)


























class AsyncHTTP:

    def get_or_create_eventloop(self):
        # https://techoverflow.net/2020/10/01/how-to-fix-python-asyncio-runtimeerror-there-is-no-current-event-loop-in-thread/
        try:
            return asyncio.get_event_loop()
        except RuntimeError as err:
            if "There is no current event loop in thread" in str(err):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()

    async def _read_lines(self, url: str, client: httpx.AsyncClient):
        assert len(url) > 10
        try:
            async with client.stream("GET", url) as resp:
                async for line in resp.aiter_lines():
                    yield json.loads(line)
        except httpx.RemoteProtocolError as e:
            print('read_lines: ', e)
            yield e


async def get_catalog_v2():
    url = 'https://a.4cdn.org/wg/catalog.json'
    client = httpx.AsyncClient()
    aa = AsyncHTTP()
    async_gen = aa._read_lines(url, client)

    all_posts = []
    # _type = ''
    async for page in async_gen:
        # _type = type(page)
        for thread in page:
            for item in thread['threads']:
                all_posts.append(item)

            # all_posts.append(thread)
            # thread = jsonable_encoder(thread)
            # all_posts.append(CatalogThread(**thread))
    # print(_type)
    await async_gen.aclose()
    await client.aclose()
    return all_posts
