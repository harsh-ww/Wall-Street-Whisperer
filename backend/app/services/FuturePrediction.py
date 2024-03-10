from services.AlphaVantageService import getTimeSeries
from typing import List
import pandas as pd

def getReturnsAverage(ticker: str, days: int) -> List[float]:
    """Calculates the average return for the last 100 days for a given ticker"""
    timeSeries = getTimeSeries(ticker, 'DAILY')

    # Create DataFrame
    df = pd.DataFrame.from_dict(timeSeries, orient='index')

    # Reverse ordering

    df = df[::-1]

    # Convert data types
    df = df.astype(float)

    # Calculate returns
    df['return'] = df['4. close'].pct_change()

    
    # df['return'].tolist()[1:]
    return df['return'][-days:].mean()




