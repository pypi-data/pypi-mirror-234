import datetime as dt
import sqlite3


def dict_factory(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def row_ratio(no_subplots):
    return [1 - 0.2 * (no_subplots - 1)] + [0.2] * (no_subplots - 1)


def minus_time(time: dt.time, seconds: int) -> dt.time:
    return (
        dt.datetime.combine(dt.date.today(), time) -
        dt.timedelta(seconds=seconds)
    ).time()
