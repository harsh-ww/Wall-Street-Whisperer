from typing import List

strList = List[str]

class Article():
    def __init__(self, title: str, sourceURL: str, datePublished: str, sourceName: str, authors: strList, image: str, text:str='', keywords:list=[], summary=''):
        self.title = title
        self.sourceURL = sourceURL
        self.datePublished = datePublished
        self.sourceName = sourceName
        self.authors = authors
        self.image = image
        self.summary = summary
        if text:
            self.text = text
        if keywords:
            self.keywords = keywords