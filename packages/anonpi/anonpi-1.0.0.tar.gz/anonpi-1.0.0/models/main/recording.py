import typing as t
from anonpi.models.manager import RequestCooker


class Recording(object):
    def __init__(self, src):
        self.__src = src
        __requester = RequestCooker.cook_request(rname=True, url=src)
        hv = __requester.prepare_request(__requester)
        if hv[1] != 200:
            raise ValueError("Invalid url")
        self.__audio_data = hv[0]

    @property
    def audio_url(self):
        return self.__src

    @property
    def audio_data(self):
        return self.__audio_data

    def __getitem__(self, __name: str) -> bytes | str:
        vl = getattr(self, __name)
        if vl is None:
            raise AttributeError(f"Recording object has no attribute {__name}")
        return vl
