import json
import sys
from abc import ABC, abstractclassmethod

import requests


class Stream(ABC):
    @abstractclassmethod
    def write(self, msg: str) -> None:
        pass


class Consol(Stream):
    def write(self, msg: str) -> None:
        sys.stderr.write(msg)


class HTTPSINK(Stream):
    def __init__(self, url: str) -> None:
        self.url = url

    def write(self, msg) -> None:
        with requests.Session() as session:
            session.post(
                url=self.url,
                data=json.dumps({'level': json.loads(msg)['level'], 'message': msg}, ensure_ascii=False).encode(
                    'UTF-8'
                ),
                headers={'content-type': 'application/json'},
            )
