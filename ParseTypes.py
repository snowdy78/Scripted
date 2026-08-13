import datetime
from typing import TypedDict

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
    def __init__(self, params: ParseParams, content, date_parsed: datetime.datetime | None = datetime.datetime.now()):
        self.params = params
        self.content = content
        self.date_parsed = date_parsed

class Script(TypedDict):
    url: str
    topic_id: int
    subtopic_id: int | None
    content: str | None
    date_parsed: datetime.datetime | None

class Subtopic(TypedDict):
    id: int
    name: str
    topic_id: str

class Topic(TypedDict):
    id: int
    name: str

def createScript(url: str, topic: str, subtopic: str | None = None, content: str | None = None, date_parsed: datetime.datetime | None = None) -> Script:
    return {
        "url": url,
        "topic": topic,
        "subtopic": subtopic,
        "content": content,
        "date_parsed": date_parsed
    }

def createSubtopic(subtopic: str, topic: str) -> Subtopic:
    return {
        "subtopic": subtopic,
        "topic": topic
    }

def createTopic(topic: str, subtopics: list[str]) -> Topic:
    return {
        "topic": topic,
        "subtopics": [createSubtopic(subtopic, topic) for subtopic in subtopics]
    }


class Cookie:
    def __init__(self, name: str, value: str, domain: str, path: str ='/'):
        self.name = name
        self.value = value
        self.domain = domain
        self.path = path
