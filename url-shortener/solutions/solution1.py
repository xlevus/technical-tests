#!/usr/bin/env python3

## README.md:
##
## Requirements: tornado
##
## Testing: `./solution1.py test`
## Running `./solution1.py`
##
## Scaling: This will probably handle >1k RPS as-is. If resiliency is
## required, subclass `Database` with something that talks to a database.
## and pass an instance in to `get_app`.

import sys
import json
import random
import string
from typing import Any
from urllib.parse import urlparse
import unittest

import tornado.ioloop
import tornado.testing
import tornado.web

SHORT_URL_LEN = 8


def random_string(length) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits)
                   for x in range(length))


class Database(object):
    """Simple async database implementation.
    """
    def __init__(self) -> None:
        self.db = {}

    async def set(self, key: str, value: Any) -> None:
        self.db[key] = value

    async def get(self, key: str) -> Any:
        return self.db[key]

    async def contains(self, key: str) -> bool:
        return key in self.db


class ShortenHandler(tornado.web.RequestHandler):
    def initialize(self, database: Database):
        self.db = database

    def write_error(self, status, message: str = None, **kwargs):
        self.write({"error": message})

    def prepare(self):
        try:
            self.json_body = json.loads(self.request.body)
        except ValueError:
            raise tornado.web.HTTPError(400)

    async def post(self):

        try:
            parsed = urlparse(self.json_body['url'])
        except KeyError:
            self.send_error(400, message='No URL provided.')
            return

        if parsed.scheme not in {'http', 'https'}:
            self.send_error(400, message="Invalid URL protocol.")
            return

        if not parsed.netloc:
            self.send_error(400, message="Invalid URL.")
            return

        while True:
            key = random_string(SHORT_URL_LEN)
            if not (await self.db.contains(key)):
                break

        await self.db.set(key, self.json_body['url'])
        self.set_status(201)
        self.write({'shortened_url':
                    f"{self.request.protocol}://{self.request.host}/{key}"})


class GetUrlHandler(tornado.web.RequestHandler):
    def initialize(self, database: Database):
        self.db = database

    async def get(self, key: str):
        try:
            url = await self.db.get(key)
            self.redirect(url)
        except KeyError:
            raise tornado.web.HTTPError(404)


def get_app(database: Database) -> tornado.web.Application:
    return tornado.web.Application([
        (r"/shorten_url/?", ShortenHandler, {'database': database}),
        (r"/([A-Za-z0-9]+)/?", GetUrlHandler, {'database': database})
    ])


class TestURLShortener(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        return get_app(Database())

    def fetch(self, *a, body=None, **k):
        if isinstance(body, dict):
            body = json.dumps(body)
        resp = super().fetch(*a, body=body, **k)
        return resp

    def test_shorten_url(self):
        resp = self.fetch(
            '/shorten_url',
            method='POST',
            body={'url': 'https://example.com/'})

        self.assertEqual(resp.code, 201)

        b = json.loads(resp.body)
        url = b['shortened_url']

        resp2 = self.fetch(url, follow_redirects=False)
        self.assertEqual(resp2.code, 302)
        self.assertEqual(resp2.headers['Location'], 'https://example.com/')

    def _test_bad_body(self, b, message=None):
        resp = self.fetch('/shorten_url', method='POST', body=b)
        self.assertEqual(resp.code, 400)

    def test_shorten_url_bad_json(self):
        self._test_bad_body('')
        self._test_bad_body('{json}')

    def test_shorten_url_no_url(self):
        self._test_bad_body({'qrl': 'http://example.com'})

    def test_shorten_url_bad_scheme(self):
        self._test_bad_body({'url': 'ftp://example.com'})

    def test_shorten_url_bad_uri(self):
        self._test_bad_body({'url': 'https://'})


if __name__ == '__main__':
    if sys.argv[-1] == 'test':
        sys.argv = sys.argv[:-1]
        unittest.main()

    else:
        db = Database()
        app = get_app(db)
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()
