import requests
from .AlphaVantageService import getCompanyNews
from .PerigonService import getCompanyNewsPerigon
from models.Article import Article
from models.Company import Company, StockExchange


US_STOCK_EXCHANGES = [StockExchange.NASDAQ, StockExchange.NYSE]

# fetches news articles for a given company
def fetch_news(company: Company, pastHours: int, count:int=15) -> list[Article]:
    articles = []
    articles = getCompanyNewsPerigon(company.name, pastHours, count)
        
    return articles
