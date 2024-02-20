class Article():
    def __init__(self, title: str, sourceURL: str, datePublished: str, sourceName: str, authors: list[str], image: str):
        self.title = title
        self.sourceURL = sourceURL
        self.datePublished = datePublished
        self.sourceName = sourceName
        self.authors = authors
        self.image = image