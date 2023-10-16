import datetime as dt
import json
from pathlib import Path
from typing import Literal

import pytz

from bsc_utils.database import Database, query
from bsc_utils.exceptions import SymbolNotFoundError
from bsc_utils.helpers import minus_time
from bsc_utils.resources import queries


def latest_td(symbol: str) -> dt.datetime:
    return td_ago(symbol, 0)


def prev_td(symbol: str) -> dt.datetime:
    return td_ago(symbol, 1)


def td_ago(symbol: str, offset: int) -> dt.datetime:
    symbol_type = get_symbol_type(symbol)
    td_ago_query = queries.ORACLE.td_ago(symbol_type)
    r = query(
        Database.ORACLE, td_ago_query, params=(symbol, offset), as_df=False
    )

    return r[0].get('TRADE_DATE')


def session_time(
    timestamp: dt.datetime,
    region: Literal['VN', 'US', 'UK', 'JP', 'AU'] = 'VN',
) -> str | list:
    with open(Path('bsc_utils') / 'resources' / 'sessions.json', 'r') as f:
        sessions = json.load(f).get(region)

    local_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    timestamp = local_tz.localize(timestamp)

    for session, session_time in sessions.items():
        start = dt.time.fromisoformat(session_time.get('start'))
        end = dt.time.fromisoformat(session_time.get('end'))
        end = minus_time(end, seconds=1)

        tz = pytz.timezone(session_time.get('timezone'))
        regional_timestamp = timestamp.astimezone(tz)

        if start < regional_timestamp.time() < end:
            return session
        elif start == regional_timestamp.time():
            return f'{session} Start'
        elif end == regional_timestamp.time():
            return f'{session} End'

    return 'Market Close'


def get_symbol_type(symbol: str) -> Literal['EXCHANGE', 'SECURITY']:
    for symbol_type in ['EXCHANGE', 'SECURITY']:
        codes = query(
            Database.ORACLE, queries.ORACLE.codes[symbol_type], as_df=False
        )
        codes = [c[f'{symbol_type}_CODE'] for c in codes]
        if symbol in codes:
            return symbol_type

    raise SymbolNotFoundError(symbol)
