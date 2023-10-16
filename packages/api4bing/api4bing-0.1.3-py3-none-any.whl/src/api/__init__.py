import rookiepy
import requests
from .headers import HEADERS
from bs4 import BeautifulSoup as bs
from urllib.parse import parse_qs, urlsplit, urlunsplit, urlparse, urlunparse
import time
from typing import List
import webbrowser
from api.cross_open import default_open
import tempfile


class HighDemandException(Exception):
    pass

class ContentWarningException(Exception):
    pass



class Image:
    def __init__(self, url: str) -> None:
        self.url = url
    
    def save(self, path: str = None) -> str:
        if not path:
            path = tempfile.mktemp(".jpg")
        with requests.get(self.url, stream=True) as res, open(path, 'wb') as f:
            res.raise_for_status()
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        return path

    def bytes(self):
        res = requests.get(self.url)
        res.raise_for_status()
        return res.content


    def open(self, in_browser = False):
        if in_browser:
            webbrowser.open(self.url)
        else:
            path = self.save()
            default_open(path)
        


class BingAPI:
    def __init__(self, session: requests.Session = None) -> None:
        self.s = session or self._create_session()
        self._check_auth(self.s.cookies)

    def _create_session(self):
        """
        Create session from web browsers automatically using package called rookiepy
        """
        cookies = rookiepy.load(['bing.com', 'microsoft.com'])
        cj = rookiepy.to_cookiejar(cookies)
        for c in cj:
            c.expires = None
        
        session = requests.session()
        session.cookies = cj
        session.headers = HEADERS
        return session

    def _clean_url(self, url):
        """
        remove_query_params_and_fragment
        """
        return urlunsplit(urlsplit(url)._replace(query="", fragment=""))


    def _parse_create_url(self, url):
        """
        Parse the URL returned from create_images 
        for conveniend URL with SSR
        """
        url = urlparse(url)
        host = url.netloc
        path = url.path
        schema = url.scheme
        params = parse_qs(url.query)
        id = params.get('id', [''])[0]
        if not id:
            raise HighDemandException()
        q = params.get('q', [''])[0].replace(' ', '-')
        new_url = urlunparse((url.scheme, url.netloc, f'{path}/{q}/{id}', '', '', ''))
        return new_url



    def _create_images(self, prompt) -> str:
        """
        Actual request to create the image from prompt
        """
        data = {
            'q': prompt,
            'qs': 'ds',
        }
        response = self.s.post(f'https://www.bing.com/images/create?q={prompt}', headers=HEADERS, data=data)
        response.raise_for_status()
        text = response.text
        
        if 'unable to process new requests.' in text:
            raise HighDemandException("Can't generate image due to high demand")
        parsed = self._parse_create_url(response.url)
        return parsed


    def _check_auth(self, cookies):
        """
        Check if authenticated with microsoft
        """
        res = requests.get("https://account.microsoft.com/devices", timeout=10, cookies=cookies, headers=HEADERS)
        assert res.url == 'https://account.microsoft.com/devices', 'Please Login first at https://login.live.com/'

    def get_images(self, url: str) -> List[Image]:
        """
        Get images from the URL created by create_image
        """
        images: List[Image] = list()
        res = self.s.get(url)
        res.raise_for_status()
        doc = bs(res.text, features='html.parser')
        _is_loading = doc.find('div', {'id': 'giloader'}) is not None
        images_div = doc.find('div', {'class': 'dgControl dtl'})


        if not images_div: # loading or error
            if 'Content Warning' in res.text:
                raise ContentWarningException("Got Content Warning")
        else:
            images_elements = images_div.findAll("img")
            for img_element in images_elements:
                url = img_element['src']
                if url:
                    url = self._clean_url(url)
                    images.append(Image(url))
        return images
    
    def create_images(self, prompt, timeout = 120, max_retries = 4, sleep_sec = 2):
        """
        High level function to create images using retry mechanism
        """
        start = time.time()
        for i in range(max_retries + 1):
            try:
                url = self._create_images(prompt)
            except Exception as e:
                if i >= max_retries:
                    raise e
                time.sleep(sleep_sec)
        images = []
        while True:
            images = self.get_images(url)
            if images:
                break
            if time.time() - start > timeout:
                raise TimeoutError(f"Cant get images for url {url}")
            time.sleep(5)
        return images
