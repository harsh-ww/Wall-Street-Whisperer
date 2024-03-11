from services.PerigonService import getCompanyNewsPerigon
from models.Article import Article
from models.Company import Company, StockExchange
from typing import List


US_STOCK_EXCHANGES = [StockExchange.NASDAQ, StockExchange.NYSE]

# fetches news articles for a given company
def fetch_news(company: Company, pastHours: int, count:int=15) -> List[Article]:
    articles = []
    articles = getCompanyNewsPerigon(company.name, pastHours, count)
        
    return articles
