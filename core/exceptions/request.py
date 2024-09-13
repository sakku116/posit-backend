class RequestException(Exception):
    def __init__(self, *args: object, url: str = "") -> None:
        self.url = url
        super().__init__(*args)
