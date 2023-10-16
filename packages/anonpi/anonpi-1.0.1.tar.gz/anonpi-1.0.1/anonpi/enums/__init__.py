from anonpi.enums.languages import AnonLang
from json import dumps


class Language(AnonLang):

    @classmethod
    def iterr(cls):
        return dict(zip([x for x in dir(cls) if not x.startswith("__") and not x.startswith("_") and not x in ['iterr', 'valid']], [getattr(cls, x) for x in dir(cls) if not x.startswith("__") and not x.startswith("_")]))

    @classmethod
    def valid(cls, lang: str):
        if (lang.lower() in cls.iterr().values()):
            return lang.lower()
        if (lang.upper() in cls.iterr().keys()):
            return getattr(cls, lang.upper())
        else:
            raise ValueError(
                "Invalid Language || List of Languages: \n" + dumps(cls.iterr(), indent=4))


__slots__ = ['Language']
