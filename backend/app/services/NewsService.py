import requests
from .AlphaVantageService import getCompanyNews
from .PerigonService import getCompanyNewsPerigon

from ..models.Article import Article
from ..models.Company import Company, StockExchange


US_STOCK_EXCHANGES = [StockExchange.NASDAQ, StockExchange.NYSE]

def fetch_news(company: Company, pastHours: int, count:int=50) -> list[Article]:
    articles = []

    # Use AlphaVantage for US companies
    if company.exchange in US_STOCK_EXCHANGES:
        articles = getCompanyNews(company.ticker, pastHours, count)
    else:
        # use perigon for non-US companies 
        articles = getCompanyNewsPerigon(company.name, pastHours, count)
    
    return articles


if __name__ == '__main__':
    tesco = Company('Tesco', StockExchange.LSE, 'TSCO')
    articles = fetch_news(tesco, 48)
    for a in articles:
        print(vars(a))