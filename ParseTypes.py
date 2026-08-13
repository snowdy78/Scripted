import datetime

class ParseParams:
    def __init__(self, url: str):
        self.url = url

class ParseRequestData:
    def __init__(
        self,
        params: ParseParams,
        method: str = "GET",
        body = {},
        headers = {}
    ):
        self.params = params
        self.method = method
        self.body = body
        self.headers = headers

class ParseResponseData:
    def __init__(
        self,
        params: ParseParams,
        content: str = "",
        date_parsed: datetime.datetime | None = None
    ):
        self.params = params
        self.content = content
        self.date_parsed = date_parsed

class Script:
    def __init__(
        self, url: str,
        topic: int | str,
        subtopic_id: int | None = None,
        content: str = "",
        date_parsed: datetime.datetime = datetime.datetime.now()
    ):
        self.url = url
        self.topic = topic
        self.subtopic_id = subtopic_id
        self.content = content
        self.date_parsed = date_parsed

class Subtopic:
    def __init__(
        self,
        identifier: int,
        name: str,
        topic_id: int
    ):
        self.id = identifier
        self.name = name
        self.topic_id = topic_id

class Topic:
    def __init__(
        self,
        identifier: int,
        name: str
    ):
        self.id = identifier
        self.name = name

class Cookie:
    def __init__(self, name: str, value: str, domain: str, path: str ='/'):
        self.name = name
        self.value = value
        self.domain = domain
        self.path = path
