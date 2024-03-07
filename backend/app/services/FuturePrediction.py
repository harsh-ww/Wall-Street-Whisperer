from services.AlphaVantageService import getTimeSeries
from typing import List
import pandas as pd

def getReturns(ticker: str) -> List[float]:
    """Calculates the returns for the last 100 days for a given ticker"""
    timeSeries = getTimeSeries(ticker, 'DAILY')

    # Create DataFrame
    df = pd.DataFrame.from_dict(timeSeries, orient='index')

    # Reverse ordering

    df = df[::-1]

    # Convert data types
    df = df.astype(float)

    # Calculate returns
    df['return'] = df['4. close'].pct_change()

    return df['return'].tolist()[1:]

def predictFuture(sentimentScores, returns):
    mean_sentiment = sum(sentimentScores)/len(sentimentScores)
    



