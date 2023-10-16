class MerryMimetype:

    def __init__(self, _type, tail):

        self._type = _type
        self.tail = tail

    def __str__(self) -> str:
            return f"{self._type}/{self.tail}"
