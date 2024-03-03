import requests
from .AlphaVantageService import getCompanyNews
from .PerigonService import getCompanyNewsPerigon

from models.Article import Article
from models.Company import Company, StockExchange


US_STOCK_EXCHANGES = [StockExchange.NASDAQ, StockExchange.NYSE]

def fetch_news(company: Company, pastHours: int, count:int=50) -> list[Article]:
    articles = []
    articles = getCompanyNewsPerigon(company.name, pastHours, count)

    # # Use AlphaVantage for US companies
    # if company.exchange in US_STOCK_EXCHANGES:
    #     articles = getCompanyNews(company.ticker, pastHours, count)
    # else:
    #     # use perigon for non-US companies 
        
    
    return articles
