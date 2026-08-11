import datetime

class ParseParams:
    def __init__(self, url: str):
        self.url = url

class ParseRequestData:
    def __init__(self, params: ParseParams, method: str = "GET", body = {}, headers = {}):
        self.params = params
        self.method = method
        self.body = body
        self.headers = headers

class ParseResponseData:
    def __init__(self, params: ParseParams, content, date_parsed: datetime.datetime | None = None):
        self.params = params
        self.content = content
        self.date_parsed = date_parsed

class Cookie:
    def __init__(self, name: str, value: str, domain: str, path: str ='/'):
        self.name = name
        self.value = value
        self.domain = domain
        self.path = path
