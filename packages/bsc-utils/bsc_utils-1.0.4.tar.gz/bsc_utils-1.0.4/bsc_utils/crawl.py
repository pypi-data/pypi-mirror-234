import datetime as dt
from typing import Literal

import pandas as pd
import yfinance


def yf(
    ticker: str,
    start: str | dt.datetime,
    end: str | dt.datetime,
    interval: str = Literal['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h',
                            '1d', '5d', '1wk', '1mo', '3mo'],
) -> pd.DataFrame:
    market = yfinance.Ticker(ticker)
    quotes = market.history(start=start, end=end, interval=interval)
    quotes = quotes.drop(['Dividends', 'Stock Splits'], axis=1).round(2)
    quotes.reset_index(inplace=True)
    quotes.rename(
        columns=(
            {
                c: c.upper()
                for c in quotes.columns if c != 'Date'
            } | {
                'Date': 'TRADE_DATE'
            }
        ),
        inplace=True
    )

    return quotes


def fred(series_id: str):
    series = pd.read_csv(
        f'https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}',
        parse_dates=['DATE']
    )
    series.rename(columns={'DATE': 'TRADE_DATE'}, inplace=True)

    return series
