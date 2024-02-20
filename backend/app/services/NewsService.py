import requests
from .AlphaVantageService import getCompanyNews

from ..models.Article import Article
from ..models.Company import Company, StockExchange


US_STOCK_EXCHANGES = [StockExchange.NASDAQ, StockExchange.NYSE]

def fetch_news(company: Company, pastHours: int, count:int=50) -> list[Article]:
    articles = []
    print(company.exchange)
    print(company.exchange in US_STOCK_EXCHANGES)
    # Use AlphaVantage for US companies
    if company.exchange in US_STOCK_EXCHANGES:
        print('getting news')
        articles = getCompanyNews(company.ticker, pastHours, count)
    else:
        # use perigon for non-US companies 
        pass
    
    return articles
